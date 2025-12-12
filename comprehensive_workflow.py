#!/usr/bin/env python3
"""
CTMM Comprehensive Workflow Integration
=======================================

This script demonstrates the complete "es ist nicht mehr weit" (it's not far anymore) 
comprehensive toolset for the CTMM project. It integrates all the key tools:

1. LaTeX de-escaping solution
2. Enhanced CTMM build system  
3. Validation and testing
4. Documentation generation

Usage:
    python3 comprehensive_workflow.py [--full] [--cleanup]
"""

import sys
import subprocess
import logging
from pathlib import Path
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def print_banner(title):
    """Print a formatted banner."""
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)

def print_step(step_num, description):
    """Print a formatted step."""
    print(f"\n{step_num}. {description}")
    print("-" * 50)

def run_command(cmd, description, check=True):
    """Run a command and handle errors gracefully."""
    try:
        print(f"Running: {description}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, errors='replace')
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            if check:
                return False
            return True
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        if check:
            return False
        return True

def comprehensive_workflow(args):
    """Execute the comprehensive CTMM workflow."""
    
    print_banner("CTMM COMPREHENSIVE WORKFLOW - 'es ist nicht mehr weit'")
    print("Integrating LaTeX de-escaping, build system, and validation")
    
    success_count = 0
    total_steps = 0
    
    # Step 1: Validate current state
    print_step(1, "System Validation")
    total_steps += 1
    
    if run_command("python3 validate_latex_syntax.py", "LaTeX syntax validation"):
        success_count += 1
    
    # Step 2: CTMM Build System Check
    print_step(2, "CTMM Build System Check")
    total_steps += 1
    
    if run_command("python3 ctmm_build.py", "CTMM build system check"):
        success_count += 1
    
    # Step 3: Unit Tests
    print_step(3, "Unit Test Validation")
    total_steps += 1
    
    if run_command("python3 test_ctmm_build.py", "Unit tests"):
        success_count += 1
    
    # Step 4: De-escaping workflow demonstration (if requested)
    if args.full:
        print_step(4, "LaTeX De-escaping Workflow")
        total_steps += 1
        
        if run_command("python3 conversion_workflow.py", "De-escaping workflow demo"):
            success_count += 1
    
    # Step 5: Build system analysis
    print_step(5 if args.full else 4, "Detailed Build Analysis")
    total_steps += 1
    
    if run_command("python3 build_system.py --verbose", "Detailed build analysis", check=False):
        success_count += 1
    
    # Step 6: Workflow structure test
    print_step(6 if args.full else 5, "Workflow Structure Test")
    total_steps += 1
    
    if run_command("python3 test_workflow_structure.py", "Workflow structure test"):
        success_count += 1
    
    # Step 7: Final validation
    final_step = 7 if args.full else 6
    print_step(final_step, "Final Integration Validation")
    total_steps += 1
    
    # Check that all key files exist and are functional
    key_files = [
        "main.tex",
        "ctmm_build.py", 
        "fix_latex_escaping.py",
        "conversion_workflow.py",
        "test_ctmm_build.py"
    ]
    
    missing_files = [f for f in key_files if not Path(f).exists()]
    if not missing_files:
        print("✅ All key workflow files present")
        success_count += 1
    else:
        print(f"❌ Missing key files: {missing_files}")
    
    # Step 8: Cleanup (if requested)
    if args.cleanup:
        print_step(final_step + 1, "Cleanup")
        run_command("make clean", "Cleaning build artifacts", check=False)
    
    # Summary
    print_banner("COMPREHENSIVE WORKFLOW SUMMARY")
    print(f"Steps completed: {success_count}/{total_steps}")
    print(f"Success rate: {(success_count/total_steps)*100:.1f}%")
    
    if success_count == total_steps:
        print("\n🎉 COMPREHENSIVE TOOLSET VALIDATION: SUCCESS")
        print("✅ The CTMM comprehensive toolset is fully operational!")
        print("\n📋 READY FOR:")
        print("  - Production LaTeX document creation")
        print("  - Automated de-escaping of converted files")
        print("  - Continuous integration workflows")
        print("  - Therapeutic material development")
    else:
        print(f"\n⚠️  VALIDATION INCOMPLETE: {total_steps - success_count} issues found")
        print("Please review the failed steps above.")
    
    print("\n" + "="*60)
    print("Workflow completed. 'es ist nicht mehr weit' - we've arrived!")
    print("="*60)
    
    return success_count == total_steps

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CTMM Comprehensive Workflow Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 comprehensive_workflow.py           # Basic workflow
  python3 comprehensive_workflow.py --full    # Include de-escaping demo
  python3 comprehensive_workflow.py --cleanup # Run with cleanup
        """
    )
    
    parser.add_argument(
        '--full', 
        action='store_true',
        help='Run full workflow including de-escaping demonstration'
    )
    
    parser.add_argument(
        '--cleanup',
        action='store_true', 
        help='Clean up build artifacts after completion'
    )
    
    args = parser.parse_args()
    
    # Ensure we're in the right directory
    if not Path('main.tex').exists():
        print("Error: This script must be run from the CTMM repository root")
        print("Expected to find main.tex in current directory")
        sys.exit(1)
    
    success = comprehensive_workflow(args)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()