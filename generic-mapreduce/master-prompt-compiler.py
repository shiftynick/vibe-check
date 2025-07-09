#!/usr/bin/env python3
"""
Master Prompt Compiler for Generic Map-Reduce Framework
Generates single-file setup instructions like the original VIBE_CHECK_SETUP.md
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class MasterPromptCompiler:
    """Compiles configuration into single-file setup instructions"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        with open(config_path, 'r') as f:
            self.config = json.load(f)
    
    def compile_setup_instructions(self) -> str:
        """Generate complete setup instructions as a single markdown file"""
        
        project = self.config['project']
        populate = self.config['populate']
        map_config = self.config['map']
        reduce_config = self.config['reduce']
        
        # Generate the master setup file
        setup_content = f"""# {project['name'].upper().replace('-', '_')}_SETUP.md

## Setup Instructions for {project['description']}

You are tasked with setting up the {project['name']} system within an existing repository. This will create a `{project['name']}-framework` folder in the current directory that contains all processing artifacts.

### 1. Create Directory Structure

Create the following directory hierarchy within a new `{project['name']}-framework` folder:

```
{project['name']}-framework/
├── data/
├── results/
├── synthesis/
├── logs/
└── prompts/
```

### 2. Create Configuration Files

#### 2.1 Create `{project['name']}-framework/config.json`

Create this file with the following content:

```json
{json.dumps(self.config, indent=2)}
```

#### 2.2 Create `{project['name']}-framework/data/master.json`

Create this file with the following content:

```json
{{
  "metadata": {{
    "project": {json.dumps(project, indent=4)},
    "generated": "",
    "total_items": 0,
    "collection_strategy": "{populate['collection_strategy']}"
  }},
  "items": {{}}
}}
```

#### 2.3 Create `{project['name']}-framework/prompts/PROCESSING_INSTRUCTIONS.md`

Create this file with the following content:

```markdown
# PROCESSING INSTRUCTIONS - {project['name']}

## What is this system?

{project['description']}

## Your Role

You are the Item Processor AI. Your task is to analyze EXACTLY ONE item and produce a comprehensive analysis following a deterministic algorithm.

## Inputs

- `ITEM_PATH` - The specific item path provided by the processing script
- `OUTPUT_FILE` - Pre-created output file path ready for you to populate
- Access to `{project['name']}-framework/` directory for reading and writing artifacts

## Assessment Dimensions

{self._generate_assessment_instructions(map_config['assessment_dimensions'])}

## Precise Algorithm to Follow

### Step 1: Analyze the Item

- Read the complete item from ITEM_PATH
- Identify item type and characteristics
- Note primary purpose and content

### Step 2: Assess Each Dimension

{self._generate_dimension_assessments(map_config['assessment_dimensions'])}

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

#### 2.4 Create `{project['name']}-framework/prompts/SYNTHESIS_INSTRUCTIONS.md`

Create this file with the following content:

```markdown
# SYNTHESIS INSTRUCTIONS - {project['name']}

## What is Synthesis?

Synthesis is the "reduce" step in the {project['name']} workflow. After individual items have been processed (the "map" step), synthesis analyzes all collected results to identify patterns, prioritize findings, and create actionable recommendations.

## Your Task

Analyze the {{issue_count}} findings from {{file_count}} items and create a comprehensive synthesis report.

**Filter Context:**
- Severity: {{severity}}
- Category: {{category}}

## Findings to Analyze

{{issues_data}}

## Required Output Format

{self._generate_synthesis_sections(reduce_config.get('output_sections', []))}

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

#### 3.1 Create `{project['name']}-framework/process.py`

Create this streamlined executable script:

```python
#!/usr/bin/env python3
\"\"\"{project['name']} - Automated Processing System\"\"\"

import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# ANSI colors
R, G, Y, B, N = "\\033[0;31m", "\\033[0;32m", "\\033[1;33m", "\\033[0;34m", "\\033[0m"

def status(color, msg):
    print(f"{{color}}{{msg}}{{N}}")

class {self._to_class_name(project['name'])}:
    def __init__(self):
        self.framework_dir = Path("{project['name']}-framework")
        self.config_file = self.framework_dir / "config.json"
        self.master_file = self.framework_dir / "data" / "master.json"
        
        # Load configuration
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
    
    def populate(self, target_directories=None):
        \"\"\"Stage 1: Populate - collect items for processing\"\"\"
        status(B, "=== Stage 1: Populate ===")
        
        # Collection logic based on strategy
        strategy = self.config['populate']['collection_strategy']
        
        if strategy == 'filesystem':
            items = self._collect_filesystem_items(target_directories)
        elif strategy == 'git':
            items = self._collect_git_items(target_directories)
        else:
            raise ValueError(f"Unsupported collection strategy: {{strategy}}")
        
        # Apply filters
        items = self._apply_filters(items)
        
        # Save to master file
        master_data = {{
            "metadata": {{
                "project": self.config['project'],
                "generated": datetime.utcnow().isoformat() + 'Z',
                "total_items": len(items),
                "collection_strategy": strategy
            }},
            "items": {{}}
        }}
        
        for item in items:
            master_data['items'][item['path']] = item
        
        with open(self.master_file, 'w') as f:
            json.dump(master_data, f, indent=2)
        
        status(G, f"✓ Populated {{len(items)}} items")
        return 0
    
    def _collect_filesystem_items(self, target_directories):
        \"\"\"Collect items using filesystem strategy\"\"\"
        items = []
        include_patterns = self.config['populate']['item_filters']['include_patterns']
        
        search_paths = [Path(d) for d in target_directories] if target_directories else [Path('.')]
        
        for search_path in search_paths:
            for pattern in include_patterns:
                for item_path in search_path.rglob(pattern):
                    if item_path.is_file():
                        items.append({{
                            'path': str(item_path.relative_to('.')),
                            'size': item_path.stat().st_size,
                            'status': 'not_analyzed'
                        }})
        
        return items
    
    def _collect_git_items(self, target_directories):
        \"\"\"Collect items using git strategy\"\"\"
        # Git collection logic here
        return self._collect_filesystem_items(target_directories)  # Fallback
    
    def _apply_filters(self, items):
        \"\"\"Apply configured filters to items\"\"\"
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
        \"\"\"Stage 2: Process single item\"\"\"
        with open(self.master_file, 'r') as f:
            master_data = json.load(f)
        
        # Find next item to process
        for item_path, item in master_data['items'].items():
            if item['status'] == 'not_analyzed':
                return self._process_item(item_path, item)
        
        status(G, "All items processed!")
        return 0
    
    def _process_item(self, item_path, item):
        \"\"\"Process a single item\"\"\"
        status(B, f"Processing: {{item_path}}")
        
        # Create output file
        output_file = self.framework_dir / "results" / f"{{Path(item_path).stem}}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create processing prompt
        with open(self.framework_dir / "prompts" / "PROCESSING_INSTRUCTIONS.md", 'r') as f:
            instructions = f.read()
        
        prompt = f"Process this item:\\nITEM_PATH: {{item_path}}\\nOUTPUT_FILE: {{output_file}}\\n\\n{{instructions}}"
        
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
        \"\"\"Stage 3: Synthesize results\"\"\"
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
                issues_data += f"\\n**{{finding.get('severity', 'unknown').upper()}}**: {{finding.get('description', '')}}\\n"
        
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
            synthesis_file = self.framework_dir / "synthesis" / f"synthesis_{{datetime.now():%Y%m%d_%H%M%S}}.md"
            synthesis_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(synthesis_file, 'w') as f:
                f.write(result.stdout)
            
            status(G, f"✓ Synthesis complete: {{synthesis_file}}")
            return 0
        else:
            status(R, "✗ Synthesis failed!")
            return 1

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="{project['description']}")
    parser.add_argument("command", choices=["populate", "process", "synthesize"])
    parser.add_argument("directories", nargs="*", help="Target directories (optional)")
    
    args = parser.parse_args()
    
    processor = {self._to_class_name(project['name'])}()
    
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
chmod +x {project['name']}-framework/process.py
```

### 5. Usage

#### 5.1 Basic Workflow

```bash
# 1. Populate items
python3 {project['name']}-framework/process.py populate

# 2. Process items
python3 {project['name']}-framework/process.py process

# 3. Synthesize results
python3 {project['name']}-framework/process.py synthesize
```

### 6. Important Notes

- **Single-File Setup**: This system is designed to work as a self-contained processing framework
- **Claude Integration**: Optimized for use with Claude Code CLI
- **Resumable**: Processing can be interrupted and resumed
- **Configurable**: All behavior defined in the configuration file

This setup creates a complete, self-contained processing system based on your configuration.

When finished with the setup, you can begin processing by running the populate command. The system will automatically handle item collection, individual processing, and synthesis according to your configuration.

**Cost Warning**: Using this system with API keys can be expensive on large datasets. Claude Code subscription is recommended for extensive processing.
"""

        return setup_content
    
    def _generate_assessment_instructions(self, dimensions):
        """Generate assessment instructions for each dimension"""
        instructions = []
        
        for dimension in dimensions:
            name = dimension['name']
            description = dimension['description']
            scoring = dimension.get('scoring_rubric', {})
            specific = dimension.get('specific_instructions', '')
            
            instruction = f"""
### {name.title()}

**Description**: {description}

**Scoring**: {scoring.get('scale', {}).get('min', 1)}-{scoring.get('scale', {}).get('max', 5)} scale

**Criteria**:
"""
            
            for score, criteria in scoring.get('criteria', {}).items():
                instruction += f"- {score}: {criteria}\n"
            
            instruction += f"\n**Instructions**: {specific}\n"
            
            instructions.append(instruction)
        
        return "\n".join(instructions)
    
    def _generate_dimension_assessments(self, dimensions):
        """Generate step-by-step assessment instructions"""
        assessments = []
        
        for dimension in dimensions:
            name = dimension['name']
            assessments.append(f"- **{name.title()}**: {dimension['description']}")
        
        return "\n".join(assessments)
    
    def _generate_synthesis_sections(self, sections):
        """Generate synthesis output sections"""
        if not sections:
            return "Create a comprehensive synthesis report covering key findings and recommendations."
        
        section_text = ""
        for section in sections:
            section_text += f"\n### {section['name'].replace('_', ' ').title()}\n\n"
            section_text += f"{section['description']}\n\n"
            if section.get('template'):
                section_text += f"Template: {section['template']}\n\n"
        
        return section_text
    
    def _to_class_name(self, project_name):
        """Convert project name to class name"""
        return ''.join(word.capitalize() for word in project_name.replace('-', '_').split('_'))

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Master Prompt Compiler - Generate single-file setup instructions"
    )
    parser.add_argument(
        "config",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: PROJECT_NAME_SETUP.md)"
    )
    
    args = parser.parse_args()
    
    try:
        compiler = MasterPromptCompiler(Path(args.config))
        setup_content = compiler.compile_setup_instructions()
        
        # Determine output file
        if args.output:
            output_file = Path(args.output)
        else:
            project_name = compiler.config['project']['name']
            output_file = Path(f"{project_name.upper().replace('-', '_')}_SETUP.md")
        
        # Write setup file
        with open(output_file, 'w') as f:
            f.write(setup_content)
        
        print(f"✓ Master setup file generated: {output_file}")
        return 0
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())