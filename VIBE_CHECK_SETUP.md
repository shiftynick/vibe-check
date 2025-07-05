# VIBE_CHECK_SETUP.md

## Setup Instructions for Vibe-Check Code Review System

You are tasked with setting up the Vibe-Check code review system within an existing repository. This will create a `vibe-check` folder in the current directory that contains all review artifacts, while treating the rest of the repository as the source code to be reviewed.

### 1. Create Directory Structure

Create the following directory hierarchy within a new `vibe-check` folder:

```
vibe-check/
├── prompts/
└── reviews/
    ├── modules/
    └── system/
```

### 2. Create Initial Files

#### 2.1 Create `vibe-check/reviews/_MASTER.md`

Create this file with the following content:

```markdown
# Vibe-Check Master Review Ledger

This is the single source of truth for all code review progress.

## Review Status Legend
- ❌ = Not reviewed
- 🔒 = In progress
- ✅ = Completed
- 🔄 = Needs update (source changed)

## Review Progress

| File Path | Lang | LOC | Reviewed? | Review Date | Reviewer | Security | Perf | Maint | Consistency | Best Pract | Code Smell | Open Issues | Dep Count |
|-----------|------|-----|-----------|-------------|----------|----------|------|-------|-------------|------------|------------|-------------|-----------|

*Note: Scores are 1-5 (5 = excellent). This table will be populated as files are reviewed.*
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
2. Updated row in `vibe-check/reviews/_MASTER.md` with scores and metadata
3. Updated dependencies in `vibe-check/reviews/_DEPENDENCIES.yml`

## Precise Algorithm to Follow

### Step 1: Lock the File
- Open `vibe-check/reviews/_MASTER.md`
- Find the row for FILE_PATH
- Change the "Reviewed?" column from ❌ to 🔒 (in-progress)
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
- Reopen `vibe-check/reviews/_MASTER.md`
- Find the FILE_PATH row
- Update columns:
  - Reviewed? = ✅
  - Review Date = TODAY
  - Reviewer = Your AI identifier
  - All metric scores (1-5)
  - Open Issues = total count
  - Dep Count = number of dependencies
- Remove the 🔒 lock
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
- File not found: Update _MASTER.md to mark as "NOT_FOUND" and stop
- Cannot parse: Score all metrics as 1 with explanation in summary
- Lock conflict: Wait and retry once, then report conflict
```

### 3. Verification Checklist

After creating all files, verify:

- [ ] `vibe-check/` directory exists in repository root
- [ ] `vibe-check/prompts/` directory exists
- [ ] `vibe-check/reviews/` directory exists
- [ ] `vibe-check/reviews/modules/` directory exists  
- [ ] `vibe-check/reviews/system/` directory exists
- [ ] `vibe-check/prompts/REVIEWER_INSTRUCTIONS.md` exists with complete algorithm
- [ ] `vibe-check/reviews/_MASTER.md` exists and contains the table structure
- [ ] `vibe-check/reviews/_DEPENDENCIES.yml` exists with YAML format
- [ ] `vibe-check/reviews/system/HOTSPOTS.md` exists with section headers
- [ ] `vibe-check/reviews/system/METRICS_SUMMARY.md` exists with metric table
- [ ] `vibe-check/reviews/modules/README.md` exists with navigation guide

### 4. Next Steps

Once this structure is in place:

1. Run an inventory script to populate `vibe-check/reviews/_MASTER.md` with all source files in the repository (excluding the vibe-check folder itself)
2. Begin the review process following the algorithm in the REVIEWER_INSTRUCTIONS.md
3. Create review files in `vibe-check/reviews/modules/` mirroring the repository structure
4. The vibe-check system will treat all files outside the vibe-check folder as source code to review

### 5. Important Notes

- All files should be created with UTF-8 encoding
- Use Unix-style line endings (LF)
- Maintain consistent indentation (2 spaces for YAML, your preference for Markdown)
- Do not modify these template files except to add actual review data
- Source code files should be treated as read-only during reviews
- The vibe-check folder should be added to `.gitignore` if you don't want to commit reviews
- Alternatively, commit the vibe-check folder to track review history over time

This setup creates the foundational structure for the Vibe-Check review system overlaid on your existing repository. All subsequent reviews will populate these files according to the deterministic algorithm defined in the design document.