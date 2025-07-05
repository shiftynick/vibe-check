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

# Check if there are any files to review
FILES_TO_REVIEW=$(python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
    unreviewed = [f for f, info in data['files'].items() if info['status'] == 'not_reviewed']
    print(len(unreviewed))
")

if [[ "$FILES_TO_REVIEW" -eq 0 ]]; then
    print_status "$GREEN" "All files have been reviewed! No files left to process."
    exit 0
fi

print_status "$BLUE" "=== Starting Vibe-Check Single Review ==="
print_status "$YELLOW" "Files remaining to review: $FILES_TO_REVIEW"
print_status "$YELLOW" "Logging to: $LOG_FILE"
print_status "$YELLOW" "Permission mode: Auto-accepting file edits"
echo ""

# Read the reviewer instructions
INSTRUCTIONS=$(cat "$REVIEWER_INSTRUCTIONS")

# Create the prompt for Claude
PROMPT="You have access to a vibe-check directory at path 'vibe-check/' containing review artifacts.

Please follow these instructions exactly:

$INSTRUCTIONS

Start by reading vibe-check/reviews/_MASTER.json to find the next unreviewed file and begin the review process."

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
    # Try to parse as JSON
    if echo "$line" | python3 -c "import json, sys; data=json.load(sys.stdin); sys.exit(0 if data.get('type') in ['assistant', 'result'] else 1)" 2>/dev/null; then
        # Extract and display assistant messages
        OUTPUT=$(echo "$line" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('type') == 'assistant':
    # Extract text content from assistant messages
    msg = data.get('message', {})
    content = msg.get('content', [])
    for item in content:
        if item.get('type') == 'text':
            print(item.get('text', ''))
elif data.get('type') == 'result':
    # Store result for later - need to escape the JSON string
    json_str = json.dumps(data)
    print(f'__RESULT_JSON__:{json_str}')
" 2>/dev/null || echo "")
        
        if [[ -n "$OUTPUT" ]]; then
            echo "$OUTPUT"
        fi
    else
        # Not JSON, just display it
        echo "$line"
    fi
done

CLAUDE_EXIT_CODE=${PIPESTATUS[0]}
set -e

echo "----------------------------------------"

# Check exit code
if [[ $CLAUDE_EXIT_CODE -eq 0 ]]; then
    print_status "$GREEN" "✓ Review completed successfully!"
    
    # Try to extract cost information from the result JSON in log file
    RESULT_JSON=$(grep "__RESULT_JSON__:" "$LOG_FILE" 2>/dev/null | sed 's/__RESULT_JSON__://' || echo "")
    
    if [[ -n "$RESULT_JSON" ]]; then
        COST_INFO=$(echo "$RESULT_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    cost = data.get('total_cost_usd', 'N/A')
    duration = data.get('duration_ms', 'N/A')
    turns = data.get('num_turns', 'N/A')
    
    if cost != 'N/A':
        print(f'Cost: \\${cost:.4f} USD')
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
    exit $CLAUDE_EXIT_CODE
fi