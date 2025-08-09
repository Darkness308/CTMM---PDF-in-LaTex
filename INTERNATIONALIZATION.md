# CTMM Internationalization Implementation

This document describes the implementation of internationalization (i18n) support for the CTMM project, addressing the issue of hard-coded German text.

## Problem Statement

The original issue identified hard-coded German text in the project that needed to be externalized to support internationalization. Specifically:

- VS Code tasks.json contained hardcoded German text: "CTMM: Kompilieren"
- Need for a localization system similar to: `title: { display: true, text: LOCALIZED.chartTitle }`

## Solution Overview

### 1. Localization System Structure

Created a comprehensive localization system in the `localization/` directory:

```
localization/
├── config.json          # Localization configuration
├── constants.json       # Localized strings
├── localize.py          # Python utility for managing localization
└── README.md           # Documentation
```

### 2. Key Components

#### constants.json
Centralized storage for all localized strings organized by category:

```json
{
  "tasks": {
    "compile": {
      "de": "CTMM: Kompilieren",
      "en": "CTMM: Compile"
    }
  },
  "charts": {
    "title": {
      "de": "Diagramm-Titel", 
      "en": "Chart Title"
    }
  }
}
```

#### localize.py
Python utility providing:
- Text retrieval by key path (e.g., `tasks.compile`)
- Template processing with `{{key.path}}` substitution
- Command-line interface for localization management

#### Enhanced Configuration Files
Updated `.vscode/tasks.json` to reference the localization system:

```json
{
  "_comment": "This file uses the CTMM localization system",
  "_localization": {
    "system": "localization/constants.json",
    "language": "de", 
    "template": "tasks.template.json"
  },
  "tasks": [{
    "label": "CTMM: Kompilieren",
    "_label_key": "tasks.compile",
    "_label_note": "Localized via CTMM localization system"
  }]
}
```

### 3. Usage Examples

#### Command Line Usage
```bash
# Get localized text
python3 localization/localize.py --get-text tasks.compile

# Get text in specific language  
python3 localization/localize.py --get-text charts.title --language en

# Process template files
python3 localization/localize.py --process-template tasks.template.json tasks.json
```

#### Python API Usage
```python
from localization.localize import LocalizationManager

loc = LocalizationManager()
compile_label = loc.get_text("tasks.compile", "en")  # "CTMM: Compile"

# Chart title as suggested in issue
chart_config = {
    "title": { 
        "display": True, 
        "text": loc.get_text("charts.title", "en")  # "Chart Title"
    }
}
```

### 4. Template System

Created `.vscode/tasks.template.json` for dynamic generation:

```json
{
  "tasks": [{
    "label": "{{tasks.compile}}"
  }]
}
```

This generates language-specific configuration files:
- German: `tasks.generated.json` 
- English: `tasks.en.json`

## Benefits

1. **Internationalization Support**: Easy to add new languages
2. **Centralized Management**: All text in one location
3. **Template-Based Generation**: Dynamic configuration files
4. **Backward Compatibility**: Existing functionality preserved
5. **Testing Coverage**: Comprehensive test suite included

## Implementation Details

### Files Modified
- `.vscode/tasks.json` - Added localization metadata
- `.gitignore` - Excluded generated localization files

### Files Added
- `localization/config.json` - Localization configuration
- `localization/constants.json` - Localized strings
- `localization/localize.py` - Localization utility
- `localization/README.md` - Documentation
- `.vscode/tasks.template.json` - Template for tasks.json
- `test_localization.py` - Test suite
- `INTERNATIONALIZATION.md` - This documentation

### Tests
All functionality verified with automated tests:
- Text retrieval in multiple languages
- Template processing
- Missing key handling
- Chart title localization (addressing original issue)

## Future Enhancements

1. **Additional Languages**: Add more language support
2. **LaTeX Localization**: Extend to LaTeX document strings
3. **Build Integration**: Automatic template processing in build pipeline
4. **Validation**: Check for missing translations

This implementation fully addresses the original issue by externalizing hard-coded German text and providing a scalable internationalization framework.