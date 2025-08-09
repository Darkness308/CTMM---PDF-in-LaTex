# CTMM Localization System

This directory contains the internationalization (i18n) system for the CTMM project.

## Files

- `config.json` - Localization configuration (default language, supported languages, etc.)
- `constants.json` - Localized strings organized by category and key
- `localize.py` - Python utility for managing localized strings

## Usage

### Command Line Tool

```bash
# Get localized text for a specific key
python3 localization/localize.py --get-text tasks.compile

# Get text in a specific language
python3 localization/localize.py --get-text tasks.compile --language en

# Update VS Code tasks.json with localized strings
python3 localization/localize.py --update-tasks
```

### Python API

```python
from localization.localize import LocalizationManager

loc = LocalizationManager()
text = loc.get_text("tasks.compile", "en")  # Returns "CTMM: Compile"
```

## Adding New Localized Strings

1. Add the string to `constants.json` following the existing structure:
   ```json
   {
     "category": {
       "key": {
         "de": "German text",
         "en": "English text"
       }
     }
   }
   ```

2. Use the `localize.py` utility to retrieve the text in your code or configuration files.

## Supported Languages

- `de` (German) - Default language
- `en` (English) - Fallback language

Add new languages by updating `config.json` and adding the corresponding translations to `constants.json`.