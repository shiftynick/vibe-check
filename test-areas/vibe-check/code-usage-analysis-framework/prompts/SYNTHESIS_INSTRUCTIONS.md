# SYNTHESIS INSTRUCTIONS - code-usage-analysis

## What is Synthesis?

Synthesis is the "reduce" step in the code-usage-analysis workflow. After individual items have been processed (the "map" step), synthesis analyzes all collected results to identify patterns, prioritize findings, and create actionable recommendations.

## Your Task

Analyze the {{issue_count}} findings from {{file_count}} items and create a comprehensive synthesis report.

**Filter Context:**
- Severity: {{severity}}
- Category: {{category}}

## Findings to Analyze

{{issues_data}}

## Required Output Format


### Architecture Overview

High-level system architecture based on usage patterns

Template: ## Architecture Overview

Provide a clear picture of the system architecture based on file relationships and usage patterns.


### Dependency Graph

Key dependency relationships and chains

Template: ## Dependency Graph

Map out the most important dependency relationships, highlighting critical paths and potential issues.


### Core Components

Most used and critical files in the system

Template: ## Core Components

Identify the files that are most central to the system's operation, ordered by importance and usage.


### Integration Boundaries

Key interfaces and system boundaries

Template: ## Integration Boundaries

Describe the main integration points and boundaries between different parts of the system.


### Refactoring Opportunities

Opportunities to improve system structure

Template: ## Refactoring Opportunities

Based on usage patterns and coupling, identify opportunities to improve the system architecture.


### Orphaned Code

Potentially unused or disconnected code

Template: ## Orphaned Code

List files that appear to be unused or disconnected from the main system.



## Guidelines

- Focus on actionable insights and patterns
- Prioritize findings by impact and effort required
- Group similar findings to identify trends
- Provide specific, implementable recommendations
- Balance thoroughness with conciseness

## Output Style

- Use clear, professional language
- Include specific item references when relevant
- Quantify impact where possible
- Organize recommendations by priority and effort required