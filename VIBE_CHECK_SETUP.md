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

#### 2.2 Create `vibe-check/reviews/system/HOTSPOTS.md`

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

#### 2.3 Create `vibe-check/reviews/system/METRICS_SUMMARY.md`

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

#### 2.4 Create `vibe-check/reviews/modules/README.md`

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

#### 2.5 Create `vibe-check/reviews/_SCRATCHSHEET.md`

Create this file with the following content:

```markdown
---
last_updated: 2025-07-06T00:00:00Z
entry_count: 0
max_entries: 50
---

# Project Conventions & Patterns

## Naming Conventions
<!-- Key naming patterns discovered across the codebase -->

## Architecture Patterns
<!-- Important architectural decisions and patterns -->

## Common Dependencies
<!-- Frequently used libraries and versions -->

## Security Patterns
<!-- Project-specific security requirements -->

## Performance Patterns
<!-- Known optimizations or bottlenecks -->

## Testing Conventions
<!-- Test framework patterns and requirements -->
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

## Precise Algorithm to Follow

### Step 0: Read Global Scratchsheet
- Open and read `vibe-check/reviews/_SCRATCHSHEET.md`
- Note any project-wide conventions and patterns
- Use these patterns to inform your consistency assessments
- Keep the scratchsheet content in mind throughout the review

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

### Step 4: Create Review Markdown

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

### Step 5: Update Global Scratchsheet
- Open `vibe-check/reviews/_SCRATCHSHEET.md`
- Add any newly discovered project-wide patterns that:
  - Apply to multiple files (3+ occurrences)
  - Are not language defaults
  - Would help future reviews
- Keep entries concise (1-2 lines each)
- Remove outdated or least useful entries if over 50 total
- Update the entry_count in frontmatter
- Update the last_updated timestamp
- Example additions:
  - "All API routes use kebab-case, not camelCase"
  - "Error messages always include context object"
  - "Test files use 'describe/it' not 'test' blocks"
  - "All async functions have explicit error handling"

### Step 6: Complete
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
        
        # Create prompt with scratchsheet
        with open(self.inst_file, 'r') as f: instructions = f.read()
        
        # Read scratchsheet if it exists
        scratchsheet_file = self.vibe_dir / "reviews" / "_SCRATCHSHEET.md"
        scratchsheet_content = ""
        if scratchsheet_file.exists():
            with open(scratchsheet_file, 'r') as f:
                scratchsheet_content = f"\n\n## Global Scratchsheet\nThe following patterns have been discovered across the codebase:\n\n{f.read()}"
        
        prompt = f"You have access to vibe-check/ directory.\n\nReview this file:\nFILE_PATH: {file_to_review}{scratchsheet_content}\n\n{instructions}"
        
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
    
    def synthesize(self, severity: str = 'medium', category: str = 'all', 
                   score_threshold: Optional[int] = None, critical_only: bool = False,
                   interactive: bool = True) -> int:
        """Synthesize individual reviews into actionable insights"""
        if not self.check_setup(): return 1
        
        # Check prerequisites
        try: subprocess.run(["claude", "--version"], capture_output=True, check=True)
        except:
            print_status(RED, "Error: Claude CLI not found! Install: npm install -g @anthropic-ai/claude-code")
            return 1
        
        if not self.master_file.exists():
            print_status(RED, "No reviews found! Run populate and review first.")
            return 1
        
        # Create synthesis directory structure
        synthesis_dir = self.vibe_dir / "synthesis"
        synthesis_dir.mkdir(exist_ok=True)
        (synthesis_dir / "priority-high").mkdir(exist_ok=True)
        (synthesis_dir / "priority-medium").mkdir(exist_ok=True)
        (synthesis_dir / "priority-low").mkdir(exist_ok=True)
        
        # Load completed reviews
        data = self.load_master()
        completed_files = {fp: info for fp, info in data['files'].items() 
                          if info['status'] == 'completed'}
        
        if not completed_files:
            print_status(RED, "No completed reviews found! Run reviews first.")
            return 1
        
        # Collect issues from review files
        issues = self._collect_issues(completed_files)
        
        if not issues:
            print_status(YELLOW, "No issues found in completed reviews.")
            return 0
        
        # Filter issues based on criteria
        filtered_issues = self._filter_issues(issues, severity, category, score_threshold, critical_only)
        
        # Interactive mode selection
        if interactive and len(issues) > 100:
            filtered_issues = self._interactive_selection(issues, filtered_issues)
        
        if not filtered_issues:
            print_status(YELLOW, f"No issues found matching criteria (severity: {severity}, category: {category})")
            return 0
        
        print_status(BLUE, f"Synthesizing {len(filtered_issues)} issues across {len(set(i['file'] for i in filtered_issues))} files...")
        
        # Process in chunks
        return self._process_synthesis_chunks(filtered_issues, severity)
    
    def _collect_issues(self, completed_files: Dict) -> List[Dict]:
        """Collect all issues from completed review files"""
        issues = []
        reviews_dir = self.vibe_dir / "reviews" / "modules"
        
        for file_path in completed_files.keys():
            # Handle nested directory structure
            review_file = reviews_dir / f"{file_path}.md"
            
            if review_file.exists():
                file_issues = self._parse_review_file(review_file, file_path)
                issues.extend(file_issues)
        return issues
    
    def _parse_review_file(self, review_file: Path, file_path: str) -> List[Dict]:
        """Parse a review markdown file and extract issues"""
        issues = []
        try:
            with open(review_file, 'r') as f:
                content = f.read()
            
            # Extract YAML frontmatter for scores
            scores = {}
            if content.startswith('---'):
                yaml_end = content.find('---', 3)
                if yaml_end > 0:
                    yaml_content = content[3:yaml_end]
                    # Parse scores (simplified)
                    for line in yaml_content.split('\n'):
                        if 'score:' in line and '{' in line:
                            # Handle format like "  security:        {score: 1, open_issues: 4}"
                            if ':' in line:
                                metric = line.split(':')[0].strip()
                                score_part = line.split('score:')[1].strip()
                                if score_part.startswith('{') or score_part[0].isdigit():
                                    try:
                                        # Extract just the score number
                                        score_str = score_part.split(',')[0].replace('{', '').strip()
                                        score = int(score_str)
                                        scores[metric] = score
                                    except (ValueError, IndexError):
                                        pass
            
            # Extract issues from markdown sections
            lines = content.split('\n')
            current_category = None
            
            for i, line in enumerate(lines):
                if line.startswith('## ') and 'Issues' in line:
                    current_category = line.replace('## ', '').replace(' Issues', '').lower()
                elif line.startswith('### ') and current_category:
                    # Found an issue
                    parts = line[4:].split(' - ', 1)
                    if len(parts) == 2:
                        # Extract severity, handling format like "1. HIGH" or "HIGH"
                        severity_part = parts[0].strip('[]').upper()
                        # Remove number prefix if present (e.g., "1. HIGH" -> "HIGH")
                        if '. ' in severity_part:
                            severity = severity_part.split('. ', 1)[1]
                        else:
                            severity = severity_part
                        title = parts[1]
                        
                        # Find location and description
                        location = description = recommendation = ""
                        for j in range(i+1, min(i+10, len(lines))):
                            if lines[j].startswith('- **Location**:'):
                                location = lines[j].replace('- **Location**:', '').strip()
                            elif lines[j].startswith('- **Description**:'):
                                description = lines[j].replace('- **Description**:', '').strip()
                            elif lines[j].startswith('- **Recommendation**:'):
                                recommendation = lines[j].replace('- **Recommendation**:', '').strip()
                            elif lines[j].startswith('##') or lines[j].startswith('###'):
                                break
                        
                        issue = {
                            'file': file_path,
                            'category': current_category,
                            'severity': severity,
                            'title': title,
                            'location': location,
                            'description': description,
                            'recommendation': recommendation,
                            'file_scores': scores
                        }
                        issues.append(issue)
        
        except Exception as e:
            print_status(YELLOW, f"Warning: Could not parse {review_file}: {e}")
        
        return issues
    
    def _filter_issues(self, issues: List[Dict], severity: str, category: str, 
                      score_threshold: Optional[int], critical_only: bool) -> List[Dict]:
        """Filter issues based on specified criteria"""
        filtered = issues.copy()
        
        # Filter by severity
        severity_levels = {
            'high': ['HIGH'],
            'medium': ['HIGH', 'MEDIUM'],
            'low': ['HIGH', 'MEDIUM', 'LOW']
        }
        if severity in severity_levels:
            filtered = [i for i in filtered if i['severity'] in severity_levels[severity]]
        
        # Filter by category
        if category != 'all':
            filtered = [i for i in filtered if i['category'] == category.lower()]
        
        # Filter by score threshold
        if score_threshold:
            filtered = [i for i in filtered if any(score and score < score_threshold 
                       for score in i['file_scores'].values())]
        
        # Filter critical files only
        if critical_only:
            filtered = [i for i in filtered if any(score and score <= 2 
                       for score in i['file_scores'].values())]
        
        return filtered
    
    def _interactive_selection(self, all_issues: List[Dict], filtered_issues: List[Dict]) -> List[Dict]:
        """Interactive selection when there are many issues"""
        total = len(all_issues)
        high_count = len([i for i in all_issues if i['severity'] == 'HIGH'])
        medium_count = len([i for i in all_issues if i['severity'] == 'MEDIUM'])
        low_count = len([i for i in all_issues if i['severity'] == 'LOW'])
        
        print(f"\n{BLUE}Found {total} total issues:{NC}")
        print(f"  - {high_count} HIGH severity issues")
        print(f"  - {medium_count} MEDIUM severity issues")
        print(f"  - {low_count} LOW severity issues")
        print(f"\nCurrent filter would process {len(filtered_issues)} issues.")
        print(f"\nSelect synthesis mode:")
        print(f"1. Quick (HIGH only) - ~{high_count} issues")
        print(f"2. Standard (HIGH + MEDIUM) - ~{high_count + medium_count} issues")
        print(f"3. Comprehensive (All) - ~{total} issues")
        print(f"4. Continue with current filter - {len(filtered_issues)} issues")
        
        while True:
            try:
                choice = input(f"\n{YELLOW}Choice (1-4): {NC}").strip()
                if choice == '1':
                    return self._filter_issues(all_issues, 'high', 'all', None, False)
                elif choice == '2':
                    return self._filter_issues(all_issues, 'medium', 'all', None, False)
                elif choice == '3':
                    return self._filter_issues(all_issues, 'low', 'all', None, False)
                elif choice == '4':
                    return filtered_issues
                else:
                    print("Please enter 1, 2, 3, or 4")
            except KeyboardInterrupt:
                print(f"\n{YELLOW}Cancelled.{NC}")
                return []
    
    def _process_synthesis_chunks(self, issues: List[Dict], severity: str) -> int:
        """Process issues in manageable chunks"""
        # Group issues by priority
        high_issues = [i for i in issues if i['severity'] == 'HIGH']
        medium_issues = [i for i in issues if i['severity'] == 'MEDIUM']
        low_issues = [i for i in issues if i['severity'] == 'LOW']
        
        chunks = []
        
        # Create chunks based on severity (smaller chunks for higher priority)
        if high_issues:
            chunks.extend(self._create_chunks(high_issues, 10, "Critical Issues"))
        if medium_issues:
            chunks.extend(self._create_chunks(medium_issues, 20, "Important Issues"))
        if low_issues:
            chunks.extend(self._create_chunks(low_issues, 30, "Other Issues"))
        
        if not chunks:
            print_status(YELLOW, "No issues to synthesize.")
            return 0
        
        print_status(BLUE, f"Processing {len(chunks)} chunks...")
        
        results = []
        for i, (chunk_issues, chunk_name) in enumerate(chunks, 1):
            print(f"\n{YELLOW}Processing chunk {i}/{len(chunks)}: {chunk_name} ({len(chunk_issues)} issues){NC}")
            
            result = self._synthesize_chunk(chunk_issues, chunk_name, i)
            if result:
                results.append(result)
        
        # Create final synthesis
        if results:
            self._create_final_synthesis(results, severity)
            print_status(GREEN, f"✓ Synthesis complete! Check vibe-check/synthesis/ directory")
            return 0
        else:
            print_status(RED, "✗ Synthesis failed")
            return 1
    
    def _create_chunks(self, issues: List[Dict], chunk_size: int, name: str) -> List[Tuple[List[Dict], str]]:
        """Split issues into chunks of specified size"""
        chunks = []
        for i in range(0, len(issues), chunk_size):
            chunk = issues[i:i+chunk_size]
            chunk_name = f"{name} {i//chunk_size + 1}" if len(issues) > chunk_size else name
            chunks.append((chunk, chunk_name))
        return chunks
    
    def _synthesize_chunk(self, issues: List[Dict], chunk_name: str, chunk_num: int) -> Optional[str]:
        """Synthesize a single chunk of issues"""
        # Create synthesis prompt
        prompt = self._create_synthesis_prompt(issues, chunk_name)
        
        # Set up logging
        self.log_dir.mkdir(exist_ok=True)
        log_file = self.log_dir / f"synthesis_{chunk_num}_{datetime.now():%Y%m%d_%H%M%S}.log"
        
        # Run Claude
        cmd = ['claude', '--print', prompt, '--output-format', 'stream-json', '--permission-mode', 'acceptEdits', '--verbose']
        
        try:
            with open(log_file, 'w') as log:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                output_lines = []
                
                for line in iter(proc.stdout.readline, ''):
                    log.write(line)
                    try:
                        d = json.loads(line.strip())
                        if d.get('type') == 'assistant':
                            for item in d.get('message', {}).get('content', []):
                                if item.get('type') == 'text' and (text := item.get('text', '').strip()):
                                    output_lines.append(text)
                    except: pass
                
                proc.wait()
            
            if proc.returncode == 0:
                return '\n'.join(output_lines)
            else:
                print_status(RED, f"✗ Chunk {chunk_num} failed")
                return None
                
        except Exception as e:
            print_status(RED, f"✗ Error processing chunk {chunk_num}: {e}")
            return None
    
    def _create_synthesis_prompt(self, issues: List[Dict], chunk_name: str) -> str:
        """Create prompt for synthesizing a chunk of issues"""
        issues_text = ""
        
        # Group issues by category
        by_category = {}
        for issue in issues:
            cat = issue['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(issue)
        
        for category, cat_issues in by_category.items():
            issues_text += f"\n## {category.title()} Issues\n"
            for issue in cat_issues:
                issues_text += f"\n### {issue['severity']} - {issue['title']}\n"
                issues_text += f"**File**: {issue['file']}\n"
                if issue['location']:
                    issues_text += f"**Location**: {issue['location']}\n"
                if issue['description']:
                    issues_text += f"**Description**: {issue['description']}\n"
                if issue['recommendation']:
                    issues_text += f"**Recommendation**: {issue['recommendation']}\n"
        
        return f"""You are analyzing code review findings to create actionable synthesis reports.

TASK: Synthesize the following {len(issues)} code review issues into actionable insights.

CHUNK: {chunk_name}

ISSUES TO ANALYZE:
{issues_text}

SYNTHESIS REQUIREMENTS:
1. **Cross-cutting patterns**: Identify issues that appear across multiple files
2. **Priority ranking**: Rank issues by business impact and fix effort  
3. **Root causes**: Look for underlying architectural or process issues
4. **Quick wins**: Identify high-impact, low-effort fixes
5. **Dependencies**: Note issues that must be fixed in order

OUTPUT FORMAT:
# {chunk_name} - Synthesis Report

## Executive Summary
[2-3 sentences summarizing the most critical findings]

## Priority Issues (Fix First)
[List 3-5 highest priority issues with business justification]

## Cross-cutting Patterns
[Issues appearing in multiple files - suggest systemic fixes]

## Quick Wins  
[High-impact, low-effort improvements]

## Root Cause Analysis
[Underlying issues causing multiple problems]

## Recommended Action Plan
[Prioritized steps for addressing these issues]

Keep the report concise and actionable. Focus on business impact over technical details."""
    
    def _create_final_synthesis(self, chunk_results: List[str], severity: str) -> None:
        """Create final synthesis combining all chunk results"""
        synthesis_dir = self.vibe_dir / "synthesis" / f"priority-{severity}"
        
        # Create executive summary
        exec_summary = synthesis_dir / "EXECUTIVE_SUMMARY.md"
        action_plan = synthesis_dir / "ACTION_PLAN.md"
        
        # Combine chunk results
        combined_content = "\n\n".join(chunk_results)
        
        # Create final synthesis prompt
        final_prompt = f"""You are creating a final executive synthesis of code review findings.

TASK: Create an executive summary and action plan from the following chunk syntheses.

CHUNK SYNTHESES:
{combined_content}

Create two outputs:

1. EXECUTIVE_SUMMARY.md - High-level overview for leadership
2. ACTION_PLAN.md - Prioritized implementation plan for developers

Focus on:
- Overall codebase health assessment
- Top 5 critical issues requiring immediate attention  
- Estimated effort/timeline for fixes
- Business risk assessment
- Long-term recommendations

Keep both documents concise and business-focused."""
        
        # For now, just create the synthesis files from the chunk results
        # The final synthesis with Claude can be added later
        with open(exec_summary, 'w') as f:
            f.write(f"# Executive Summary\n\nGenerated: {datetime.now()}\n\n")
            f.write("## Synthesis Results\n\n")
            f.write(combined_content)
        
        with open(action_plan, 'w') as f:
            f.write(f"# Action Plan\n\nGenerated: {datetime.now()}\n\n")
            f.write("## Prioritized Recommendations\n\n")
            f.write("Review the detailed synthesis below for actionable recommendations.\n\n")
            f.write(combined_content)
        
        # Update HOTSPOTS.md and METRICS_SUMMARY.md
        self._update_system_files()
    
    def _update_system_files(self) -> None:
        """Update HOTSPOTS.md and METRICS_SUMMARY.md with synthesis results"""
        # This is a placeholder - could be enhanced to automatically update system files
        # based on synthesis results
        hotspots_file = self.vibe_dir / "reviews" / "system" / "HOTSPOTS.md"
        metrics_file = self.vibe_dir / "reviews" / "system" / "METRICS_SUMMARY.md"
        
        # Add timestamp to show when synthesis was last run
        timestamp = f"\n\n*Last synthesis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        if hotspots_file.exists():
            with open(hotspots_file, 'a') as f:
                f.write(timestamp)
        
        if metrics_file.exists():
            with open(metrics_file, 'a') as f:
                f.write(timestamp)

def main():
    parser = argparse.ArgumentParser(description='Vibe-Check: AI code review', prog='vibe-check')
    sub = parser.add_subparsers(dest='cmd', help='Commands')
    
    p = sub.add_parser('populate', help='Scan and populate file list')
    p.add_argument('--no-git', action='store_true', help='Ignore git')
    
    sub.add_parser('review', help='Review single file')
    
    r = sub.add_parser('review-all', help='Review all files')
    r.add_argument('--delay', type=int, default=5, help='Delay between reviews')
    
    sub.add_parser('status', help='Show progress')
    
    # Synthesize command with options
    s = sub.add_parser('synthesize', help='Synthesize reviews into actionable insights')
    s.add_argument('--severity', choices=['high', 'medium', 'low'], default='medium',
                   help='Issue severity level (default: medium)')
    s.add_argument('--category', choices=['security', 'performance', 'maintainability', 
                   'consistency', 'best_practices', 'code_smell', 'all'], default='all',
                   help='Issue category filter (default: all)')
    s.add_argument('--score-threshold', type=int, metavar='N',
                   help='Only include files with scores < N')
    s.add_argument('--critical-only', action='store_true',
                   help='Only include critical files (scores <= 2)')
    s.add_argument('--no-interactive', action='store_true',
                   help='Skip interactive mode selection')
    
    args = parser.parse_args()
    if not args.cmd: parser.print_help(); return 1
    
    vc = VibeCheck()
    
    if args.cmd == 'populate': return vc.populate(args.no_git)
    elif args.cmd == 'review': return vc.review()
    elif args.cmd == 'review-all': return vc.review_all(args.delay)
    elif args.cmd == 'status': return vc.status()
    elif args.cmd == 'synthesize': 
        return vc.synthesize(
            severity=args.severity,
            category=args.category,
            score_threshold=args.score_threshold,
            critical_only=args.critical_only,
            interactive=not args.no_interactive
        )
    
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
- [ ] `vibe-check/reviews/_SCRATCHSHEET.md` exists with frontmatter
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

# Synthesize reviews into actionable insights
./vibe-check/scripts/vibe-check synthesize [OPTIONS]

# Synthesis options:
#   --severity {high,medium,low}     Issue severity level (default: medium)
#   --category {security,performance,maintainability,consistency,best_practices,code_smell,all}
#                                   Issue category filter (default: all)  
#   --score-threshold N             Only include files with scores < N
#   --critical-only                 Only include critical files (scores <= 2)
#   --no-interactive               Skip interactive mode selection

# Examples:
./vibe-check/scripts/vibe-check synthesize --severity high --critical-only
./vibe-check/scripts/vibe-check synthesize --category security --severity medium
./vibe-check/scripts/vibe-check synthesize --score-threshold 3
```

### 6. Synthesis Functionality

The `synthesize` command processes completed individual file reviews and creates actionable insights by analyzing patterns across multiple files. This is essential for large codebases where hundreds or thousands of individual issues need to be prioritized and organized.

#### 6.1 How Synthesis Works

1. **Issue Collection**: Scans all completed review files and extracts individual issues
2. **Filtering**: Applies severity, category, and score-based filters to focus on relevant issues
3. **Chunking**: Groups issues into manageable chunks (10-30 issues each) for AI processing
4. **Analysis**: Uses Claude to identify cross-cutting patterns, root causes, and priorities
5. **Synthesis**: Combines chunk analyses into executive summaries and action plans

#### 6.2 Output Structure

Synthesis creates organized reports in `vibe-check/synthesis/`:

```
vibe-check/synthesis/
├── priority-high/           # HIGH severity issues only
│   ├── EXECUTIVE_SUMMARY.md # Leadership overview
│   └── ACTION_PLAN.md       # Prioritized implementation steps
├── priority-medium/         # HIGH + MEDIUM issues
│   ├── EXECUTIVE_SUMMARY.md
│   └── ACTION_PLAN.md
└── priority-low/            # All issues (comprehensive analysis)
    ├── EXECUTIVE_SUMMARY.md
    └── ACTION_PLAN.md
```

#### 6.3 Filtering Strategies

**By Severity:**
- `high`: Only critical issues requiring immediate attention
- `medium`: Important issues worth addressing soon (default)
- `low`: Complete picture including minor improvements

**By Category:**
- `security`: Focus on vulnerabilities and security concerns
- `performance`: Focus on efficiency and scalability issues
- `all`: Cross-cutting analysis across all issue types (default)

**By File Quality:**
- `--score-threshold 3`: Only files with quality scores below 3
- `--critical-only`: Only files with scores 1-2 (critical quality issues)

#### 6.4 Interactive Mode

For large codebases (>100 issues), synthesis automatically offers interactive selection:

```
Found 1,247 total issues:
  - 23 HIGH severity issues
  - 156 MEDIUM severity issues
  - 1,068 LOW severity issues

Select synthesis mode:
1. Quick (HIGH only) - ~23 issues
2. Standard (HIGH + MEDIUM) - ~179 issues
3. Comprehensive (All) - ~1,247 issues
4. Continue with current filter - 45 issues

Choice: 1
```

#### 6.5 Best Practices

1. **Start Small**: Begin with `--severity high --critical-only` for immediate priorities
2. **Category Focus**: Use `--category security` for security audits
3. **Iterative Approach**: Run synthesis after every 10-20 completed reviews
4. **Team Coordination**: Share executive summaries with leadership, action plans with developers

### 7. Important Notes

- All files should be created with UTF-8 encoding
- Use Unix-style line endings (LF)
- The unified script is only 326 lines but provides all functionality
- Source code files are treated as read-only during reviews
- The vibe-check folder can be added to `.gitignore` if you don't want to commit reviews
- Alternatively, commit the vibe-check folder to track review history over time
- The script automatically handles interrupted reviews by resuming "in_progress" files

This setup creates a complete code review system with a single, compact Python script that handles all operations efficiently.