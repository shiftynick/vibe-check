#!/usr/bin/env python3
"""
Generic Map-Reduce Framework for AI-Powered Analysis
Configurable system for populate -> map -> reduce workflows
"""

import argparse
import json
import re
import subprocess
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ANSI colors for output
R, G, Y, B, N = "\033[0;31m", "\033[0;32m", "\033[1;33m", "\033[0;34m", "\033[0m"


def status(color, msg):
    """Print colored status message"""
    print(f"{color}{msg}{N}")


@dataclass
class ProcessingResult:
    """Standardized result from any processing engine"""
    success: bool
    output_data: Any
    output_lines: List[str]
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    duration: float = 0.0
    error_message: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None


class ProcessingEngine(ABC):
    """Abstract base class for all processing engines"""

    @abstractmethod
    def check_availability(self) -> bool:
        """Check if processing engine is available"""
        pass

    @abstractmethod
    def process_item(self, prompt: str, log_file: Path) -> ProcessingResult:
        """Process a single item"""
        pass

    @abstractmethod
    def synthesize_results(self, prompt: str, log_file: Path) -> ProcessingResult:
        """Synthesize multiple results"""
        pass


class ClaudeProcessingEngine(ProcessingEngine):
    """Claude CLI implementation of the processing engine"""

    def check_availability(self) -> bool:
        """Check if Claude CLI is available"""
        try:
            subprocess.run(["claude", "--version"], capture_output=True, check=True)
            return True
        except:
            return False

    def process_item(self, prompt: str, log_file: Path) -> ProcessingResult:
        """Process item using Claude CLI"""
        return self._run_claude_command(prompt, log_file, is_synthesis=False)

    def synthesize_results(self, prompt: str, log_file: Path) -> ProcessingResult:
        """Synthesize results using Claude CLI"""
        return self._run_claude_command(prompt, log_file, is_synthesis=True)

    def _run_claude_command(self, prompt: str, log_file: Path, is_synthesis: bool = False) -> ProcessingResult:
        """Run Claude CLI with proper parsing"""
        cmd = [
            "claude",
            "--print",
            prompt,
            "--output-format",
            "stream-json",
            "--permission-mode",
            "acceptEdits",
            "--verbose",
        ]
        start_time = time.time()

        tokens_used = input_tokens = output_tokens = 0
        cost_usd = 0.0
        output_lines = []
        error_message = None
        output_data = None

        try:
            with open(log_file, "w") as log:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
                for line in iter(proc.stdout.readline, ""):
                    log.write(line)
                    try:
                        d = json.loads(line.strip())
                        if d.get("type") == "assistant":
                            for item in d.get("message", {}).get("content", []):
                                if item.get("type") == "text" and (
                                    text := item.get("text", "").strip()
                                ):
                                    output_lines.append(text)
                                    if not is_synthesis:
                                        print(f"{text}\n---")
                        elif d.get("type") == "result":
                            # Final result contains usage and cost information
                            usage = d.get("usage", {})
                            if usage:
                                input_tokens = usage.get("input_tokens", 0) + usage.get(
                                    "cache_read_input_tokens", 0
                                )
                                output_tokens = usage.get("output_tokens", 0)
                                tokens_used = input_tokens + output_tokens
                                cost_usd = d.get("total_cost_usd", 0.0)
                        elif d.get("type") == "assistant" and "usage" in d.get(
                            "message", {}
                        ):
                            # Also check assistant messages for usage data
                            usage = d["message"]["usage"]
                            input_tokens = usage.get("input_tokens", 0) + usage.get(
                                "cache_read_input_tokens", 0
                            )
                            output_tokens = usage.get("output_tokens", 0)
                            tokens_used = input_tokens + output_tokens
                            # Fallback calculation if no total_cost_usd
                            if cost_usd == 0.0:
                                cost_usd = (
                                    input_tokens * 3.0 + output_tokens * 15.0
                                ) / 1_000_000
                    except:
                        pass
                proc.wait()

            duration = time.time() - start_time
            success = proc.returncode == 0

            if not success:
                error_message = f"Claude CLI failed with return code {proc.returncode}"
            else:
                output_data = "\n".join(output_lines)

        except Exception as e:
            duration = time.time() - start_time
            success = False
            error_message = f"Failed to execute Claude CLI: {str(e)}"

        return ProcessingResult(
            success=success,
            output_data=output_data,
            output_lines=output_lines,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=tokens_used,
            cost_usd=cost_usd,
            duration=duration,
            error_message=error_message,
        )


class ConfigLoader:
    """Configuration loader and validator"""

    @staticmethod
    def load_config(config_path: Path) -> Dict[str, Any]:
        """Load configuration from file"""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r') as f:
            if config_path.suffix.lower() == '.json':
                return json.load(f)
            else:
                raise ValueError(f"Unsupported configuration format: {config_path.suffix}")

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration"""
        required_fields = {
            'project': ['name', 'version', 'description'],
            'populate': ['collection_strategy', 'item_filters', 'metadata_extraction'],
            'map': ['processing_template', 'assessment_dimensions'],
            'reduce': ['synthesis_template', 'aggregation_rules']
        }

        for section_name, fields in required_fields.items():
            if section_name not in config:
                raise ValueError(f"Missing required configuration section: {section_name}")
            section = config[section_name]
            for field in fields:
                if field not in section:
                    raise ValueError(f"Missing required {section_name} field: {field}")
        return True


class TemplateEngine:
    """Simple template engine for variable substitution"""

    @staticmethod
    def render_template(template: str, variables: Dict[str, Any]) -> str:
        """Render template with variables"""
        result = template
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            result = result.replace(placeholder, str(value))
        return result

    @staticmethod
    def extract_variables(template: str) -> List[str]:
        """Extract variables from template"""
        return re.findall(r'\{([^}]+)\}', template)


class GenericMapReduce:
    """Main framework class for generic map-reduce processing"""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = ConfigLoader.load_config(config_path)
        ConfigLoader.validate_config(self.config)

        self.framework_dir = Path(f"{self.config['project']['name']}-framework")
        self.data_dir = self.framework_dir / "data"
        self.results_dir = self.framework_dir / "results"
        self.logs_dir = self.framework_dir / "logs"
        engine_type = self.config.get('execution', {}).get('engine', 'claude')
        if engine_type == 'claude':
            self.processing_engine = ClaudeProcessingEngine()
        else:
            raise ValueError(f"Unsupported processing engine: {engine_type}")

    def _load_master_data(self) -> Dict[str, Any]:
        """Load master data"""
        master_file = self.data_dir / "master.json"
        if not master_file.exists():
            return {}

        with open(master_file, 'r') as f:
            if master_file.suffix == '.json':
                return json.load(f)
            else:
                raise ValueError(f"Unsupported master file format: {master_file.suffix}")

    def _save_master_data(self, data: Dict[str, Any]):
        """Save master data"""
        master_file = self.data_dir / "master.json"

        with open(master_file, 'w') as f:
            if master_file.suffix == '.json':
                json.dump(data, f, indent=2)
            else:
                raise ValueError(f"Unsupported master file format: {master_file.suffix}")

    def populate(self, target_directories: Optional[List[str]] = None) -> int:
        """Stage 1: Populate - collect items for processing"""
        for directory in [self.framework_dir, self.data_dir, self.results_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        status(B, "=== Stage 1: Populate ===")

        populate_config = self.config['populate']
        strategy = populate_config['collection_strategy']
        if strategy == 'filesystem':
            items = self._collect_filesystem_items(target_directories)
        elif strategy == 'git':
            items = self._collect_git_items(target_directories)
        else:
            raise ValueError(f"Unsupported collection strategy: {strategy}")

        filtered_items = self._apply_filters(items, populate_config['item_filters'])
        items_with_metadata = self._extract_metadata(filtered_items, populate_config['metadata_extraction'])
        master_data = {
            'metadata': {
                'project': self.config['project'],
                'generated': datetime.utcnow().isoformat() + 'Z',
                'total_items': len(items_with_metadata),
                'collection_strategy': strategy
            },
            'items': {}
        }

        for item in items_with_metadata:
            master_data['items'][item['path']] = item

        self._save_master_data(master_data)

        status(G, f"✓ Populated {len(items_with_metadata)} items")
        return 0

    def _collect_filesystem_items(self, target_directories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Collect items from filesystem"""
        items = []

        search_paths = [Path(d) for d in target_directories] if target_directories else [Path('.')]

        for search_path in search_paths:
            if not search_path.exists():
                status(Y, f"Warning: Directory not found: {search_path}")
                continue

            for item_path in search_path.rglob('*'):
                if item_path.is_file():
                    items.append({
                        'path': str(item_path.relative_to('.')),
                        'absolute_path': str(item_path),
                        'size': item_path.stat().st_size,
                        'modified': datetime.fromtimestamp(item_path.stat().st_mtime).isoformat()
                    })

        return items

    def _collect_git_items(self, target_directories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Collect items from git"""
        items = []

        try:
            if target_directories:
                for directory in target_directories:
                    result = subprocess.run(
                        ['git', 'ls-files', directory],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            item_path = Path(line)
                            if item_path.exists():
                                items.append({
                                    'path': line,
                                    'absolute_path': str(item_path.absolute()),
                                    'size': item_path.stat().st_size,
                                    'modified': datetime.fromtimestamp(item_path.stat().st_mtime).isoformat()
                                })
            else:
                result = subprocess.run(
                    ['git', 'ls-files'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in result.stdout.strip().split('\n'):
                    if line:
                        item_path = Path(line)
                        if item_path.exists():
                            items.append({
                                'path': line,
                                'absolute_path': str(item_path.absolute()),
                                'size': item_path.stat().st_size,
                                'modified': datetime.fromtimestamp(item_path.stat().st_mtime).isoformat()
                            })
        except subprocess.CalledProcessError:
            status(Y, "Git not available, falling back to filesystem strategy")
            return self._collect_filesystem_items(target_directories)

        return items

    def _apply_filters(self, items: List[Dict[str, Any]], filter_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply filters to items"""
        filtered_items = []

        include_patterns = filter_config.get('include_patterns', [])
        exclude_patterns = filter_config.get('exclude_patterns', [])
        exclude_directories = filter_config.get('exclude_directories', [])
        max_size = filter_config.get('max_size_bytes', float('inf'))

        for item in items:
            path = Path(item['path'])

            if any(part in exclude_directories for part in path.parts):
                continue
            if item['size'] > max_size:
                continue
            if include_patterns and not any(path.match(pattern) for pattern in include_patterns):
                continue
            if exclude_patterns and any(path.match(pattern) for pattern in exclude_patterns):
                continue

            filtered_items.append(item)

        return filtered_items

    def _extract_metadata(self, items: List[Dict[str, Any]], metadata_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract metadata from items"""
        extraction_rules = metadata_config.get('extraction_rules', {})
        required_fields = metadata_config.get('required_fields', [])

        items_with_metadata = []

        for item in items:
            # Start with basic item data
            enhanced_item = item.copy()

            # Apply extraction rules
            for field, rule in extraction_rules.items():
                try:
                    if rule == 'file_extension.title()':
                        enhanced_item[field] = Path(item['path']).suffix[1:].title()
                    elif rule == 'count_lines(file_content)':
                        with open(item['path'], 'r', encoding='utf-8', errors='ignore') as f:
                            enhanced_item[field] = sum(1 for _ in f)
                    elif rule.startswith("'") and rule.endswith("'"):
                        enhanced_item[field] = rule[1:-1]  # String literal
                    else:
                        enhanced_item[field] = rule  # Direct value
                except Exception:
                    enhanced_item[field] = None

            # Ensure required fields are present
            for field in required_fields:
                if field not in enhanced_item:
                    enhanced_item[field] = None

            items_with_metadata.append(enhanced_item)

        return items_with_metadata

    def map_process(self) -> int:
        """Stage 2: Map - process individual items"""
        if not self.framework_dir.exists():
            status(R, "Framework not initialized. Run populate first.")
            return 1

        # Check processing engine availability
        if not self.processing_engine.check_availability():
            status(R, "Error: Processing engine not available!")
            return 1

        master_data = self._load_master_data()
        if not master_data:
            status(R, "No master data found. Run populate first.")
            return 1

        # Find next item to process
        items = master_data.get('items', {})
        item_to_process = None
        item_key = None

        for key, item in items.items():
            if item.get('status') in ['not_reviewed', 'in_progress']:
                item_to_process = item
                item_key = key
                break

        if not item_to_process:
            status(G, "All items processed!")
            return 0

        status(B, f"=== Stage 2: Map - Processing {item_key} ===")

        # Mark item as in progress
        master_data['items'][item_key]['status'] = 'in_progress'
        self._save_master_data(master_data)

        # Create output file for this item
        output_file = self._create_output_file(item_to_process)

        # Load global context if available
        global_context = self._load_global_context()

        # Get global context configuration
        global_context_config = self.config['map'].get('global_context', {})

        # Prepare template variables
        template_vars = {
            'item_path': item_to_process['path'],
            'item_data': json.dumps(item_to_process, indent=2),
            'output_file': str(output_file),
            'global_context': global_context,
            'context_file': global_context_config.get('context_file', ''),
            'assessment_instructions': self._build_assessment_instructions(),
            'output_requirements': self._build_output_requirements()
        }

        # Render processing template
        processing_template = self.config['map']['processing_template']
        prompt = TemplateEngine.render_template(processing_template, template_vars)

        # Append instructions to update the global context
        prompt += f"\n\n## Global Context Update Instructions\nAfter you have completed your review, update the global context file with your findings. {global_context_config.get('context_update_rules', '')}"

        # Run processing
        self.logs_dir.mkdir(exist_ok=True)
        log_file = self.logs_dir / f"map_{datetime.now():%Y%m%d_%H%M%S}.log"

        result = self.processing_engine.process_item(prompt, log_file)

        if result.success:
            # Mark item as completed
            master_data = self._load_master_data()
            master_data['items'][item_key]['status'] = 'completed'
            master_data['items'][item_key]['processed_at'] = datetime.utcnow().isoformat() + 'Z'
            self._save_master_data(master_data)

            # Display summary
            status(G, "✓ Processing completed!")
            print(f"{B}=== Processing Summary ==={N}")
            print(f"Item: {Y}{item_key}{N}")
            print(f"Duration: {Y}{result.duration:.1f}s{N}")
            if result.total_tokens > 0:
                print(f"Tokens: {Y}{result.input_tokens:,}{N} in + {Y}{result.output_tokens:,}{N} out = {Y}{result.total_tokens:,}{N} total")
                print(f"Cost: {Y}${result.cost_usd:.4f}{N}")

            # Show progress
            remaining = sum(1 for item in master_data['items'].values() if item.get('status') in ['not_reviewed', 'in_progress'])
            completed = sum(1 for item in master_data['items'].values() if item.get('status') == 'completed')
            total = len(master_data['items'])
            print(f"Progress: {Y}{completed}/{total}{N} items ({Y}{remaining}{N} remaining)")

            return 0
        else:
            status(R, f"✗ Processing failed! {result.error_message or 'Unknown error'}")
            status(R, f"Check log: {log_file}")
            return 1

    def map_process_all(self, delay: int = 5) -> int:
        """Process all remaining items"""
        if not self.framework_dir.exists():
            return 1

        processed = 0
        while True:
            master_data = self._load_master_data()
            if not master_data:
                break

            remaining = sum(1 for item in master_data['items'].values() if item.get('status') in ['not_reviewed', 'in_progress'])
            if remaining == 0:
                break

            status(Y, f"Remaining: {remaining}, Starting #{processed + 1}")
            if self.map_process() == 0:
                processed += 11
                if remaining > 1:
                    time.sleep(delay)
            else:
                status(R, "Failed! Stopping.")
                return 1

        status(G, f"✓ Processed {processed} items")
        return 0

    def _create_output_file(self, item: Dict[str, Any]) -> Path:
        """Create output file for processed item"""
        # Create output directory structure that mirrors the source
        item_path = Path(item['path'])
        output_dir = self.results_dir / item_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create output file - always xml for map stage
        output_file = output_dir / f"{item_path.stem}.xml"

        # Initialize output file with XML structure (always use XML for map stage)
        initial_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<analysis>
  <metadata>
    <source_file>{item['path']}</source_file>
    <language>{item.get('language', 'Unknown')}</language>
    <loc>{item.get('loc', 0)}</loc>
    <processed_at>{datetime.utcnow().isoformat() + 'Z'}</processed_at>
    <processor>AI-Assistant</processor>
    <status>in_progress</status>
  </metadata>
  <scores>
    <!-- Scores will be added here -->
  </scores>
  <findings>
    <!-- Findings will be added here -->
  </findings>
  <summary></summary>
  <recommendations>
    <!-- Recommendations will be added here -->
  </recommendations>
</analysis>"""
        with open(output_file, 'w') as f:
            f.write(initial_content)

        return output_file

    def _load_global_context(self) -> str:
        """Load global context for processing"""
        map_config = self.config['map']
        global_context_config = map_config.get('global_context', {})
        context_file = global_context_config.get('context_file')

        if context_file:
            context_path = self.framework_dir / context_file
            # Create the context file and its directory if they don't exist
            context_path.parent.mkdir(parents=True, exist_ok=True)
            if not context_path.exists():
                self._initialize_global_context(context_path)

            with open(context_path, 'r') as f:
                return f.read()

        return "No global context available."

    def _initialize_global_context(self, context_path: Path):
        """Initialize the scratchsheet with configurable structure"""
        project_name = self.config['project']['name']
        global_context_config = self.config['map'].get('global_context', {})

        template = global_context_config.get('template',
            "# {project_name} - Project Context & Patterns\n\n## Project Overview\nThis scratchsheet tracks project-wide patterns, conventions, and insights discovered during code review.\n\n{sections}\n\n---\n*This scratchsheet is automatically updated during the review process*").replace('\\n', '\n')

        sections_content = ""
        for section in global_context_config.get('sections', []):
            sections_content += f"### {section['name']}\n"
            if section.get('description'):
                sections_content += f"*{section['description']}*\n\n"
            sections_content += f"- {section.get('placeholder', 'TBD')}\n\n"

        initial_content = template.format(
            project_name=project_name.title(),
            sections=sections_content.strip()
        )

        with open(context_path, 'w') as f:
            f.write(initial_content)

    def _build_assessment_instructions(self) -> str:
        """Build assessment instructions from configuration"""
        map_config = self.config['map']
        dimensions = map_config.get('assessment_dimensions', [])

        instructions = []
        for dimension in dimensions:
            name = dimension['name']
            description = dimension['description']
            scoring = dimension.get('scoring_rubric', {})
            specific_instructions = dimension.get('specific_instructions', '')

            instruction = f"""
For **{name.title()}** ({description}):
{specific_instructions}

Scoring rubric:
{json.dumps(scoring, indent=2)}
"""
            instructions.append(instruction)

        return "\n".join(instructions)

    def _build_output_requirements(self) -> str:
        """Build output requirements from configuration"""
        map_config = self.config['map']
        output_schema = map_config.get('output_schema', {})

        requirements = f"""
Output Format: xml
Required Structure: {json.dumps(output_schema, indent=2)}

Please ensure your output follows this structure exactly.
"""
        return requirements

    def status(self) -> int:
        """Show processing status"""
        if not self.framework_dir.exists():
            status(R, "Framework not initialized. Run populate first.")
            return 1

        master_data = self._load_master_data()
        if not master_data:
            status(R, "No master data found. Run populate first.")
            return 1

        items = master_data.get('items', {})
        total = len(items)

        if total == 0:
            status(Y, "No items to process.")
            return 0

        # Count by status
        status_counts = {}
        for item in items.values():
            item_status = item.get('status', 'unknown')
            status_counts[item_status] = status_counts.get(item_status, 0) + 1

        status(B, "=== Processing Status ===")
        print(f"Total items: {Y}{total}{N}")

        for item_status, count in sorted(status_counts.items()):
            color = G if item_status == 'completed' else Y if item_status == 'in_progress' else R
            print(f"{item_status:15} {color}{count:4d}{N} ({count/total*100:5.1f}%)")

        if total > 0:
            completed = status_counts.get('completed', 0)
            pct = completed / total
            bar = "█" * int(20 * pct) + "░" * int(20 * (1 - pct))
            print(f"Progress: [{G}{bar}{N}] {pct*100:.1f}%")

        return 0

    def reduce_synthesize(self, severity: str = "medium", category: str = "all") -> int:
        """Stage 3: Reduce - synthesize results into actionable insights"""
        if not self.framework_dir.exists():
            status(R, "Framework not initialized. Run populate first.")
            return 1

        # Check processing engine availability
        if not self.processing_engine.check_availability():
            status(R, "Error: Processing engine not available!")
            return 1

        # Collect all results
        results = self._collect_results()
        if not results:
            status(Y, "No results found to synthesize")
            return 0

        # Filter results based on parameters
        filtered_results = self._filter_results(results, severity, category)
        if not filtered_results:
            status(Y, f"No {severity} {category} results found")
            return 0

        status(B, f"=== Stage 3: Reduce - Synthesizing {len(filtered_results)} results ===")

        # Create synthesis directory
        synthesis_dir = self.framework_dir / "synthesis"
        synthesis_dir.mkdir(exist_ok=True)

        # Prepare synthesis data
        synthesis_data = self._prepare_synthesis_data(filtered_results, severity, category)

        # Render synthesis template
        reduce_config = self.config['reduce']
        synthesis_template = reduce_config['synthesis_template']
        prompt = TemplateEngine.render_template(synthesis_template, synthesis_data)

        # Run synthesis
        self.logs_dir.mkdir(exist_ok=True)
        log_file = self.logs_dir / f"reduce_{datetime.now():%Y%m%d_%H%M%S}.log"

        result = self.processing_engine.synthesize_results(prompt, log_file)

        if result.success:
            # Save synthesis result
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            synthesis_file = synthesis_dir / f"synthesis_{severity}_{category}_{timestamp}.md"

            with open(synthesis_file, 'w') as f:
                f.write(f"# Synthesis Report ({severity.title()} {category.title()})\n\n")
                f.write(f"Generated: {datetime.now()}\n\n")
                f.write(result.output_data)

            status(G, f"✓ Synthesis complete: {synthesis_file}")
            print(f"{B}=== Synthesis Summary ==={N}")
            print(f"Results processed: {Y}{len(filtered_results)}{N}")
            print(f"Duration: {Y}{result.duration:.1f}s{N}")
            if result.total_tokens > 0:
                print(f"Tokens: {Y}{result.input_tokens:,}{N} in + {Y}{result.output_tokens:,}{N} out = {Y}{result.total_tokens:,}{N} total")
                print(f"Cost: {Y}${result.cost_usd:.4f}{N}")

            return 0
        else:
            status(R, f"✗ Synthesis failed! {result.error_message or 'Unknown error'}")
            status(R, f"Check log: {log_file}")
            return 1

    def _collect_results(self) -> List[Dict[str, Any]]:
        """Collect all processing results"""
        results = []

        # Traverse results directory
        for result_file in self.results_dir.rglob('*'):
            if result_file.is_file():
                try:
                    if result_file.suffix == '.xml':
                        # Parse XML results (only XML files supported)
                        import xml.etree.ElementTree as ET
                        tree = ET.parse(result_file)
                        root = tree.getroot()

                        # Extract key data from XML
                        xml_data = {
                            'metadata': {
                                'source_file': result_file.stem,
                                'format': 'xml'
                            },
                            'scores': {},
                            'findings': []
                        }

                        # Extract scores
                        for score_elem in root.findall('.//scores/*'):
                            if score_elem.text:
                                xml_data['scores'][score_elem.tag] = int(score_elem.text)

                        # Extract issues/findings
                        for issue_elem in root.findall('.//issues/issue'):
                            issue = {}
                            for child in issue_elem:
                                issue[child.tag] = child.text
                            xml_data['findings'].append(issue)

                        results.append(xml_data)
                except Exception as e:
                    status(Y, f"Warning: Could not parse {result_file}: {e}")

        return results

    def _filter_results(self, results: List[Dict[str, Any]], severity: str, category: str) -> List[Dict[str, Any]]:
        """Filter results based on severity and category"""
        filtered = []

        severity_map = {
            'high': ['high', 'critical'],
            'medium': ['high', 'critical', 'medium'],
            'low': ['high', 'critical', 'medium', 'low']
        }

        allowed_severities = severity_map.get(severity, ['high', 'critical', 'medium', 'low'])

        for result in results:
            findings = result.get('findings', [])

            if category != 'all' and not any(f.get('category', '').lower() == category.lower() for f in findings):
                continue

            if findings:
                if any(f.get('severity', '').lower() in allowed_severities for f in findings):
                    filtered.append(result)
            else:
                filtered.append(result)

        return filtered

    def _prepare_synthesis_data(self, results: List[Dict[str, Any]], severity: str, category: str) -> Dict[str, Any]:
        """Prepare data for synthesis template"""

        all_findings = []
        for result in results:
            findings = result.get('findings', [])
            for finding in findings:
                finding['file'] = result.get('metadata', {}).get('source_file', 'unknown')
                all_findings.append(finding)

        # Format findings text
        findings_text = ""
        for finding in all_findings:
            findings_text += f"\n**{finding.get('severity', 'unknown').upper()} {finding.get('category', 'unknown')}**: {finding.get('description', 'No description')}"
            findings_text += f"\n  File: {finding.get('file', 'unknown')}"
            if finding.get('line'):
                findings_text += f":{finding.get('line', '')}"
            findings_text += f"\n  Recommendation: {finding.get('recommendation', 'No recommendation')}\n"

        template_vars = {
            'issue_count': len(all_findings),
            'file_count': len(results),
            'severity': severity,
            'category': category,
            'issues_data': findings_text,
            'results_data': json.dumps(results, indent=2)
        }

        output_sections = self.config['reduce'].get('output_sections', [])
        if output_sections:
            template_vars['output_sections'] = "\n".join(f"\n{section['template']}\n" for section in output_sections)

        return template_vars


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generic Map-Reduce Framework for AI-Powered Analysis"
    )
    parser.add_argument(
        "config",
        help="Path to configuration file"
    )

    sub = parser.add_subparsers(dest="command", help="Commands")

    # Populate command
    populate_parser = sub.add_parser("populate", help="Collect items for processing")
    populate_parser.add_argument("directories", nargs="*", help="Specific directories to process (optional)")

    # Status command
    sub.add_parser("status", help="Show processing status")

    # Process command
    sub.add_parser("map-next", help="Process next item")
    process_all_parser = sub.add_parser("map-all", help="Process all items")
    process_all_parser.add_argument("--delay", type=int, default=5, help="Delay between items (seconds)")

    # Reduce command
    reduce_parser = sub.add_parser("reduce", help="Synthesize results")
    reduce_parser.add_argument("--severity", choices=["high", "medium", "low"], default="medium", help="Severity level to include")
    reduce_parser.add_argument("--category", default="all", help="Category to filter by (or 'all' for all categories)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        framework = GenericMapReduce(Path(args.config))

        if args.command == "populate":
            return framework.populate(args.directories)
        elif args.command == "status":
            return framework.status()
        elif args.command == "map-next":
            return framework.map_process()
        elif args.command == "map-all":
            return framework.map_process_all(args.delay)
        elif args.command == "reduce":
            return framework.reduce_synthesize(args.severity, args.category)
        else:
            parser.print_help()
            return 1

    except Exception as e:
        status(R, f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
