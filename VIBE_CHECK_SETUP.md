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
- Each source code file will have a corresponding `.xml` review file
- Module-level README files synthesize findings across all files in that module
- Directory structure mirrors the repository structure (excluding the vibe-check folder itself)

## Navigation Tips
- Review files use the same name as source files but with `.xml` extension
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

1. A complete review XML file at `vibe-check/reviews/modules/.../[filename].xml`

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

### Step 4: Create Review XML

Use this exact template:

\`\`\`xml
<review>
  <metadata>
    <file>[FILE_PATH]</file>
    <language>[DETECTED_LANGUAGE]</language>
    <loc>[LINE_COUNT]</loc>
    <reviewer>AI-[IDENTIFIER]</reviewer>
    <date>[YYYY-MM-DD]</date>
    <status>complete</status>
  </metadata>
  
  <scores>
    <metric name="security" score="[1-5]" open_issues="[COUNT]"/>
    <metric name="performance" score="[1-5]" open_issues="[COUNT]"/>
    <metric name="maintainability" score="[1-5]" open_issues="[COUNT]"/>
    <metric name="consistency" score="[1-5]" open_issues="[COUNT]"/>
    <metric name="best_practices" score="[1-5]" open_issues="[COUNT]"/>
    <metric name="code_smell" score="[1-5]" open_issues="[COUNT]"/>
  </scores>
  
  <issues>
    <issue category="security" severity="HIGH">
      <title>Hardcoded JWT Secret</title>
      <location>Line 39</location>
      <description>JWT tokens are signed with a hardcoded secret 'supersecret123', making all tokens vulnerable to forgery</description>
      <recommendation>Use environment variables or secure configuration management for JWT secrets</recommendation>
    </issue>
    
    <issue category="performance" severity="MEDIUM">
      <title>N+1 Query Problem</title>
      <location>Lines 46-52</location>
      <description>getAllUsers method executes one query per user to fetch posts, causing N+1 queries</description>
      <recommendation>Use JOIN operations or batch queries to fetch all posts in a single query</recommendation>
    </issue>
  </issues>
  
  <summary>Brief description of file purpose and overall health assessment</summary>
  
  <positive_observations>
    <observation>Uses bcrypt for password hashing with appropriate salt rounds</observation>
    <observation>Clean class-based architecture with dependency injection</observation>
    <observation>Consistent naming conventions following camelCase</observation>
  </positive_observations>
  
  <context>
    <tests>No test files found</tests>
    <documentation>No documentation found</documentation>
    <configuration>No configuration files found</configuration>
  </context>
  
  <checklist>
    <item completed="false">Lints clean</item>
    <item completed="false">Tests present</item>
    <item completed="false">Documentation updated</item>
    <item completed="false">Security review complete</item>
    <item completed="false">Performance acceptable</item>
  </checklist>
</review>
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

Create this streamlined executable script that handles all vibe-check operations:

```python
#!/usr/bin/env python3
"""vibe-check - Streamlined code review system CLI"""

import argparse, json, subprocess, sys, os, time, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# ANSI colors
R, G, Y, B, N = '\033[0;31m', '\033[0;32m', '\033[1;33m', '\033[0;34m', '\033[0m'
def status(color, msg): print(f"{color}{msg}{N}")

# Core file extensions  
EXTS = {'js','jsx','ts','tsx','py','java','go','rs','rb','php','c','cpp','h','hpp','cs','swift','kt','sh','sql'}

class VibeCheck:
    def __init__(self):
        self.vibe_dir = Path("vibe-check")
        self.master_file = self.vibe_dir / "reviews" / "_MASTER.json"
        self.inst_file = self.vibe_dir / "prompts" / "REVIEWER_INSTRUCTIONS.md"
        self.log_dir = self.vibe_dir / "logs"
    
    def load_master(self): 
        with open(self.master_file, 'r') as f: return json.load(f)
    
    def save_master(self, data):
        with open(self.master_file, 'w') as f: json.dump(data, f, indent=2)
    
    def populate(self, no_git=False):
        """Scan repository and populate file list"""
        if not self.vibe_dir.exists():
            status(R, "Error: vibe-check directory not found!")
            return 1
        
        # Get files
        files = []
        if not no_git:
            try:
                result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, check=True)
                files = [Path(line) for line in result.stdout.strip().split('\n') if line and not line.startswith('vibe-check/')]
                status(G, "Git repository detected")
            except:
                no_git = True
        
        if no_git:
            exclude = {'.git','node_modules','venv','__pycache__','build','dist','vibe-check'}
            files = [p.relative_to('.') for p in Path('.').rglob('*') 
                    if p.is_file() and not any(part.startswith('.') or part in exclude for part in p.parts)]
            status(Y, "Using find (non-git)")
        
        # Build master data
        data = {
            "metadata": {"version": "1.0", "generated": datetime.utcnow().isoformat() + "Z", "total_files": 0, "total_loc": 0},
            "files": {}
        }
        
        file_count = total_loc = 0
        for f in files:
            if f.suffix[1:] not in EXTS: continue
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    loc = sum(1 for _ in file)
            except: loc = 0
            
            file_count += 1
            total_loc += loc
            data["files"][str(f)] = {"language": f.suffix[1:].title(), "loc": loc, "status": "not_reviewed"}
        
        data["metadata"]["total_files"] = file_count
        data["metadata"]["total_loc"] = total_loc
        self.save_master(data)
        status(G, f"✓ Populated {file_count} files, {total_loc} LOC")
        return 0
    
    def review(self):
        """Review a single file"""
        if not self.vibe_dir.exists() or not self.master_file.exists():
            status(R, "Missing files! Run populate first.")
            return 1
        
        # Check Claude CLI
        try: subprocess.run(["claude", "--version"], capture_output=True, check=True)
        except: status(R, "Error: Claude CLI not found!"); return 1
        
        # Find next file
        data = self.load_master()
        file_to_review = None
        for fp, info in data['files'].items():
            if info['status'] in ['in_progress', 'not_reviewed']:
                file_to_review = fp
                break
        
        if not file_to_review:
            status(G, "All files reviewed!")
            return 0
        
        # Setup and run review
        self.log_dir.mkdir(exist_ok=True)
        log_file = self.log_dir / f"review_{datetime.now():%Y%m%d_%H%M%S}.log"
        
        data['files'][file_to_review]['status'] = 'in_progress'
        self.save_master(data)
        status(B, f"Reviewing: {file_to_review}")
        
        # Create prompt
        with open(self.inst_file, 'r') as f: instructions = f.read()
        scratchsheet_file = self.vibe_dir / "reviews" / "_SCRATCHSHEET.md"
        scratchsheet_content = ""
        if scratchsheet_file.exists():
            with open(scratchsheet_file, 'r') as f:
                scratchsheet_content = f"\\n\\nGlobal Scratchsheet:\\n{f.read()}"
        
        prompt = f"Review this file:\\nFILE_PATH: {file_to_review}{scratchsheet_content}\\n\\n{instructions}"
        
        # Run Claude
        cmd = ['claude', '--print', prompt, '--output-format', 'stream-json', '--permission-mode', 'acceptEdits', '--verbose']
        
        with open(log_file, 'w') as log:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in iter(proc.stdout.readline, ''):
                log.write(line)
                try:
                    d = json.loads(line.strip())
                    if d.get('type') == 'assistant':
                        for item in d.get('message', {}).get('content', []):
                            if item.get('type') == 'text' and (text := item.get('text', '').strip()):
                                print(f"{text}\\n---")
                except: pass
            proc.wait()
        
        if proc.returncode == 0:
            data = self.load_master()
            data['files'][file_to_review]['status'] = 'completed'
            self.save_master(data)
            status(G, "✓ Review completed!")
            return 0
        else:
            status(R, f"✗ Review failed! Check: {log_file}")
            return 1
    
    def review_all(self, delay=5):
        """Review all remaining files"""
        if not self.vibe_dir.exists(): return 1
        
        reviewed = 0
        while True:
            remaining = sum(1 for info in self.load_master()['files'].values() 
                          if info['status'] in ['not_reviewed', 'in_progress'])
            if remaining == 0: break
            
            status(Y, f"Remaining: {remaining}, Starting #{reviewed + 1}")
            if self.review() == 0:
                reviewed += 1
                if remaining > 1: time.sleep(delay)
            else:
                status(R, "Failed! Stopping.")
                return 1
        
        status(G, f"✓ Reviewed {reviewed} files")
        return 0
    
    def status(self):
        """Show review status"""
        if not self.vibe_dir.exists() or not self.master_file.exists(): return 1
        
        data = self.load_master()
        files = data['files']
        total = len(files)
        
        counts = {}
        for info in files.values():
            s = info['status']
            counts[s] = counts.get(s, 0) + 1
        
        status(B, "=== Vibe-Check Status ===")
        print(f"Total files: {Y}{total}{N}, LOC: {Y}{data['metadata']['total_loc']}{N}")
        
        for st, count in sorted(counts.items()):
            color = G if st == 'completed' else Y if st == 'in_progress' else R
            print(f"{st:15} {color}{count:4d}{N} ({count/total*100:5.1f}%)")
        
        if total > 0:
            done = counts.get('completed', 0)
            pct = done / total
            bar = '█' * int(20 * pct) + '░' * int(20 * (1-pct))
            print(f"Progress: [{G}{bar}{N}] {pct*100:.1f}%")
        return 0
    
    def synthesize(self, severity='medium', category='all'):
        """Synthesize reviews into actionable insights"""
        if not self.vibe_dir.exists() or not self.master_file.exists():
            status(R, "No reviews found!")
            return 1
        
        # Check Claude CLI
        try: subprocess.run(["claude", "--version"], capture_output=True, check=True)
        except: status(R, "Error: Claude CLI not found!"); return 1
        
        # Create synthesis directory
        synthesis_dir = self.vibe_dir / "synthesis"
        synthesis_dir.mkdir(exist_ok=True)
        
        # Collect issues from XML review files
        issues = self._collect_issues()
        if not issues:
            status(Y, "No issues found")
            return 0
        
        # Filter by severity
        severity_map = {'high': ['HIGH'], 'medium': ['HIGH', 'MEDIUM'], 'low': ['HIGH', 'MEDIUM', 'LOW']}
        if severity in severity_map:
            issues = [i for i in issues if i['severity'] in severity_map[severity]]
        
        # Filter by category
        if category != 'all':
            issues = [i for i in issues if i['category'] == category.lower()]
        
        if not issues:
            status(Y, f"No {severity} {category} issues found")
            return 0
        
        status(B, f"Synthesizing {len(issues)} issues across {len(set(i['file'] for i in issues))} files...")
        
        # Create synthesis prompt
        issues_text = ""
        for issue in issues:
            issues_text += f"\\n**{issue['severity']} {issue['category']}**: {issue['title']} ({issue['file']}:{issue['location']})"
            issues_text += f"\\n  Description: {issue['description']}"
            issues_text += f"\\n  Recommendation: {issue['recommendation']}\\n"
        
        prompt = f"""Analyze these {len(issues)} code review issues and create an actionable synthesis report.

ISSUES:
{issues_text}

Create a concise report with:
1. Executive Summary (2-3 sentences)
2. Top 5 Priority Issues (with business impact)
3. Quick Wins (high-impact, low-effort fixes)
4. Root Causes (systemic issues)
5. Action Plan (prioritized steps)

Focus on business impact and actionability."""
        
        # Run synthesis
        self.log_dir.mkdir(exist_ok=True)
        log_file = self.log_dir / f"synthesis_{datetime.now():%Y%m%d_%H%M%S}.log"
        cmd = ['claude', '--print', prompt, '--output-format', 'stream-json', '--permission-mode', 'acceptEdits', '--verbose']
        
        output_lines = []
        with open(log_file, 'w') as log:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
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
            # Save synthesis result
            synthesis_file = synthesis_dir / f"synthesis_{severity}_{datetime.now():%Y%m%d_%H%M%S}.md"
            with open(synthesis_file, 'w') as f:
                f.write(f"# Synthesis Report ({severity.title()} Issues)\\n\\n")
                f.write(f"Generated: {datetime.now()}\\n\\n")
                f.write('\\n'.join(output_lines))
            
            status(G, f"✓ Synthesis complete: {synthesis_file}")
            return 0
        else:
            status(R, "✗ Synthesis failed")
            return 1
    
    def _collect_issues(self):
        """Collect all issues from XML review files"""
        issues = []
        reviews_dir = self.vibe_dir / "reviews" / "modules"
        
        for xml_file in reviews_dir.rglob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Get file path from metadata
                file_elem = root.find('.//metadata/file')
                file_path = file_elem.text if file_elem is not None else str(xml_file.stem)
                
                # Extract scores
                scores = {}
                for metric in root.findall('.//scores/metric'):
                    name, score = metric.get('name'), metric.get('score')
                    if name and score: scores[name] = int(score)
                
                # Extract issues
                for issue_elem in root.findall('.//issues/issue'):
                    title_elem = issue_elem.find('title')
                    location_elem = issue_elem.find('location')
                    description_elem = issue_elem.find('description')
                    recommendation_elem = issue_elem.find('recommendation')
                    
                    if title_elem is not None:
                        issues.append({
                            'file': file_path,
                            'category': issue_elem.get('category', ''),
                            'severity': issue_elem.get('severity', ''),
                            'title': title_elem.text or '',
                            'location': location_elem.text if location_elem is not None else '',
                            'description': description_elem.text if description_elem is not None else '',
                            'recommendation': recommendation_elem.text if recommendation_elem is not None else '',
                            'file_scores': scores
                        })
            except Exception as e:
                status(Y, f"Warning: Could not parse {xml_file}: {e}")
        
        return issues

def main():
    parser = argparse.ArgumentParser(description='Vibe-Check: Streamlined AI code review')
    sub = parser.add_subparsers(dest='cmd', help='Commands')
    
    p = sub.add_parser('populate', help='Scan and populate file list')
    p.add_argument('--no-git', action='store_true', help='Ignore git')
    
    sub.add_parser('review', help='Review single file')
    
    r = sub.add_parser('review-all', help='Review all files')
    r.add_argument('--delay', type=int, default=5, help='Delay between reviews')
    
    sub.add_parser('status', help='Show progress')
    
    s = sub.add_parser('synthesize', help='Synthesize reviews')
    s.add_argument('--severity', choices=['high', 'medium', 'low'], default='medium', help='Issue severity')
    s.add_argument('--category', choices=['security', 'performance', 'maintainability', 'consistency', 'best_practices', 'code_smell', 'all'], default='all', help='Issue category')
    
    args = parser.parse_args()
    if not args.cmd: parser.print_help(); return 1
    
    vc = VibeCheck()
    
    if args.cmd == 'populate': return vc.populate(args.no_git)
    elif args.cmd == 'review': return vc.review()
    elif args.cmd == 'review-all': return vc.review_all(args.delay)
    elif args.cmd == 'status': return vc.status()
    elif args.cmd == 'synthesize': return vc.synthesize(args.severity, args.category)
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
```

### 3. Make Script Executable

```bash
chmod +x vibe-check/scripts/vibe-check
```

### 4. Verify Setup

Check that all files were created properly:

```bash
ls -la vibe-check/
ls -la vibe-check/reviews/
ls -la vibe-check/scripts/
```

You should see:
- `vibe-check/reviews/_MASTER.json` 
- `vibe-check/reviews/_SCRATCHSHEET.md`
- `vibe-check/prompts/REVIEWER_INSTRUCTIONS.md`
- `vibe-check/scripts/vibe-check` (executable)

### 5. Usage

#### 5.1 Basic Workflow

```bash
# 1. Scan repository and populate file list
./vibe-check/scripts/vibe-check populate

# 2. Review a single file (automatically picks next unreviewed file)
./vibe-check/scripts/vibe-check review

# 3. Review all files in sequence
./vibe-check/scripts/vibe-check review-all

# 4. Check progress
./vibe-check/scripts/vibe-check status

# 5. Generate synthesis report
./vibe-check/scripts/vibe-check synthesize
```

#### 5.2 Advanced Options

```bash
# Populate without git (use filesystem scan)
./vibe-check/scripts/vibe-check populate --no-git

# Review all with custom delay between reviews
./vibe-check/scripts/vibe-check review-all --delay 10

# Synthesize by severity level
./vibe-check/scripts/vibe-check synthesize --severity high
./vibe-check/scripts/vibe-check synthesize --severity medium
./vibe-check/scripts/vibe-check synthesize --severity low

# Synthesize by category
./vibe-check/scripts/vibe-check synthesize --category security
./vibe-check/scripts/vibe-check synthesize --category performance
```

### 6. Output Structure

After running reviews, you'll find:

```
vibe-check/
├── reviews/
│   ├── _MASTER.json          # Master tracking file
│   ├── _SCRATCHSHEET.md      # Global patterns
│   └── modules/              # XML review files mirror your repo structure
│       ├── src/
│       │   ├── main.js.xml   # Individual file reviews in XML format
│       │   └── utils.js.xml
│       └── tests/
├── synthesis/                # Generated synthesis reports
│   └── synthesis_medium_20240615_143022.md
└── logs/                     # Detailed logs for debugging
    ├── review_20240615_142001.log
    └── synthesis_20240615_143022.log
```

### 7. Important Notes

- **Streamlined Design**: Script reduced from 751 to 351 lines (53% reduction)
- **No Dependencies**: Uses only Python standard library (no pip installs required)
- **XML Format**: Individual reviews use structured XML for reliable parsing
- **Git Integration**: Automatically detects git repositories and respects .gitignore patterns
- **Synthesis**: Single-pass analysis instead of complex chunking
- **Logging**: All operations logged for debugging
- **Resumable**: Interrupted reviews can be resumed automatically

This setup creates a complete, streamlined code review system optimized for simplicity and reliability.
