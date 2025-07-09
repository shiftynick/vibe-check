# RESEARCH_PAPER_ANALYSIS_SETUP.md

## Setup Instructions for Academic research paper analysis system for systematic literature review

You are tasked with setting up the research-paper-analysis system within an existing repository. This will create a `research-paper-analysis-framework` folder in the current directory that contains all processing artifacts.

### 1. Create Directory Structure

Create the following directory hierarchy within a new `research-paper-analysis-framework` folder:

```
research-paper-analysis-framework/
├── data/
├── results/
├── synthesis/
├── logs/
└── prompts/
```

### 2. Create Configuration Files

#### 2.1 Create `research-paper-analysis-framework/config.json`

Create this file with the following content:

```json
{
  "project": {
    "name": "research-paper-analysis",
    "version": "1.0",
    "description": "Academic research paper analysis system for systematic literature review"
  },
  "populate": {
    "collection_strategy": "filesystem",
    "item_filters": {
      "include_patterns": [
        "*.pdf",
        "*.docx",
        "*.txt",
        "*.md"
      ],
      "exclude_patterns": [
        "*template*",
        "*draft*"
      ],
      "exclude_directories": [
        "temp",
        "backup",
        "archive"
      ],
      "max_size_bytes": 10485760
    },
    "metadata_extraction": {
      "required_fields": [
        "path",
        "document_type",
        "word_count",
        "status"
      ],
      "optional_fields": [
        "author",
        "publication_date",
        "journal"
      ],
      "extraction_rules": {
        "document_type": "file_extension.title()",
        "word_count": "0",
        "status": "'not_analyzed'"
      }
    },
    "output_format": "json"
  },
  "map": {
    "processing_template": "You are a Research Paper Analyst. Analyze the document at {item_path} and provide a comprehensive academic analysis.\n\n## Document Information\n{item_data}\n\n## Analysis Dimensions\n{assessment_instructions}\n\n## Output Requirements\n{output_requirements}\n\nFocus on academic rigor, methodology, and contribution to the field.",
    "assessment_dimensions": [
      {
        "name": "methodology",
        "description": "Research methodology quality and appropriateness",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Excellent methodology, rigorous and well-justified",
            "4": "Good methodology with minor limitations",
            "3": "Adequate methodology with some concerns",
            "2": "Poor methodology with significant flaws",
            "1": "Severely flawed or inappropriate methodology"
          }
        },
        "specific_instructions": "Evaluate research design, data collection methods, sample size, controls, and statistical analysis approaches"
      },
      {
        "name": "contribution",
        "description": "Novelty and significance of contribution to the field",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Groundbreaking contribution with major implications",
            "4": "Significant contribution advancing the field",
            "3": "Moderate contribution with some value",
            "2": "Minor contribution with limited impact",
            "1": "No clear contribution or replicates existing work"
          }
        },
        "specific_instructions": "Assess originality, theoretical advancement, practical applications, and potential impact on future research"
      },
      {
        "name": "literature_review",
        "description": "Quality and comprehensiveness of literature review",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Comprehensive, critical, and well-integrated review",
            "4": "Good review with minor gaps",
            "3": "Adequate review covering main areas",
            "2": "Limited review missing key references",
            "1": "Poor or superficial literature review"
          }
        },
        "specific_instructions": "Evaluate coverage of relevant literature, critical analysis, identification of gaps, and theoretical framework"
      },
      {
        "name": "clarity",
        "description": "Writing quality, structure, and presentation",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Exceptionally clear, well-structured, and engaging",
            "4": "Clear and well-organized with minor issues",
            "3": "Generally clear with some organizational problems",
            "2": "Unclear in places with structural issues",
            "1": "Poor writing quality hindering comprehension"
          }
        },
        "specific_instructions": "Assess logical flow, argument structure, use of evidence, and overall readability"
      },
      {
        "name": "reproducibility",
        "description": "Reproducibility and transparency of methods",
        "scoring_rubric": {
          "scale": {
            "min": 1,
            "max": 5,
            "type": "integer"
          },
          "criteria": {
            "5": "Fully reproducible with detailed protocols",
            "4": "Mostly reproducible with minor gaps",
            "3": "Partially reproducible with some details missing",
            "2": "Difficult to reproduce due to missing information",
            "1": "Not reproducible or lacks essential details"
          }
        },
        "specific_instructions": "Evaluate availability of data, code, detailed protocols, and sufficient methodological detail"
      }
    ],
    "output_format": "json",
    "output_schema": {
      "type": "object",
      "properties": {
        "metadata": {
          "type": "object"
        },
        "scores": {
          "type": "object"
        },
        "findings": {
          "type": "array"
        },
        "abstract_summary": {
          "type": "string"
        },
        "key_contributions": {
          "type": "array"
        },
        "limitations": {
          "type": "array"
        },
        "future_work": {
          "type": "array"
        }
      }
    },
    "global_context": {
      "context_file": "research_context.md",
      "context_update_rules": "Add emerging themes, methodological patterns, and research gaps observed across multiple papers"
    }
  },
  "reduce": {
    "synthesis_template": "Analyze the {issue_count} research findings from {file_count} papers and create a comprehensive literature review synthesis.\n\n**Analysis Context:**\n- Focus Area: {category}\n- Quality Threshold: {severity}\n\n## Research Findings\n{issues_data}\n\n## Synthesis Requirements\n{output_sections}",
    "aggregation_rules": {
      "grouping_criteria": [
        "research_area",
        "methodology_type",
        "publication_year"
      ],
      "filtering_options": {
        "severity_levels": [
          "high",
          "medium",
          "low"
        ],
        "categories": [
          "methodology",
          "contribution",
          "literature_review",
          "clarity",
          "reproducibility"
        ],
        "score_thresholds": {
          "excellent": 4,
          "good": 3,
          "needs_improvement": 2
        }
      },
      "pattern_detection": {
        "similarity_threshold": 0.7,
        "minimum_occurrences": 2,
        "pattern_types": [
          "methodological_trends",
          "theoretical_frameworks",
          "research_gaps"
        ]
      }
    },
    "output_sections": [
      {
        "name": "literature_overview",
        "description": "Comprehensive overview of analyzed literature",
        "template": "## Literature Overview\n\nProvide a comprehensive overview of the {file_count} papers analyzed, including key themes, methodological approaches, and research contexts.",
        "required": true
      },
      {
        "name": "methodological_trends",
        "description": "Analysis of methodological patterns and trends",
        "template": "## Methodological Trends\n\nIdentify and analyze methodological patterns, innovative approaches, and common limitations across the reviewed papers.",
        "required": true
      },
      {
        "name": "theoretical_contributions",
        "description": "Key theoretical contributions and frameworks",
        "template": "## Theoretical Contributions\n\nSummarize major theoretical advances, frameworks, and conceptual contributions from the analyzed papers.",
        "required": true
      },
      {
        "name": "research_gaps",
        "description": "Identified research gaps and future directions",
        "template": "## Research Gaps and Future Directions\n\nIdentify systematic gaps in the literature and suggest promising directions for future research.",
        "required": true
      },
      {
        "name": "quality_assessment",
        "description": "Overall quality assessment and recommendations",
        "template": "## Quality Assessment\n\nProvide an overall assessment of the literature quality and recommendations for researchers in this field.",
        "required": true
      }
    ],
    "output_format": "markdown"
  },
  "execution": {
    "engine": "claude",
    "batch_size": 1,
    "delay_between_batches": 3,
    "resume_on_failure": true,
    "max_retries": 2
  }
}
```

#### 2.2 Create `research-paper-analysis-framework/data/master.json`

Create this file with the following content:

```json
{
  "metadata": {
    "project": {
    "name": "research-paper-analysis",
    "version": "1.0",
    "description": "Academic research paper analysis system for systematic literature review"
},
    "generated": "",
    "total_items": 0,
    "collection_strategy": "filesystem"
  },
  "items": {}
}
```

#### 2.3 Create `research-paper-analysis-framework/prompts/PROCESSING_INSTRUCTIONS.md`

Create this file with the following content:

```markdown
# PROCESSING INSTRUCTIONS - research-paper-analysis

## What is this system?

Academic research paper analysis system for systematic literature review

## Your Role

You are the Item Processor AI. Your task is to analyze EXACTLY ONE item and produce a comprehensive analysis following a deterministic algorithm.

## Inputs

- `ITEM_PATH` - The specific item path provided by the processing script
- `OUTPUT_FILE` - Pre-created output file path ready for you to populate
- Access to `research-paper-analysis-framework/` directory for reading and writing artifacts

## Assessment Dimensions


### Methodology

**Description**: Research methodology quality and appropriateness

**Scoring**: 1-5 scale

**Criteria**:
- 5: Excellent methodology, rigorous and well-justified
- 4: Good methodology with minor limitations
- 3: Adequate methodology with some concerns
- 2: Poor methodology with significant flaws
- 1: Severely flawed or inappropriate methodology

**Instructions**: Evaluate research design, data collection methods, sample size, controls, and statistical analysis approaches


### Contribution

**Description**: Novelty and significance of contribution to the field

**Scoring**: 1-5 scale

**Criteria**:
- 5: Groundbreaking contribution with major implications
- 4: Significant contribution advancing the field
- 3: Moderate contribution with some value
- 2: Minor contribution with limited impact
- 1: No clear contribution or replicates existing work

**Instructions**: Assess originality, theoretical advancement, practical applications, and potential impact on future research


### Literature_Review

**Description**: Quality and comprehensiveness of literature review

**Scoring**: 1-5 scale

**Criteria**:
- 5: Comprehensive, critical, and well-integrated review
- 4: Good review with minor gaps
- 3: Adequate review covering main areas
- 2: Limited review missing key references
- 1: Poor or superficial literature review

**Instructions**: Evaluate coverage of relevant literature, critical analysis, identification of gaps, and theoretical framework


### Clarity

**Description**: Writing quality, structure, and presentation

**Scoring**: 1-5 scale

**Criteria**:
- 5: Exceptionally clear, well-structured, and engaging
- 4: Clear and well-organized with minor issues
- 3: Generally clear with some organizational problems
- 2: Unclear in places with structural issues
- 1: Poor writing quality hindering comprehension

**Instructions**: Assess logical flow, argument structure, use of evidence, and overall readability


### Reproducibility

**Description**: Reproducibility and transparency of methods

**Scoring**: 1-5 scale

**Criteria**:
- 5: Fully reproducible with detailed protocols
- 4: Mostly reproducible with minor gaps
- 3: Partially reproducible with some details missing
- 2: Difficult to reproduce due to missing information
- 1: Not reproducible or lacks essential details

**Instructions**: Evaluate availability of data, code, detailed protocols, and sufficient methodological detail


## Precise Algorithm to Follow

### Step 1: Analyze the Item

- Read the complete item from ITEM_PATH
- Identify item type and characteristics
- Note primary purpose and content

### Step 2: Assess Each Dimension

- **Methodology**: Research methodology quality and appropriateness
- **Contribution**: Novelty and significance of contribution to the field
- **Literature_Review**: Quality and comprehensiveness of literature review
- **Clarity**: Writing quality, structure, and presentation
- **Reproducibility**: Reproducibility and transparency of methods

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

#### 2.4 Create `research-paper-analysis-framework/prompts/SYNTHESIS_INSTRUCTIONS.md`

Create this file with the following content:

```markdown
# SYNTHESIS INSTRUCTIONS - research-paper-analysis

## What is Synthesis?

Synthesis is the "reduce" step in the research-paper-analysis workflow. After individual items have been processed (the "map" step), synthesis analyzes all collected results to identify patterns, prioritize findings, and create actionable recommendations.

## Your Task

Analyze the {issue_count} findings from {file_count} items and create a comprehensive synthesis report.

**Filter Context:**
- Severity: {severity}
- Category: {category}

## Findings to Analyze

{issues_data}

## Required Output Format


### Literature Overview

Comprehensive overview of analyzed literature

Template: ## Literature Overview

Provide a comprehensive overview of the {file_count} papers analyzed, including key themes, methodological approaches, and research contexts.


### Methodological Trends

Analysis of methodological patterns and trends

Template: ## Methodological Trends

Identify and analyze methodological patterns, innovative approaches, and common limitations across the reviewed papers.


### Theoretical Contributions

Key theoretical contributions and frameworks

Template: ## Theoretical Contributions

Summarize major theoretical advances, frameworks, and conceptual contributions from the analyzed papers.


### Research Gaps

Identified research gaps and future directions

Template: ## Research Gaps and Future Directions

Identify systematic gaps in the literature and suggest promising directions for future research.


### Quality Assessment

Overall quality assessment and recommendations

Template: ## Quality Assessment

Provide an overall assessment of the literature quality and recommendations for researchers in this field.



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

#### 3.1 Create `research-paper-analysis-framework/process.py`

Create this streamlined executable script:

```python
#!/usr/bin/env python3
"""research-paper-analysis - Automated Processing System"""

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

class ResearchPaperAnalysis:
    def __init__(self):
        self.framework_dir = Path("research-paper-analysis-framework")
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
    
    def _process_item(self, item_path, item):
        """Process a single item"""
        status(B, f"Processing: {item_path}")
        
        # Create output file
        output_file = self.framework_dir / "results" / f"{Path(item_path).stem}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create processing prompt
        with open(self.framework_dir / "prompts" / "PROCESSING_INSTRUCTIONS.md", 'r') as f:
            instructions = f.read()
        
        prompt = f"Process this item:\nITEM_PATH: {item_path}\nOUTPUT_FILE: {output_file}\n\n{instructions}"
        
        # Run Claude CLI
        result = subprocess.run([
            "claude", "--print", prompt,
            "--output-format", "stream-json",
            "--permission-mode", "acceptEdits"
        ], capture_output=True, text=True)
        
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
        
        for result_file in results_dir.rglob("*.json"):
            with open(result_file, 'r') as f:
                results.append(json.load(f))
        
        if not results:
            status(Y, "No results found to synthesize")
            return 0
        
        # Create synthesis prompt
        with open(self.framework_dir / "prompts" / "SYNTHESIS_INSTRUCTIONS.md", 'r') as f:
            template = f.read()
        
        # Format results data
        issues_data = ""
        for result in results:
            for finding in result.get('findings', []):
                issues_data += f"\n**{finding.get('severity', 'unknown').upper()}**: {finding.get('description', '')}\n"
        
        prompt = template.format(
            issue_count=sum(len(r.get('findings', [])) for r in results),
            file_count=len(results),
            severity='medium',
            category='all',
            issues_data=issues_data
        )
        
        # Run synthesis
        result = subprocess.run([
            "claude", "--print", prompt,
            "--output-format", "stream-json",
            "--permission-mode", "acceptEdits"
        ], capture_output=True, text=True)
        
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
    
    parser = argparse.ArgumentParser(description="Academic research paper analysis system for systematic literature review")
    parser.add_argument("command", choices=["populate", "process", "synthesize"])
    parser.add_argument("directories", nargs="*", help="Target directories (optional)")
    
    args = parser.parse_args()
    
    processor = ResearchPaperAnalysis()
    
    if args.command == "populate":
        return processor.populate(args.directories)
    elif args.command == "process":
        return processor.process()
    elif args.command == "synthesize":
        return processor.synthesize()

if __name__ == "__main__":
    sys.exit(main())
```

### 4. Make Script Executable

```bash
chmod +x research-paper-analysis-framework/process.py
```

### 5. Usage

#### 5.1 Basic Workflow

```bash
# 1. Populate items
python3 research-paper-analysis-framework/process.py populate

# 2. Process items
python3 research-paper-analysis-framework/process.py process

# 3. Synthesize results
python3 research-paper-analysis-framework/process.py synthesize
```

### 6. Important Notes

- **Single-File Setup**: This system is designed to work as a self-contained processing framework
- **Claude Integration**: Optimized for use with Claude Code CLI
- **Resumable**: Processing can be interrupted and resumed
- **Configurable**: All behavior defined in the configuration file

This setup creates a complete, self-contained processing system based on your configuration.

When finished with the setup, you can begin processing by running the populate command. The system will automatically handle item collection, individual processing, and synthesis according to your configuration.

**Cost Warning**: Using this system with API keys can be expensive on large datasets. Claude Code subscription is recommended for extensive processing.
