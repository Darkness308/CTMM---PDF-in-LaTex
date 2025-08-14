#!/usr/bin/env python3
"""
CTMM Unified Tool - Production-Ready Interface
==============================================

Unified command-line interface for complete CTMM workflow management.
Integrates build system, de-escaping, validation, and workflow orchestration.

This tool provides a single entry point for all CTMM operations:
- Build system management and template generation
- LaTeX de-escaping with enhanced pattern recognition
- Comprehensive validation and testing
- Workflow orchestration and integration

Usage:
    python3 ctmm_unified_tool.py [command] [options]

Commands:
    build       - Run CTMM build system check and template generation
    de-escape   - Fix LaTeX over-escaping in converted files
    validate    - Run comprehensive validation suite
    workflow    - Execute complete workflow integration
    test        - Run all test suites
    clean       - Clean build artifacts
    help        - Show detailed help

Examples:
    python3 ctmm_unified_tool.py build
    python3 ctmm_unified_tool.py de-escape converted/
    python3 ctmm_unified_tool.py workflow --full
    python3 ctmm_unified_tool.py validate --verbose
"""

import sys
import subprocess
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class CTMMUnifiedTool:
    """Unified interface for all CTMM tools and workflows."""
    
    def __init__(self):
        self.tools = {
            'ctmm_build.py': 'CTMM build system and template generation',
            'fix_latex_escaping.py': 'LaTeX de-escaping tool',
            'comprehensive_workflow.py': 'Complete workflow integration',
            'test_ctmm_build.py': 'Unit test suite',
            'validate_latex_syntax.py': 'LaTeX syntax validation',
            'build_system.py': 'Detailed build analysis'
        }
        
        # Validate tool availability
        self.available_tools = self._check_tool_availability()
    
    def _check_tool_availability(self) -> Dict[str, bool]:
        """Check which tools are available in the current directory."""
        available = {}
        for tool in self.tools:
            tool_path = Path(tool)
            available[tool] = tool_path.exists()
            if not tool_path.exists():
                logger.warning(f"Tool {tool} not found")
        return available
    
    def _run_command(self, cmd: List[str], description: str, check: bool = True) -> bool:
        """Run a command and handle errors gracefully."""
        try:
            logger.info(f"Running: {description}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=check)
            
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode != 0:
                logger.error(f"Error in {description}: {result.stderr}")
                return False
                
            logger.info(f"✅ {description} - SUCCESS")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ {description} - FAILED: {e}")
            if e.stdout:
                print(e.stdout)
            if e.stderr:
                print(e.stderr)
            return False
        except FileNotFoundError:
            logger.error(f"❌ {description} - Tool not found")
            return False
    
    def build(self, args) -> bool:
        """Run CTMM build system check and template generation."""
        print("="*60)
        print("CTMM BUILD SYSTEM")
        print("="*60)
        
        if not self.available_tools.get('ctmm_build.py'):
            logger.error("ctmm_build.py not available")
            return False
        
        cmd = ['python3', 'ctmm_build.py']
        return self._run_command(cmd, "CTMM build system check")
    
    def de_escape(self, args) -> bool:
        """Fix LaTeX over-escaping in converted files."""
        print("="*60)
        print("LATEX DE-ESCAPING")
        print("="*60)
        
        if not self.available_tools.get('fix_latex_escaping.py'):
            logger.error("fix_latex_escaping.py not available")
            return False
        
        if not args.input_dir:
            logger.error("Input directory required for de-escaping")
            return False
        
        cmd = ['python3', 'fix_latex_escaping.py']
        cmd.append(args.input_dir)
        
        if args.output_dir:
            cmd.append(args.output_dir)
        if args.backup:
            cmd.append('--backup')
        if args.validate:
            cmd.append('--validate')
        if args.verbose:
            cmd.append('--verbose')
        
        return self._run_command(cmd, "LaTeX de-escaping")
    
    def validate(self, args) -> bool:
        """Run comprehensive validation suite."""
        print("="*60)
        print("COMPREHENSIVE VALIDATION")
        print("="*60)
        
        success_count = 0
        total_tests = 0
        
        # LaTeX syntax validation
        if self.available_tools.get('validate_latex_syntax.py'):
            total_tests += 1
            if self._run_command(['python3', 'validate_latex_syntax.py'], "LaTeX syntax validation"):
                success_count += 1
        
        # Unit tests
        if self.available_tools.get('test_ctmm_build.py'):
            total_tests += 1
            if self._run_command(['python3', 'test_ctmm_build.py'], "Unit tests"):
                success_count += 1
        
        # Build system check
        if self.available_tools.get('ctmm_build.py'):
            total_tests += 1
            if self._run_command(['python3', 'ctmm_build.py'], "Build system check"):
                success_count += 1
        
        # Detailed analysis (if verbose)
        if args.verbose and self.available_tools.get('build_system.py'):
            total_tests += 1
            if self._run_command(['python3', 'build_system.py', '--verbose'], "Detailed build analysis", check=False):
                success_count += 1
        
        print(f"\nValidation Summary: {success_count}/{total_tests} tests passed")
        return success_count == total_tests
    
    def workflow(self, args) -> bool:
        """Execute complete workflow integration."""
        print("="*60)
        print("COMPREHENSIVE WORKFLOW")
        print("="*60)
        
        if not self.available_tools.get('comprehensive_workflow.py'):
            logger.error("comprehensive_workflow.py not available")
            return False
        
        cmd = ['python3', 'comprehensive_workflow.py']
        
        if args.full:
            cmd.append('--full')
        if args.cleanup:
            cmd.append('--cleanup')
        
        return self._run_command(cmd, "Comprehensive workflow")
    
    def test(self, args) -> bool:
        """Run all test suites."""
        print("="*60)
        print("TEST SUITES")
        print("="*60)
        
        success_count = 0
        total_tests = 0
        
        # Unit tests
        if self.available_tools.get('test_ctmm_build.py'):
            total_tests += 1
            if self._run_command(['python3', 'test_ctmm_build.py'], "Unit tests"):
                success_count += 1
        
        # Integration tests (if available)
        if Path('test_integration.py').exists():
            total_tests += 1
            if self._run_command(['python3', 'test_integration.py'], "Integration tests"):
                success_count += 1
        
        # Workflow structure tests
        if Path('test_workflow_structure.py').exists():
            total_tests += 1
            if self._run_command(['python3', 'test_workflow_structure.py'], "Workflow structure tests"):
                success_count += 1
        
        print(f"\nTest Summary: {success_count}/{total_tests} test suites passed")
        return success_count == total_tests
    
    def clean(self, args) -> bool:
        """Clean build artifacts."""
        print("="*60)
        print("CLEANING BUILD ARTIFACTS")
        print("="*60)
        
        # Use make clean if available
        if Path('Makefile').exists():
            return self._run_command(['make', 'clean'], "Clean build artifacts", check=False)
        else:
            # Manual cleanup
            artifacts = [
                '*.aux', '*.log', '*.out', '*.toc', '*.pdf',
                'main_basic_test.*', '*.temp.*', 'build_error_*.log'
            ]
            
            import glob
            removed_count = 0
            for pattern in artifacts:
                for file_path in glob.glob(pattern):
                    try:
                        Path(file_path).unlink()
                        removed_count += 1
                        logger.info(f"Removed {file_path}")
                    except Exception as e:
                        logger.warning(f"Could not remove {file_path}: {e}")
            
            print(f"Cleaned {removed_count} artifacts")
            return True
    
    def status(self, args) -> bool:
        """Show system status and tool availability."""
        print("="*60)
        print("CTMM SYSTEM STATUS")
        print("="*60)
        
        print("Tool Availability:")
        for tool, description in self.tools.items():
            status = "✅ Available" if self.available_tools.get(tool) else "❌ Missing"
            print(f"  {tool:<25} - {status} - {description}")
        
        print(f"\nAvailable tools: {sum(self.available_tools.values())}/{len(self.tools)}")
        
        # Check key files
        key_files = ['main.tex', 'Makefile', 'style/', 'modules/']
        print("\nKey Files:")
        for file_path in key_files:
            path = Path(file_path)
            exists = path.exists()
            status = "✅" if exists else "❌"
            print(f"  {file_path:<25} - {status}")
        
        return True


def main():
    """Main entry point for the unified tool."""
    parser = argparse.ArgumentParser(
        description="CTMM Unified Tool - Production-Ready Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s build                          # Run build system check
  %(prog)s de-escape converted/           # Fix LaTeX escaping
  %(prog)s validate --verbose             # Run validation with details
  %(prog)s workflow --full                # Run complete workflow
  %(prog)s test                           # Run all tests
  %(prog)s clean                          # Clean artifacts
  %(prog)s status                         # Show system status
        """
    )
    
    # Add subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Run CTMM build system check')
    
    # De-escape command
    de_escape_parser = subparsers.add_parser('de-escape', help='Fix LaTeX over-escaping')
    de_escape_parser.add_argument('input_dir', help='Directory containing .tex files')
    de_escape_parser.add_argument('output_dir', nargs='?', help='Output directory (optional)')
    de_escape_parser.add_argument('--backup', action='store_true', help='Create backup files')
    de_escape_parser.add_argument('--validate', action='store_true', help='Validate after fixing')
    de_escape_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Run comprehensive validation')
    validate_parser.add_argument('--verbose', '-v', action='store_true', help='Include detailed analysis')
    
    # Workflow command
    workflow_parser = subparsers.add_parser('workflow', help='Execute complete workflow')
    workflow_parser.add_argument('--full', action='store_true', help='Include de-escaping demo')
    workflow_parser.add_argument('--cleanup', action='store_true', help='Clean up after completion')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run all test suites')
    
    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean build artifacts')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show detailed help')
    
    args = parser.parse_args()
    
    # Show help if no command specified
    if not args.command:
        parser.print_help()
        return 0
    
    # Handle help command
    if args.command == 'help':
        parser.print_help()
        print("\n" + "="*60)
        print("DETAILED COMMAND DESCRIPTIONS")
        print("="*60)
        print("""
build     - Runs the CTMM build system to check dependencies, create missing
            templates, and validate the LaTeX build process.

de-escape - Fixes systematic over-escaping issues in converted LaTeX files.
            Can process directories of .tex files with backup and validation.

validate  - Runs comprehensive validation including LaTeX syntax checking,
            unit tests, and build system validation.

workflow  - Executes the complete CTMM workflow integration including all
            validation steps and optional de-escaping demonstration.

test      - Runs all available test suites including unit tests, integration
            tests, and workflow structure tests.

clean     - Removes build artifacts and temporary files created during the
            build and test processes.

status    - Shows the current status of the CTMM system including tool
            availability and key file presence.
        """)
        return 0
    
    # Ensure we're in the right directory
    if not Path('main.tex').exists():
        logger.error("This tool must be run from the CTMM repository root")
        logger.error("Expected to find main.tex in current directory")
        return 1
    
    # Create unified tool instance
    tool = CTMMUnifiedTool()
    
    # Execute command
    command_map = {
        'build': tool.build,
        'de-escape': tool.de_escape,
        'validate': tool.validate,
        'workflow': tool.workflow,
        'test': tool.test,
        'clean': tool.clean,
        'status': tool.status
    }
    
    if args.command in command_map:
        success = command_map[args.command](args)
        return 0 if success else 1
    else:
        logger.error(f"Unknown command: {args.command}")
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())