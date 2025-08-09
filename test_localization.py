#!/usr/bin/env python3
"""
Test suite for CTMM Localization System
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add localization module to path
sys.path.insert(0, str(Path(__file__).parent / "localization"))

from localize import LocalizationManager


class TestCTMMLocalization(unittest.TestCase):
    """Test cases for CTMM localization system."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(__file__).parent
        os.chdir(self.test_dir)
        self.loc_manager = LocalizationManager("localization")
    
    def test_load_constants(self):
        """Test loading localization constants."""
        self.assertIsInstance(self.loc_manager.constants, dict)
        self.assertIn("tasks", self.loc_manager.constants)
        self.assertIn("compile", self.loc_manager.constants["tasks"])
    
    def test_get_text_german(self):
        """Test getting German text (default)."""
        text = self.loc_manager.get_text("tasks.compile")
        self.assertEqual(text, "CTMM: Kompilieren")
    
    def test_get_text_english(self):
        """Test getting English text."""
        text = self.loc_manager.get_text("tasks.compile", "en")
        self.assertEqual(text, "CTMM: Compile")
    
    def test_get_text_missing_key(self):
        """Test behavior with missing key."""
        text = self.loc_manager.get_text("nonexistent.key")
        self.assertEqual(text, "[MISSING: nonexistent.key]")
    
    def test_template_processing(self):
        """Test template processing functionality."""
        # Create a temporary template
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            template_content = {
                "label": "{{tasks.compile}}",
                "description": "{{charts.title}}"
            }
            json.dump(template_content, f, indent=2)
            template_path = f.name
        
        try:
            # Process template
            output_path = template_path.replace('.json', '_output.json')
            success = self.loc_manager.process_template(template_path, output_path, "de")
            self.assertTrue(success)
            
            # Check output
            with open(output_path, 'r', encoding='utf-8') as f:
                result = json.load(f)
            
            self.assertEqual(result["label"], "CTMM: Kompilieren")
            self.assertEqual(result["description"], "Diagramm-Titel")
            
        finally:
            # Clean up
            for path in [template_path, output_path]:
                if os.path.exists(path):
                    os.unlink(path)
    
    def test_chart_title_localization(self):
        """Test the specific chart title mentioned in the issue."""
        # Test German (default)
        de_title = self.loc_manager.get_text("charts.title")
        self.assertEqual(de_title, "Diagramm-Titel")
        
        # Test English
        en_title = self.loc_manager.get_text("charts.title", "en")
        self.assertEqual(en_title, "Chart Title")
        
        # Verify this could be used as suggested: title: { display: true, text: LOCALIZED.chartTitle }
        chart_config = {
            "title": {
                "display": True,
                "text": self.loc_manager.get_text("charts.title", "en")
            }
        }
        
        self.assertEqual(chart_config["title"]["text"], "Chart Title")
        self.assertTrue(chart_config["title"]["display"])


def test_hardcoded_text_externalized():
    """Test that hardcoded German text has been properly externalized."""
    # Test that the tasks.json now references the localization system
    tasks_json_path = Path(__file__).parent / ".vscode" / "tasks.json"
    
    if tasks_json_path.exists():
        with open(tasks_json_path, 'r', encoding='utf-8') as f:
            tasks_data = json.load(f)
        
        # Check that localization metadata exists
        assert "_localization" in tasks_data, "tasks.json should contain localization metadata"
        assert "_label_key" in tasks_data["tasks"][0], "Task should reference localization key"
        
        print("✓ Hardcoded text has been externalized to localization system")
    else:
        print("⚠ tasks.json not found, skipping externalization test")


if __name__ == "__main__":
    # Run the specific test for externalization
    test_hardcoded_text_externalized()
    
    # Run unittest suite
    unittest.main(verbosity=2)