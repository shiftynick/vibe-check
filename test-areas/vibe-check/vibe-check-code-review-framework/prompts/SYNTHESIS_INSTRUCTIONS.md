# SYNTHESIS INSTRUCTIONS - vibe-check-code-review

## What is Synthesis?

Synthesis is the "reduce" step in the vibe-check-code-review workflow. After individual items have been processed (the "map" step), synthesis analyzes all collected results to identify patterns, prioritize findings, and create actionable recommendations.

## Your Task

Analyze the {{issue_count}} findings from {{file_count}} items and create a comprehensive synthesis report.

**Filter Context:**
- Severity: {{severity}}
- Category: {{category}}

## Findings to Analyze

{{issues_data}}

## Required Output Format


### Executive Summary

Overall code health assessment and most critical areas

Template: ## Executive Summary

Provide 2-3 sentences covering overall code health and most critical areas requiring attention.


### Priority Issues

Top 5 issues with business impact

Template: ## Top 5 Priority Issues

Focus on issues affecting security, performance, or maintainability with business rationale for prioritization.


### Quick Wins

High-impact, low-effort fixes

Template: ## Quick Wins

Issues that can be resolved quickly but provide significant value, suitable for immediate implementation.


### Root Causes

Systemic issues and patterns

Template: ## Root Causes

Patterns indicating deeper architectural or process problems, training or tooling gaps.


### Action Plan

Prioritized implementation steps

Template: ## Action Plan

Concrete steps for addressing identified issues with timeline and resource considerations.



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