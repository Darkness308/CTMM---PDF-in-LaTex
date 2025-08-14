#!/usr/bin/env python3
"""
CI Build Analyzer for CTMM LaTeX System
Provides enhanced analysis and reporting for CI/CD environments.
"""

import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime
import ctmm_build

# Configure logging for CI environment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - CI-ANALYZER - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CIBuildAnalyzer:
    """Enhanced build analysis for CI environments."""
    
    def __init__(self):
        self.ci_info = ctmm_build.detect_ci_environment()
        self.latex_available = ctmm_build.check_latex_availability()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self.ci_info,
            "latex_available": self.latex_available,
            "tests": {}
        }
    
    def run_comprehensive_analysis(self):
        """Run comprehensive CI build analysis."""
        logger.info("Starting comprehensive CI build analysis...")
        
        # Basic dependency checks
        self.check_python_dependencies()
        self.check_latex_packages()
        
        # Build system tests
        self.test_build_system()
        
        # File integrity checks
        self.verify_file_integrity()
        
        # Generate CI report
        self.generate_ci_report()
        
        return self.results
    
    def check_python_dependencies(self):
        """Check Python dependencies required for build system."""
        logger.info("Checking Python dependencies...")
        
        required_modules = ['re', 'subprocess', 'pathlib', 'logging']
        optional_modules = ['chardet']
        
        missing_required = []
        missing_optional = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_required.append(module)
        
        for module in optional_modules:
            try:
                __import__(module)
            except ImportError:
                missing_optional.append(module)
        
        self.results["tests"]["python_dependencies"] = {
            "required_missing": missing_required,
            "optional_missing": missing_optional,
            "status": "PASS" if not missing_required else "FAIL"
        }
        
        if missing_required:
            logger.error("Missing required Python modules: %s", missing_required)
        if missing_optional:
            logger.warning("Missing optional Python modules: %s", missing_optional)
        
        logger.info("Python dependency check: %s", self.results["tests"]["python_dependencies"]["status"])
    
    def check_latex_packages(self):
        """Check LaTeX package availability in CI environment."""
        logger.info("Checking LaTeX package availability...")
        
        if not self.latex_available:
            self.results["tests"]["latex_packages"] = {
                "status": "SKIPPED",
                "reason": "LaTeX not available"
            }
            logger.warning("Skipping LaTeX package check - LaTeX not available")
            return
        
        # Required packages for CTMM system
        required_packages = [
            'xcolor', 'hyperref', 'fontawesome5', 'tcolorbox', 
            'tabularx', 'amssymb', 'babel', 'inputenc', 'fontenc'
        ]
        
        package_status = {}
        
        for package in required_packages:
            try:
                # Test package availability
                test_content = f"""\\documentclass{{article}}
\\usepackage{{{package}}}
\\begin{{document}}
Test
\\end{{document}}"""
                
                with open('package_test.tex', 'w') as f:
                    f.write(test_content)
                
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', 'package_test.tex'],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                package_status[package] = "AVAILABLE" if result.returncode == 0 else "MISSING"
                
            except Exception as e:
                package_status[package] = f"ERROR: {e}"
            finally:
                # Cleanup
                for ext in ['.tex', '.aux', '.log', '.pdf']:
                    cleanup_file = Path(f'package_test{ext}')
                    if cleanup_file.exists():
                        cleanup_file.unlink(missing_ok=True)
        
        missing_packages = [pkg for pkg, status in package_status.items() if status != "AVAILABLE"]
        
        self.results["tests"]["latex_packages"] = {
            "packages": package_status,
            "missing": missing_packages,
            "status": "PASS" if not missing_packages else "FAIL"
        }
        
        if missing_packages:
            logger.error("Missing LaTeX packages: %s", missing_packages)
        else:
            logger.info("All required LaTeX packages available")
    
    def test_build_system(self):
        """Test the CTMM build system comprehensively."""
        logger.info("Testing CTMM build system...")
        
        try:
            # Run build system and capture results
            references = ctmm_build.scan_references()
            all_files = references["style_files"] + references["module_files"]
            missing_files = ctmm_build.check_missing_files(all_files)
            
            basic_build_ok = ctmm_build.test_basic_build()
            full_build_ok = ctmm_build.test_full_build()
            
            self.results["tests"]["build_system"] = {
                "style_files": len(references["style_files"]),
                "module_files": len(references["module_files"]),
                "missing_files": len(missing_files),
                "basic_build": "PASS" if basic_build_ok else "FAIL",
                "full_build": "PASS" if full_build_ok else "FAIL",
                "status": "PASS" if (basic_build_ok and full_build_ok) else "FAIL"
            }
            
            logger.info("Build system test: %s", self.results["tests"]["build_system"]["status"])
            
        except Exception as e:
            self.results["tests"]["build_system"] = {
                "status": "ERROR",
                "error": str(e)
            }
            logger.error("Build system test failed: %s", e)
    
    def verify_file_integrity(self):
        """Verify integrity of critical project files."""
        logger.info("Verifying file integrity...")
        
        critical_files = [
            'main.tex',
            'ctmm_build.py',
            'test_ctmm_build.py',
            '.github/workflows/latex-build.yml',
            '.github/workflows/latex-validation.yml'
        ]
        
        file_status = {}
        
        for file_path in critical_files:
            path = Path(file_path)
            if path.exists():
                try:
                    # Check if file is readable
                    with open(path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    file_status[file_path] = {
                        "exists": True,
                        "readable": True,
                        "size": path.stat().st_size,
                        "status": "OK"
                    }
                except Exception as e:
                    file_status[file_path] = {
                        "exists": True,
                        "readable": False,
                        "error": str(e),
                        "status": "ERROR"
                    }
            else:
                file_status[file_path] = {
                    "exists": False,
                    "status": "MISSING"
                }
        
        failed_files = [f for f, status in file_status.items() if status["status"] != "OK"]
        
        self.results["tests"]["file_integrity"] = {
            "files": file_status,
            "failed": failed_files,
            "status": "PASS" if not failed_files else "FAIL"
        }
        
        if failed_files:
            logger.error("File integrity issues: %s", failed_files)
        else:
            logger.info("All critical files verified")
    
    def generate_ci_report(self):
        """Generate comprehensive CI report."""
        logger.info("Generating CI analysis report...")
        
        # Summary statistics
        total_tests = len(self.results["tests"])
        passed_tests = len([t for t in self.results["tests"].values() if t.get("status") == "PASS"])
        failed_tests = len([t for t in self.results["tests"].values() if t.get("status") == "FAIL"])
        error_tests = len([t for t in self.results["tests"].values() if t.get("status") == "ERROR"])
        skipped_tests = len([t for t in self.results["tests"].values() if t.get("status") == "SKIPPED"])
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "skipped": skipped_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "overall_status": "PASS" if failed_tests == 0 and error_tests == 0 else "FAIL"
        }
        
        # Save detailed report
        report_file = "ci_analysis_report.json"
        try:
            with open(report_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            logger.info("Detailed report saved to %s", report_file)
        except Exception as e:
            logger.error("Failed to save report: %s", e)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print analysis summary to console."""
        summary = self.results["summary"]
        
        print("\n" + "="*60)
        print("CI BUILD ANALYSIS SUMMARY")
        print("="*60)
        print(f"Environment: {', '.join(self.ci_info['environments']) if self.ci_info['is_ci'] else 'Local'}")
        print(f"LaTeX Available: {'Yes' if self.latex_available else 'No'}")
        print(f"Timestamp: {self.results['timestamp']}")
        print("-"*60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Errors: {summary['errors']}")
        print(f"Skipped: {summary['skipped']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Overall Status: {summary['overall_status']}")
        print("="*60)
        
        # Test details
        for test_name, test_result in self.results["tests"].items():
            status = test_result.get("status", "UNKNOWN")
            print(f"{test_name}: {status}")
            if status == "FAIL" and "missing" in test_result:
                print(f"  Missing: {test_result['missing']}")
            elif status == "ERROR" and "error" in test_result:
                print(f"  Error: {test_result['error']}")


def main():
    """Main function for CI build analysis."""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("""
CI Build Analyzer for CTMM LaTeX System

Usage: python3 ci_build_analyzer.py

This tool performs comprehensive analysis of the build environment
and generates detailed reports for CI/CD troubleshooting.

Features:
- Python dependency verification
- LaTeX package availability checking
- Build system testing
- File integrity verification
- Comprehensive CI reporting
        """)
        return 0
    
    analyzer = CIBuildAnalyzer()
    results = analyzer.run_comprehensive_analysis()
    
    # Return appropriate exit code for CI
    return 0 if results["summary"]["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())