#!/usr/bin/env python3
"""
File System Creator for Generic Map-Reduce Framework
Creates the actual file system structure from a configuration JSON
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


class FileSystemCreator:
    """Creates file system structure from configuration"""

    def __init__(self, config_path: Path, output_dir: Path):
        self.config_path = config_path
        self.output_dir = output_dir

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.project = self.config['project']
        self.project_name = self.project['name']
        self.framework_dir = self.output_dir / f"{self.project_name}-framework"

    def create_directory_structure(self):
        """Create the directory hierarchy"""
        print(f"Creating directory structure in {self.framework_dir}")

        # Create main directories
        directories = [
            self.framework_dir / "data",
            self.framework_dir / "results",
            self.framework_dir / "synthesis",
            self.framework_dir / "logs",
            self.framework_dir / "prompts"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created {directory.relative_to(self.output_dir)}")

    def create_config_files(self):
        """Create configuration files"""
        print("\nCreating configuration files...")

        # Create config.json
        config_file = self.framework_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print("  ✓ Created config.json")

        # Create data/master.json
        master_file = self.framework_dir / "data" / "master.json"
        master_data = {
            "metadata": {
                "project": self.project,
                "generated": datetime.now().isoformat(),
                "total_items": 0,
                "collection_strategy": self.config['populate']['collection_strategy']
            },
            "items": {}
        }
        with open(master_file, 'w') as f:
            json.dump(master_data, f, indent=2)
        print("  ✓ Created data/master.json")

        # Create global_context.md if configured
        if 'map' in self.config and 'global_context' in self.config['map']:
            context_config = self.config['map']['global_context']
            # Handle context_file path - it might be relative to framework_dir
            context_file_path = context_config.get('context_file', 'data/global_context.md')
            if not context_file_path.startswith('/'):
                context_file = self.framework_dir / context_file_path
            else:
                context_file = Path(context_file_path)

            # Ensure parent directory exists
            context_file.parent.mkdir(parents=True, exist_ok=True)

            # Generate initial content from template
            template = context_config.get('template', '# {project_name} - Project Context & Patterns\n\n{sections}')
            sections_content = []

            for section in context_config.get('sections', []):
                section_content = f"## {section['name']}\n\n"
                section_content += f"{section['description']}\n\n"
                section_content += f"{section.get('placeholder', 'TBD')}\n"
                sections_content.append(section_content)

            content = template.replace('{project_name}', self.project_name)
            content = content.replace('{sections}', '\n'.join(sections_content))

            with open(context_file, 'w') as f:
                f.write(content)
            print(f"  ✓ Created {context_file.relative_to(self.framework_dir)}")

    def create_prompt_files(self):
        """Create prompt instruction files"""
        print("\nCreating prompt files...")

        # Create PROCESSING_INSTRUCTIONS.md
        processing_file = self.framework_dir / "prompts" / "PROCESSING_INSTRUCTIONS.md"
        processing_content = self._generate_processing_instructions()
        with open(processing_file, 'w') as f:
            f.write(processing_content)
        print("  ✓ Created prompts/PROCESSING_INSTRUCTIONS.md")

        # Create SYNTHESIS_INSTRUCTIONS.md
        synthesis_file = self.framework_dir / "prompts" / "SYNTHESIS_INSTRUCTIONS.md"
        synthesis_content = self._generate_synthesis_instructions()
        with open(synthesis_file, 'w') as f:
            f.write(synthesis_content)
        print("  ✓ Created prompts/SYNTHESIS_INSTRUCTIONS.md")

    def _load_template(self, template_name):
        """Load a template file from the templates directory"""
        template_path = Path(__file__).parent / "templates" / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        with open(template_path, 'r') as f:
            return f.read()

    def _generate_processing_instructions(self):
        """Generate processing instructions content"""
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
        content = template.replace("{project_name}", self.project_name)
        content = content.replace("{project_description}", self.project['description'])
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
        """Generate synthesis instructions content"""
        reduce_config = self.config['reduce']

        # Load the template
        template = self._load_template("synthesis_instructions.md.template")

        # Generate synthesis sections
        synthesis_sections = self._generate_synthesis_sections(reduce_config.get('output_sections', []))

        # Replace placeholders in template
        content = template.replace("{project_name}", self.project_name)
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

    def create_processing_script(self):
        """Create the process.py script with embedded framework code"""
        print("\nCreating processing script...")

        # Load the generic-mapreduce.py framework
        framework_path = Path(__file__).parent / "generic-mapreduce.py"
        if not framework_path.exists():
            raise FileNotFoundError(f"Framework file not found: {framework_path}")

        with open(framework_path, 'r') as f:
            framework_code = f.read()

        # Process the framework code
        processed_code = self._process_framework_code(framework_code)

        # Write the process.py file
        process_file = self.framework_dir / "process.py"
        with open(process_file, 'w') as f:
            f.write(processed_code)

        # Make it executable
        os.chmod(process_file, 0o755)
        print("  ✓ Created process.py (executable)")

    def _process_framework_code(self, framework_code):
        """Process framework code to embed configuration"""
        import re

        # Replace the main class name
        class_name = self._to_class_name(self.project_name)
        framework_code = framework_code.replace(
            'class GenericMapReduce:',
            f'class {class_name}:'
        )

        # Replace the main() function description
        framework_code = framework_code.replace(
            'description="Generic Map-Reduce Framework for AI-Powered Analysis"',
            f'description="{self.project["description"]}"'
        )

        # Replace the class name in the main() function
        framework_code = framework_code.replace(
            'framework = GenericMapReduce(Path(args.config))',
            f'framework = {class_name}()'
        )

        # Remove config_path argument
        framework_code = framework_code.replace(
            'parser.add_argument(\n        "config",\n        help="Path to configuration file"\n    )',
            ''
        )
        framework_code = framework_code.replace(
            'config_path = Path(args.config)',
            '# Configuration is loaded from config.json in the framework directory'
        )

        # Create __init__ method that loads config from file
        embedded_init = f'''def __init__(self):
        # Load configuration from file system
        self.framework_dir = Path("{self.project_name}-framework")
        config_path = self.framework_dir / "config.json"

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {{config_path}}")

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.data_dir = self.framework_dir / "data"
        self.results_dir = self.framework_dir / "results"
        self.synthesis_dir = self.framework_dir / "synthesis"
        self.logs_dir = self.framework_dir / "logs"

        # Initialize processing engine
        self.processing_engine = ClaudeProcessingEngine()

    '''

        # Replace the original __init__ method
        init_pattern = r'def __init__\(self, config_path: Path\):.*?(?=def [^\s]|\nclass |\n$)'
        framework_code = re.sub(init_pattern, embedded_init, framework_code, flags=re.DOTALL)

        return framework_code

    def _to_class_name(self, project_name):
        """Convert project name to class name"""
        return ''.join(word.capitalize() for word in project_name.replace('-', '_').split('_'))

    def create_file_system(self):
        """Create the complete file system"""
        print(f"\n🚀 Creating {self.project_name} file system...\n")

        self.create_directory_structure()
        self.create_config_files()
        self.create_prompt_files()
        self.create_processing_script()

        print(f"\n✅ Successfully created {self.project_name}-framework in {self.output_dir}")
        print("\nNext steps:")
        print("  1. cd to your codebase")
        print("  2. python3 process.py populate")
        print("  3. python3 process.py map-all")
        print("  4. python3 process.py reduce")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Create file system structure from Generic Map-Reduce configuration"
    )
    parser.add_argument(
        "config",
        help="Path to configuration JSON file"
    )
    parser.add_argument(
        "output_dir",
        help="Output directory where the file system will be created"
    )

    args = parser.parse_args()

    try:
        config_path = Path(args.config)
        output_dir = Path(args.output_dir)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        creator = FileSystemCreator(config_path, output_dir)
        creator.create_file_system()

        return 0

    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
