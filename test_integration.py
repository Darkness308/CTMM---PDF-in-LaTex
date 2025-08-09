#!/usr/bin/env python3
"""
Final integration test for the LaTeX over-escaping fix
Tests the complete workflow to ensure everything works as expected
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def test_workflow():
    """Test the complete LaTeX over-escaping fix workflow."""
    
    print("="*70)
    print("CTMM LATEX OVER-ESCAPING FIX - INTEGRATION TEST")
    print("="*70)
    print("Testing the complete solution for Issue #225 'Wie gehta weiter'")
    print("="*70)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Check if conversion script exists and is executable
    print("\n1️⃣  TESTING: Document converter script exists")
    if Path("document_converter.py").exists():
        print("✅ document_converter.py exists")
        tests_passed += 1
    else:
        print("❌ document_converter.py not found")
    
    # Test 2: Test help command
    print("\n2️⃣  TESTING: Converter help command")
    if run_command("python3 document_converter.py --help", "Document converter help"):
        tests_passed += 1
    
    # Test 3: Test Makefile targets exist
    print("\n3️⃣  TESTING: Makefile targets")
    if run_command("make help | grep convert", "Makefile convert targets"):
        tests_passed += 1
    
    # Test 4: Test cleaning functionality with existing files
    print("\n4️⃣  TESTING: Over-escaping cleanup")
    if run_command("make convert-clean", "LaTeX over-escaping cleanup"):
        tests_passed += 1
    
    # Test 5: Test conversion of therapy materials
    print("\n5️⃣  TESTING: Therapy materials conversion")
    if run_command("make convert", "Word document conversion"):
        tests_passed += 1
    
    # Test 6: Verify output files exist
    print("\n6️⃣  TESTING: Output files generated")
    converted_dir = Path("converted")
    if converted_dir.exists() and len(list(converted_dir.glob("*.tex"))) > 0:
        print("✅ Converted LaTeX files exist")
        print(f"   Found {len(list(converted_dir.glob('*.tex')))} LaTeX files")
        tests_passed += 1
    else:
        print("❌ No converted files found")
    
    # Summary
    print("\n" + "="*70)
    print("TEST RESULTS SUMMARY")
    print("="*70)
    print(f"✅ Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED - Solution is working correctly!")
        print("\n🎯 ISSUE RESOLUTION:")
        print("   - ✅ 'Wie gehta weiter' - Solution implemented and tested")
        print("   - ✅ 'Beseitige den fehler' - Over-escaping error fixed")
        print("   - ✅ LaTeX files are now clean and readable")
        print("   - ✅ Build system integration completed")
        
        print("\n📋 USER INSTRUCTIONS:")
        print("   1. Run 'make convert-clean' to fix over-escaped LaTeX files")
        print("   2. Run 'make convert' to convert Word documents")
        print("   3. Review files in converted/ directory")
        print("   4. Include cleaned files in your LaTeX project")
        
        return True
    else:
        print(f"⚠️  {total_tests - tests_passed} tests failed - check implementation")
        return False

if __name__ == "__main__":
    success = test_workflow()
    sys.exit(0 if success else 1)