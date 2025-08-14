#!/usr/bin/env python3
"""
CTMM Unified Tool - Comprehensive Workflow Management System
============================================================

This unified interface integrates all CTMM toolset components:
- Build system (ctmm_build.py)
- LaTeX de-escaping (fix_latex_escaping.py) 
- Validation and testing
- Workflow orchestration

Usage:
    python3 ctmm_unified_tool.py build
    python3 ctmm_unified_tool.py de-escape [directory]
    python3 ctmm_unified_tool.py validate
    python3 ctmm_unified_tool.py workflow [--full]
    python3 ctmm_unified_tool.py test
    python3 ctmm_unified_tool.py --help

Examples:
    python3 ctmm_unified_tool.py build                    # Run CTMM build system
    python3 ctmm_unified_tool.py de-escape converted/     # Fix LaTeX escaping
    python3 ctmm_unified_tool.py validate                 # Validate LaTeX syntax
    python3 ctmm_unified_tool.py workflow --full          # Full workflow validation
    python3 ctmm_unified_tool.py test                     # Run all tests
"""

import sys
import os
import subprocess
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any
import importlib.util

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class CTMMUnifiedTool:
    """Unified interface for all CTMM toolset operations."""
    
    def __init__(self):
        self.tools = {
            'build': self._run_build,
            'de-escape': self._run_deescaping,
            'validate': self._run_validation,
            'workflow': self._run_workflow,
            'test': self._run_tests,
            'status': self._show_status,
        }
        
        self.stats = {
            'operations_run': 0,
            'operations_successful': 0,
            'files_processed': 0
        }
    
    def print_banner(self, title: str):
        """Print a formatted banner."""
        print("\n" + "="*70)
        print(f"{title:^70}")
        print("="*70)
    
    def print_section(self, title: str):
        """Print a section header."""
        print(f"\n📋 {title}")
        print("-" * 50)
    
    def run_command(self, cmd: str, description: str, capture_output: bool = True) -> tuple:
        """
        Run a command and return success status and output.
        
        Args:
            cmd: Command to run
            description: Human-readable description
            capture_output: Whether to capture output
            
        Returns:
            Tuple of (success, output)
        """
        try:
            self.stats['operations_run'] += 1
            logger.info(f"Running: {description}")
            
            if capture_output:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, errors='replace')
                success = result.returncode == 0
                output = result.stdout.strip() if result.stdout else result.stderr.strip()
            else:
                result = subprocess.run(cmd, shell=True)
                success = result.returncode == 0
                output = ""
            
            if success:
                self.stats['operations_successful'] += 1
                logger.info(f"✅ {description} - SUCCESS")
            else:
                logger.error(f"❌ {description} - FAILED")
                if output:
                    logger.error(f"Error: {output}")
            
            return success, output
            
        except Exception as e:
            logger.error(f"❌ {description} - EXCEPTION: {e}")
            return False, str(e)
    
    def _run_build(self, args: argparse.Namespace) -> bool:
        """Run CTMM build system."""
        self.print_section("CTMM Build System")
        
        success, output = self.run_command("python3 ctmm_build.py", "CTMM build system check")
        if output:
            print(output)
        
        return success
    
    def _run_deescaping(self, args: argparse.Namespace) -> bool:
        """Run LaTeX de-escaping tool."""
        self.print_section("LaTeX De-escaping")
        
        # Get directory from args or use default
        target_dir = getattr(args, 'directory', 'converted') or 'converted'
        
        if not os.path.exists(target_dir):
            logger.warning(f"Directory {target_dir} does not exist. Creating example...")
            Path(target_dir).mkdir(exist_ok=True)
            logger.info(f"Created directory: {target_dir}")
            print(f"💡 Tip: Place .tex files in {target_dir}/ to process them")
            return True
        
        # Check if directory has .tex files
        tex_files = list(Path(target_dir).glob('*.tex'))
        if not tex_files:
            logger.info(f"No .tex files found in {target_dir}")
            return True
        
        # Run de-escaping
        cmd = f"python3 fix_latex_escaping.py --backup --verbose {target_dir}"
        success, output = self.run_command(cmd, f"De-escaping LaTeX files in {target_dir}")
        
        if output:
            print(output)
        
        self.stats['files_processed'] += len(tex_files)
        return success
    
    def _run_validation(self, args: argparse.Namespace) -> bool:
        """Run validation checks."""
        self.print_section("LaTeX Syntax Validation")
        
        success, output = self.run_command("python3 validate_latex_syntax.py", "LaTeX syntax validation")
        if output:
            print(output)
        
        return success
    
    def _run_workflow(self, args: argparse.Namespace) -> bool:
        """Run comprehensive workflow."""
        self.print_section("Comprehensive Workflow")
        
        full_flag = "--full" if getattr(args, 'full', False) else ""
        cmd = f"python3 comprehensive_workflow.py {full_flag}"
        
        success, output = self.run_command(cmd, "Comprehensive workflow validation", capture_output=False)
        
        return success
    
    def _run_tests(self, args: argparse.Namespace) -> bool:
        """Run all tests."""
        self.print_section("Test Suite")
        
        # Run unit tests
        success1, output1 = self.run_command("python3 test_ctmm_build.py", "Unit tests")
        if output1:
            print("Unit Test Results:")
            print(output1)
        
        # Run workflow structure tests
        success2, output2 = self.run_command("python3 test_workflow_structure.py", "Workflow structure tests")
        if output2:
            print("Workflow Structure Test Results:")
            print(output2)
        
        return success1 and success2
    
    def _show_status(self, args: argparse.Namespace) -> bool:
        """Show system status."""
        self.print_section("CTMM System Status")
        
        # Check key files
        key_files = [
            ("main.tex", "Main LaTeX document"),
            ("ctmm_build.py", "Build system"),
            ("fix_latex_escaping.py", "De-escaping tool"),
            ("comprehensive_workflow.py", "Workflow manager"),
            ("test_ctmm_build.py", "Unit tests"),
        ]
        
        print("📁 Key Files:")
        all_present = True
        for filename, description in key_files:
            if os.path.exists(filename):
                print(f"  ✅ {filename:<25} - {description}")
            else:
                print(f"  ❌ {filename:<25} - {description} (MISSING)")
                all_present = False
        
        # Check directories
        directories = [
            ("style/", "LaTeX style files"),
            ("modules/", "Content modules"),
            ("converted/", "Converted files for de-escaping"),
        ]
        
        print("\n📂 Directories:")
        for dirname, description in directories:
            if os.path.exists(dirname):
                count = len(list(Path(dirname).glob('*'))) if os.path.isdir(dirname) else 0
                print(f"  ✅ {dirname:<25} - {description} ({count} files)")
            else:
                print(f"  ❌ {dirname:<25} - {description} (MISSING)")
        
        # Quick validation
        print(f"\n🔍 Quick Validation:")
        success, _ = self.run_command("python3 ctmm_build.py", "Build system check")
        
        print(f"\n📊 Overall Status: {'✅ OPERATIONAL' if all_present and success else '⚠️  NEEDS ATTENTION'}")
        
        return all_present and success
    
    def run(self, args: List[str]) -> int:
        """
        Main entry point for the unified tool.
        
        Args:
            args: Command line arguments
            
        Returns:
            Exit code (0 for success, 1 for failure)
        """
        parser = argparse.ArgumentParser(
            description="CTMM Unified Tool - Comprehensive Workflow Management",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s build                    Run CTMM build system
  %(prog)s de-escape converted/     Fix LaTeX escaping in directory
  %(prog)s validate                 Validate LaTeX syntax
  %(prog)s workflow --full          Run full workflow validation
  %(prog)s test                     Run all tests
  %(prog)s status                   Show system status
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Build command
        build_parser = subparsers.add_parser('build', help='Run CTMM build system')
        
        # De-escape command
        deescape_parser = subparsers.add_parser('de-escape', help='Fix LaTeX over-escaping')
        deescape_parser.add_argument('directory', nargs='?', default='converted',
                                   help='Directory containing .tex files to process')
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate LaTeX syntax')
        
        # Workflow command
        workflow_parser = subparsers.add_parser('workflow', help='Run comprehensive workflow')
        workflow_parser.add_argument('--full', action='store_true',
                                   help='Run full workflow with all optional steps')
        
        # Test command
        test_parser = subparsers.add_parser('test', help='Run all tests')
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Show system status')
        
        # Parse arguments
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return 1
        
        # Print banner
        self.print_banner("CTMM Unified Tool - Comprehensive LaTeX Workflow Management")
        
        # Run the requested command
        if parsed_args.command in self.tools:
            try:
                success = self.tools[parsed_args.command](parsed_args)
                
                # Print summary
                self.print_section("Operation Summary")
                print(f"Operations run: {self.stats['operations_run']}")
                print(f"Operations successful: {self.stats['operations_successful']}")
                if self.stats['files_processed'] > 0:
                    print(f"Files processed: {self.stats['files_processed']}")
                
                success_rate = (self.stats['operations_successful'] / max(self.stats['operations_run'], 1)) * 100
                print(f"Success rate: {success_rate:.1f}%")
                
                if success:
                    print("\n🎉 Operation completed successfully!")
                    return 0
                else:
                    print("\n⚠️  Operation completed with issues.")
                    return 1
                    
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return 1
        else:
            logger.error(f"Unknown command: {parsed_args.command}")
            parser.print_help()
            return 1

def main():
    """Main entry point."""
    tool = CTMMUnifiedTool()
    return tool.run(sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main())