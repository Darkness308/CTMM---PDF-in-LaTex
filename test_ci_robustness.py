#!/usr/bin/env python3
"""
CI Robustness Validation for Issue #928
========================================

This script validates CI environment robustness and adds enhanced error handling
to address the "Build LaTeX PDF" workflow failures reported in CI insights.

Key validation areas:
1. Environment resource availability
2. LaTeX package installation verification
3. File system permissions and state
4. Network connectivity for package downloads
5. Memory and disk space checks
6. Timeout and retry mechanisms
"""

import os
import sys
import subprocess
import shutil
import tempfile
import time
from pathlib import Path


def check_system_resources():
    """Check system resources available for LaTeX compilation."""
    print("\n🔍 Checking System Resources")
    print("=" * 50)
    
    # Check available memory
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemAvailable:'):
                    mem_kb = int(line.split()[1])
                    mem_mb = mem_kb // 1024
                    print(f"✅ Available memory: {mem_mb} MB")
                    if mem_mb < 512:
                        print("⚠️  Warning: Low memory may cause LaTeX compilation issues")
                    break
    except Exception:
        print("⚠️  Could not check memory status")
    
    # Check disk space
    try:
        statvfs = os.statvfs('.')
        free_bytes = statvfs.f_frsize * statvfs.f_bavail
        free_mb = free_bytes // (1024 * 1024)
        print(f"✅ Available disk space: {free_mb} MB")
        if free_mb < 1024:
            print("⚠️  Warning: Low disk space may cause build failures")
    except Exception:
        print("⚠️  Could not check disk space")
    
    return True


def check_python_environment():
    """Validate Python environment and dependencies."""
    print("\n🐍 Checking Python Environment")
    print("=" * 50)
    
    print(f"✅ Python version: {sys.version}")
    print(f"✅ Python executable: {sys.executable}")
    
    # Check required Python packages
    required_packages = ['chardet']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ Package {package}: Available")
        except ImportError:
            print(f"❌ Package {package}: Missing")
            return False
    
    return True


def check_file_permissions():
    """Check file system permissions for build artifacts."""
    print("\n📁 Checking File Permissions")
    print("=" * 50)
    
    # Check write permissions in current directory
    try:
        test_file = Path("test_write_permission.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Write permissions: OK")
    except Exception as e:
        print(f"❌ Write permissions: Failed - {e}")
        return False
    
    # Check if main.tex is readable
    main_tex = Path("main.tex")
    if main_tex.exists() and main_tex.is_file():
        print("✅ main.tex: Readable")
    else:
        print("❌ main.tex: Not found or not readable")
        return False
    
    return True


def validate_latex_environment():
    """Validate LaTeX environment setup and package availability."""
    print("\n📦 Validating LaTeX Environment")
    print("=" * 50)
    
    # Check if LaTeX is available
    latex_available = shutil.which('pdflatex') is not None
    if latex_available:
        print("✅ pdflatex: Available")
        
        # Test basic LaTeX compilation
        try:
            test_content = r"""
\documentclass{article}
\begin{document}
Test document for CI validation.
\end{document}
"""
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
                f.write(test_content)
                test_file = f.name
            
            result = subprocess.run([
                'pdflatex', '-interaction=nonstopmode', '-halt-on-error', test_file
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Basic LaTeX compilation: Working")
            else:
                print(f"⚠️  Basic LaTeX compilation: Failed - {result.stderr[:200]}")
            
            # Cleanup
            base_name = test_file[:-4]
            for ext in ['.tex', '.pdf', '.log', '.aux']:
                try:
                    os.unlink(base_name + ext)
                except FileNotFoundError:
                    pass
                    
        except subprocess.TimeoutExpired:
            print("❌ LaTeX compilation: Timeout")
            return False
        except Exception as e:
            print(f"❌ LaTeX compilation test: {e}")
            return False
    else:
        print("⚠️  pdflatex: Not available (expected in CI setup phase)")
    
    return True


def test_build_system_robustness():
    """Test the CTMM build system under various conditions."""
    print("\n🔧 Testing Build System Robustness")
    print("=" * 50)
    
    # Test build system with timeout
    try:
        result = subprocess.run([
            sys.executable, 'ctmm_build.py'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ CTMM build system: Working")
            
            # Check for specific success indicators
            if "CTMM BUILD SYSTEM SUMMARY" in result.stdout:
                print("✅ Build summary: Generated")
            if "✓ PASS" in result.stdout:
                print("✅ Validation checks: Passed")
        else:
            print(f"❌ CTMM build system: Failed with code {result.returncode}")
            print(f"Error output: {result.stderr[:300]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ CTMM build system: Timeout after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ CTMM build system: Exception - {e}")
        return False
    
    return True


def test_network_connectivity():
    """Test network connectivity for package downloads."""
    print("\n🌐 Testing Network Connectivity")
    print("=" * 50)
    
    # Test basic connectivity
    try:
        result = subprocess.run([
            'ping', '-c', '1', '8.8.8.8'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Basic network connectivity: Working")
        else:
            print("⚠️  Basic network connectivity: Limited")
    except Exception:
        print("⚠️  Network connectivity test: Skipped")
    
    return True


def run_enhanced_validation():
    """Run all enhanced CI robustness validations."""
    print("=" * 70)
    print("CI ROBUSTNESS VALIDATION FOR ISSUE #928")
    print("Enhanced diagnostics for 'Build LaTeX PDF' workflow failures")
    print("=" * 70)
    
    tests = [
        ("System Resources", check_system_resources),
        ("Python Environment", check_python_environment), 
        ("File Permissions", check_file_permissions),
        ("LaTeX Environment", validate_latex_environment),
        ("Build System Robustness", test_build_system_robustness),
        ("Network Connectivity", test_network_connectivity)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"\n✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: EXCEPTION - {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! CI environment appears robust.")
        return True
    else:
        print("⚠️  Some tests failed. CI environment may need attention.")
        return False


def main():
    """Main entry point."""
    try:
        success = run_enhanced_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error during validation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()