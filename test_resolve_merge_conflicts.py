#!/usr/bin/env python3
"""
Test cases for resolve_merge_conflicts.py to verify conflict detection logic
"""

import re

def test_conflict_detection():
    """Test various conflict marker patterns"""
    
    # Compile regex patterns (same as in resolve_merge_conflicts.py)
    conflict_start_re = re.compile(r'^<{7}(\s|$)')
    conflict_sep_re = re.compile(r'^={7}(\s|$)')
    conflict_end_re = re.compile(r'^>{7}(\s|$)')
    
    # Test cases
    test_cases = [
        # Valid conflict markers
        ("<<<<<<< HEAD", True, "start"),
        ("<<<<<<< main", True, "start"),
        ("<<<<<<< feature-branch", True, "start"),
        ("<<<<<<< ", True, "start"),  # With trailing space
        ("<<<<<<<", True, "start"),  # Without space
        ("=======", True, "separator"),
        ("======= ", True, "separator"),  # With trailing space
        (">>>>>>> main", True, "end"),
        (">>>>>>> feature", True, "end"),
        (">>>>>>> ", True, "end"),
        (">>>>>>>", True, "end"),
        
        # Invalid markers (wrong number of chars)
        ("<<<<<< HEAD", False, "start"),  # Only 6 chars
        ("<<<<<<<< HEAD", False, "start"),  # 8 chars
        ("======", False, "separator"),  # Only 6 chars
        ("========", False, "separator"),  # 8 chars
        (">>>>>> main", False, "end"),  # Only 6 chars
        (">>>>>>>> main", False, "end"),  # 8 chars
        
        # Not at line start
        ("  <<<<<<< HEAD", False, "start"),
        ("  =======", False, "separator"),
        ("  >>>>>>> main", False, "end"),
    ]
    
    print("Testing conflict marker detection:")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for test_string, should_match, marker_type in test_cases:
        if marker_type == "start":
            matches = bool(conflict_start_re.match(test_string))
        elif marker_type == "separator":
            matches = bool(conflict_sep_re.match(test_string))
        else:  # end
            matches = bool(conflict_end_re.match(test_string))
        
        if matches == should_match:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1
        
        expected = "should match" if should_match else "should NOT match"
        result = "matched" if matches else "did not match"
        print(f"{status}: '{test_string}' ({marker_type}) - {expected}, {result}")
    
    print("=" * 70)
    print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(test_conflict_detection())
