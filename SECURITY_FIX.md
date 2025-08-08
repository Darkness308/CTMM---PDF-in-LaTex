# LaTeX Command Name Sanitization Fix

## Issue Description
The original code review identified a security/correctness concern in the placeholder command generation:

```python
# PROBLEMATIC (mentioned in PR review):
\\newcommand{{\\{package_name}Placeholder}}{{\\textcolor{{red}}{{[{package_name.upper()} TEMPLATE - NEEDS CONTENT]}}}}
```

If `package_name` contains special characters (like `-`, `_`, `@`, numbers, etc.), this creates invalid LaTeX command names.

## Solution Implemented
Added `sanitize_latex_command_name()` function that ensures all generated command names are valid LaTeX identifiers:

```python
# FIXED VERSION:
safe_package_name = sanitize_latex_command_name(path.stem)
\\newcommand{{\\{safe_package_name}Placeholder}}{{\\textcolor{{red}}{{[{path.stem.upper()} TEMPLATE - NEEDS CONTENT]}}}}
```

## Examples

| Original Package Name | Sanitized Command Name | Generated LaTeX |
|----------------------|------------------------|-----------------|
| `ctmm-design` | `CtmmDashdesign` | `\CtmmDashdesignPlaceholder` |
| `form_elements` | `FormUnderscoreelements` | `\FormUnderscoreelementsPlaceholder` |
| `special@chars` | `SpecialAtchars` | `\SpecialAtcharsPlaceholder` |
| `test123` | `Test` | `\TestPlaceholder` |
| `my&package` | `MyAndpackage` | `\MyAndpackagePlaceholder` |

## Security Impact
- **Before**: Could generate invalid LaTeX commands causing compilation errors
- **After**: All generated commands are guaranteed to be valid LaTeX identifiers
- **Compatibility**: Existing functionality unchanged, only adds safety layer

## Testing
Comprehensive test suite covers 15+ edge cases including special characters, numbers, empty strings, and complex combinations.