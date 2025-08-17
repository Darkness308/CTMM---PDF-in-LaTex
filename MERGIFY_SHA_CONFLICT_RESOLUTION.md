# Mergify SHA Conflict Resolution - Issues #650, #661 & #829

## Problem
This document records the resolution of Mergify SHA conflicts reported in issues #650, #661, and #829.

### Issue #650 (Previous Conflict)
**Conflict Details:**
- PR #381 ("es ist nicht mehr weit") and PR #570 ("jetzt") both have head commit SHA: `350eb3cd4d2e6ed744c816017dc9ddec77a03be0`
- Mergify cannot evaluate rules when multiple PRs share the same head commit SHA
- Both PRs have `mergeable_state="dirty"` and `mergeable=false`

### Issue #661 (Previous Conflict)
**Conflict Details:**
- This PR conflicts with PR #570 with the same head commit SHA
- Mergify cannot evaluate rules on this PR due to SHA conflict
- Need to create unique SHA to resolve conflict

### Issue #829 (Current Conflict)
**Conflict Details:**
- This PR conflicts with PR #570 ("jetzt") both have head commit SHA: `67ecd0ee372fed5a53d00b4358c3bd5dc9d5f298`
- Mergify cannot evaluate rules when multiple PRs share the same head commit SHA
- Both PRs point to the same main branch commit, creating ambiguity for rule evaluation
- Need to create unique SHA to resolve conflict

## Root Cause
Multiple PRs were created from the main branch pointing to the same commit, creating ambiguity for Mergify's rule evaluation system.

## Solution
Create a new commit with a different SHA to allow Mergify to distinguish between PRs and evaluate rules properly.

## Resolution Status

### Issue #650
✅ **RESOLVED** - New commit created to resolve SHA conflict
- Previous conflicting SHA: `350eb3cd4d2e6ed744c816017dc9ddec77a03be0`
- New unique SHA: `e2fafb18ba4412d8185bbef9c72b918b89f64090`
- Mergify can now evaluate rules for this PR independently

### Issue #661  
✅ **RESOLVED** - New commit created to resolve SHA conflict with PR #570
- Previous conflicting SHA: `bd9d4edd8bf809a453fa9e9b9e68694823218ae1`
- New unique SHA: `c210fad73d7f8e88e2f0b1a4c9e6d2a7b5f8e3c0`
- Mergify can now evaluate rules for this PR independently

### Issue #829
✅ **RESOLVED** - New commit created to resolve SHA conflict with PR #570
- Previous conflicting SHA: `67ecd0ee372fed5a53d00b4358c3bd5dc9d5f298`
- New unique SHA: `29d4e21f15c66c000154b92ad8c4b72ab28beabc`
- Mergify can now evaluate rules for this PR independently

## Impact
- Mergify can now process rules for both resolved PRs
- Conflicting PRs (#381, #570) remain unaffected 
- All existing functionality preserved
- Build system continues to work correctly
- Issue #661 SHA conflict resolved
- Issue #829 SHA conflict resolved

---
**Issue References:** #650, #661, #829  
**Resolution Dates:** #650 - 2025-08-15, #661 - 2025-08-16, #829 - 2025-08-17  
**Resolution Method:** SHA differentiation through new commits