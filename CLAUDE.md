# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vibe-check is an AI-powered code review system designed to systematically analyze source code quality across multiple dimensions. The system generates structured, version-controlled reviews in markdown format.

## Project Structure

The project follows this directory structure:
- `/code/` - Source code to be reviewed (read-only)
- `/reviews/` - All review artifacts
  - `_MASTER.md` - Central progress tracking ledger
  - `_DEPENDENCIES.yml` - Repository-wide dependency graph
  - `/modules/` - Mirrors /code/ structure with review files
  - `/system/` - System-wide reports (HOTSPOTS.md, METRICS_SUMMARY.md)

## Review Process

When implementing reviews, follow the deterministic workflow from initial-design.md:
1. Check _MASTER.md for file status before reviewing
2. Generate reviews in markdown format with YAML frontmatter
3. Score each file on 6 metrics (1-5 scale): Security, Performance, Maintainability, Consistency, Best Practices, Code Smell
4. Track dependencies (outbound_calls and inbound_refs)
5. Update _MASTER.md after each review

## Key Commands

Since this is a design-phase project, no build/test commands exist yet. When implementing:
- Consider creating a CLI tool for the review process
- Implement validation for review file formats
- Create scripts to generate _MASTER.md and dependency graphs

## Important Design Principles

1. **Deterministic Reviews**: Each file should be reviewable independently
2. **Version Control**: All reviews are text files suitable for Git
3. **Structured Format**: Use consistent markdown/YAML formats as specified in initial-design.md
4. **Dependency Tracking**: Maintain bidirectional dependency information
5. **Progress Tracking**: Keep _MASTER.md updated as the source of truth

## File Format Standards

### Review Files
- Must include YAML frontmatter with: file_path, review_date, reviewer, version_hash, scores, dependencies
- Use markdown sections for Summary, Security Analysis, Performance Analysis, etc.
- Include specific code references with line numbers

### _MASTER.md Format
- Table format with columns: File, Status, Version Hash, Last Reviewed, Reviewer, Overall Score
- Status values: pending, in-progress, completed, needs-update

### _DEPENDENCIES.yml Format
- Dictionary mapping file paths to their outbound_calls and inbound_refs arrays