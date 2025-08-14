#!/usr/bin/env python3
"""
CTMM Unified Tool - Comprehensive Workflow Management
====================================================

This unified command-line interface integrates the complete CTMM toolset:

1. Build System Management (ctmm_build.py)
2. LaTeX De-escaping (fix_latex_escaping.py) 
3. Workflow Orchestration (comprehensive_workflow.py)
4. Validation and Testing

Usage:
    python3 ctmm_unified_tool.py <command> [options]

Commands:
    build       - Run CTMM build system check and compilation
    fix-escaping - Fix over-escaped LaTeX files  
    validate    - Run comprehensive validation suite
    workflow    - Execute complete CTMM workflow
    test        - Run all tests (unit + integration)
    clean       - Clean build artifacts
    help        - Show detailed help for each command

Examples:
    python3 ctmm_unified_tool.py build
    python3 ctmm_unified_tool.py fix-escaping converted/ fixed/
    python3 ctmm_unified_tool.py workflow --full
    python3 ctmm_unified_tool.py test --integration
"""

import sys
import subprocess
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any
import importlib.util

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class CTMMUnifiedTool:
    """Unified interface for CTMM toolset operations."""
    
    def __init__(self):
        self.tools = {
            'build': 'ctmm_build.py',
            'fix-escaping': 'fix_latex_escaping.py', 
            'workflow': 'comprehensive_workflow.py',
            'validate': 'validate_latex_syntax.py'
        }
        
    def print_banner(self, title: str) -> None:
        """Print a formatted banner."""
        print("\n" + "="*70)
        print(f"{title:^70}")
        print("="*70)
        
    def print_section(self, title: str) -> None:
        """Print a section header."""
        print(f"\n📋 {title}")
        print("-" * (len(title) + 4))
        
    def run_command(self, cmd: str, description: str, check: bool = True) -> bool:
        """Run a shell command with error handling."""
        try:
            print(f"🔧 {description}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, errors='replace')
            
            if result.returncode == 0:
                print(f"✅ {description} - SUCCESS")
                if result.stdout.strip():
                    # Print important output lines
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if any(keyword in line.lower() for keyword in ['pass', 'fail', 'error', 'warning', 'success', '✓', '✗']):
                            print(f"   {line}")
                return True
            else:
                print(f"❌ {description} - FAILED")
                if result.stderr.strip():
                    print(f"   Error: {result.stderr.strip()}")
                return False if check else True
                
        except Exception as e:
            print(f"❌ {description} - ERROR: {e}")
            return False if check else True
            
    def load_tool_module(self, tool_path: str):
        """Dynamically load a tool module."""
        try:
            spec = importlib.util.spec_from_file_location("tool_module", tool_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            logger.error(f"Failed to load tool {tool_path}: {e}")
            return None
            
    def cmd_build(self, args: argparse.Namespace) -> int:
        """Execute CTMM build system check and optional PDF compilation."""
        self.print_banner("CTMM BUILD SYSTEM")
        
        success = True
        
        # Run build system check
        self.print_section("Build System Check")
        if not self.run_command("python3 ctmm_build.py", "CTMM build system validation"):
            success = False
            
        # Optional PDF compilation
        if args.compile and success:
            self.print_section("PDF Compilation")
            if not self.run_command("pdflatex -interaction=nonstopmode main.tex", "LaTeX compilation (pass 1)", check=False):
                print("⚠️  LaTeX compilation failed - pdflatex may not be available")
            else:
                self.run_command("pdflatex -interaction=nonstopmode main.tex", "LaTeX compilation (pass 2)", check=False)
                
        return 0 if success else 1
        
    def cmd_fix_escaping(self, args: argparse.Namespace) -> int:
        """Execute LaTeX de-escaping operations."""
        self.print_banner("LATEX DE-ESCAPING")
        
        if not args.input_dir:
            print("❌ Input directory required for fix-escaping command")
            return 1
            
        # Build command
        cmd_parts = ["python3", "fix_latex_escaping.py"]
        cmd_parts.append(args.input_dir)
        
        if args.output_dir:
            cmd_parts.append(args.output_dir)
            
        if args.validate:
            cmd_parts.append("--validate")
        if args.verbose:
            cmd_parts.append("--verbose")
        if args.backup:
            cmd_parts.append("--backup")
            
        cmd = " ".join(cmd_parts)
        
        self.print_section("De-escaping LaTeX Files")
        success = self.run_command(cmd, f"Processing files in {args.input_dir}")
        
        return 0 if success else 1
        
    def cmd_validate(self, args: argparse.Namespace) -> int:
        """Execute comprehensive validation suite."""
        self.print_banner("COMPREHENSIVE VALIDATION")
        
        success_count = 0
        total_tests = 0
        
        validations = [
            ("python3 validate_latex_syntax.py", "LaTeX syntax validation"),
            ("python3 ctmm_build.py", "Build system validation"),
            ("python3 test_ctmm_build.py", "Unit tests validation")
        ]
        
        if args.integration:
            validations.append(("python3 test_integration.py", "Integration tests"))
            
        for cmd, description in validations:
            total_tests += 1
            self.print_section(description.title())
            if self.run_command(cmd, description):
                success_count += 1
                
        # Summary
        self.print_section("Validation Summary")
        print(f"Tests passed: {success_count}/{total_tests}")
        print(f"Success rate: {(success_count/total_tests)*100:.1f}%")
        
        if success_count == total_tests:
            print("🎉 All validations passed!")
            return 0
        else:
            print(f"⚠️  {total_tests - success_count} validation(s) failed")
            return 1
            
    def cmd_workflow(self, args: argparse.Namespace) -> int:
        """Execute complete CTMM workflow."""
        self.print_banner("COMPREHENSIVE WORKFLOW")
        
        # Build workflow command
        cmd_parts = ["python3", "comprehensive_workflow.py"]
        
        if args.full:
            cmd_parts.append("--full")
        if args.cleanup:
            cmd_parts.append("--cleanup")
            
        cmd = " ".join(cmd_parts)
        
        self.print_section("Executing Workflow")
        success = self.run_command(cmd, "Complete CTMM workflow execution")
        
        return 0 if success else 1
        
    def cmd_test(self, args: argparse.Namespace) -> int:
        """Execute test suites."""
        self.print_banner("CTMM TEST SUITE")
        
        success_count = 0
        total_tests = 0
        
        # Unit tests
        self.print_section("Unit Tests")
        total_tests += 1
        if self.run_command("python3 test_ctmm_build.py", "Unit tests for build system"):
            success_count += 1
            
        # Integration tests
        if args.integration:
            self.print_section("Integration Tests")
            total_tests += 1
            if self.run_command("python3 test_integration.py", "Integration test suite"):
                success_count += 1
        
        # Workflow structure tests
        if Path("test_workflow_structure.py").exists():
            self.print_section("Workflow Structure Tests")
            total_tests += 1
            if self.run_command("python3 test_workflow_structure.py", "Workflow structure validation"):
                success_count += 1
                
        # Summary
        self.print_section("Test Summary")
        print(f"Test suites passed: {success_count}/{total_tests}")
        print(f"Success rate: {(success_count/total_tests)*100:.1f}%")
        
        return 0 if success_count == total_tests else 1
        
    def cmd_clean(self, args: argparse.Namespace) -> int:
        """Clean build artifacts."""
        self.print_banner("CLEANUP")
        
        self.print_section("Removing Build Artifacts")
        success = self.run_command("make clean", "Cleaning build artifacts")
        
        if args.deep:
            self.print_section("Deep Clean")
            deep_clean_cmd = "rm -rf __pycache__/ *.pyc *.pyo .pytest_cache/ *.bak"
            self.run_command(deep_clean_cmd, "Deep cleanup", check=False)
            
        return 0 if success else 1
        
    def cmd_status(self, args: argparse.Namespace) -> int:
        """Show CTMM system status."""
        self.print_banner("CTMM SYSTEM STATUS")
        
        # Check key files
        self.print_section("Key Files Status")
        key_files = [
            "main.tex", "ctmm_build.py", "fix_latex_escaping.py", 
            "comprehensive_workflow.py", "test_ctmm_build.py"
        ]
        
        all_present = True
        for file in key_files:
            if Path(file).exists():
                print(f"✅ {file}")
            else:
                print(f"❌ {file} - MISSING")
                all_present = False
                
        # Quick validation
        self.print_section("Quick System Check")
        if all_present:
            self.run_command("python3 ctmm_build.py", "Build system check", check=False)
        else:
            print("⚠️  Cannot run system check - missing key files")
            
        return 0 if all_present else 1

def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        description="CTMM Unified Tool - Comprehensive Workflow Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s build                              # Run build system check
  %(prog)s build --compile                    # Check + compile PDF
  %(prog)s fix-escaping converted/            # Fix LaTeX escaping in-place
  %(prog)s fix-escaping converted/ fixed/     # Fix with output directory
  %(prog)s validate                           # Run core validations
  %(prog)s validate --integration             # Include integration tests
  %(prog)s workflow --full                    # Complete workflow
  %(prog)s test --integration                 # Run all tests
  %(prog)s clean                              # Clean build artifacts
  %(prog)s status                             # Show system status

For more detailed help on any command:
  %(prog)s <command> --help
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Run CTMM build system')
    build_parser.add_argument('--compile', action='store_true', 
                             help='Also compile PDF with pdflatex')
    
    # Fix-escaping command
    fix_parser = subparsers.add_parser('fix-escaping', help='Fix over-escaped LaTeX files')
    fix_parser.add_argument('input_dir', help='Directory containing .tex files to fix')
    fix_parser.add_argument('output_dir', nargs='?', help='Output directory (optional)')
    fix_parser.add_argument('--validate', action='store_true', help='Validate after fixing')
    fix_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    fix_parser.add_argument('--backup', action='store_true', help='Create backup files')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Run validation suite')
    validate_parser.add_argument('--integration', action='store_true', 
                                help='Include integration tests')
    
    # Workflow command
    workflow_parser = subparsers.add_parser('workflow', help='Execute complete workflow')
    workflow_parser.add_argument('--full', action='store_true', help='Run full workflow')
    workflow_parser.add_argument('--cleanup', action='store_true', help='Clean up after')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run test suites')
    test_parser.add_argument('--integration', action='store_true', 
                           help='Include integration tests')
    
    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean build artifacts')
    clean_parser.add_argument('--deep', action='store_true', help='Deep clean (remove cache)')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    
    return parser

def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
        
    tool = CTMMUnifiedTool()
    
    # Route to appropriate command handler
    command_handlers = {
        'build': tool.cmd_build,
        'fix-escaping': tool.cmd_fix_escaping,
        'validate': tool.cmd_validate,
        'workflow': tool.cmd_workflow,
        'test': tool.cmd_test,
        'clean': tool.cmd_clean,
        'status': tool.cmd_status
    }
    
    handler = command_handlers.get(args.command)
    if handler:
        try:
            return handler(args)
        except KeyboardInterrupt:
            print("\n⚠️  Operation cancelled by user")
            return 1
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return 1
    else:
        print(f"❌ Unknown command: {args.command}")
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())