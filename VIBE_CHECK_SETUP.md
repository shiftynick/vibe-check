# VIBE_CHECK_SETUP.md

## Setup Instructions for Vibe-Check Code Review System

You are tasked with setting up the Vibe-Check code review system within an existing repository. This will create a `vibe-check` folder in the current directory that contains all review artifacts, while treating the rest of the repository as the source code to be reviewed.

### 1. Create Directory Structure

Create the following directory hierarchy within a new `vibe-check` folder:

```
vibe-check/
├── prompts/
├── scripts/
└── reviews/
    ├── modules/
    └── system/
```

### 2. Create Initial Files

#### 2.1 Create `vibe-check/reviews/_MASTER.json`

Create this file with the following content:

```json
{
  "metadata": {
    "version": "1.0",
    "description": "Vibe-Check Master Review Ledger - Single source of truth for all code review progress",
    "generated": "",
    "total_files": 0,
    "total_loc": 0,
    "status_legend": {
      "not_reviewed": "File has not been reviewed yet",
      "in_progress": "Review is currently in progress",
      "completed": "Review has been completed",
      "needs_update": "Source file changed, review needs update"
    },
    "score_range": {
      "min": 1,
      "max": 5,
      "description": "1 = Critical issues, 5 = Excellent"
    }
  },
  "files": {}
}
```

#### 2.2 Create `vibe-check/reviews/_DEPENDENCIES.yml`

Create this file with the following content:

```yaml
# Vibe-Check Dependency Graph
# This file tracks all file-to-file dependencies in the codebase
# Format:
#   file_path:
#     outbound: [list of files this file depends on]
#     inbound: [list of files that depend on this file]

# Dependencies will be populated as files are reviewed
```

#### 2.3 Create `vibe-check/reviews/system/HOTSPOTS.md`

Create this file with the following content:

```markdown
# Cross-Cutting Issues and Hotspots

This file tracks issues that span multiple files or represent systemic patterns in the codebase.

## Issue Categories
- **Security**: Vulnerabilities affecting multiple components
- **Architecture**: Design patterns and structural concerns
- **Performance**: System-wide performance bottlenecks
- **Duplication**: Code duplication patterns
- **Dependencies**: Circular dependencies or problematic coupling

## Active Hotspots

*This section will be populated as reviews progress and patterns emerge.*

---

## Resolved Hotspots

*Archive of previously identified and resolved cross-cutting issues.*
```

#### 2.4 Create `vibe-check/reviews/system/METRICS_SUMMARY.md`

Create this file with the following content:

```markdown
# Repository-Wide Metrics Summary

## Overall Health Score
*To be calculated after initial reviews*

## Metric Breakdown

| Metric | Average Score | Files Below 3 | Files At 5 |
|--------|---------------|---------------|------------|
| Security | - | - | - |
| Performance | - | - | - |
| Maintainability | - | - | - |
| Consistency | - | - | - |
| Best Practices | - | - | - |
| Code Smell | - | - | - |

## Statistics
- Total Files Reviewed: 0
- Total Lines of Code: 0
- Total Open Issues: 0
- Average Dependencies per File: 0

## Trends
*Tracking improvements over time*

Last Updated: [Date will be auto-updated]
```

#### 2.5 Create `vibe-check/reviews/modules/README.md`

Create this file with the following content:

```markdown
# Modules Directory

This directory mirrors the structure of the repository root (excluding the vibe-check folder). Each subdirectory represents a module or component in the source code.

## Structure
- Each source code file will have a corresponding `.md` review file
- Module-level README files synthesize findings across all files in that module
- Directory structure mirrors the repository structure (excluding the vibe-check folder itself)

## Navigation Tips
- Review files use the same name as source files but with `.md` extension
- Use relative paths when referencing other reviews
- Module READMEs are created after all files in the module are reviewed
```

#### 2.6 Create `vibe-check/prompts/REVIEWER_INSTRUCTIONS.md`

Create this file with the following content:

```markdown
# REVIEWER INSTRUCTIONS - Vibe-Check Single File Review

## What is Vibe-Check?

Vibe-Check is a systematic code review system that analyzes source code quality across six key dimensions:
1. **Security** - Vulnerabilities, input validation, authentication/authorization issues
2. **Performance** - Efficiency, resource usage, scalability concerns
3. **Maintainability** - Code clarity, modularity, documentation quality
4. **Consistency** - Adherence to project conventions and patterns
5. **Best Practices** - Industry standards, design patterns, idiomatic code
6. **Code Smell** - Anti-patterns, technical debt, refactoring opportunities

Each dimension is scored 1-5 (5 = excellent, 1 = critical issues requiring rewrite).

## Your Role

You are the File Reviewer AI. Your task is to analyze EXACTLY ONE source file and produce a comprehensive review following a deterministic algorithm.

## Inputs

- `FILE_PATH` - The specific file path provided by the review script (relative to repository root)
- Access to `vibe-check/reviews/` directory for reading and writing review artifacts
- The fixed metrics list: Security, Performance, Maintainability, Consistency, Best_Practices, Code_Smell

## Outputs

1. A complete review markdown file at `vibe-check/reviews/modules/.../[filename].md`
2. Updated dependencies in `vibe-check/reviews/_DEPENDENCIES.yml`

## Precise Algorithm to Follow

### Step 1: Analyze the Source File
- Read the complete source code from FILE_PATH
- Detect programming language
- Count lines of code (LOC)
- Note file's primary purpose and functionality

### Step 2: Run Static Analysis
- Apply appropriate linting rules for the language
- Run security scanning tools if available
- Calculate complexity metrics
- Check for formatting issues

### Step 3: Assess Each Metric (in order)

For **Security**:
- Check for input validation
- Look for authentication/authorization issues
- Identify potential injection vulnerabilities
- Review cryptographic usage
- Check for exposed secrets or credentials

For **Performance**:
- Identify inefficient algorithms (O(n²) or worse)
- Look for N+1 query patterns
- Check for memory leaks or excessive allocations
- Review caching opportunities
- Identify blocking operations

For **Maintainability**:
- Assess code readability and clarity
- Check for appropriate abstractions
- Review error handling completeness
- Evaluate test coverage needs
- Check documentation quality

For **Consistency**:
- Compare against project conventions
- Check naming patterns
- Review code formatting
- Verify import organization
- Check comment style

For **Best Practices**:
- Verify SOLID principles adherence
- Check for proper error handling
- Review logging practices
- Assess API design
- Check for proper resource cleanup

For **Code Smell**:
- Identify duplicate code
- Find overly complex methods
- Check for god objects/functions
- Look for magic numbers
- Identify tight coupling

For each metric:
- List specific findings with line numbers
- Assign severity (High/Medium/Low)
- Provide actionable recommendations
- Count open issues
- Assign 1-5 score using this rubric:
  - 5 = Exemplary, no findings
  - 4 = Minor issues only
  - 3 = At least one medium severity issue
  - 2 = High severity issues present
  - 1 = Critical flaws, rewrite needed

### Step 4: Identify Dependencies
- Parse all imports/includes/requires
- List external library dependencies
- Note internal project file dependencies
- Record in format: relative/path/to/file.ext

### Step 5: Create Review Markdown

Use this exact template:

\`\`\`markdown
---
file: [FILE_PATH]
language: [DETECTED_LANGUAGE]
loc: [LINE_COUNT]
reviewer: AI-[IDENTIFIER]
date: [YYYY-MM-DD]
status: complete
metrics:
  security:        {score: [1-5], open_issues: [COUNT]}
  performance:     {score: [1-5], open_issues: [COUNT]}
  maintainability: {score: [1-5], open_issues: [COUNT]}
  consistency:     {score: [1-5], open_issues: [COUNT]}
  best_practices:  {score: [1-5], open_issues: [COUNT]}
  code_smell:      {score: [1-5], open_issues: [COUNT]}
dependencies:
  - [path/to/dependency1.ext]
  - [path/to/dependency2.ext]
reverse_dependencies: []
---

# 1. Summary
[Brief description of file purpose and overall health assessment]

# 2. Detailed findings

## Security Issues
### 1. [HIGH/MEDIUM/LOW] - [Issue Title]
- **Location**: Lines [START]-[END]
- **Description**: [Detailed description of the security issue]
- **Recommendation**: [Specific steps to fix the issue]

## Performance Issues
### 2. [HIGH/MEDIUM/LOW] - [Issue Title]
- **Location**: Lines [START]-[END]
- **Description**: [Detailed description of the performance issue]
- **Recommendation**: [Specific steps to fix the issue]

## Maintainability Issues
### 3. [HIGH/MEDIUM/LOW] - [Issue Title]
- **Location**: Lines [START]-[END]
- **Description**: [Detailed description of the maintainability issue]
- **Recommendation**: [Specific steps to fix the issue]

## Consistency Issues
### 4. [HIGH/MEDIUM/LOW] - [Issue Title]
- **Location**: Lines [START]-[END]
- **Description**: [Detailed description of the consistency issue]
- **Recommendation**: [Specific steps to fix the issue]

## Best Practices Issues
### 5. [HIGH/MEDIUM/LOW] - [Issue Title]
- **Location**: Lines [START]-[END]
- **Description**: [Detailed description of the best practices issue]
- **Recommendation**: [Specific steps to fix the issue]

## Code Smell Issues
### 6. [HIGH/MEDIUM/LOW] - [Issue Title]
- **Location**: Lines [START]-[END]
- **Description**: [Detailed description of the code smell]
- **Recommendation**: [Specific steps to fix the issue]

# 3. Positive observations
[List well-implemented aspects, good patterns, strong test coverage, etc.]

# 4. Context & links
- Related tests: [path/to/test/file]
- Documentation: [path/to/docs]
- Configuration: [path/to/config]

# 5. Checklist
- [ ] Lints clean
- [ ] Tests present
- [ ] Documentation updated
- [ ] Security review complete
- [ ] Performance acceptable
\`\`\`

### Step 6: Update Dependencies
- Open `vibe-check/reviews/_DEPENDENCIES.yml`
- Add or update entry:
  ```yaml
  [FILE_PATH]:
    outbound:
      - [dependency1]
      - [dependency2]
    inbound: []  # Will be populated by system scripts
  ```
- Save the file

### Step 7: Complete
- Save all modified files
- Output only: "Review of [FILE_PATH] complete."
- Do not provide any additional commentary

## Important Rules

1. Review ONLY the single file specified
2. Be objective and consistent in scoring
3. Always provide actionable recommendations
4. Use exact file paths (no wildcards or patterns)
5. Maintain the exact format specified
6. Complete ALL sections even if empty
7. Never modify source code files
8. Keep findings specific with line numbers
9. Focus on substantive issues over style preferences
10. End with only the completion message

## Error Handling

If you encounter any errors:
- File not found: Update _MASTER.json to mark status as "not_found" and stop
- Cannot parse: Score all metrics as 1 with explanation in summary
- Lock conflict: Wait and retry once, then report conflict
```

#### 2.7 Create `vibe-check/scripts/populate_master.sh`

Create this executable script with the following content:

```bash
#!/bin/bash

# Vibe-Check Master List Population Script
# This script scans the repository and populates the initial _MASTER.json file
# It respects .gitignore patterns and excludes the vibe-check directory itself

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
VIBE_CHECK_DIR="vibe-check"
MASTER_FILE="$VIBE_CHECK_DIR/reviews/_MASTER.json"

# Common source file extensions to include
SOURCE_EXTENSIONS=(
    "js" "jsx" "ts" "tsx"           # JavaScript/TypeScript
    "py" "pyw"                      # Python
    "java" "kt" "kts"               # Java/Kotlin
    "c" "cpp" "cc" "cxx" "h" "hpp"  # C/C++
    "cs"                            # C#
    "go"                            # Go
    "rs"                            # Rust
    "rb"                            # Ruby
    "php"                           # PHP
    "swift"                         # Swift
    "m" "mm"                        # Objective-C
    "scala"                         # Scala
    "r" "R"                         # R
    "lua"                           # Lua
    "pl" "pm"                       # Perl
    "sh" "bash" "zsh"               # Shell
    "sql"                           # SQL
    "vue"                           # Vue
    "elm"                           # Elm
    "ex" "exs"                      # Elixir
)

# Function to check if file has a valid source extension
has_valid_extension() {
    local file="$1"
    local ext="${file##*.}"
    
    for valid_ext in "${SOURCE_EXTENSIONS[@]}"; do
        if [[ "$ext" == "$valid_ext" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to count lines of code (excluding empty lines and comments)
count_lines() {
    local file="$1"
    # Simple line count - can be enhanced for more accuracy
    wc -l < "$file" | tr -d ' '
}

# Function to detect language from file extension
detect_language() {
    local file="$1"
    local ext="${file##*.}"
    
    case "$ext" in
        js|jsx) echo "JavaScript";;
        ts|tsx) echo "TypeScript";;
        py|pyw) echo "Python";;
        java) echo "Java";;
        kt|kts) echo "Kotlin";;
        c|h) echo "C";;
        cpp|cc|cxx|hpp) echo "C++";;
        cs) echo "C#";;
        go) echo "Go";;
        rs) echo "Rust";;
        rb) echo "Ruby";;
        php) echo "PHP";;
        swift) echo "Swift";;
        m|mm) echo "Objective-C";;
        scala) echo "Scala";;
        r|R) echo "R";;
        lua) echo "Lua";;
        pl|pm) echo "Perl";;
        sh|bash|zsh) echo "Shell";;
        sql) echo "SQL";;
        vue) echo "Vue";;
        elm) echo "Elm";;
        ex|exs) echo "Elixir";;
        *) echo "Unknown";;
    esac
}

# Check if vibe-check directory exists
if [[ ! -d "$VIBE_CHECK_DIR" ]]; then
    echo -e "${RED}Error: vibe-check directory not found!${NC}"
    echo "Please run the setup script first to create the vibe-check structure."
    exit 1
fi

# Check if git is available and we're in a git repository
# For testing, we can force non-git mode by setting FORCE_NO_GIT=1
if [[ "${FORCE_NO_GIT:-0}" == "1" ]]; then
    USE_GIT=false
    echo -e "${YELLOW}Forced non-git mode. Using find command.${NC}"
elif command -v git &> /dev/null && git rev-parse --git-dir &> /dev/null 2>/dev/null; then
    USE_GIT=true
    echo -e "${GREEN}Git repository detected. Using git ls-files to respect .gitignore${NC}"
else
    USE_GIT=false
    echo -e "${YELLOW}Not a git repository or git not available. Using find command.${NC}"
fi

# Create temporary file for JSON content
TEMP_FILE=$(mktemp)

# Initialize JSON structure
cat > "$TEMP_FILE" << EOF
{
  "metadata": {
    "version": "1.0",
    "description": "Vibe-Check Master Review Ledger - Single source of truth for all code review progress",
    "generated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "total_files": 0,
    "total_loc": 0,
    "status_legend": {
      "not_reviewed": "File has not been reviewed yet",
      "in_progress": "Review is currently in progress",
      "completed": "Review has been completed",
      "needs_update": "Source file changed, review needs update"
    },
    "score_range": {
      "min": 1,
      "max": 5,
      "description": "1 = Critical issues, 5 = Excellent"
    }
  },
  "files": {
EOF

# Collect source files
echo -e "\n${GREEN}Scanning for source files...${NC}"
file_count=0
total_loc=0

# Function to process a file
process_file() {
    local file="$1"
    
    # Skip if file doesn't exist or is a directory
    if [[ ! -f "$file" ]] || [[ -d "$file" ]]; then
        return
    fi
    
    # Skip if not a source file
    if ! has_valid_extension "$file"; then
        return
    fi
    
    # Get file info
    local lang=$(detect_language "$file")
    local loc=$(count_lines "$file")
    
    # Add to total
    ((file_count++))
    ((total_loc+=loc))
    
    # Add comma if not first file
    if [[ $file_count -gt 1 ]]; then
        echo "," >> "$TEMP_FILE"
    fi
    
    # Add JSON entry for file
    cat >> "$TEMP_FILE" << EOF
    "$file": {
      "language": "$lang",
      "loc": $loc,
      "status": "not_reviewed",
      "review_date": null,
      "reviewer": null,
      "scores": {
        "security": null,
        "performance": null,
        "maintainability": null,
        "consistency": null,
        "best_practices": null,
        "code_smell": null
      },
      "open_issues": 0,
      "dependency_count": 0
    }
EOF
    
    # Progress indicator
    if [[ $((file_count % 10)) -eq 0 ]]; then
        echo -ne "\rProcessed $file_count files..."
    fi
}

if [[ "$USE_GIT" == true ]]; then
    # Use git ls-files to get all tracked files
    while IFS= read -r file; do
        # Skip vibe-check directory
        if [[ "$file" == "$VIBE_CHECK_DIR/"* ]]; then
            continue
        fi
        process_file "$file"
    done < <(git ls-files)
else
    # Use find command, excluding common directories
    while IFS= read -r file; do
        # Remove leading ./ from path
        file="${file#./}"
        process_file "$file"
    done < <(find . -type f \
        -not -path "./$VIBE_CHECK_DIR/*" \
        -not -path "*/\.*" \
        -not -path "*/node_modules/*" \
        -not -path "*/venv/*" \
        -not -path "*/env/*" \
        -not -path "*/__pycache__/*" \
        -not -path "*/build/*" \
        -not -path "*/dist/*" \
        -not -path "*/target/*" \
        -not -path "*/vendor/*" \
        -not -path "*/coverage/*" \
        -not -path "*/.git/*")
fi

echo -e "\n"

# Close JSON structure
echo "" >> "$TEMP_FILE"
echo "  }" >> "$TEMP_FILE"
echo "}" >> "$TEMP_FILE"

# Now update the metadata with actual counts
# Create a new temp file with updated metadata
TEMP_FILE2=$(mktemp)
awk -v files="$file_count" -v loc="$total_loc" '
    /"total_files":/ { sub(/: [0-9]+/, ": " files) }
    /"total_loc":/ { sub(/: [0-9]+/, ": " loc) }
    { print }
' "$TEMP_FILE" > "$TEMP_FILE2"

# Move temp file to actual location
mv "$TEMP_FILE2" "$MASTER_FILE"
rm -f "$TEMP_FILE"

# Summary
echo -e "${GREEN}✓ Master list populated successfully!${NC}"
echo -e "  Files found: ${YELLOW}$file_count${NC}"
echo -e "  Total LOC: ${YELLOW}$total_loc${NC}"
echo -e "  Output: ${YELLOW}$MASTER_FILE${NC}"
echo ""
echo "Next steps:"
echo "1. Review the generated list in $MASTER_FILE"
echo "2. Use the reviewer AI with REVIEWER_INSTRUCTIONS.md to process each file"
echo "3. The AI will update this master list as reviews are completed"
```

After creating this file, make it executable:
```bash
chmod +x vibe-check/scripts/populate_master.sh
```

#### 2.8 Create `vibe-check/scripts/run_single_review.sh`

Create this executable script with the following content:

```bash
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
```

After creating this file, make it executable:
```bash
chmod +x vibe-check/scripts/run_single_review.sh
```

#### 2.9 Create `vibe-check/scripts/review_all.sh`

Create this executable script with the following content:

```bash
#!/bin/bash

# Vibe-Check Review All Files
# This script runs reviews for all unreviewed files using run_single_review.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SINGLE_REVIEW_SCRIPT="$SCRIPT_DIR/run_single_review.sh"
MASTER_FILE="vibe-check/reviews/_MASTER.json"

# Function to print colored messages
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if single review script exists
if [[ ! -x "$SINGLE_REVIEW_SCRIPT" ]]; then
    print_status "$RED" "Error: $SINGLE_REVIEW_SCRIPT not found or not executable!"
    exit 1
fi

# Check authentication method
if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
    print_status "$GREEN" "✓ Using Anthropic API key from environment"
else
    print_status "$YELLOW" "No ANTHROPIC_API_KEY found - will use Claude subscription"
    echo "Make sure you're signed into Claude CLI"
fi

print_status "$BLUE" "=== Vibe-Check Batch Review Process ==="
echo ""

# Counter for tracking
TOTAL_REVIEWED=0
FAILED_REVIEWS=0

# Loop until all files are reviewed or an error occurs
while true; do
    # Check remaining files
    if [[ ! -f "$MASTER_FILE" ]]; then
        print_status "$RED" "Error: $MASTER_FILE not found!"
        exit 1
    fi
    
    REMAINING=$(python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
    unreviewed = [f for f, info in data['files'].items() if info['status'] == 'not_reviewed']
    print(len(unreviewed))
")
    
    if [[ "$REMAINING" -eq 0 ]]; then
        print_status "$GREEN" "✓ All files have been reviewed!"
        break
    fi
    
    print_status "$YELLOW" "Files remaining: $REMAINING"
    print_status "$BLUE" "Starting review #$((TOTAL_REVIEWED + 1))..."
    echo ""
    
    # Run single review
    if "$SINGLE_REVIEW_SCRIPT"; then
        ((TOTAL_REVIEWED++))
        print_status "$GREEN" "✓ Review #$TOTAL_REVIEWED completed successfully"
    else
        ((FAILED_REVIEWS++))
        print_status "$RED" "✗ Review failed! Stopping batch process."
        break
    fi
    
    # Add a small delay between reviews to avoid rate limiting
    if [[ "$REMAINING" -gt 1 ]]; then
        print_status "$YELLOW" "Waiting 5 seconds before next review..."
        sleep 5
    fi
    
    echo ""
    echo "========================================"
    echo ""
done

# Final summary
echo ""
print_status "$BLUE" "=== Batch Review Summary ==="
print_status "$GREEN" "Total files reviewed: $TOTAL_REVIEWED"
if [[ "$FAILED_REVIEWS" -gt 0 ]]; then
    print_status "$RED" "Failed reviews: $FAILED_REVIEWS"
    exit 1
else
    print_status "$GREEN" "All reviews completed successfully!"
    exit 0
fi
```

After creating this file, make it executable:
```bash
chmod +x vibe-check/scripts/review_all.sh
```

### 3. Verification Checklist

After creating all files, verify:

- [ ] `vibe-check/` directory exists in repository root
- [ ] `vibe-check/prompts/` directory exists
- [ ] `vibe-check/scripts/` directory exists
- [ ] `vibe-check/reviews/` directory exists
- [ ] `vibe-check/reviews/modules/` directory exists  
- [ ] `vibe-check/reviews/system/` directory exists
- [ ] `vibe-check/prompts/REVIEWER_INSTRUCTIONS.md` exists with complete algorithm
- [ ] `vibe-check/reviews/_MASTER.json` exists with proper JSON structure
- [ ] `vibe-check/reviews/_DEPENDENCIES.yml` exists with YAML format
- [ ] `vibe-check/reviews/system/HOTSPOTS.md` exists with section headers
- [ ] `vibe-check/reviews/system/METRICS_SUMMARY.md` exists with metric table
- [ ] `vibe-check/reviews/modules/README.md` exists with navigation guide
- [ ] `vibe-check/scripts/populate_master.sh` exists and is executable
- [ ] `vibe-check/scripts/run_single_review.sh` exists and is executable
- [ ] `vibe-check/scripts/review_all.sh` exists and is executable

### 4. Next Steps

Once this structure is in place:

1. Check if your project uses Git:
   ```bash
   # Check if current directory is a Git repository
   git rev-parse --git-dir > /dev/null 2>&1 && echo "Git repository detected" || echo "Not a Git repository"
   ```

2. Run the populate_master.sh script based on your Git status:
   ```bash
   # If Git repository detected (will respect .gitignore):
   ./vibe-check/scripts/populate_master.sh
   
   # If NOT a Git repository (will use find command):
   FORCE_NO_GIT=1 ./vibe-check/scripts/populate_master.sh
   ```
   
   The script will automatically detect Git and inform you which mode it's using:
   - **Git mode**: "Git repository detected. Using git ls-files to respect .gitignore"
   - **Non-Git mode**: "Not a git repository or git not available. Using find command."

3. Review the generated master list to ensure all expected files are included

4. Run a single file review:
   ```bash
   # With API key
   export ANTHROPIC_API_KEY="your-api-key"
   ./vibe-check/scripts/run_single_review.sh
   
   # Or with Claude subscription (requires claude login)
   ./vibe-check/scripts/run_single_review.sh
   ```
5. The script will:
   - Find the next unreviewed file automatically
   - Show Claude's analysis in real-time with separators
   - Save full logs to `vibe-check/logs/`
   - Update `_MASTER.json` with scores and status
   - Create review markdown in `vibe-check/reviews/modules/`
   - Display cost and execution summary

6. Repeat step 4 to review more files, or use batch processing:
   ```bash
   # Review all remaining files automatically
   ./vibe-check/scripts/review_all.sh
   ```
   The batch script will:
   - Review all unreviewed files one by one
   - Add 5-second delays between reviews to avoid rate limiting
   - Stop if any review fails
   - Display a summary at the end

7. Monitor progress by checking the status field in `_MASTER.json`

### 5. Important Notes

- All files should be created with UTF-8 encoding
- Use Unix-style line endings (LF)
- Maintain consistent indentation (2 spaces for YAML, your preference for Markdown)
- Do not modify these template files except to add actual review data
- Source code files should be treated as read-only during reviews
- The vibe-check folder should be added to `.gitignore` if you don't want to commit reviews
- Alternatively, commit the vibe-check folder to track review history over time

This setup creates the foundational structure for the Vibe-Check review system overlaid on your existing repository. All subsequent reviews will populate these files according to the deterministic algorithm defined in the design document.