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

```markdown
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
```

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