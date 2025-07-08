# SYNTHESIS INSTRUCTIONS - Vibe-Check Issue Analysis

## What is Synthesis?

Synthesis is the "reduce" step in the vibe-check map-reduce workflow. After individual files have been reviewed (the "map" step), synthesis analyzes all collected issues to identify patterns, prioritize problems, and create actionable recommendations for the development team.

## Your Task

Analyze the {issue_count} code review issues from {file_count} files and create an actionable synthesis report.

**Filter Context:**
- Severity: {severity}
- Category: {category}

## Issues to Analyze

{issues_text}

## Required Output Format

Create a concise report with:

1. **Executive Summary** (2-3 sentences)
   - Overall code health assessment
   - Most critical areas requiring attention

2. **Top 5 Priority Issues** (with business impact)
   - Focus on issues that affect security, performance, or maintainability
   - Include business rationale for prioritization

3. **Quick Wins** (high-impact, low-effort fixes)
   - Issues that can be resolved quickly but provide significant value
   - Suitable for immediate implementation

4. **Root Causes** (systemic issues)
   - Patterns that indicate deeper architectural or process problems
   - Issues that suggest training or tooling gaps

5. **Action Plan** (prioritized steps)
   - Concrete steps for addressing identified issues
   - Timeline and resource considerations

## Guidelines

- **Focus on business impact and actionability**
- Prioritize issues by risk and effort required
- Group similar issues to identify patterns
- Provide specific, implementable recommendations
- Consider both technical debt and immediate fixes
- Balance thoroughness with conciseness

## Output Style

- Use clear, professional language suitable for technical and non-technical stakeholders
- Include specific file names and line numbers when relevant
- Quantify impact where possible (performance improvements, security risk levels)
- Organize recommendations by priority and effort required