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

#### 2.7 Create `vibe-check/scripts/vibe-check`

Create this unified executable script that handles all vibe-check operations:

```python
#!/usr/bin/env python3
"""vibe-check - Unified code review system CLI"""

import argparse
import json
import subprocess
import sys
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# ANSI color codes
RED, GREEN, YELLOW, BLUE, NC = '\033[0;31m', '\033[0;32m', '\033[1;33m', '\033[0;34m', '\033[0m'

def print_status(color: str, msg: str): print(f"{color}{msg}{NC}")

# Common source file extensions and language mapping
SOURCE_EXTS = {'js','jsx','ts','tsx','py','pyw','java','kt','kts','c','cpp','cc','cxx','h','hpp',
               'cs','go','rs','rb','php','swift','m','mm','scala','r','R','lua','pl','pm',
               'sh','bash','zsh','sql','vue','elm','ex','exs'}

LANG_MAP = {'js':'JavaScript','jsx':'JavaScript','ts':'TypeScript','tsx':'TypeScript',
            'py':'Python','pyw':'Python','java':'Java','kt':'Kotlin','kts':'Kotlin',
            'c':'C','h':'C','cpp':'C++','cc':'C++','cxx':'C++','hpp':'C++','cs':'C#',
            'go':'Go','rs':'Rust','rb':'Ruby','php':'PHP','swift':'Swift',
            'm':'Objective-C','mm':'Objective-C','scala':'Scala','r':'R','R':'R',
            'lua':'Lua','pl':'Perl','pm':'Perl','sh':'Shell','bash':'Shell','zsh':'Shell',
            'sql':'SQL','vue':'Vue','elm':'Elm','ex':'Elixir','exs':'Elixir'}

class VibeCheck:
    def __init__(self):
        self.vibe_dir = Path("vibe-check")
        self.master_file = self.vibe_dir / "reviews" / "_MASTER.json"
        self.inst_file = self.vibe_dir / "prompts" / "REVIEWER_INSTRUCTIONS.md"
        self.log_dir = self.vibe_dir / "logs"
    
    def check_setup(self):
        if not self.vibe_dir.exists():
            print_status(RED, "Error: vibe-check directory not found! Run setup first.")
            return False
        return True
    
    def load_master(self) -> Dict:
        with open(self.master_file, 'r') as f: return json.load(f)
    
    def save_master(self, data: Dict):
        with open(self.master_file, 'w') as f: json.dump(data, f, indent=2)
    
    def count_remaining(self) -> int:
        if not self.master_file.exists(): return 0
        data = self.load_master()
        return sum(1 for info in data['files'].values() if info['status'] in ['not_reviewed', 'in_progress'])
    
    def populate(self, no_git: bool = False) -> int:
        """Scan repository and populate file list"""
        if not self.check_setup(): return 1
        
        # Detect git
        use_git = False
        if not no_git:
            try:
                subprocess.run(['git', 'rev-parse', '--git-dir'], capture_output=True, check=True)
                use_git = True
                print_status(GREEN, "Git repository detected. Using git ls-files.")
            except: print_status(YELLOW, "Not a git repository. Using find.")
        
        # Get files
        files = []
        if use_git:
            result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
            for line in result.stdout.strip().split('\n'):
                if line and not line.startswith(str(self.vibe_dir) + '/'):
                    files.append(Path(line))
        else:
            exclude = {'.git','node_modules','venv','env','__pycache__','build','dist','target','vendor','coverage',str(self.vibe_dir)}
            for p in Path('.').rglob('*'):
                if p.is_file() and not any(part.startswith('.') or part in exclude for part in p.parts):
                    files.append(p.relative_to('.'))
        
        # Build master data
        data = {
            "metadata": {
                "version": "1.0",
                "description": "Vibe-Check Master Review Ledger",
                "generated": datetime.utcnow().isoformat() + "Z",
                "total_files": 0, "total_loc": 0,
                "status_legend": {
                    "not_reviewed": "File has not been reviewed yet",
                    "in_progress": "Review is currently in progress",
                    "completed": "Review has been completed",
                    "needs_update": "Source file changed, review needs update"
                },
                "score_range": {"min": 1, "max": 5, "description": "1 = Critical issues, 5 = Excellent"}
            },
            "files": {}
        }
        
        print(f"\n{GREEN}Scanning for source files...{NC}")
        file_count = total_loc = 0
        
        for f in files:
            if f.suffix[1:] not in SOURCE_EXTS: continue
            
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    loc = sum(1 for _ in file)
            except: loc = 0
            
            file_count += 1
            total_loc += loc
            
            data["files"][str(f)] = {
                "language": LANG_MAP.get(f.suffix[1:], 'Unknown'),
                "loc": loc, "status": "not_reviewed",
                "review_date": None, "reviewer": None,
                "scores": {k: None for k in ["security","performance","maintainability","consistency","best_practices","code_smell"]},
                "open_issues": 0, "dependency_count": 0
            }
            
            if file_count % 10 == 0: print(f"\rProcessed {file_count} files...", end='', flush=True)
        
        data["metadata"]["total_files"] = file_count
        data["metadata"]["total_loc"] = total_loc
        
        self.save_master(data)
        print(f"\n{GREEN}✓ Master list populated!{NC}")
        print(f"  Files: {YELLOW}{file_count}{NC}, LOC: {YELLOW}{total_loc}{NC}")
        return 0
    
    def review(self) -> int:
        """Review a single file"""
        if not self.check_setup(): return 1
        
        # Check prerequisites
        try: subprocess.run(["claude", "--version"], capture_output=True, check=True)
        except:
            print_status(RED, "Error: Claude CLI not found! Install: npm install -g @anthropic-ai/claude-code")
            return 1
        
        if os.environ.get("ANTHROPIC_API_KEY"):
            print_status(GREEN, "✓ Using API key")
        else:
            print_status(YELLOW, "No API key - using Claude subscription")
        
        if not self.inst_file.exists() or not self.master_file.exists():
            print_status(RED, "Missing files! Run populate first.")
            return 1
        
        # Find next file
        data = self.load_master()
        file_to_review = None
        
        for fp, info in data['files'].items():
            if info['status'] == 'in_progress':
                file_to_review = fp
                break
        
        if not file_to_review:
            for fp, info in data['files'].items():
                if info['status'] == 'not_reviewed':
                    file_to_review = fp
                    break
        
        if not file_to_review:
            print_status(GREEN, "All files reviewed!")
            return 0
        
        # Setup review
        self.log_dir.mkdir(exist_ok=True)
        log_file = self.log_dir / f"review_{datetime.now():%Y%m%d_%H%M%S}.log"
        remaining = self.count_remaining()
        
        print_status(BLUE, "=== Starting Review ===")
        print(f"{YELLOW}File: {file_to_review}\nRemaining: {remaining}\nLog: {log_file}{NC}\n")
        
        # Mark in progress
        if data['files'][file_to_review]['status'] != 'in_progress':
            data['files'][file_to_review]['status'] = 'in_progress'
            self.save_master(data)
            print_status(GREEN, f"✓ Marked {file_to_review} as in_progress")
        else:
            print_status(YELLOW, f"⚠ Resuming {file_to_review}")
        
        # Create prompt
        with open(self.inst_file, 'r') as f: instructions = f.read()
        prompt = f"You have access to vibe-check/ directory.\n\nReview this file:\nFILE_PATH: {file_to_review}\n\n{instructions}"
        
        # Run Claude
        cmd = ['claude', '--print', prompt, '--output-format', 'stream-json', '--permission-mode', 'acceptEdits', '--verbose']
        print_status(BLUE, "Launching Claude...")
        print("-" * 40)
        
        with open(log_file, 'w') as log:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            log_content = []
            
            for line in iter(proc.stdout.readline, ''):
                log.write(line)
                log_content.append(line.strip())
                
                try:
                    d = json.loads(line.strip())
                    if d.get('type') == 'assistant':
                        for item in d.get('message', {}).get('content', []):
                            if item.get('type') == 'text' and (text := item.get('text', '').strip()):
                                print(f"{text}\n---")
                except: pass
            
            proc.wait()
        
        print("-" * 40)
        
        # Handle result
        if proc.returncode == 0:
            print_status(GREEN, "✓ Review completed!")
            data = self.load_master()
            data['files'][file_to_review]['status'] = 'completed'
            self.save_master(data)
            
            # Parse metrics
            for line in reversed(log_content):
                if '"type":"result"' in line or '"type": "result"' in line:
                    try:
                        r = json.loads(line)
                        print(f"\n{BLUE}=== Summary ==={NC}")
                        if (c := r.get('total_cost_usd')) != 'N/A': print(f"Cost: ${c:.4f}")
                        if (d := r.get('duration_ms')) != 'N/A': print(f"Duration: {d/1000:.1f}s")
                        if (t := r.get('num_turns')) != 'N/A': print(f"Turns: {t}")
                        break
                    except: pass
            
            print(f"\n{YELLOW}Remaining: {self.count_remaining()}{NC}")
            return 0
        else:
            print_status(RED, f"✗ Review failed! Check: {log_file}")
            data = self.load_master()
            data['files'][file_to_review]['status'] = 'not_reviewed'
            self.save_master(data)
            return 1
    
    def review_all(self, delay: int = 5) -> int:
        """Review all remaining files"""
        if not self.check_setup(): return 1
        
        print_status(BLUE, "=== Batch Review ===")
        reviewed = failed = 0
        
        while self.count_remaining() > 0:
            print(f"\n{YELLOW}Remaining: {self.count_remaining()}\nStarting #{reviewed + 1}...{NC}\n")
            
            if self.review() == 0:
                reviewed += 1
                print_status(GREEN, f"✓ Review #{reviewed} done")
            else:
                failed += 1
                print_status(RED, "✗ Failed! Stopping.")
                break
            
            if self.count_remaining() > 0:
                print(f"{YELLOW}Waiting {delay}s...{NC}")
                time.sleep(delay)
            print("\n" + "="*40)
        
        print(f"\n{BLUE}=== Summary ==={NC}")
        print(f"{GREEN}Reviewed: {reviewed}{NC}")
        if failed: print(f"{RED}Failed: {failed}{NC}")
        return 1 if failed else 0
    
    def status(self) -> int:
        """Show review status"""
        if not self.check_setup() or not self.master_file.exists(): return 1
        
        data = self.load_master()
        files = data['files']
        total = len(files)
        
        counts = {}
        for info in files.values():
            s = info['status']
            counts[s] = counts.get(s, 0) + 1
        
        print(f"{BLUE}=== Vibe-Check Status ==={NC}\n")
        print(f"Total files: {YELLOW}{total}{NC}")
        print(f"Total LOC: {YELLOW}{data['metadata']['total_loc']}{NC}\n")
        
        for status, count in sorted(counts.items()):
            color = GREEN if status == 'completed' else YELLOW if status == 'in_progress' else RED
            print(f"{status:15} {color}{count:4d}{NC} ({count/total*100:5.1f}%)")
        
        if total > 0:
            done = counts.get('completed', 0)
            pct = done / total
            bar = '█' * int(40 * pct) + '░' * int(40 * (1-pct))
            print(f"\nProgress: [{GREEN}{bar}{NC}] {pct*100:.1f}%")
        
        return 0

def main():
    parser = argparse.ArgumentParser(description='Vibe-Check: AI code review', prog='vibe-check')
    sub = parser.add_subparsers(dest='cmd', help='Commands')
    
    p = sub.add_parser('populate', help='Scan and populate file list')
    p.add_argument('--no-git', action='store_true', help='Ignore git')
    
    sub.add_parser('review', help='Review single file')
    
    r = sub.add_parser('review-all', help='Review all files')
    r.add_argument('--delay', type=int, default=5, help='Delay between reviews')
    
    sub.add_parser('status', help='Show progress')
    
    args = parser.parse_args()
    if not args.cmd: parser.print_help(); return 1
    
    vc = VibeCheck()
    
    if args.cmd == 'populate': return vc.populate(args.no_git)
    elif args.cmd == 'review': return vc.review()
    elif args.cmd == 'review-all': return vc.review_all(args.delay)
    elif args.cmd == 'status': return vc.status()
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
```

After creating this file, make it executable:
```bash
chmod +x vibe-check/scripts/vibe-check
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
- [ ] `vibe-check/scripts/vibe-check` exists and is executable

### 4. Usage Instructions

Once the structure is in place, use the unified `vibe-check` command for all operations:

#### 4.1 Check if your project uses Git:
```bash
# Check if current directory is a Git repository
git rev-parse --git-dir > /dev/null 2>&1 && echo "Git repository detected" || echo "Not a Git repository"
```

#### 4.2 Populate the file list:
```bash
# If Git repository (respects .gitignore):
./vibe-check/scripts/vibe-check populate

# If NOT a Git repository (scans all files):
./vibe-check/scripts/vibe-check populate --no-git
```

The script will automatically detect Git and inform you which mode it's using:
- **Git mode**: "Git repository detected. Using git ls-files."
- **Non-Git mode**: "Not a git repository. Using find."

#### 4.3 Review a single file:
```bash
# With API key
export ANTHROPIC_API_KEY="your-api-key"
./vibe-check/scripts/vibe-check review

# Or with Claude subscription (requires claude login)
./vibe-check/scripts/vibe-check review
```

The script will:
- Find the next unreviewed file automatically (or resume in-progress files)
- Show Claude's analysis in real-time
- Save full logs to `vibe-check/logs/`
- Update `_MASTER.json` with status
- Create review markdown in `vibe-check/reviews/modules/`
- Display cost and execution summary

#### 4.4 Review all remaining files:
```bash
# Review all with default 5-second delay
./vibe-check/scripts/vibe-check review-all

# Review all with custom delay
./vibe-check/scripts/vibe-check review-all --delay 10
```

The batch review will:
- Process all unreviewed files one by one
- Add delays between reviews to avoid rate limiting
- Stop if any review fails
- Display a summary at the end

#### 4.5 Check review progress:
```bash
./vibe-check/scripts/vibe-check status
```

This shows:
- Total files and lines of code
- Breakdown by status (not_reviewed, in_progress, completed)
- Visual progress bar
- Percentage completion

### 5. Command Reference

```bash
# Show help
./vibe-check/scripts/vibe-check --help

# Populate file list
./vibe-check/scripts/vibe-check populate [--no-git]

# Review single file
./vibe-check/scripts/vibe-check review

# Review all files
./vibe-check/scripts/vibe-check review-all [--delay SECONDS]

# Show status
./vibe-check/scripts/vibe-check status
```

### 6. Important Notes

- All files should be created with UTF-8 encoding
- Use Unix-style line endings (LF)
- The unified script is only 326 lines but provides all functionality
- Source code files are treated as read-only during reviews
- The vibe-check folder can be added to `.gitignore` if you don't want to commit reviews
- Alternatively, commit the vibe-check folder to track review history over time
- The script automatically handles interrupted reviews by resuming "in_progress" files

This setup creates a complete code review system with a single, compact Python script that handles all operations efficiently.