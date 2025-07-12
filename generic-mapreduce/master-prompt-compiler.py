#!/usr/bin/env python3
"""
Master Prompt Compiler for Generic Map-Reduce Framework
Generates single-file setup instructions like the original VIBE_CHECK_SETUP.md
"""

import argparse
import json
import sys
from pathlib import Path


class MasterPromptCompiler:
    """Compiles configuration into single-file setup instructions"""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def _load_template(self, template_name):
        """Load a template file from the templates directory"""
        template_path = Path(__file__).parent / "templates" / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        with open(template_path, 'r') as f:
            return f.read()

    def compile_setup_instructions(self) -> str:
        """Generate complete setup instructions as a single markdown file"""

        project = self.config['project']
        populate = self.config['populate']
        map_config = self.config['map']
        reduce_config = self.config['reduce']

        config_for_output = self.config.copy()

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
{self._generate_processing_instructions()}
```

#### 2.4 Create `{project['name']}-framework/prompts/SYNTHESIS_INSTRUCTIONS.md`

Create this file with the following content:

```markdown
{self._generate_synthesis_instructions()}
```

### 3. Create Processing Script

#### 3.1 Create `{project['name']}-framework/process.py`

Create this streamlined executable script:

```python
{self._load_and_process_framework_code(project)}
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
python3 {project['name']}-framework/process.py map-next # Map next item
python3 {project['name']}-framework/process.py map-all  # Map all items

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

    def _generate_processing_instructions(self):
        """Generate processing instructions using template"""
        project = self.config['project']
        map_config = self.config['map']

        # Load the template
        template = self._load_template("processing_instructions.md.template")

        # Generate dynamic content
        assessment_dimensions = self._generate_assessment_instructions(map_config['assessment_dimensions'])
        dimension_assessments = self._generate_dimension_assessments(map_config['assessment_dimensions'])

        # Generate global context section if configured
        global_context_section = ""
        if 'map' in self.config and 'global_context' in self.config['map']:
            global_context_section = f"""
### Step 5: Update Global Context

After completing your analysis, review your findings and determine if any project-wide patterns should be added to the global context.

**Context Update Rules**: {self.config['map']['global_context'].get('context_update_rules', 'Add newly discovered project-wide patterns')}

**Current Global Context**:
{{{{global_context}}}}

**Task**: If your analysis reveals patterns that:
1. Apply to multiple files (3+)
2. Are not language defaults
3. Would help future reviews

Then update the global context file by appending new insights to the appropriate sections.

**Action**: If you identify new patterns, append them to `{{{{context_file}}}}` with:
- A timestamp header: `## Update from [ITEM_PATH] review (YYYY-MM-DD HH:MM)`
- Specific patterns under relevant sections
- Brief description of why this pattern is significant

Focus on discovering:
- Architecture patterns you observed
- Code conventions that should be followed
- Common issues that appear across files
- Security considerations specific to this project
- Performance patterns and optimizations
- Maintainability standards

Only add patterns that would genuinely help future reviews. Skip obvious language defaults or one-off issues.
"""

        # Replace placeholders in template
        content = template.replace("{project_name}", project['name'])
        content = content.replace("{project_description}", project['description'])
        content = content.replace("{assessment_dimensions}", assessment_dimensions)
        content = content.replace("{dimension_assessments}", dimension_assessments)
        content = content.replace("{global_context_section}", global_context_section)

        return content

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

    def _generate_synthesis_instructions(self):
        """Generate synthesis instructions using template"""
        project = self.config['project']
        reduce_config = self.config['reduce']

        # Load the template
        template = self._load_template("synthesis_instructions.md.template")

        # Generate synthesis sections
        synthesis_sections = self._generate_synthesis_sections(reduce_config.get('output_sections', []))

        # Replace placeholders in template
        content = template.replace("{project_name}", project['name'])
        content = content.replace("{synthesis_sections}", synthesis_sections)

        return content

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

    def _load_and_process_framework_code(self, project):
        """Load generic-mapreduce.py and process it as a template"""
        # Read the actual framework file
        # The framework file is in the same directory as this compiler
        framework_path = Path(__file__).parent / "generic-mapreduce.py"
        with open(framework_path, 'r') as f:
            framework_code = f.read()

        # Replace the main class name with project-specific class name
        class_name = self._to_class_name(project['name'])
        framework_code = framework_code.replace(
            'class GenericMapReduce:',
            f'class {class_name}:'
        )

        # Replace the main() function argument parsing with project-specific description
        framework_code = framework_code.replace(
            'description="Generic Map-Reduce Framework for AI-Powered Analysis"',
            f'description="{project["description"]}"'
        )

        # Replace the complex subparser structure with simple argument parsing
        # Find the start of subparser setup and replace with simple choice-based args
        subparser_start = 'sub = parser.add_subparsers(dest="command", help="Commands")'
        if subparser_start in framework_code:
            # Find the entire subparser section
            lines = framework_code.split('\n')
            start_idx = None
            end_idx = None

            for i, line in enumerate(lines):
                if subparser_start in line:
                    start_idx = i
                # Look for the end of subparser definitions (next significant code block)
                elif start_idx is not None and ('if args.command' in line or 'framework = GenericMapReduce' in line):
                    end_idx = i
                    break

            if start_idx is not None and end_idx is not None:
                # Replace subparser section with simple argument parsing
                new_args = [
                    '    parser.add_argument("command", choices=["populate", "map-next", "map-all", "reduce"])',
                    '    parser.add_argument("directories", nargs="*", help="Target directories (optional)")',
                    ''
                ]
                lines[start_idx:end_idx] = new_args
                framework_code = '\n'.join(lines)

        # Replace the command handling section to use simpler method names
        old_patterns = [
            ('framework.populate(args.directories)', 'processor.populate(args.directories)'),
            ('framework.map_process()', 'processor.process()'),
            ('framework.map_process_all()', 'processor.process_all()'),
            ('framework.reduce()', 'processor.synthesize()'),
            ('return framework.populate', 'return processor.populate'),
            ('return framework.map_process()', 'return processor.process()'),
            ('return framework.map_process_all()', 'return processor.process_all()'),
            ('return framework.reduce()', 'return processor.synthesize()'),
        ]

        for old, new in old_patterns:
            framework_code = framework_code.replace(old, new)

        # Remove the config_path argument and related code
        framework_code = framework_code.replace(
            'parser.add_argument(\n        "config",\n        help="Path to configuration file"\n    )',
            ''
        )

        # Replace config loading with embedded config
        framework_code = framework_code.replace(
            'config_path = Path(args.config)',
            '# Configuration is embedded in the setup'
        )
        framework_code = framework_code.replace(
            'framework = GenericMapReduce(config_path)',
            f'processor = {class_name}()'
        )

        # Add the embedded configuration at the beginning of the main class
        # Find the class definition and add __init__ with embedded config
        config_json = json.dumps(self.config, indent=8)
        embedded_init = f'''    def __init__(self):
        # Embedded configuration
        self.config = {config_json}

        self.framework_dir = Path("{project['name']}-framework")
        self.data_dir = self.framework_dir / "data"
        self.results_dir = self.framework_dir / "results"
        self.synthesis_dir = self.framework_dir / "synthesis"
        self.logs_dir = self.framework_dir / "logs"

        # Initialize processing engine
        self.processing_engine = ClaudeProcessingEngine()'''

        # Replace the original __init__ method
        import re
        init_pattern = r'def __init__\(self, config_path: Path\):.*?(?=def [^\s]|\nclass |\n$)'
        framework_code = re.sub(init_pattern, embedded_init, framework_code, flags=re.DOTALL)

        return framework_code


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
