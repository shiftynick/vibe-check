#!/bin/bash

# Vibe-Check Single Review Runner
# This script runs a single file review using Claude Code SDK
# It reads the REVIEWER_INSTRUCTIONS.md and executes one review cycle

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VIBE_CHECK_DIR="vibe-check"
REVIEWER_INSTRUCTIONS="$VIBE_CHECK_DIR/prompts/REVIEWER_INSTRUCTIONS.md"
MASTER_FILE="$VIBE_CHECK_DIR/reviews/_MASTER.json"
LOG_DIR="$VIBE_CHECK_DIR/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Generate timestamp for this run
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/review_${TIMESTAMP}.log"

# Function to print colored messages
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    print_status "$RED" "Error: Claude Code CLI not found!"
    echo "Please install it with: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Check authentication method
if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
    print_status "$GREEN" "✓ Using Anthropic API key from environment"
else
    print_status "$YELLOW" "No ANTHROPIC_API_KEY found - will attempt to use Claude subscription"
    echo "Make sure you're signed into Claude CLI"
fi

# Check if vibe-check structure exists
if [[ ! -f "$REVIEWER_INSTRUCTIONS" ]]; then
    print_status "$RED" "Error: $REVIEWER_INSTRUCTIONS not found!"
    echo "Please run the vibe-check setup first."
    exit 1
fi

if [[ ! -f "$MASTER_FILE" ]]; then
    print_status "$RED" "Error: $MASTER_FILE not found!"
    echo "Please run populate_master.sh first."
    exit 1
fi

# Find and lock the next file to review
# Priority: 1) in_progress (resume failed), 2) not_reviewed
FILE_TO_REVIEW=$(python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
    # First check for any in_progress files (failed previous runs)
    for file_path, info in data['files'].items():
        if info['status'] == 'in_progress':
            print(file_path)
            exit(0)
    # Then check for not_reviewed files
    for file_path, info in data['files'].items():
        if info['status'] == 'not_reviewed':
            print(file_path)
            exit(0)
" || echo "")

if [[ -z "$FILE_TO_REVIEW" ]]; then
    print_status "$GREEN" "All files have been reviewed! No files left to process."
    exit 0
fi

# Count remaining files
FILES_TO_REVIEW=$(python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
    unreviewed = [f for f, info in data['files'].items() if info['status'] == 'not_reviewed']
    print(len(unreviewed))
")

print_status "$BLUE" "=== Starting Vibe-Check Single Review ==="
print_status "$YELLOW" "File to review: $FILE_TO_REVIEW"
print_status "$YELLOW" "Files remaining to review: $FILES_TO_REVIEW"
print_status "$YELLOW" "Logging to: $LOG_FILE"
print_status "$YELLOW" "Permission mode: Auto-accepting file edits"
echo ""

# Check if file is already in_progress or needs to be marked
FILE_STATUS=$(python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
print(data['files']['$FILE_TO_REVIEW']['status'])
")

if [[ "$FILE_STATUS" == "in_progress" ]]; then
    print_status "$YELLOW" "⚠ Resuming previously failed review for $FILE_TO_REVIEW"
else
    # Mark file as in_progress
    python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
data['files']['$FILE_TO_REVIEW']['status'] = 'in_progress'
with open('$MASTER_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
    print_status "$GREEN" "✓ Marked $FILE_TO_REVIEW as in_progress"
fi

# Read the reviewer instructions
INSTRUCTIONS=$(cat "$REVIEWER_INSTRUCTIONS")

# Create the prompt for Claude with specific file
PROMPT="You have access to a vibe-check directory at path 'vibe-check/' containing review artifacts.

You are tasked with reviewing the following file:
FILE_PATH: $FILE_TO_REVIEW

Please follow these instructions exactly:

$INSTRUCTIONS"

# Run Claude with the review instructions
# Using --print for non-interactive mode
# Using text output format for direct visibility
# Tee to both stdout and log file for visibility and record keeping
print_status "$BLUE" "Launching Claude Code for review..."
echo "----------------------------------------"

# Execute Claude and capture exit code
# Use stream-json output to get both real-time output and cost information
# Use acceptEdits permission mode to allow file modifications without prompts
set +e
claude --print "$PROMPT" \
    --output-format stream-json \
    --permission-mode acceptEdits \
    --verbose 2>&1 | tee "$LOG_FILE" | while IFS= read -r line; do
    # Try to parse as JSON - be silent about non-JSON lines
    if echo "$line" | python3 -c "import json, sys; json.load(sys.stdin)" 2>/dev/null; then
        # It's valid JSON - extract and display only assistant text messages
        OUTPUT=$(echo "$line" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if data.get('type') == 'assistant':
        # Extract text content from assistant messages
        msg = data.get('message', {})
        content = msg.get('content', [])
        for item in content:
            if item.get('type') == 'text':
                text = item.get('text', '').strip()
                if text:  # Only print non-empty text
                    print(text)
                    print('---')  # Add separator after each response
    elif data.get('type') == 'result':
        # Don't print the result JSON here - we'll handle it later
        pass
except:
    pass  # Silently ignore any parsing errors
" 2>/dev/null || true)
        
        if [[ -n "$OUTPUT" ]]; then
            echo "$OUTPUT"
        fi
    fi
    # Removed the else clause - don't display non-JSON lines
done

CLAUDE_EXIT_CODE=${PIPESTATUS[0]}
set -e

echo "----------------------------------------"

# Check exit code
if [[ $CLAUDE_EXIT_CODE -eq 0 ]]; then
    print_status "$GREEN" "✓ Review completed successfully!"
    
    # Mark file as completed
    python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
data['files']['$FILE_TO_REVIEW']['status'] = 'completed'
with open('$MASTER_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
    print_status "$GREEN" "✓ Marked $FILE_TO_REVIEW as completed"
    
    # Try to extract cost information from the result JSON in log file
    # Look for the last line with type: "result" in the log
    RESULT_JSON=$(grep '"type": *"result"' "$LOG_FILE" 2>/dev/null | tail -1 || echo "")
    
    if [[ -n "$RESULT_JSON" ]]; then
        COST_INFO=$(echo "$RESULT_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    cost = data.get('total_cost_usd', 'N/A')
    duration = data.get('duration_ms', 'N/A')
    turns = data.get('num_turns', 'N/A')
    
    if cost != 'N/A':
        print(f'Cost: \${cost:.4f} USD')
    else:
        print('Cost: Not available')
    
    if duration != 'N/A':
        duration_sec = duration / 1000
        print(f'Duration: {duration_sec:.1f} seconds')
    
    if turns != 'N/A':
        print(f'Turns: {turns}')
except:
    print('Cost information not available')
" 2>/dev/null || echo "Cost information not available")
        
        echo ""
        print_status "$BLUE" "=== Execution Summary ==="
        echo "$COST_INFO"
    fi
    
    # Check how many files are left
    REMAINING=$(python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
    unreviewed = [f for f, info in data['files'].items() if info['status'] == 'not_reviewed']
    print(len(unreviewed))
")
    
    echo ""
    print_status "$YELLOW" "Files remaining to review: $REMAINING"
    exit 0
else
    print_status "$RED" "✗ Review failed with exit code: $CLAUDE_EXIT_CODE"
    print_status "$RED" "Check the log file for details: $LOG_FILE"
    
    # Mark file back to not_reviewed on failure
    python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
data['files']['$FILE_TO_REVIEW']['status'] = 'not_reviewed'
with open('$MASTER_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
    print_status "$YELLOW" "⚠ Reverted $FILE_TO_REVIEW back to not_reviewed status"
    
    exit $CLAUDE_EXIT_CODE
fi