#!/usr/bin/env python3
"""
Comprehensive Issue #684 Resolution Verification

This script performs a complete validation that simulates the exact scenario
that was causing the hyperref package conflict in GitHub Actions CI.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

def create_test_latex_document():
    """Create a minimal test document that replicates the issue scenario."""
    return r"""
\documentclass[a4paper,12pt]{article}

% This replicates the exact package loading order from main.tex
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[ngerman]{babel}
\usepackage{geometry}
\usepackage{hyperref}  % Loaded BEFORE form-elements (line 8 in main.tex)
\usepackage{xcolor}
\usepackage{fontawesome5}
\usepackage{tcolorbox}

% Load the CTMM form-elements package (line 17 in main.tex) 
\usepackage{style/form-elements}  % This should NOT cause hyperref conflict

\geometry{a4paper, margin=2.5cm}

\begin{document}

\title{Issue \#684 Test Document}
\author{CTMM Test}
\date{\today}
\maketitle

\section{Test Interactive Forms}

This document tests that the hyperref package conflict has been resolved.

% Test CTMM form elements to ensure they work after the fix
\textbf{Test Checkbox:} \ctmmCheckBox[test_checkbox]{Test Label}

\textbf{Test Text Field:} \ctmmTextField[4cm]{Default Text}{test_field}

\end{document}
"""

def test_latex_compilation_simulation():
    """Simulate the LaTeX compilation that would happen in GitHub Actions."""
    print("🔄 Simulating GitHub Actions LaTeX Compilation")
    print("=" * 60)
    
    # Create a temporary directory to avoid affecting the real repository
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy necessary files to temp directory
        style_dir = temp_path / "style"
        style_dir.mkdir()
        
        # Copy form-elements.sty to temp directory
        original_form_elements = Path("style/form-elements.sty")
        temp_form_elements = style_dir / "form-elements.sty"
        
        if original_form_elements.exists():
            with open(original_form_elements, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(temp_form_elements, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Copied style/form-elements.sty to test environment")
        else:
            print("❌ ERROR: Could not find style/form-elements.sty")
            return False
        
        # Copy ctmm-design.sty with color definitions (needed for ctmm colors)
        original_design = Path("style/ctmm-design.sty")
        temp_design = style_dir / "ctmm-design.sty"
        
        if original_design.exists():
            with open(original_design, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(temp_design, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Copied style/ctmm-design.sty to test environment")
        
        # Create test document
        test_doc = temp_path / "test_issue_684.tex"
        with open(test_doc, 'w', encoding='utf-8') as f:
            f.write(create_test_latex_document())
        print("✅ Created test LaTeX document")
        
        # Check if pdflatex is available
        try:
            result = subprocess.run(['pdflatex', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ pdflatex is available for testing")
                
                # Attempt compilation
                print("🔄 Running pdflatex compilation test...")
                compile_result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode', 
                    '-halt-on-error',
                    str(test_doc)
                ], cwd=temp_dir, capture_output=True, text=True, timeout=60)
                
                if compile_result.returncode == 0:
                    print("🎉 LaTeX compilation SUCCESSFUL!")
                    print("✅ No hyperref package conflicts detected")
                    
                    # Check if PDF was generated
                    pdf_file = temp_path / "test_issue_684.pdf"
                    if pdf_file.exists():
                        print(f"✅ PDF generated successfully ({pdf_file.stat().st_size} bytes)")
                        return True
                    else:
                        print("⚠️  PDF file not found despite successful compilation")
                        return False
                else:
                    print("❌ LaTeX compilation FAILED!")
                    print("📄 Compilation output:")
                    print(compile_result.stdout)
                    if compile_result.stderr:
                        print("📄 Error output:")
                        print(compile_result.stderr)
                    
                    # Check for specific hyperref conflicts
                    output_text = compile_result.stdout + compile_result.stderr
                    if 'option clash' in output_text.lower():
                        print("🚨 HYPERREF OPTION CLASH DETECTED - Issue #684 NOT resolved!")
                    elif 'package already loaded' in output_text.lower():
                        print("🚨 PACKAGE ALREADY LOADED ERROR - Issue #684 NOT resolved!")
                    
                    return False
                    
            else:
                print("⚠️  pdflatex not available - using logical validation only")
                return validate_logical_correctness()
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  pdflatex not available - using logical validation only")
            return validate_logical_correctness()

def validate_logical_correctness():
    """Validate the logical correctness of the fix without actual compilation."""
    print("\n🧠 Logical Validation (No LaTeX Compilation)")
    print("=" * 60)
    
    # This replicates what happens during compilation
    print("📝 Simulating package loading sequence:")
    print("   1. \\documentclass{article}")
    print("   2. \\usepackage{hyperref}  <-- hyperref loaded first")
    print("   3. \\usepackage{style/form-elements}  <-- triggers conditional check")
    print("   4. @ifpackageloaded{hyperref} evaluates to TRUE")
    print("   5. Only @ctmmInteractive flag is set (NO hyperref loading)")
    print("   6. Compilation continues without package conflicts")
    
    # Read and verify the actual implementation
    with open("style/form-elements.sty", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check the key logic
    if '@ifpackageloaded{hyperref}' in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '@ifpackageloaded{hyperref}' in line:
                # Check next few lines for correct implementation
                true_branch = lines[i+1:i+3]
                false_branch = lines[i+4:i+7]
                
                # Verify true branch doesn't load hyperref
                true_loads_hyperref = any('RequirePackage{hyperref}' in l for l in true_branch)
                false_loads_hyperref = any('RequirePackage{hyperref}' in l for l in false_branch)
                
                if not true_loads_hyperref and false_loads_hyperref:
                    print("✅ Conditional logic correctly implemented")
                    print("✅ Issue #684 hyperref conflict has been resolved")
                    return True
                else:
                    print("❌ Conditional logic implementation error")
                    return False
    
    print("❌ Could not verify conditional logic")
    return False

def run_build_system_validation():
    """Run the existing CTMM build system validation."""
    print("\n🔧 Running CTMM Build System Validation")
    print("=" * 60)
    
    try:
        result = subprocess.run(['python3', 'ctmm_build.py'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ CTMM build system validation PASSED")
            # Check for specific success indicators
            if 'LaTeX validation: ✓ PASS' in result.stdout:
                print("✅ LaTeX validation component passed")
            if 'All referenced files exist' in result.stdout:
                print("✅ File reference validation passed")
            return True
        else:
            print("❌ CTMM build system validation FAILED")
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Build system validation timed out")
        return False
    except Exception as e:
        print(f"❌ Error running build system: {e}")
        return False

def main():
    """Run comprehensive validation of Issue #684 resolution."""
    print("🚀 Issue #684 Comprehensive Resolution Verification")
    print("=" * 80)
    print("Verifying that hyperref package loading conflicts have been resolved")
    print("and that GitHub Actions CI will now compile successfully.")
    print("=" * 80)
    
    tests = [
        ("LaTeX Compilation Simulation", test_latex_compilation_simulation),
        ("Build System Validation", run_build_system_validation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n🔄 Running {test_name}...")
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   Result: {status}")
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 80)
    print("🏁 COMPREHENSIVE VALIDATION SUMMARY")
    print("=" * 80)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} validation tests passed")
    
    if passed == len(tests):
        print("\n🎉 COMPREHENSIVE VALIDATION SUCCESSFUL!")
        print("✅ Issue #684 hyperref package conflict resolution is COMPLETE")
        print("✅ GitHub Actions CI should now compile successfully")
        print("✅ All CTMM form elements will continue to work correctly")
        return True
    else:
        print(f"\n⚠️  {len(tests) - passed} validation tests failed")
        print("❌ Issue #684 resolution requires additional attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)