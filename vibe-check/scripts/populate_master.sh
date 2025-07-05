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