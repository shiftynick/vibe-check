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

#### 2.7 Create `vibe-check/scripts/populate_master.py`

Create this executable script with the following content:

```python
#!/usr/bin/env python3
"""
populate_master.py - Scan repository and populate the initial _MASTER.json file
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

def print_status(color: str, message: str):
    """Print colored status message"""
    print(f"{color}{message}{Colors.NC}")

class VibeCheckPopulator:
    # Common source file extensions to include
    SOURCE_EXTENSIONS = {
        # JavaScript/TypeScript
        'js', 'jsx', 'ts', 'tsx',
        # Python
        'py', 'pyw',
        # Java/Kotlin
        'java', 'kt', 'kts',
        # C/C++
        'c', 'cpp', 'cc', 'cxx', 'h', 'hpp',
        # C#
        'cs',
        # Go
        'go',
        # Rust
        'rs',
        # Ruby
        'rb',
        # PHP
        'php',
        # Swift
        'swift',
        # Objective-C
        'm', 'mm',
        # Scala
        'scala',
        # R
        'r', 'R',
        # Lua
        'lua',
        # Perl
        'pl', 'pm',
        # Shell
        'sh', 'bash', 'zsh',
        # SQL
        'sql',
        # Vue
        'vue',
        # Elm
        'elm',
        # Elixir
        'ex', 'exs'
    }
    
    # Language mapping
    LANGUAGE_MAP = {
        'js': 'JavaScript', 'jsx': 'JavaScript',
        'ts': 'TypeScript', 'tsx': 'TypeScript',
        'py': 'Python', 'pyw': 'Python',
        'java': 'Java',
        'kt': 'Kotlin', 'kts': 'Kotlin',
        'c': 'C', 'h': 'C',
        'cpp': 'C++', 'cc': 'C++', 'cxx': 'C++', 'hpp': 'C++',
        'cs': 'C#',
        'go': 'Go',
        'rs': 'Rust',
        'rb': 'Ruby',
        'php': 'PHP',
        'swift': 'Swift',
        'm': 'Objective-C', 'mm': 'Objective-C',
        'scala': 'Scala',
        'r': 'R', 'R': 'R',
        'lua': 'Lua',
        'pl': 'Perl', 'pm': 'Perl',
        'sh': 'Shell', 'bash': 'Shell', 'zsh': 'Shell',
        'sql': 'SQL',
        'vue': 'Vue',
        'elm': 'Elm',
        'ex': 'Elixir', 'exs': 'Elixir'
    }
    
    def __init__(self):
        self.vibe_check_dir = Path("vibe-check")
        self.master_file = self.vibe_check_dir / "reviews" / "_MASTER.json"
        self.use_git = False
        self.force_no_git = os.environ.get('FORCE_NO_GIT', '0') == '1'
    
    def check_prerequisites(self) -> bool:
        """Check if vibe-check directory exists"""
        if not self.vibe_check_dir.exists():
            print_status(Colors.RED, "Error: vibe-check directory not found!")
            print("Please run the setup script first to create the vibe-check structure.")
            return False
        return True
    
    def detect_git(self) -> bool:
        """Check if git is available and we're in a git repository"""
        if self.force_no_git:
            print_status(Colors.YELLOW, "Forced non-git mode. Using find command.")
            return False
        
        try:
            # Check if git is available
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            # Check if we're in a git repo
            subprocess.run(['git', 'rev-parse', '--git-dir'], capture_output=True, check=True)
            print_status(Colors.GREEN, "Git repository detected. Using git ls-files to respect .gitignore")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_status(Colors.YELLOW, "Not a git repository or git not available. Using find command.")
            return False
    
    def has_valid_extension(self, file_path: Path) -> bool:
        """Check if file has a valid source extension"""
        return file_path.suffix[1:] in self.SOURCE_EXTENSIONS
    
    def count_lines(self, file_path: Path) -> int:
        """Count lines of code (simple line count)"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0
    
    def detect_language(self, file_path: Path) -> str:
        """Detect language from file extension"""
        ext = file_path.suffix[1:]
        return self.LANGUAGE_MAP.get(ext, 'Unknown')
    
    def get_git_files(self) -> List[Path]:
        """Get list of tracked files from git"""
        try:
            result = subprocess.run(
                ['git', 'ls-files'],
                capture_output=True,
                text=True,
                check=True
            )
            files = []
            for line in result.stdout.strip().split('\n'):
                if line and not line.startswith(str(self.vibe_check_dir) + '/'):
                    files.append(Path(line))
            return files
        except subprocess.CalledProcessError:
            return []
    
    def get_all_files(self) -> List[Path]:
        """Get all files using pathlib (non-git mode)"""
        files = []
        exclude_dirs = {
            '.git', 'node_modules', 'venv', 'env', '__pycache__',
            'build', 'dist', 'target', 'vendor', 'coverage',
            str(self.vibe_check_dir)
        }
        
        for path in Path('.').rglob('*'):
            # Skip if any parent directory is in exclude list
            if any(part.startswith('.') or part in exclude_dirs for part in path.parts):
                continue
            
            if path.is_file() and not path.name.startswith('.'):
                # Make path relative to current directory
                try:
                    relative_path = path.relative_to('.')
                    files.append(relative_path)
                except ValueError:
                    pass
        
        return files
    
    def create_master_data(self, files: List[Path]) -> Dict:
        """Create the master JSON structure"""
        data = {
            "metadata": {
                "version": "1.0",
                "description": "Vibe-Check Master Review Ledger - Single source of truth for all code review progress",
                "generated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
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
        
        file_count = 0
        total_loc = 0
        
        print(f"\n{Colors.GREEN}Scanning for source files...{Colors.NC}")
        
        for file_path in files:
            if not self.has_valid_extension(file_path):
                continue
            
            lang = self.detect_language(file_path)
            loc = self.count_lines(file_path)
            
            file_count += 1
            total_loc += loc
            
            data["files"][str(file_path)] = {
                "language": lang,
                "loc": loc,
                "status": "not_reviewed",
                "review_date": None,
                "reviewer": None,
                "scores": {
                    "security": None,
                    "performance": None,
                    "maintainability": None,
                    "consistency": None,
                    "best_practices": None,
                    "code_smell": None
                },
                "open_issues": 0,
                "dependency_count": 0
            }
            
            # Progress indicator
            if file_count % 10 == 0:
                print(f"\rProcessed {file_count} files...", end='', flush=True)
        
        print("\n")
        
        # Update metadata
        data["metadata"]["total_files"] = file_count
        data["metadata"]["total_loc"] = total_loc
        
        return data
    
    def run(self):
        """Main execution flow"""
        # Check prerequisites
        if not self.check_prerequisites():
            return 1
        
        # Detect git mode
        self.use_git = self.detect_git()
        
        # Get list of files
        if self.use_git:
            files = self.get_git_files()
        else:
            files = self.get_all_files()
        
        # Create master data
        data = self.create_master_data(files)
        
        # Save to file
        with open(self.master_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Summary
        print_status(Colors.GREEN, "✓ Master list populated successfully!")
        print(f"  Files found: {Colors.YELLOW}{data['metadata']['total_files']}{Colors.NC}")
        print(f"  Total LOC: {Colors.YELLOW}{data['metadata']['total_loc']}{Colors.NC}")
        print(f"  Output: {Colors.YELLOW}{self.master_file}{Colors.NC}")
        print()
        print("Next steps:")
        print(f"1. Review the generated list in {self.master_file}")
        print("2. Use the reviewer AI with REVIEWER_INSTRUCTIONS.md to process each file")
        print("3. The AI will update this master list as reviews are completed")
        
        return 0

def main():
    """Main entry point"""
    populator = VibeCheckPopulator()
    sys.exit(populator.run())

if __name__ == "__main__":
    main()
```

After creating this file, make it executable:
```bash
chmod +x vibe-check/scripts/populate_master.py
```

#### 2.8 Create `vibe-check/scripts/run_single_review.py`

Create this executable script with the following content:

```python
#!/usr/bin/env python3
"""
run_single_review.py - Run a single file review using Claude Code CLI
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
import time
import re

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_status(color: str, message: str):
    """Print colored status message"""
    print(f"{color}{message}{Colors.NC}")

class VibeCheckReviewer:
    def __init__(self):
        self.vibe_check_dir = Path("vibe-check")
        self.master_file = self.vibe_check_dir / "reviews" / "_MASTER.json"
        self.instructions_file = self.vibe_check_dir / "prompts" / "REVIEWER_INSTRUCTIONS.md"
        self.log_dir = self.vibe_check_dir / "logs"
        
        # Create logs directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate log file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"review_{timestamp}.log"
    
    def check_prerequisites(self) -> bool:
        """Check if all required files and tools are available"""
        # Check if Claude CLI is installed
        try:
            subprocess.run(["claude", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_status(Colors.RED, "Error: Claude Code CLI not found!")
            print("Please install it with: npm install -g @anthropic-ai/claude-code")
            return False
        
        # Check authentication
        if os.environ.get("ANTHROPIC_API_KEY"):
            print_status(Colors.GREEN, "✓ Using Anthropic API key from environment")
        else:
            print_status(Colors.YELLOW, "No ANTHROPIC_API_KEY found - will attempt to use Claude subscription")
            print("Make sure you're signed into Claude CLI")
        
        # Check if vibe-check structure exists
        if not self.instructions_file.exists():
            print_status(Colors.RED, f"Error: {self.instructions_file} not found!")
            print("Please run the vibe-check setup first.")
            return False
        
        if not self.master_file.exists():
            print_status(Colors.RED, f"Error: {self.master_file} not found!")
            print("Please run populate_master.py first.")
            return False
        
        return True
    
    def load_master_data(self) -> Dict[str, Any]:
        """Load the master JSON file"""
        with open(self.master_file, 'r') as f:
            return json.load(f)
    
    def save_master_data(self, data: Dict[str, Any]):
        """Save the master JSON file"""
        with open(self.master_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def find_next_file(self) -> Optional[str]:
        """Find next file to review (in_progress first, then not_reviewed)"""
        data = self.load_master_data()
        
        # First check for any in_progress files (failed previous runs)
        for file_path, info in data['files'].items():
            if info['status'] == 'in_progress':
                return file_path
        
        # Then check for not_reviewed files
        for file_path, info in data['files'].items():
            if info['status'] == 'not_reviewed':
                return file_path
        
        return None
    
    def count_remaining_files(self) -> int:
        """Count how many files are left to review"""
        data = self.load_master_data()
        return sum(1 for info in data['files'].values() 
                  if info['status'] in ['not_reviewed', 'in_progress'])
    
    def mark_file_status(self, file_path: str, status: str):
        """Update file status in master JSON"""
        data = self.load_master_data()
        data['files'][file_path]['status'] = status
        self.save_master_data(data)
    
    def get_file_status(self, file_path: str) -> str:
        """Get current status of a file"""
        data = self.load_master_data()
        return data['files'][file_path]['status']
    
    def create_prompt(self, file_path: str) -> str:
        """Create the prompt for Claude"""
        with open(self.instructions_file, 'r') as f:
            instructions = f.read()
        
        prompt = f"""You have access to a vibe-check directory at path 'vibe-check/' containing review artifacts.

You are tasked with reviewing the following file:
FILE_PATH: {file_path}

Please follow these instructions exactly:

{instructions}"""
        
        return prompt
    
    def parse_claude_output(self, log_content: str) -> Dict[str, Any]:
        """Extract cost and other metrics from Claude's output"""
        # Find the last result JSON in the log
        result_lines = [line for line in log_content.split('\n') 
                       if '"type": "result"' in line or '"type":"result"' in line]
        
        if not result_lines:
            return {}
        
        try:
            result_json = json.loads(result_lines[-1])
            cost = result_json.get('total_cost_usd', 'N/A')
            duration = result_json.get('duration_ms', 'N/A')
            turns = result_json.get('num_turns', 'N/A')
            
            return {
                'cost': cost,
                'duration': duration,
                'turns': turns
            }
        except json.JSONDecodeError:
            return {}
    
    def run_claude_review(self, file_path: str) -> Tuple[bool, str]:
        """Execute Claude with the review prompt"""
        prompt = self.create_prompt(file_path)
        
        # Build the Claude command
        cmd = [
            'claude',
            '--print', prompt,
            '--output-format', 'stream-json',
            '--permission-mode', 'acceptEdits',
            '--verbose'
        ]
        
        print_status(Colors.BLUE, "Launching Claude Code for review...")
        print("----------------------------------------")
        
        # Open log file for writing
        with open(self.log_file, 'w') as log:
            # Run Claude and capture output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            log_content = []
            
            # Process output line by line
            for line in iter(process.stdout.readline, ''):
                # Write to log file
                log.write(line)
                log.flush()
                log_content.append(line.strip())
                
                # Try to parse as JSON for display
                try:
                    data = json.loads(line.strip())
                    if data.get('type') == 'assistant':
                        # Extract text content from assistant messages
                        message = data.get('message', {})
                        content = message.get('content', [])
                        for item in content:
                            if item.get('type') == 'text':
                                text = item.get('text', '').strip()
                                if text:
                                    print(text)
                                    print('---')
                except json.JSONDecodeError:
                    # Not JSON, skip
                    pass
            
            # Wait for process to complete
            process.wait()
            
        print("----------------------------------------")
        
        # Check exit code
        success = process.returncode == 0
        log_text = '\n'.join(log_content)
        
        return success, log_text
    
    def run(self):
        """Main execution flow"""
        # Check prerequisites
        if not self.check_prerequisites():
            return 1
        
        # Find next file to review
        file_to_review = self.find_next_file()
        if not file_to_review:
            print_status(Colors.GREEN, "All files have been reviewed! No files left to process.")
            return 0
        
        # Count remaining files
        remaining = self.count_remaining_files()
        
        print_status(Colors.BLUE, "=== Starting Vibe-Check Single Review ===")
        print_status(Colors.YELLOW, f"File to review: {file_to_review}")
        print_status(Colors.YELLOW, f"Files remaining to review: {remaining}")
        print_status(Colors.YELLOW, f"Logging to: {self.log_file}")
        print_status(Colors.YELLOW, "Permission mode: Auto-accepting file edits")
        print()
        
        # Check if file is already in progress
        current_status = self.get_file_status(file_to_review)
        if current_status == 'in_progress':
            print_status(Colors.YELLOW, f"⚠ Resuming previously failed review for {file_to_review}")
        else:
            # Mark as in progress
            self.mark_file_status(file_to_review, 'in_progress')
            print_status(Colors.GREEN, f"✓ Marked {file_to_review} as in_progress")
        
        # Run the review
        success, log_content = self.run_claude_review(file_to_review)
        
        if success:
            print_status(Colors.GREEN, "✓ Review completed successfully!")
            
            # Mark as completed
            self.mark_file_status(file_to_review, 'completed')
            print_status(Colors.GREEN, f"✓ Marked {file_to_review} as completed")
            
            # Extract and display cost information
            metrics = self.parse_claude_output(log_content)
            if metrics:
                print()
                print_status(Colors.BLUE, "=== Execution Summary ===")
                
                if metrics['cost'] != 'N/A':
                    print(f"Cost: ${metrics['cost']:.4f} USD")
                else:
                    print("Cost: Not available")
                
                if metrics['duration'] != 'N/A':
                    duration_sec = metrics['duration'] / 1000
                    print(f"Duration: {duration_sec:.1f} seconds")
                
                if metrics['turns'] != 'N/A':
                    print(f"Turns: {metrics['turns']}")
            
            # Check remaining files
            remaining = self.count_remaining_files()
            print()
            print_status(Colors.YELLOW, f"Files remaining to review: {remaining}")
            
            return 0
        else:
            print_status(Colors.RED, "✗ Review failed!")
            print_status(Colors.RED, f"Check the log file for details: {self.log_file}")
            
            # Revert to not_reviewed
            self.mark_file_status(file_to_review, 'not_reviewed')
            print_status(Colors.YELLOW, f"⚠ Reverted {file_to_review} back to not_reviewed status")
            
            return 1

def main():
    """Main entry point"""
    reviewer = VibeCheckReviewer()
    sys.exit(reviewer.run())

if __name__ == "__main__":
    main()
```

After creating this file, make it executable:
```bash
chmod +x vibe-check/scripts/run_single_review.py
```

#### 2.9 Create `vibe-check/scripts/review_all.py`

Create this executable script with the following content:

```python
#!/usr/bin/env python3
"""
review_all.py - Run reviews for all unreviewed files using run_single_review
"""

import subprocess
import sys
import os
import time
from pathlib import Path
import json
from typing import Dict, Any

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_status(color: str, message: str):
    """Print colored status message"""
    print(f"{color}{message}{Colors.NC}")

class VibeCheckBatchReviewer:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.single_review_script = self.script_dir / "run_single_review.py"
        self.master_file = Path("vibe-check/reviews/_MASTER.json")
        self.delay_seconds = 5
    
    def check_prerequisites(self) -> bool:
        """Check if required files exist"""
        if not self.single_review_script.exists():
            print_status(Colors.RED, f"Error: {self.single_review_script} not found!")
            return False
        
        if not self.single_review_script.is_file() or not os.access(self.single_review_script, os.X_OK):
            print_status(Colors.RED, f"Error: {self.single_review_script} is not executable!")
            return False
        
        if not self.master_file.exists():
            print_status(Colors.RED, f"Error: {self.master_file} not found!")
            return False
        
        # Check authentication
        if os.environ.get("ANTHROPIC_API_KEY"):
            print_status(Colors.GREEN, "✓ Using Anthropic API key from environment")
        else:
            print_status(Colors.YELLOW, "No ANTHROPIC_API_KEY found - will use Claude subscription")
            print("Make sure you're signed into Claude CLI")
        
        return True
    
    def count_remaining_files(self) -> int:
        """Count how many files are left to review"""
        try:
            with open(self.master_file, 'r') as f:
                data = json.load(f)
            
            return sum(1 for info in data['files'].values() 
                      if info['status'] in ['not_reviewed', 'in_progress'])
        except Exception:
            return 0
    
    def run_single_review(self) -> bool:
        """Run a single review and return success status"""
        try:
            # Run the single review script
            result = subprocess.run(
                [sys.executable, str(self.single_review_script)],
                capture_output=False,  # Let output go to console
                text=True
            )
            
            return result.returncode == 0
        except Exception as e:
            print_status(Colors.RED, f"Error running review: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        # Check prerequisites
        if not self.check_prerequisites():
            return 1
        
        print_status(Colors.BLUE, "=== Vibe-Check Batch Review Process ===")
        print()
        
        # Counters
        total_reviewed = 0
        failed_reviews = 0
        
        # Main review loop
        while True:
            # Check remaining files
            remaining = self.count_remaining_files()
            
            if remaining == 0:
                print_status(Colors.GREEN, "✓ All files have been reviewed!")
                break
            
            print_status(Colors.YELLOW, f"Files remaining: {remaining}")
            print_status(Colors.BLUE, f"Starting review #{total_reviewed + 1}...")
            print()
            
            # Run single review
            if self.run_single_review():
                total_reviewed += 1
                print_status(Colors.GREEN, f"✓ Review #{total_reviewed} completed successfully")
            else:
                failed_reviews += 1
                print_status(Colors.RED, "✗ Review failed! Stopping batch process.")
                break
            
            # Add delay between reviews to avoid rate limiting
            if remaining > 1:
                print_status(Colors.YELLOW, f"Waiting {self.delay_seconds} seconds before next review...")
                time.sleep(self.delay_seconds)
            
            print()
            print("=" * 40)
            print()
        
        # Final summary
        print()
        print_status(Colors.BLUE, "=== Batch Review Summary ===")
        print_status(Colors.GREEN, f"Total files reviewed: {total_reviewed}")
        
        if failed_reviews > 0:
            print_status(Colors.RED, f"Failed reviews: {failed_reviews}")
            return 1
        else:
            print_status(Colors.GREEN, "All reviews completed successfully!")
            return 0

def main():
    """Main entry point"""
    reviewer = VibeCheckBatchReviewer()
    sys.exit(reviewer.run())

if __name__ == "__main__":
    main()
```

After creating this file, make it executable:
```bash
chmod +x vibe-check/scripts/review_all.py
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
- [ ] `vibe-check/scripts/populate_master.py` exists and is executable
- [ ] `vibe-check/scripts/run_single_review.py` exists and is executable
- [ ] `vibe-check/scripts/review_all.py` exists and is executable

### 4. Next Steps

Once this structure is in place:

1. Check if your project uses Git:
   ```bash
   # Check if current directory is a Git repository
   git rev-parse --git-dir > /dev/null 2>&1 && echo "Git repository detected" || echo "Not a Git repository"
   ```

2. Run the populate_master.py script based on your Git status:
   ```bash
   # If Git repository detected (will respect .gitignore):
   ./vibe-check/scripts/populate_master.py
   
   # If NOT a Git repository (will use find command):
   FORCE_NO_GIT=1 ./vibe-check/scripts/populate_master.py
   ```
   
   The script will automatically detect Git and inform you which mode it's using:
   - **Git mode**: "Git repository detected. Using git ls-files to respect .gitignore"
   - **Non-Git mode**: "Not a git repository or git not available. Using find command."

3. Review the generated master list to ensure all expected files are included

4. Run a single file review:
   ```bash
   # With API key
   export ANTHROPIC_API_KEY="your-api-key"
   ./vibe-check/scripts/run_single_review.py
   
   # Or with Claude subscription (requires claude login)
   ./vibe-check/scripts/run_single_review.py
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
   ./vibe-check/scripts/review_all.py
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