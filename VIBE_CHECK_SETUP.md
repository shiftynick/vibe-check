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

- `FILE_PATH` - The path to the source file to review (relative to repository root, excluding vibe-check folder)
- Access to `vibe-check/reviews/` directory for reading and writing review artifacts
- The fixed metrics list: Security, Performance, Maintainability, Consistency, Best_Practices, Code_Smell

## Outputs

1. A complete review markdown file at `vibe-check/reviews/modules/.../[filename].md`
2. Updated entry in `vibe-check/reviews/_MASTER.json` with scores and metadata
3. Updated dependencies in `vibe-check/reviews/_DEPENDENCIES.yml`

## Precise Algorithm to Follow

### Step 1: Lock the File
- Open `vibe-check/reviews/_MASTER.json`
- Find the entry for FILE_PATH in the "files" object
- Change the "status" from "not_reviewed" to "in_progress"
- Save the file

### Step 2: Analyze the Source File
- Read the complete source code from FILE_PATH
- Detect programming language
- Count lines of code (LOC)
- Note file's primary purpose and functionality

### Step 3: Run Static Analysis
- Apply appropriate linting rules for the language
- Run security scanning tools if available
- Calculate complexity metrics
- Check for formatting issues

### Step 4: Assess Each Metric (in order)

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

### Step 5: Identify Dependencies
- Parse all imports/includes/requires
- List external library dependencies
- Note internal project file dependencies
- Record in format: relative/path/to/file.ext

### Step 6: Create Review Markdown

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

| # | Category | Severity | Location | Description | Recommendation |
|---|----------|----------|----------|-------------|----------------|
| 1 | [METRIC] | [HIGH/MED/LOW] | L[START]-[END] | [Issue description] | [How to fix] |

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

### Step 7: Update Master Ledger
- Reopen `vibe-check/reviews/_MASTER.json`
- Find the FILE_PATH entry in the "files" object
- Update fields:
  - status = "completed"
  - review_date = TODAY (ISO format)
  - reviewer = Your AI identifier
  - scores = object with all metric scores (1-5)
  - open_issues = total count
  - dependency_count = number of dependencies
- Save the file

### Step 8: Update Dependencies
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

### Step 9: Commit and Complete
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

### 4. Next Steps

Once this structure is in place:

1. Run `./vibe-check/scripts/populate_master.sh` to scan the repository and populate `vibe-check/reviews/_MASTER.json` with all source files
   - Use `FORCE_NO_GIT=1 ./vibe-check/scripts/populate_master.sh` if not using git
2. Review the generated master list to ensure all expected files are included
3. Begin the review process by providing the REVIEWER_INSTRUCTIONS.md to an AI agent
4. The AI will process files one at a time, updating the master list and creating review artifacts
5. Monitor progress by checking the status field in `_MASTER.json`

### 5. Important Notes

- All files should be created with UTF-8 encoding
- Use Unix-style line endings (LF)
- Maintain consistent indentation (2 spaces for YAML, your preference for Markdown)
- Do not modify these template files except to add actual review data
- Source code files should be treated as read-only during reviews
- The vibe-check folder should be added to `.gitignore` if you don't want to commit reviews
- Alternatively, commit the vibe-check folder to track review history over time

This setup creates the foundational structure for the Vibe-Check review system overlaid on your existing repository. All subsequent reviews will populate these files according to the deterministic algorithm defined in the design document.