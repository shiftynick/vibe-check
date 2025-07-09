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
        map_config = self.config['map'].copy()  # Make a copy to modify
        reduce_config = self.config['reduce']
        
        # Force XML output format for map stage
        map_config['output_format'] = 'xml'
        
        # Update config with forced XML format
        config_for_output = self.config.copy()
        config_for_output['map'] = map_config
        
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
{json.dumps(config_for_output, indent=2)}
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
    
    def _parse_xml_to_dict(self, element):
        \"\"\"Parse XML element to dictionary structure\"\"\"
        result = {{}}
        
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
        \"\"\"Load global context for processing\"\"\"
        global_context_config = self.config['map'].get('global_context', {{}})
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
        \"\"\"Initialize the scratchsheet with configurable structure\"\"\"
        project_name = self.config['project']['name']
        global_context_config = self.config['map'].get('global_context', {{}})
        
        # Use configurable template or fallback to basic template
        template = global_context_config.get('template', 
            "# {{project_name}} - Project Context & Patterns\\n\\n## Project Overview\\nThis scratchsheet tracks project-wide patterns, conventions, and insights discovered during code review.\\n\\n{{sections}}\\n\\n---\\n*This scratchsheet is automatically updated during the review process*")
        
        # Build sections from configuration
        sections_config = global_context_config.get('sections', [])
        sections_content = ""
        
        for section in sections_config:
            section_name = section['name']
            section_description = section.get('description', '')
            placeholder = section.get('placeholder', 'TBD')
            
            sections_content += f"### {{section_name}}\\n"
            if section_description:
                sections_content += f"*{{section_description}}*\\n\\n"
            sections_content += f"- {{placeholder}}\\n\\n"
        
        # Replace template variables
        initial_content = template.format(
            project_name=project_name.title(),
            sections=sections_content.strip()
        )
        
        with open(context_path, 'w') as f:
            f.write(initial_content)
    
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
    
    def process_all(self):
        \"\"\"Stage 2: Process all items\"\"\"
        processed = 0
        while True:
            with open(self.master_file, 'r') as f:
                master_data = json.load(f)
            
            # Find items to process
            remaining = [path for path, item in master_data['items'].items() if item['status'] == 'not_analyzed']
            
            if not remaining:
                break
            
            status(Y, f"Remaining: {{len(remaining)}}, Processing #{{processed + 1}}")
            
            if self.process() == 0:
                processed += 1
                # Small delay between items
                time.sleep(2)
            else:
                status(R, "Processing failed! Stopping.")
                return 1
        
        status(G, f"✓ Processed {{processed}} items total")
        return 0
    
    def _process_item(self, item_path, item):
        \"\"\"Process a single item\"\"\"
        status(B, f"Processing: {{item_path}}")
        
        # Create output file that mirrors source structure
        output_format = 'xml'  # Always use XML for map stage output
        item_path_obj = Path(item_path)
        
        # Mirror the source directory structure
        output_file = self.framework_dir / "results" / item_path_obj.parent / f"{{item_path_obj.stem}}.{{output_format}}"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load global context (scratchsheet)
        global_context = self._load_global_context()
        
        # Create processing prompt
        with open(self.framework_dir / "prompts" / "PROCESSING_INSTRUCTIONS.md", 'r') as f:
            instructions = f.read()
        
        prompt = f"Process this item:\\nITEM_PATH: {{item_path}}\\nOUTPUT_FILE: {{output_file}}\\nGLOBAL_CONTEXT: {{global_context}}\\n\\n{{instructions}}"
        
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
        for line in stdout.strip().split('\\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    if data.get('type') == 'assistant':
                        for content in data.get('message', {{}}).get('content', []):
                            if content.get('type') == 'text':
                                print(content.get('text', ''))
                                print("---")
                except json.JSONDecodeError:
                    pass
        
        result = type('Result', (), {{'returncode': proc.returncode, 'stdout': stdout, 'stderr': stderr}})()
        
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
                    result = {{'content': content, 'metadata': {{'item_path': str(result_file)}}}}
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
            item_path = result.get('metadata', {{}}).get('item_path', 'unknown')
            if isinstance(item_path, dict) and 'text' in item_path:
                item_path = item_path['text']
            
            # Handle findings structure (could be dict or XML-parsed structure)
            findings = result.get('findings', {{}})
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
                    finding_type = finding.get('type', {{}})
                    if isinstance(finding_type, dict):
                        finding_type = finding_type.get('text', 'unknown')
                    
                    description = finding.get('description', {{}})
                    if isinstance(description, dict):
                        description = description.get('text', '')
                    
                    impact = finding.get('impact', {{}})
                    if isinstance(impact, dict):
                        impact = impact.get('text', 'No impact specified')
                    
                    location = finding.get('location', {{}})
                    if isinstance(location, dict):
                        location = location.get('text', '')
                    
                    issues_data += f"\\n**{{finding_type.upper()}} {{category.upper()}}**: {{description}}\\n"
                    issues_data += f"  File: {{item_path}}"
                    if location:
                        issues_data += f" ({{location}})"
                    issues_data += f"\\n  Impact: {{impact}}\\n"
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
        for line in stdout.strip().split('\\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    if data.get('type') == 'assistant':
                        for content in data.get('message', {{}}).get('content', []):
                            if content.get('type') == 'text':
                                content_lines.append(content.get('text', ''))
                except json.JSONDecodeError:
                    pass
        
        synthesis_content = '\\n'.join(content_lines)
        result = type('Result', (), {{'returncode': proc.returncode, 'stdout': synthesis_content, 'stderr': stderr}})()
        
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
    parser.add_argument("command", choices=["populate", "process", "process-all", "synthesize"])
    parser.add_argument("directories", nargs="*", help="Target directories (optional)")
    
    args = parser.parse_args()
    
    processor = {self._to_class_name(project['name'])}()
    
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
chmod +x {project['name']}-framework/process.py
```

### 5. Usage

#### 5.1 Basic Workflow

```bash
# 1. Populate items
python3 {project['name']}-framework/process.py populate

# 2. Process items (choose one)
python3 {project['name']}-framework/process.py process      # Process single item
python3 {project['name']}-framework/process.py process-all  # Process all items

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