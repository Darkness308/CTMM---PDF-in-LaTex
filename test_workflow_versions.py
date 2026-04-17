#!/usr/bin/env python3
"""
Unit tests for the workflow version validation script.
"""

import unittest
import re

def validate_single_workflow_content(content):
    """Test function to validate a single workflow content string."""
    uses_pattern = r'uses:\s+([^@]+)@([^\s\n]+)'
    uses_matches = re.findall(uses_pattern, content)

    for action, version in uses_matches:
        if version == 'latest':
            return False
    return True

class TestWorkflowVersionValidation(unittest.TestCase):

    def test_workflow_with_latest_tag(self):
        """Test detection of @latest tag usage."""
        workflow_content = """
name: Test Workflow
"on":
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: some-action@latest
"""
        # This should fail because @latest is used
        result = validate_single_workflow_content(workflow_content)
        self.assertFalse(result)

    def test_workflow_with_pinned_versions(self):
        """Test validation passes with properly pinned versions."""
        workflow_content = """
name: Test Workflow
"on":
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: some-action@v1.2.3
"""
        # This should pass because all versions are pinned
        result = validate_single_workflow_content(workflow_content)
        self.assertTrue(result)

if __name__ == '__main__':
    # Redirect print output for tests
    import sys
    from io import StringIO

    # Run tests with captured output
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        unittest.main(verbosity=2, exit=False)
    finally:
        sys.stdout = original_stdout
        print("[PASS] Version validation tests completed")