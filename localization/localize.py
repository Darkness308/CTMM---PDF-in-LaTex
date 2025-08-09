#!/usr/bin/env python3
"""
CTMM Localization Utility
Simple localization system for CTMM configuration files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class LocalizationManager:
    """Manages localization for CTMM project."""
    
    def __init__(self, localization_dir: str = "localization"):
        self.localization_dir = Path(localization_dir)
        self.config = self._load_config()
        self.constants = self._load_constants()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load localization configuration."""
        config_path = self.localization_dir / "config.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "defaultLanguage": "de",
                "supportedLanguages": ["de", "en"],
                "fallbackLanguage": "en"
            }
    
    def _load_constants(self) -> Dict[str, Any]:
        """Load localization constants."""
        constants_path = self.localization_dir / "constants.json"
        try:
            with open(constants_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def get_text(self, key_path: str, language: Optional[str] = None) -> str:
        """Get localized text by key path (e.g., 'tasks.compile')."""
        if language is None:
            language = self.config.get("defaultLanguage", "de")
        
        # Navigate through the nested dictionary
        current = self.constants
        for key in key_path.split('.'):
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                # Key not found, return the key itself as fallback
                return f"[MISSING: {key_path}]"
        
        # Get the localized text
        if isinstance(current, dict) and language in current:
            return current[language]
        elif isinstance(current, dict) and self.config.get("fallbackLanguage") in current:
            return current[self.config.get("fallbackLanguage")]
        else:
            return f"[MISSING: {key_path}]"
    
    def process_template(self, template_path: str, output_path: str, language: Optional[str] = None) -> bool:
        """Process a template file and replace {{key.path}} with localized strings."""
        template_file = Path(template_path)
        output_file = Path(output_path)
        
        if not template_file.exists():
            print(f"Warning: Template file {template_path} not found")
            return False
        
        if language is None:
            language = self.config.get("defaultLanguage", "de")
        
        try:
            # Read template
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace all {{key.path}} patterns
            import re
            pattern = r'\{\{([^}]+)\}\}'
            
            def replace_token(match):
                key_path = match.group(1)
                return self.get_text(key_path, language)
            
            processed_content = re.sub(pattern, replace_token, content)
            
            # Write output
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            print(f"Successfully processed template {template_path} -> {output_path}")
            return True
            
        except Exception as e:
            print(f"Error processing template {template_path}: {e}")
            return False
        """Update VS Code tasks.json to use localized strings."""
        tasks_path = Path(tasks_json_path)
        
        if not tasks_path.exists():
            print(f"Warning: {tasks_json_path} not found")
            return False
        
        try:
            # Load current tasks.json
            with open(tasks_path, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            # Update the label to use localized text
            for task in tasks_data.get("tasks", []):
                if task.get("label") == "CTMM: Kompilieren":
                    task["label"] = self.get_text("tasks.compile")
                    print(f"Updated task label to: {task['label']}")
            
            # Write back the updated tasks.json
            with open(tasks_path, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=4, ensure_ascii=False)
            
            print(f"Successfully updated {tasks_json_path}")
            return True
            
        except Exception as e:
            print(f"Error updating {tasks_json_path}: {e}")
            return False


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='CTMM Localization Utility')
    parser.add_argument('--process-template', nargs=2, metavar=('TEMPLATE', 'OUTPUT'),
                       help='Process template file with localized strings')
    parser.add_argument('--update-tasks', action='store_true',
                       help='Update VS Code tasks.json with localized strings')
    parser.add_argument('--language', default='de',
                       help='Language code (default: de)')
    parser.add_argument('--get-text', 
                       help='Get localized text for key path (e.g., tasks.compile)')
    
    args = parser.parse_args()
    
    # Determine the project root directory (parent of localization directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    loc_manager = LocalizationManager()
    
    if args.process_template:
        template_path, output_path = args.process_template
        loc_manager.process_template(template_path, output_path, args.language)
    
    if args.update_tasks:
        loc_manager.update_tasks_json()
    
    if args.get_text:
        text = loc_manager.get_text(args.get_text, args.language)
        print(text)


if __name__ == "__main__":
    main()