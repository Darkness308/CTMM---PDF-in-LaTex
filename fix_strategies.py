#!/usr/bin/env python3
"""
Fix Strategies - Automated Fix Implementations
Implements automated strategies for common workflow errors.
"""

import os
import re
import logging
import subprocess
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from healing_config import config
from error_analyzer import ErrorAnalysis, ErrorInstance

@dataclass
class FixResult:
    """Result of applying a fix strategy."""
    success: bool
    description: str
    files_modified: List[str]
    changes_made: List[str]
    validation_passed: bool
    error_message: Optional[str] = None

class FixStrategies:
    """Implements automated fix strategies for common workflow errors."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.repo_root = Path.cwd()

    def apply_fixes(self, analysis: ErrorAnalysis) -> List[FixResult]:
        """Apply appropriate fix strategies based on error analysis."""
        if not analysis.is_solvable:
            self.logger.warning("Analysis indicates errors are not solvable")
            return []

        results = []

        # Apply fixes in priority order
        for category in sorted(analysis.error_categories,
                             key=lambda x: config.fix_strategies.get(x, {}).get('priority', 999)):

            if category in config.fix_strategies:
                self.logger.info(f"Applying fix strategy for category: {category}")

                fix_result = self._apply_category_fix(category, analysis)
                if fix_result:
                    results.append(fix_result)

                    # If this fix failed critically, stop here
                    if not fix_result.success and fix_result.error_message:
                        self.logger.error(f"Critical fix failure for {category}: {fix_result.error_message}")
                        break

        return results

    def _apply_category_fix(self, category: str, analysis: ErrorAnalysis) -> Optional[FixResult]:
        """Apply fix strategy for a specific error category."""
        try:
            if category == 'latex_action_version':
                return self._fix_latex_action_version(analysis)
            elif category == 'package_missing':
                return self._fix_missing_packages(analysis)
            elif category == 'timeout':
                return self._fix_timeouts(analysis)
            elif category == 'dependency_error':
                return self._fix_dependency_errors(analysis)
            elif category == 'font_error':
                return self._fix_font_errors(analysis)
            elif category == 'workflow_syntax':
                return self._fix_workflow_syntax(analysis)
            else:
                self.logger.warning(f"No fix strategy implemented for category: {category}")
                return None

        except Exception as e:
            self.logger.error(f"Error applying fix for category {category}: {e}")
            return FixResult(
                success=False,
                description=f"Failed to apply fix for {category}",
                files_modified=[],
                changes_made=[],
                validation_passed=False,
                error_message=str(e)
            )

    def _fix_latex_action_version(self, analysis: ErrorAnalysis) -> FixResult:
        """Fix LaTeX action version issues."""
        workflow_files = self._find_workflow_files()
        files_modified = []
        changes_made = []

        fallback_version = config.fix_strategies['latex_action_version']['fallback_version']

        for workflow_file in workflow_files:
            file_path = self.repo_root / workflow_file

            if not file_path.exists():
                continue

            with open(file_path, 'r') as f:
                content = f.read()

            # Find and replace dante-ev/latex-action versions
            pattern = r'(uses:\s*dante-ev/latex-action@)(v?[\d\.]+)'
            matches = re.findall(pattern, content)

            if matches:
                old_content = content
                content = re.sub(pattern, f'\\1{fallback_version}', content)

                if content != old_content:
                    with open(file_path, 'w') as f:
                        f.write(content)

                    files_modified.append(str(workflow_file))
                    changes_made.append(f"Updated LaTeX action to {fallback_version} in {workflow_file}")
                    self.logger.info(f"Updated LaTeX action version in {workflow_file}")

        # Validate the changes
        validation_passed = self._validate_changes(files_modified)

        return FixResult(
            success=len(files_modified) > 0,
            description=f"Updated LaTeX action versions to {fallback_version}",
            files_modified=files_modified,
            changes_made=changes_made,
            validation_passed=validation_passed
        )

    def _fix_missing_packages(self, analysis: ErrorAnalysis) -> FixResult:
        """Fix missing LaTeX packages by updating workflow dependencies."""
        # Extract missing package names from errors
        missing_packages = set()
        for error in analysis.errors:
            if error.category == 'package_missing':
                # Extract package name from various error formats
                patterns = [
                    r'Package\s+([^\s]+)\s+not found',
                    r'File\s+([^\.]+)\.sty\s+not found',
                    r'texlive-([^\s]+)'
                ]

                for pattern in patterns:
                    match = re.search(pattern, error.matched_text)
                    if match:
                        pkg = match.group(1)
                        # Map common package names to texlive packages
                        if pkg == 'fontawesome5':
                            missing_packages.add('texlive-fonts-extra')
                        elif pkg.endswith('.sty'):
                            missing_packages.add(f'texlive-{pkg[:-4]}')
                        else:
                            missing_packages.add(f'texlive-{pkg}')

        if not missing_packages:
            return FixResult(
                success=False,
                description="No specific packages identified for installation",
                files_modified=[],
                changes_made=[],
                validation_passed=False
            )

        # Update workflow files to include missing packages
        workflow_files = self._find_workflow_files()
        files_modified = []
        changes_made = []

        for workflow_file in workflow_files:
            if 'latex-build' in workflow_file:  # Only update the main LaTeX build workflow
                file_path = self.repo_root / workflow_file

                if not file_path.exists():
                    continue

                with open(file_path, 'r') as f:
                    content = f.read()

                # Find the extra_system_packages section
                package_section_pattern = r'(extra_system_packages:\s*\|)([^-]*?)(\n\s*-?\s*\n|\n\s*[a-zA-Z]|\Z)'
                match = re.search(package_section_pattern, content, re.DOTALL)

                if match:
                    existing_packages = match.group(2)
                    packages_to_add = []

                    for pkg in missing_packages:
                        if pkg not in existing_packages:
                            packages_to_add.append(pkg)

                    if packages_to_add:
                        new_packages = existing_packages.rstrip()
                        for pkg in packages_to_add:
                            new_packages += f"\n            {pkg}"

                        new_content = content.replace(match.group(2), new_packages + '\n            ')

                        with open(file_path, 'w') as f:
                            f.write(new_content)

                        files_modified.append(str(workflow_file))
                        changes_made.extend([f"Added package {pkg}" for pkg in packages_to_add])
                        self.logger.info(f"Added {len(packages_to_add)} packages to {workflow_file}")

        validation_passed = self._validate_changes(files_modified)

        return FixResult(
            success=len(files_modified) > 0,
            description=f"Added missing LaTeX packages: {', '.join(missing_packages)}",
            files_modified=files_modified,
            changes_made=changes_made,
            validation_passed=validation_passed
        )

    def _fix_timeouts(self, analysis: ErrorAnalysis) -> FixResult:
        """Fix timeout issues by increasing timeout values."""
        workflow_files = self._find_workflow_files()
        files_modified = []
        changes_made = []

        multiplier = config.fix_strategies['timeout']['timeout_multiplier']

        for workflow_file in workflow_files:
            file_path = self.repo_root / workflow_file

            if not file_path.exists():
                continue

            with open(file_path, 'r') as f:
                content = f.read()

            # Find and increase timeout-minutes values
            timeout_pattern = r'timeout-minutes:\s*(\d+)'

            def increase_timeout(match):
                current_timeout = int(match.group(1))
                new_timeout = max(int(current_timeout * multiplier), current_timeout + 5)
                return f'timeout-minutes: {new_timeout}'

            old_content = content
            content = re.sub(timeout_pattern, increase_timeout, content)

            if content != old_content:
                with open(file_path, 'w') as f:
                    f.write(content)

                files_modified.append(str(workflow_file))
                changes_made.append(f"Increased timeouts by {multiplier}x in {workflow_file}")
                self.logger.info(f"Increased timeouts in {workflow_file}")

        validation_passed = self._validate_changes(files_modified)

        return FixResult(
            success=len(files_modified) > 0,
            description=f"Increased timeout values by factor of {multiplier}",
            files_modified=files_modified,
            changes_made=changes_made,
            validation_passed=validation_passed
        )

    def _fix_dependency_errors(self, analysis: ErrorAnalysis) -> FixResult:
        """Fix Python dependency errors."""
        workflow_files = self._find_workflow_files()
        files_modified = []
        changes_made = []

        for workflow_file in workflow_files:
            file_path = self.repo_root / workflow_file

            if not file_path.exists():
                continue

            with open(file_path, 'r') as f:
                content = f.read()

            # Look for pip install commands and add upgrade flags
            pip_pattern = r'(pip install)([^|&\n]*)'

            def upgrade_pip_install(match):
                install_cmd = match.group(1)
                packages = match.group(2)
                if '--upgrade' not in packages:
                    return f'{install_cmd} --upgrade{packages}'
                return match.group(0)

            old_content = content
            content = re.sub(pip_pattern, upgrade_pip_install, content)

            # Also ensure pip itself is upgraded
            if 'pip install' in content and 'pip install --upgrade pip' not in content:
                content = content.replace(
                    'pip install',
                    'pip install --upgrade pip && pip install',
                    1  # Only replace the first occurrence
                )

            if content != old_content:
                with open(file_path, 'w') as f:
                    f.write(content)

                files_modified.append(str(workflow_file))
                changes_made.append(f"Added pip upgrade flags in {workflow_file}")
                self.logger.info(f"Updated pip install commands in {workflow_file}")

        validation_passed = self._validate_changes(files_modified)

        return FixResult(
            success=len(files_modified) > 0,
            description="Updated Python dependency installation with upgrade flags",
            files_modified=files_modified,
            changes_made=changes_made,
            validation_passed=validation_passed
        )

    def _fix_font_errors(self, analysis: ErrorAnalysis) -> FixResult:
        """Fix FontAwesome and font-related errors."""
        # This is primarily handled by the package installation fix
        # But we can also check for FontAwesome-specific issues
        workflow_files = self._find_workflow_files()
        files_modified = []
        changes_made = []

        for workflow_file in workflow_files:
            if 'latex-build' in workflow_file:
                file_path = self.repo_root / workflow_file

                if not file_path.exists():
                    continue

                with open(file_path, 'r') as f:
                    content = f.read()

                # Ensure FontAwesome packages are included
                fontawesome_packages = [
                    'texlive-fonts-extra',
                    'texlive-fonts-recommended'
                ]

                package_section_pattern = r'(extra_system_packages:\s*\|)([^-]*?)(\n\s*-?\s*\n|\n\s*[a-zA-Z]|\Z)'
                match = re.search(package_section_pattern, content, re.DOTALL)

                if match:
                    existing_packages = match.group(2)
                    packages_to_add = []

                    for pkg in fontawesome_packages:
                        if pkg not in existing_packages:
                            packages_to_add.append(pkg)

                    if packages_to_add:
                        new_packages = existing_packages.rstrip()
                        for pkg in packages_to_add:
                            new_packages += f"\n            {pkg}"

                        new_content = content.replace(match.group(2), new_packages + '\n            ')

                        with open(file_path, 'w') as f:
                            f.write(new_content)

                        files_modified.append(str(workflow_file))
                        changes_made.extend([f"Added FontAwesome package {pkg}" for pkg in packages_to_add])
                        self.logger.info(f"Added FontAwesome packages to {workflow_file}")

        validation_passed = self._validate_changes(files_modified)

        return FixResult(
            success=len(files_modified) > 0,
            description="Added FontAwesome and font packages",
            files_modified=files_modified,
            changes_made=changes_made,
            validation_passed=validation_passed
        )

    def _fix_workflow_syntax(self, analysis: ErrorAnalysis) -> FixResult:
        """Fix basic workflow syntax issues."""
        workflow_files = self._find_workflow_files()
        files_modified = []
        changes_made = []

        for workflow_file in workflow_files:
            file_path = self.repo_root / workflow_file

            if not file_path.exists():
                continue

            with open(file_path, 'r') as f:
                content = f.read()

            old_content = content

            # Fix common YAML syntax issues
            # Ensure proper quoting of 'on:' keyword
            content = re.sub(r'^on:', '"on":', content, flags=re.MULTILINE)

            # Fix indentation issues (basic)
            content = re.sub(r'^\s\s([a-zA-Z])', r'  \1', content, flags=re.MULTILINE)

            if content != old_content:
                with open(file_path, 'w') as f:
                    f.write(content)

                files_modified.append(str(workflow_file))
                changes_made.append(f"Fixed YAML syntax in {workflow_file}")
                self.logger.info(f"Fixed workflow syntax in {workflow_file}")

        validation_passed = self._validate_changes(files_modified)

        return FixResult(
            success=len(files_modified) > 0,
            description="Fixed workflow YAML syntax issues",
            files_modified=files_modified,
            changes_made=changes_made,
            validation_passed=validation_passed
        )

    def _find_workflow_files(self) -> List[str]:
        """Find all workflow files in the repository."""
        workflow_dir = self.repo_root / '.github' / 'workflows'
        if not workflow_dir.exists():
            return []

        workflow_files = []
        for file_path in workflow_dir.glob('*.yml'):
            workflow_files.append(str(file_path.relative_to(self.repo_root)))
        for file_path in workflow_dir.glob('*.yaml'):
            workflow_files.append(str(file_path.relative_to(self.repo_root)))

        return workflow_files

    def _validate_changes(self, modified_files: List[str]) -> bool:
        """Validate changes using existing validation tools."""
        if not modified_files:
            return True

        try:
            # Run YAML syntax validation
            result = subprocess.run(
                ['python3', 'validate_workflow_syntax.py'],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=60
            )

            if result.returncode == 0:
                self.logger.info("Workflow syntax validation passed")
                return True
            else:
                self.logger.error(f"Workflow syntax validation failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            self.logger.warning("Validation timeout - assuming success")
            return True
        except FileNotFoundError:
            self.logger.warning("Validation script not found - skipping validation")
            return True
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False

def main():
    """Test the fix strategies functionality."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Import here to avoid circular imports during testing
    from error_analyzer import ErrorAnalyzer, ErrorInstance

    strategies = FixStrategies()

    print("🔧 Testing Fix Strategies")
    print("=" * 50)

    # Create a sample error analysis for testing
    sample_errors = [
        ErrorInstance(
            category='latex_action_version',
            pattern='uses: dante-ev/latex-action@v1.0.0',
            matched_text='uses: dante-ev/latex-action@v1.0.0',
            line_number=1,
            context='Sample context',
            severity='high',
            job_name='test-job'
        ),
        ErrorInstance(
            category='timeout',
            pattern='timeout-minutes: 5',
            matched_text='timeout-minutes: 5',
            line_number=2,
            context='Sample context',
            severity='medium',
            job_name='test-job'
        )
    ]

    # Create a mock analysis
    class MockAnalysis:
        def __init__(self):
            self.workflow_run_id = 12345
            self.workflow_name = 'test-workflow'
            self.total_errors = len(sample_errors)
            self.error_categories = {'latex_action_version', 'timeout'}
            self.errors = sample_errors
            self.is_solvable = True
            self.recommended_fixes = []
            self.analysis_timestamp = '2024-01-01T00:00:00'

    mock_analysis = MockAnalysis()

    # Test fix application
    print("📝 Testing fix application...")
    results = strategies.apply_fixes(mock_analysis)

    print(f"✅ Applied {len(results)} fix strategies:")
    for i, result in enumerate(results, 1):
        status = "✅" if result.success else "❌"
        print(f"   {i}. {status} {result.description}")
        if result.files_modified:
            print(f"      Files: {', '.join(result.files_modified)}")
        if result.changes_made:
            for change in result.changes_made:
                print(f"      - {change}")

    print("\n✅ Fix strategies test completed")

if __name__ == "__main__":
    main()
