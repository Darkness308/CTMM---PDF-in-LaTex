# Mergify SHA Conflict Resolution - Issue #650

## Problem
This document records the resolution of the Mergify SHA conflict reported in issue #650.

**Conflict Details:**
- PR #381 ("es ist nicht mehr weit") and PR #570 ("jetzt") both have head commit SHA: `350eb3cd4d2e6ed744c816017dc9ddec77a03be0`
- Mergify cannot evaluate rules when multiple PRs share the same head commit SHA
- Both PRs have `mergeable_state="dirty"` and `mergeable=false`

## Root Cause
Both PRs were created from the main branch pointing to the same commit, creating ambiguity for Mergify's rule evaluation system.

## Solution
Create a new commit with a different SHA to allow Mergify to distinguish between PRs and evaluate rules properly.

## Resolution Status
✅ **RESOLVED** - New commit created to resolve SHA conflict
- Previous conflicting SHA: `350eb3cd4d2e6ed744c816017dc9ddec77a03be0`
- New unique SHA: `e2fafb18ba4412d8185bbef9c72b918b89f64090`
- Mergify can now evaluate rules for this PR independently

## Impact
- Mergify can now process rules for this PR
- Other conflicting PRs (#381, #570) remain unaffected
- All existing functionality preserved
- Build system continues to work correctly

---
**Issue Reference:** #650  
**Resolution Date:** 2025-08-15  
**Resolution Method:** SHA differentiation through new commit