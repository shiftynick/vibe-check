# VIBE_CHECK_CODE_REVIEW_SETUP.md

## Setup Instructions for Code review system analyzing source code quality across six key dimensions

You are tasked with setting up the vibe-check-code-review system within an existing repository. This will create a `vibe-check-code-review-framework` folder in the current directory that contains all processing artifacts.

### 1. Create Directory Structure

Create the following directory hierarchy within a new `vibe-check-code-review-framework` folder:

```
vibe-check-code-review-framework/
├── data/
├── results/
├── synthesis/
├── logs/
└── prompts/
```

### 2. Create Configuration Files

#### 2.1 Create `vibe-check-code-review-framework/config.json`

Create this file with the following content:

```json
{
  "project": {
    "name": "vibe-check-code-review",
    "version": "1.0",
    "description": "Code review system analyzing source code quality across six key dimensions"
  },
  "populate": {
    "collection_strategy": "git",
    "item_filters": {
      "include_patterns": [
        "*.js",
        "*.jsx",
        "*.ts",
        "*.tsx",
        "*.vue",
        "*.svelte",
        "*.py",
        "*.java",
        "*.go",
        "*.rs",
        "*.rb",
        "*.php",
        "*.c",
        "*.cpp",
        "*.h",
        "*.hpp",
        "*.cs",
        "*.swift",
        "*.kt",
        "*.sh",
        "*.sql"
      ],
      "exclude_patterns": [
        "*.min.js",
        "*.bundle.js",
        "*.test.js",
        "*.spec.js"
      ],
      "exclude_directories": [
        ".git",
        "node_modules",
        "venv",
        "__pycache__",
        "build",
        "dist",
        "coverage"
      ],
      "max_size_bytes": 1048576
    },
    "metadata_extraction": {
      "required_fields": [
        "path",
        "language",
        "loc",
        "status"
      ],
      "optional_fields": [
        "last_modified",
        "author",
        "complexity"
      ],
      "extraction_rules": {
        "language": "file_extension.title()",
        "loc": "count_lines(file_content)",
        "status": "'not_reviewed'"
      }
    },
    "output_format": "json"
  },
  "map": {
    "processing_template": "You are the File Reviewer AI. Your task is to analyze EXACTLY ONE source file and produce a comprehensive review following a deterministic algorithm.\n\n## Inputs\n- FILE_PATH: {item_path}\n- REVIEW_OUTPUT_FILE: {output_file}\n- Global context from scratchsheet: {global_context}\n\n## Assessment Process\n{assessment_instructions}\n\n## Output Requirements\n{output_requirements}",
    "assessment_dimensions": [
      {
        "name": "security",
        "description": "Vulnerabilities, input validation, authentication/authorization issues",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Exemplary security practices, no vulnerabilities found",
            "4": "Minor security concerns that don't pose immediate risk",
            "3": "At least one medium severity security issue present",
            "2": "High severity security vulnerabilities present",
            "1": "Critical security flaws requiring immediate attention"
          }
        },
        "specific_instructions": "Check for input validation, authentication/authorization issues, potential injection vulnerabilities, cryptographic usage, and exposed secrets"
      },
      {
        "name": "performance",
        "description": "Efficiency, resource usage, scalability concerns",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Excellent performance characteristics",
            "4": "Minor performance improvements possible",
            "3": "Noticeable performance issues present",
            "2": "Significant performance problems",
            "1": "Critical performance issues affecting usability"
          }
        },
        "specific_instructions": "Identify inefficient algorithms, N+1 query patterns, memory leaks, caching opportunities, and blocking operations"
      },
      {
        "name": "maintainability",
        "description": "Code clarity, modularity, documentation quality",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Highly maintainable with excellent documentation",
            "4": "Good maintainability with minor documentation gaps",
            "3": "Adequate maintainability with some clarity issues",
            "2": "Poor maintainability, difficult to understand",
            "1": "Unmaintainable code requiring significant refactoring"
          }
        },
        "specific_instructions": "Assess code readability, abstractions, error handling, test coverage needs, and documentation quality"
      },
      {
        "name": "consistency",
        "description": "Adherence to project conventions and patterns",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Perfect consistency with project standards",
            "4": "Minor consistency deviations",
            "3": "Some inconsistencies with project patterns",
            "2": "Multiple consistency issues",
            "1": "Completely inconsistent with project standards"
          }
        },
        "specific_instructions": "Compare against project conventions, check naming patterns, code formatting, import organization, and comment style"
      },
      {
        "name": "best_practices",
        "description": "Industry standards, design patterns, idiomatic code",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Exemplary use of best practices",
            "4": "Good adherence to best practices",
            "3": "Some best practice violations",
            "2": "Multiple best practice issues",
            "1": "Poor adherence to industry standards"
          }
        },
        "specific_instructions": "Verify SOLID principles, error handling, logging practices, API design, and resource cleanup"
      },
      {
        "name": "code_smell",
        "description": "Anti-patterns, technical debt, refactoring opportunities",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "No code smells detected",
            "4": "Minor code smells present",
            "3": "Some code smells requiring attention",
            "2": "Multiple code smells present",
            "1": "Significant code smells requiring refactoring"
          }
        },
        "specific_instructions": "Identify duplicate code, overly complex methods, god objects/functions, magic numbers, and tight coupling"
      }
    ],
    "output_format": "xml",
    "output_schema": {
      "type": "object",
      "properties": {
        "metadata": {
          "type": "object"
        },
        "scores": {
          "type": "object"
        },
        "issues": {
          "type": "array"
        },
        "summary": {
          "type": "string"
        },
        "positive_observations": {
          "type": "array"
        }
      }
    },
    "global_context": {
      "context_file": "reviews/_SCRATCHSHEET.md",
      "context_update_rules": "Add newly discovered project-wide patterns that apply to 3+ files, are not language defaults, and would help future reviews",
      "template": "# {project_name} - Project Context & Patterns\n\n## Project Overview\nThis scratchsheet tracks project-wide patterns, conventions, and insights discovered during code review.\n\n## Discovered Patterns\n*Add patterns that apply to 3+ files and are not language defaults*\n\n{sections}\n\n## Review Guidelines\n*Patterns that should inform future reviews*\n\n{sections}\n\n---\n*This scratchsheet is automatically updated during the review process*",
      "sections": [
        {
          "name": "Architecture Patterns",
          "description": "Common architectural patterns and structures found across the codebase"
        },
        {
          "name": "Code Conventions",
          "description": "Project-specific coding standards and naming conventions"
        },
        {
          "name": "Common Issues",
          "description": "Recurring problems and anti-patterns found in multiple files"
        },
        {
          "name": "Dependencies & Libraries",
          "description": "Key libraries, frameworks, and dependencies used in the project"
        },
        {
          "name": "Security Considerations",
          "description": "Security patterns and considerations specific to this project"
        },
        {
          "name": "Performance Patterns",
          "description": "Performance-related patterns and optimizations"
        },
        {
          "name": "Maintainability Standards",
          "description": "Standards and practices that improve long-term maintainability"
        }
      ]
    }
  },
  "reduce": {
    "synthesis_template": "Analyze the {issue_count} code review issues from {file_count} files and create an actionable synthesis report.\n\n**Filter Context:**\n- Severity: {severity}\n- Category: {category}\n\n## Issues to Analyze\n{issues_data}\n\n## Required Output\n{output_sections}",
    "aggregation_rules": {
      "grouping_criteria": [
        "severity",
        "category",
        "file_type"
      ],
      "filtering_options": {
        "severity_levels": [
          "HIGH",
          "MEDIUM",
          "LOW"
        ],
        "categories": [
          "security",
          "performance",
          "maintainability",
          "consistency",
          "best_practices",
          "code_smell"
        ],
        "score_thresholds": {
          "critical": 2,
          "needs_attention": 3,
          "acceptable": 4
        }
      },
      "pattern_detection": {
        "similarity_threshold": 0.8,
        "minimum_occurrences": 3,
        "pattern_types": [
          "common_issues",
          "architectural_problems",
          "style_violations"
        ]
      }
    },
    "output_sections": [
      {
        "name": "executive_summary",
        "description": "Overall code health assessment and most critical areas",
        "template": "## Executive Summary\n\nProvide 2-3 sentences covering overall code health and most critical areas requiring attention.",
        "required": true
      },
      {
        "name": "priority_issues",
        "description": "Top 5 issues with business impact",
        "template": "## Top 5 Priority Issues\n\nFocus on issues affecting security, performance, or maintainability with business rationale for prioritization.",
        "required": true
      },
      {
        "name": "quick_wins",
        "description": "High-impact, low-effort fixes",
        "template": "## Quick Wins\n\nIssues that can be resolved quickly but provide significant value, suitable for immediate implementation.",
        "required": true
      },
      {
        "name": "root_causes",
        "description": "Systemic issues and patterns",
        "template": "## Root Causes\n\nPatterns indicating deeper architectural or process problems, training or tooling gaps.",
        "required": true
      },
      {
        "name": "action_plan",
        "description": "Prioritized implementation steps",
        "template": "## Action Plan\n\nConcrete steps for addressing identified issues with timeline and resource considerations.",
        "required": true
      }
    ],
    "output_format": "markdown"
  },
  "execution": {
    "engine": "claude",
    "batch_size": 1,
    "delay_between_batches": 5,
    "resume_on_failure": true,
    "max_retries": 3
  }
}
```

#### 2.2 Create `vibe-check-code-review-framework/data/master.json`

Create this file with the following content:

```json
{
  "metadata": {
    "project": {
    "name": "vibe-check-code-review",
    "version": "1.0",
    "description": "Code review system analyzing source code quality across six key dimensions"
},
    "generated": "",
    "total_items": 0,
    "collection_strategy": "git"
  },
  "items": {}
}
```

#### 2.3 Create `vibe-check-code-review-framework/prompts/PROCESSING_INSTRUCTIONS.md`

Create this file with the following content:

```markdown
# PROCESSING INSTRUCTIONS - vibe-check-code-review

## What is this system?

Code review system analyzing source code quality across six key dimensions

## Your Role

You are the Item Processor AI. Your task is to analyze EXACTLY ONE item and produce a comprehensive analysis following a deterministic algorithm.

## Inputs

- `ITEM_PATH` - The specific item path provided by the processing script
- `OUTPUT_FILE` - Pre-created output file path ready for you to populate
- Access to `vibe-check-code-review-framework/` directory for reading and writing artifacts

## Assessment Dimensions


### Security

**Description**: Vulnerabilities, input validation, authentication/authorization issues

**Scoring**: 1-5 scale

**Criteria**:
- 5: Exemplary security practices, no vulnerabilities found
- 4: Minor security concerns that don't pose immediate risk
- 3: At least one medium severity security issue present
- 2: High severity security vulnerabilities present
- 1: Critical security flaws requiring immediate attention

**Instructions**: Check for input validation, authentication/authorization issues, potential injection vulnerabilities, cryptographic usage, and exposed secrets


### Performance

**Description**: Efficiency, resource usage, scalability concerns

**Scoring**: 1-5 scale

**Criteria**:
- 5: Excellent performance characteristics
- 4: Minor performance improvements possible
- 3: Noticeable performance issues present
- 2: Significant performance problems
- 1: Critical performance issues affecting usability

**Instructions**: Identify inefficient algorithms, N+1 query patterns, memory leaks, caching opportunities, and blocking operations


### Maintainability

**Description**: Code clarity, modularity, documentation quality

**Scoring**: 1-5 scale

**Criteria**:
- 5: Highly maintainable with excellent documentation
- 4: Good maintainability with minor documentation gaps
- 3: Adequate maintainability with some clarity issues
- 2: Poor maintainability, difficult to understand
- 1: Unmaintainable code requiring significant refactoring

**Instructions**: Assess code readability, abstractions, error handling, test coverage needs, and documentation quality


### Consistency

**Description**: Adherence to project conventions and patterns

**Scoring**: 1-5 scale

**Criteria**:
- 5: Perfect consistency with project standards
- 4: Minor consistency deviations
- 3: Some inconsistencies with project patterns
- 2: Multiple consistency issues
- 1: Completely inconsistent with project standards

**Instructions**: Compare against project conventions, check naming patterns, code formatting, import organization, and comment style


### Best_Practices

**Description**: Industry standards, design patterns, idiomatic code

**Scoring**: 1-5 scale

**Criteria**:
- 5: Exemplary use of best practices
- 4: Good adherence to best practices
- 3: Some best practice violations
- 2: Multiple best practice issues
- 1: Poor adherence to industry standards

**Instructions**: Verify SOLID principles, error handling, logging practices, API design, and resource cleanup


### Code_Smell

**Description**: Anti-patterns, technical debt, refactoring opportunities

**Scoring**: 1-5 scale

**Criteria**:
- 5: No code smells detected
- 4: Minor code smells present
- 3: Some code smells requiring attention
- 2: Multiple code smells present
- 1: Significant code smells requiring refactoring

**Instructions**: Identify duplicate code, overly complex methods, god objects/functions, magic numbers, and tight coupling


## Precise Algorithm to Follow

### Step 1: Analyze the Item

- Read the complete item from ITEM_PATH
- Identify item type and characteristics
- Note primary purpose and content

### Step 2: Assess Each Dimension

- **Security**: Vulnerabilities, input validation, authentication/authorization issues
- **Performance**: Efficiency, resource usage, scalability concerns
- **Maintainability**: Code clarity, modularity, documentation quality
- **Consistency**: Adherence to project conventions and patterns
- **Best_Practices**: Industry standards, design patterns, idiomatic code
- **Code_Smell**: Anti-patterns, technical debt, refactoring opportunities

### Step 3: Complete the Output File

Fill in the pre-created output file with:

1. **Metadata section**: Update item information
2. **Scores section**: Update each dimension's score and findings count
3. **Findings section**: Add detailed findings for any issues discovered
4. **Summary section**: Provide overall assessment
5. **Recommendations section**: Add actionable recommendations

### Step 4: Complete

- Save all modified files
- Output only: "Analysis of [ITEM_PATH] complete."
- Do not provide any additional commentary

## Important Rules

1. Analyze ONLY the single item specified
2. Be objective and consistent in scoring
3. Always provide actionable recommendations
4. Use exact paths (no wildcards or patterns)
5. Maintain the exact format specified
6. Complete ALL sections even if empty
7. Never modify source files
8. Keep findings specific and detailed
9. Focus on substantive issues
10. End with only the completion message
```

#### 2.4 Create `vibe-check-code-review-framework/prompts/SYNTHESIS_INSTRUCTIONS.md`

Create this file with the following content:

```markdown
# SYNTHESIS INSTRUCTIONS - vibe-check-code-review

## What is Synthesis?

Synthesis is the "reduce" step in the vibe-check-code-review workflow. After individual items have been processed (the "map" step), synthesis analyzes all collected results to identify patterns, prioritize findings, and create actionable recommendations.

## Your Task

Analyze the {issue_count} findings from {file_count} items and create a comprehensive synthesis report.

**Filter Context:**
- Severity: {severity}
- Category: {category}

## Findings to Analyze

{issues_data}

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
```

### 3. Create Processing Script

#### 3.1 Create `vibe-check-code-review-framework/process.py`

Create this streamlined executable script:

```python
#!/usr/bin/env python3
"""vibe-check-code-review - Automated Processing System"""

import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# ANSI colors
R, G, Y, B, N = "\033[0;31m", "\033[0;32m", "\033[1;33m", "\033[0;34m", "\033[0m"

def status(color, msg):
    print(f"{color}{msg}{N}")

class VibeCheckCodeReview:
    def __init__(self):
        self.framework_dir = Path("vibe-check-code-review-framework")
        self.config_file = self.framework_dir / "config.json"
        self.master_file = self.framework_dir / "data" / "master.json"
        
        # Load configuration
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
    
    def populate(self, target_directories=None):
        """Stage 1: Populate - collect items for processing"""
        status(B, "=== Stage 1: Populate ===")
        
        # Collection logic based on strategy
        strategy = self.config['populate']['collection_strategy']
        
        if strategy == 'filesystem':
            items = self._collect_filesystem_items(target_directories)
        elif strategy == 'git':
            items = self._collect_git_items(target_directories)
        else:
            raise ValueError(f"Unsupported collection strategy: {strategy}")
        
        # Apply filters
        items = self._apply_filters(items)
        
        # Save to master file
        master_data = {
            "metadata": {
                "project": self.config['project'],
                "generated": datetime.utcnow().isoformat() + 'Z',
                "total_items": len(items),
                "collection_strategy": strategy
            },
            "items": {}
        }
        
        for item in items:
            master_data['items'][item['path']] = item
        
        with open(self.master_file, 'w') as f:
            json.dump(master_data, f, indent=2)
        
        status(G, f"✓ Populated {len(items)} items")
        return 0
    
    def _collect_filesystem_items(self, target_directories):
        """Collect items using filesystem strategy"""
        items = []
        include_patterns = self.config['populate']['item_filters']['include_patterns']
        
        search_paths = [Path(d) for d in target_directories] if target_directories else [Path('.')]
        
        for search_path in search_paths:
            for pattern in include_patterns:
                for item_path in search_path.rglob(pattern):
                    if item_path.is_file():
                        items.append({
                            'path': str(item_path.relative_to('.')),
                            'size': item_path.stat().st_size,
                            'status': 'not_analyzed'
                        })
        
        return items
    
    def _collect_git_items(self, target_directories):
        """Collect items using git strategy"""
        # Git collection logic here
        return self._collect_filesystem_items(target_directories)  # Fallback
    
    def _apply_filters(self, items):
        """Apply configured filters to items"""
        filters = self.config['populate']['item_filters']
        filtered_items = []
        
        for item in items:
            # Apply size filter
            if item['size'] > filters.get('max_size_bytes', float('inf')):
                continue
            
            # Apply exclude patterns
            if any(pattern in item['path'] for pattern in filters.get('exclude_patterns', [])):
                continue
            
            filtered_items.append(item)
        
        return filtered_items
    
    def _parse_xml_to_dict(self, element):
        """Parse XML element to dictionary structure"""
        result = {}
        
        # Handle element text
        if element.text and element.text.strip():
            result['text'] = element.text.strip()
        
        # Handle attributes
        if element.attrib:
            result['attributes'] = element.attrib
        
        # Handle child elements
        for child in element:
            child_result = self._parse_xml_to_dict(child)
            
            if child.tag in result:
                # If tag already exists, make it a list
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_result)
            else:
                result[child.tag] = child_result
        
        return result
    
    def _load_global_context(self):
        """Load global context for processing"""
        global_context_config = self.config['map'].get('global_context', {})
        context_file = global_context_config.get('context_file')
        
        if context_file:
            context_path = self.framework_dir / context_file
            # Create the context file and its directory if they don't exist
            context_path.parent.mkdir(parents=True, exist_ok=True)
            if not context_path.exists():
                self._initialize_scratchsheet(context_path)
            
            with open(context_path, 'r') as f:
                return f.read()
        
        return "No global context available."
    
    def _initialize_scratchsheet(self, context_path):
        """Initialize the scratchsheet with configurable structure"""
        project_name = self.config['project']['name']
        global_context_config = self.config['map'].get('global_context', {})
        
        # Use configurable template or fallback to basic template
        template = global_context_config.get('template', 
            "# {project_name} - Project Context & Patterns\n\n## Project Overview\nThis scratchsheet tracks project-wide patterns, conventions, and insights discovered during code review.\n\n{sections}\n\n---\n*This scratchsheet is automatically updated during the review process*")
        
        # Build sections from configuration
        sections_config = global_context_config.get('sections', [])
        sections_content = ""
        
        for section in sections_config:
            section_name = section['name']
            section_description = section.get('description', '')
            placeholder = section.get('placeholder', 'TBD')
            
            sections_content += f"### {section_name}\n"
            if section_description:
                sections_content += f"*{section_description}*\n\n"
            sections_content += f"- {placeholder}\n\n"
        
        # Replace template variables
        initial_content = template.format(
            project_name=project_name.title(),
            sections=sections_content.strip()
        )
        
        with open(context_path, 'w') as f:
            f.write(initial_content)
    
    def process(self):
        """Stage 2: Process single item"""
        with open(self.master_file, 'r') as f:
            master_data = json.load(f)
        
        # Find next item to process
        for item_path, item in master_data['items'].items():
            if item['status'] == 'not_analyzed':
                return self._process_item(item_path, item)
        
        status(G, "All items processed!")
        return 0
    
    def process_all(self):
        """Stage 2: Process all items"""
        processed = 0
        while True:
            with open(self.master_file, 'r') as f:
                master_data = json.load(f)
            
            # Find items to process
            remaining = [path for path, item in master_data['items'].items() if item['status'] == 'not_analyzed']
            
            if not remaining:
                break
            
            status(Y, f"Remaining: {len(remaining)}, Processing #{processed + 1}")
            
            if self.process() == 0:
                processed += 1
                # Small delay between items
                time.sleep(2)
            else:
                status(R, "Processing failed! Stopping.")
                return 1
        
        status(G, f"✓ Processed {processed} items total")
        return 0
    
    def _process_item(self, item_path, item):
        """Process a single item"""
        status(B, f"Processing: {item_path}")
        
        # Create output file that mirrors source structure
        output_format = 'xml'  # Always use XML for map stage output
        item_path_obj = Path(item_path)
        
        # Mirror the source directory structure
        output_file = self.framework_dir / "results" / item_path_obj.parent / f"{item_path_obj.stem}.{output_format}"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load global context (scratchsheet)
        global_context = self._load_global_context()
        
        # Create processing prompt
        with open(self.framework_dir / "prompts" / "PROCESSING_INSTRUCTIONS.md", 'r') as f:
            instructions = f.read()
        
        prompt = f"Process this item:\nITEM_PATH: {item_path}\nOUTPUT_FILE: {output_file}\nGLOBAL_CONTEXT: {global_context}\n\n{instructions}"
        
        # Run Claude CLI - pass prompt via stdin to avoid command line length limits
        proc = subprocess.Popen([
            "claude", "--print", "-",
            "--output-format", "stream-json",
            "--permission-mode", "acceptEdits",
            "--verbose"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send prompt and get streaming output
        stdout, stderr = proc.communicate(input=prompt)
        
        # Display live output (parse stream-json to show assistant messages)
        import json
        for line in stdout.strip().split('\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    if data.get('type') == 'assistant':
                        for content in data.get('message', {}).get('content', []):
                            if content.get('type') == 'text':
                                print(content.get('text', ''))
                                print("---")
                except json.JSONDecodeError:
                    pass
        
        result = type('Result', (), {'returncode': proc.returncode, 'stdout': stdout, 'stderr': stderr})()
        
        if result.returncode == 0:
            # Mark as completed
            with open(self.master_file, 'r') as f:
                master_data = json.load(f)
            master_data['items'][item_path]['status'] = 'completed'
            with open(self.master_file, 'w') as f:
                json.dump(master_data, f, indent=2)
            
            status(G, "✓ Processing completed!")
            return 0
        else:
            status(R, "✗ Processing failed!")
            return 1
    
    def synthesize(self):
        """Stage 3: Synthesize results"""
        status(B, "=== Stage 3: Synthesize ===")
        
        # Collect all results
        results = []
        results_dir = self.framework_dir / "results"
        
        output_format = 'xml'  # Always use XML for map stage output
        
        for result_file in results_dir.rglob("*.xml"):
            with open(result_file, 'r') as f:
                # Parse XML and convert to dict-like structure
                import xml.etree.ElementTree as ET
                try:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    result = self._parse_xml_to_dict(root)
                    results.append(result)
                except ET.ParseError as e:
                    # Handle malformed XML by reading as text and extracting basic info
                    f.seek(0)
                    content = f.read()
                    # Try to extract basic metadata and skip for now
                    result = {'content': content, 'metadata': {'item_path': str(result_file)}}
                    results.append(result)
        
        if not results:
            status(Y, "No results found to synthesize")
            return 0
        
        # Create synthesis prompt
        with open(self.framework_dir / "prompts" / "SYNTHESIS_INSTRUCTIONS.md", 'r') as f:
            template = f.read()
        
        # Format results data
        issues_data = ""
        total_issues = 0
        
        for result in results:
            # Get item path from metadata
            item_path = result.get('metadata', {}).get('item_path', 'unknown')
            if isinstance(item_path, dict) and 'text' in item_path:
                item_path = item_path['text']
            
            # Handle findings structure (could be dict or XML-parsed structure)
            findings = result.get('findings', {})
            if not findings:
                continue
                
            # Process each category
            for category, category_data in findings.items():
                if not category_data:
                    continue
                    
                # Handle both list and dict formats
                finding_list = category_data
                if isinstance(category_data, dict):
                    finding_list = category_data.get('finding', [])
                    if not isinstance(finding_list, list):
                        finding_list = [finding_list]
                
                for finding in finding_list:
                    if not finding:
                        continue
                        
                    # Extract finding details (handle both dict and XML structure)
                    finding_type = finding.get('type', {})
                    if isinstance(finding_type, dict):
                        finding_type = finding_type.get('text', 'unknown')
                    
                    description = finding.get('description', {})
                    if isinstance(description, dict):
                        description = description.get('text', '')
                    
                    impact = finding.get('impact', {})
                    if isinstance(impact, dict):
                        impact = impact.get('text', 'No impact specified')
                    
                    location = finding.get('location', {})
                    if isinstance(location, dict):
                        location = location.get('text', '')
                    
                    issues_data += f"\n**{finding_type.upper()} {category.upper()}**: {description}\n"
                    issues_data += f"  File: {item_path}"
                    if location:
                        issues_data += f" ({location})"
                    issues_data += f"\n  Impact: {impact}\n"
                    total_issues += 1
        
        prompt = template.format(
            issue_count=total_issues,
            file_count=len(results),
            severity='medium',
            category='all',
            issues_data=issues_data
        )
        
        # Run synthesis - pass prompt via stdin to avoid command line length limits
        proc = subprocess.Popen([
            "claude", "--print", "-",
            "--output-format", "stream-json",
            "--permission-mode", "acceptEdits",
            "--verbose"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send prompt and get streaming output
        stdout, stderr = proc.communicate(input=prompt)
        
        # Parse stream to extract content
        content_lines = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    if data.get('type') == 'assistant':
                        for content in data.get('message', {}).get('content', []):
                            if content.get('type') == 'text':
                                content_lines.append(content.get('text', ''))
                except json.JSONDecodeError:
                    pass
        
        synthesis_content = '\n'.join(content_lines)
        result = type('Result', (), {'returncode': proc.returncode, 'stdout': synthesis_content, 'stderr': stderr})()
        
        if result.returncode == 0:
            # Save synthesis result
            synthesis_file = self.framework_dir / "synthesis" / f"synthesis_{datetime.now():%Y%m%d_%H%M%S}.md"
            synthesis_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(synthesis_file, 'w') as f:
                f.write(result.stdout)
            
            status(G, f"✓ Synthesis complete: {synthesis_file}")
            return 0
        else:
            status(R, "✗ Synthesis failed!")
            return 1

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Code review system analyzing source code quality across six key dimensions")
    parser.add_argument("command", choices=["populate", "process", "process-all", "synthesize"])
    parser.add_argument("directories", nargs="*", help="Target directories (optional)")
    
    args = parser.parse_args()
    
    processor = VibeCheckCodeReview()
    
    if args.command == "populate":
        return processor.populate(args.directories)
    elif args.command == "process":
        return processor.process()
    elif args.command == "process-all":
        return processor.process_all()
    elif args.command == "synthesize":
        return processor.synthesize()

if __name__ == "__main__":
    sys.exit(main())
```

### 4. Make Script Executable

```bash
chmod +x vibe-check-code-review-framework/process.py
```

### 5. Usage

#### 5.1 Basic Workflow

```bash
# 1. Populate items
python3 vibe-check-code-review-framework/process.py populate

# 2. Process items (choose one)
python3 vibe-check-code-review-framework/process.py process      # Process single item
python3 vibe-check-code-review-framework/process.py process-all  # Process all items

# 3. Synthesize results
python3 vibe-check-code-review-framework/process.py synthesize
```

### 6. Important Notes

- **Single-File Setup**: This system is designed to work as a self-contained processing framework
- **Claude Integration**: Optimized for use with Claude Code CLI
- **Resumable**: Processing can be interrupted and resumed
- **Configurable**: All behavior defined in the configuration file

This setup creates a complete, self-contained processing system based on your configuration.

When finished with the setup, you can begin processing by running the populate command. The system will automatically handle item collection, individual processing, and synthesis according to your configuration.

**Cost Warning**: Using this system with API keys can be expensive on large datasets. Claude Code subscription is recommended for extensive processing.
