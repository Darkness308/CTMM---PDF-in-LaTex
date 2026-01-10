#!/usr/bin/env python3
"""
CTMM Unified Tool - Comprehensive Integration

This tool provides a unified interface for the complete CTMM workflow:
- Build system validation and template generation
- LaTeX de-escaping for converted documents
- Integrated validation and testing
- Complete project workflow management

Usage:
    python3 ctmm_unified_tool.py [command] [options]

Commands:
    build           - Run complete build system check
    de-escape       - Fix over-escaped LaTeX files
    validate        - Validate project state
    workflow        - Run complete integration workflow
    help            - Show detailed help
"""

import argparse
import logging
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Import our existing tools
from ctmm_build import (
    scan_references, check_missing_files, create_template,
    test_basic_build, test_full_build, filename_to_title
)
from fix_latex_escaping import LaTeXDeEscaper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class CTMMUnifiedTool:
    """Unified tool for comprehensive CTMM project management."""

    def __init__(self):
        self.main_tex = "main.tex"
        self.de_escaper = LaTeXDeEscaper()
        self.stats = {
            'build_success': False,
            'missing_files_created': 0,
            'files_de_escaped': 0,
            'validation_issues': []
        }

    def run_build_system(self, create_templates: bool = True) -> bool:
        """
        Run the complete CTMM build system check.

        Args:
            create_templates: Whether to create missing template files

        Returns:
            True if build system passes, False otherwise
        """
        logger.info("="*60)
        logger.info("CTMM UNIFIED TOOL - BUILD SYSTEM")
        logger.info("="*60)

        # 1. Scan references
        logger.info("1. Scanning file references...")
        try:
            refs = scan_references(self.main_tex)
            style_files = refs['style_files']
            module_files = refs['module_files']

            logger.info(f"Found {len(style_files)} style packages")
            logger.info(f"Found {len(module_files)} module inputs")
        except Exception as e:
            logger.error(f"Failed to scan references: {e}")
            return False

        # 2. Check missing files
        logger.info("\n2. Checking file existence...")
        all_files = style_files + module_files
        missing_files = check_missing_files(all_files)

        if missing_files:
            logger.info(f"Found {len(missing_files)} missing files")
            if create_templates:
                logger.info("Creating templates for missing files...")
                for file_path in missing_files:
                    try:
                        create_template(file_path)
                        self.stats['missing_files_created'] += 1
                        logger.info(f"✓ Created template: {file_path}")
                    except Exception as e:
                        logger.error(f"✗ Failed to create {file_path}: {e}")
            else:
                logger.warning("Templates not created (create_templates=False)")
        else:
            logger.info("✓ All referenced files exist")

        # 3. Test builds
        logger.info("\n3. Testing build system...")
        basic_success = test_basic_build(self.main_tex)
        full_success = test_full_build(self.main_tex)

        build_success = basic_success and full_success
        self.stats['build_success'] = build_success

        if build_success:
            logger.info("✓ Build system validation PASSED")
        else:
            logger.error("✗ Build system validation FAILED")

        return build_success

    def run_de_escaping(self, input_dir: str, output_dir: Optional[str] = None,
                       backup: bool = False) -> Dict:
        """
        Run LaTeX de-escaping on specified directory.

        Args:
            input_dir: Directory containing .tex files to fix
            output_dir: Output directory (optional, default: in-place)
            backup: Whether to create backup files

        Returns:
            Statistics dictionary with processing results
        """
        logger.info("="*60)
        logger.info("CTMM UNIFIED TOOL - DE-ESCAPING")
        logger.info("="*60)

        input_path = Path(input_dir)
        if not input_path.exists():
            logger.error(f"Input directory {input_dir} does not exist")
            return {}

        output_path = Path(output_dir) if output_dir else input_path

        # Create backups if requested
        if backup and output_path == input_path:
            logger.info("Creating backup files...")
            for tex_file in input_path.glob('*.tex'):
                backup_file = tex_file.with_suffix('.tex.bak')
                if not backup_file.exists():
                    tex_file.rename(backup_file)
                    logger.info(f"✓ Backup created: {backup_file}")

        # Process files
        logger.info(f"Processing LaTeX files in {input_dir}...")
        stats = self.de_escaper.process_directory(input_path, output_path)

        self.stats['files_de_escaped'] = stats['files_changed']

        logger.info(f"\n✓ De-escaping completed:")
        logger.info(f"  Files processed: {stats['files_processed']}")
        logger.info(f"  Files changed: {stats['files_changed']}")
        logger.info(f"  Total replacements: {stats['total_replacements']}")

        return stats

    def validate_project(self, check_converted: bool = True) -> List[str]:
        """
        Comprehensive project validation.

        Args:
            check_converted: Whether to validate converted directory

        Returns:
            List of validation issues found
        """
        logger.info("="*60)
        logger.info("CTMM UNIFIED TOOL - VALIDATION")
        logger.info("="*60)

        issues = []

        # 1. Validate main.tex structure
        logger.info("1. Validating main.tex structure...")
        if not Path(self.main_tex).exists():
            issues.append(f"Main file {self.main_tex} not found")
        else:
            logger.info("✓ Main file exists")

        # 2. Validate build system
        logger.info("\n2. Validating build system...")
        try:
            refs = scan_references(self.main_tex)
            missing = check_missing_files(refs['style_files'] + refs['module_files'])
            if missing:
                issues.append(f"Missing files: {missing}")
            else:
                logger.info("✓ All referenced files exist")
        except Exception as e:
            issues.append(f"Build system validation failed: {e}")

        # 3. Validate converted files if requested
        if check_converted:
            converted_dir = Path('converted')
            if converted_dir.exists():
                logger.info("\n3. Validating converted files...")
                for tex_file in converted_dir.glob('*.tex'):
                    file_issues = self.de_escaper.validate_latex_syntax(tex_file)
                    if file_issues:
                        issues.extend([f"{tex_file.name}: {issue}" for issue in file_issues])

                if not any("converted" in issue for issue in issues):
                    logger.info("✓ Converted files validation passed")
            else:
                logger.info("3. No converted directory found - skipping converted files validation")

        self.stats['validation_issues'] = issues

        if issues:
            logger.warning(f"Validation found {len(issues)} issues:")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("✓ Project validation PASSED")

        return issues

    def run_complete_workflow(self, converted_dir: Optional[str] = None) -> bool:
        """
        Run the complete CTMM integration workflow.

        Args:
            converted_dir: Directory with converted files to process

        Returns:
            True if workflow completes successfully
        """
        logger.info("="*60)
        logger.info("CTMM UNIFIED TOOL - COMPLETE WORKFLOW")
        logger.info("="*60)

        success = True

        # Step 1: Build system validation
        logger.info("STEP 1: Build System Validation")
        build_success = self.run_build_system()
        if not build_success:
            logger.error("Build system validation failed")
            success = False

        # Step 2: De-escape converted files if provided
        if converted_dir and Path(converted_dir).exists():
            logger.info(f"\nSTEP 2: De-escaping converted files from {converted_dir}")
            de_escape_stats = self.run_de_escaping(converted_dir, backup=True)
            if de_escape_stats.get('files_processed', 0) == 0:
                logger.warning("No files processed in de-escaping step")
        else:
            logger.info("\nSTEP 2: Skipping de-escaping (no converted directory specified)")

        # Step 3: Project validation
        logger.info("\nSTEP 3: Complete Project Validation")
        issues = self.validate_project()
        if issues:
            logger.warning("Project validation found issues")
            # Don't fail workflow for validation warnings

        # Step 4: Final summary
        logger.info("\n" + "="*60)
        logger.info("WORKFLOW SUMMARY")
        logger.info("="*60)
        logger.info(f"Build system: {'✓ PASS' if self.stats['build_success'] else '✗ FAIL'}")
        logger.info(f"Templates created: {self.stats['missing_files_created']}")
        logger.info(f"Files de-escaped: {self.stats['files_de_escaped']}")
        logger.info(f"Validation issues: {len(self.stats['validation_issues'])}")

        if success:
            logger.info("✓ WORKFLOW COMPLETED SUCCESSFULLY")
        else:
            logger.error("✗ WORKFLOW COMPLETED WITH ERRORS")

        return success


def main():
    """Main entry point for the unified tool."""
    parser = argparse.ArgumentParser(
        description="CTMM Unified Tool - Comprehensive Project Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  build           Run build system check and create templates
  de-escape       Fix over-escaped LaTeX files
  validate        Validate complete project state
  workflow        Run complete integration workflow

Examples:
  %(prog)s build                           # Build system check
  %(prog)s de-escape converted/            # Fix converted files
  %(prog)s validate                        # Validate project
  %(prog)s workflow --converted converted/ # Complete workflow
        """
    )

    parser.add_argument('command',
                       choices=['build', 'de-escape', 'validate', 'workflow'],
                       help='Command to execute')
    parser.add_argument('--converted', '-c',
                       help='Directory with converted files (for de-escape/workflow)')
    parser.add_argument('--output', '-o',
                       help='Output directory for de-escape (default: in-place)')
    parser.add_argument('--backup', '-b', action='store_true',
                       help='Create backup files for de-escaping')
    parser.add_argument('--no-templates', action='store_true',
                       help='Do not create template files in build command')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    tool = CTMMUnifiedTool()

    try:
        if args.command == 'build':
            success = tool.run_build_system(create_templates=not args.no_templates)
            sys.exit(0 if success else 1)

        elif args.command == 'de-escape':
            if not args.converted:
                logger.error("--converted directory required for de-escape command")
                sys.exit(1)
            stats = tool.run_de_escaping(args.converted, args.output, args.backup)
            sys.exit(0 if stats else 1)

        elif args.command == 'validate':
            issues = tool.validate_project()
            sys.exit(0 if not issues else 1)

        elif args.command == 'workflow':
            success = tool.run_complete_workflow(args.converted)
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()