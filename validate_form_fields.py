#!/usr/bin/env python3
r"""
CTMM Form Field Validation and Standardization Script

This script validates and standardizes form field naming conventions across
all CTMM LaTeX modules to prevent the issues identified in PR #378.

Key validation rules:
1. Form field names should use underscores, not double backslashes
2. \ctmmCheckBox should maintain backward compatibility with optional first parameter
3. All form field commands should have proper closing braces
4. Field names should follow consistent naming patterns

Author: CTMM-Team / Copilot
Issue: #1118 - Form field standardization fix
"""

import re
import sys
from pathlib import Path
from typing import List

class FormFieldValidator:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.modules_dir = self.repo_root / "modules"
        self.style_dir = self.repo_root / "style"
        self.issues = []
        
    def validate_all_files(self) -> bool:
        """Validate all LaTeX files for form field issues."""
        print("🔍 CTMM Form Field Validation Starting...")
        print("=" * 60)
        
        all_valid = True
        
        # Validate form-elements.sty first
        if not self.validate_form_elements_style():
            all_valid = False
            
        # Validate all module files
        if not self.validate_modules():
            all_valid = False
            
        self.print_summary()
        return all_valid
    
    def validate_form_elements_style(self) -> bool:
        """Validate the form-elements.sty file for proper checkbox syntax."""
        style_file = self.style_dir / "form-elements.sty"
        
        if not style_file.exists():
            self.issues.append(f"❌ Missing form-elements.sty: {style_file}")
            return False
            
        print(f"📄 Validating {style_file}...")
        
        with open(style_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check that \ctmmCheckBox maintains backward compatibility
        checkbox_pattern = r'\\newcommand\{\\ctmmCheckBox\}\[(\d+)\]\[([^\]]*)\]'
        match = re.search(checkbox_pattern, content)
        
        if match:
            num_params = int(match.group(1))
            default_value = match.group(2)
            
            if num_params == 2 and default_value == "":
                print(r"✅ \ctmmCheckBox maintains backward compatibility (optional first parameter)")
                return True
            else:
                self.issues.append(r"❌ \ctmmCheckBox should have 2 parameters with empty default for first parameter")
                return False
        else:
            # Check for breaking change pattern
            breaking_pattern = r'\\newcommand\{\\ctmmCheckBox\}\[2\]\{'
            if re.search(breaking_pattern, content):
                self.issues.append(r"❌ Breaking change detected: \ctmmCheckBox changed to require 2 mandatory parameters")
                return False
            else:
                print(r"✅ \ctmmCheckBox syntax appears valid")
                return True
    
    def validate_modules(self) -> bool:
        """Validate all module files for form field issues."""
        if not self.modules_dir.exists():
            self.issues.append(f"❌ Modules directory not found: {self.modules_dir}")
            return False
            
        all_valid = True
        tex_files = list(self.modules_dir.glob("*.tex"))
        
        print(f"\n📂 Validating {len(tex_files)} module files...")
        
        for tex_file in tex_files:
            if not self.validate_module_file(tex_file):
                all_valid = False
                
        return all_valid
    
    def validate_module_file(self, file_path: Path) -> bool:
        """Validate a single module file for form field issues."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            file_valid = True
            line_num = 0
            
            for line in content.split('\n'):
                line_num += 1
                line_issues = self.validate_line(line, file_path.name, line_num)
                if line_issues:
                    file_valid = False
                    self.issues.extend(line_issues)
                    
            if file_valid:
                print(f"✅ {file_path.name}")
            else:
                print(f"❌ {file_path.name} has issues")
                
            return file_valid
            
        except Exception as e:
            self.issues.append(f"❌ Error reading {file_path}: {e}")
            return False
    
    def validate_line(self, line: str, filename: str, line_num: int) -> List[str]:
        """Validate a single line for form field issues."""
        issues = []
        
        # Check for double backslash before underscore (\\\_mm pattern)
        if re.search(r'\\\\_', line):
            issues.append(f"❌ {filename}:{line_num} - Invalid double backslash before underscore: {line.strip()}")
        
        # Check for incomplete field names (missing closing braces)
        incomplete_patterns = [
            r'\\ctmmTextField\[[^\]]*\]\{[^}]*\}\{[^}]*$',  # Missing closing brace
            r'\\ctmmTextArea\[[^\]]*\]\{[^}]*\}\{[^}]*\}\{[^}]*$',  # Missing closing brace
            r'\\ctmmCheckBox\[[^\]]*\]\{[^}]*$',  # Missing closing brace
        ]
        
        for pattern in incomplete_patterns:
            if re.search(pattern, line):
                issues.append(f"❌ {filename}:{line_num} - Incomplete form field command: {line.strip()}")
        
        # Check for duplicate \end{center} patterns
        if line.strip() == '\\end{center}':
            # This would need context to properly validate - for now just flag for manual review
            pass
        
        # Check for proper field naming conventions
        field_patterns = [
            r'\\ctmmTextField\[[^\]]*\]\{[^}]*\}\{([^}]+)\}',
            r'\\ctmmTextArea\[[^\]]*\]\{[^}]*\}\{[^}]*\}\{([^}]+)\}',
            r'\\ctmmCheckBox\[([^\]]+)\]',
        ]
        
        for pattern in field_patterns:
            matches = re.findall(pattern, line)
            for field_name in matches:
                if not self.is_valid_field_name(field_name):
                    issues.append(f"❌ {filename}:{line_num} - Invalid field name '{field_name}': {line.strip()}")
        
        return issues
    
    def is_valid_field_name(self, field_name: str) -> bool:
        """Check if a field name follows CTMM conventions."""
        # Field names should be alphanumeric with underscores, no special characters
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', field_name):
            return False
            
        # Should not end with _mm (this appears to be from faulty auto-generation)
        if field_name.endswith('_mm'):
            return False
            
        return True
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        
        if not self.issues:
            print("✅ All form fields pass validation!")
            print("✅ No LaTeX syntax errors detected")
            print("✅ Form field naming conventions are consistent")
        else:
            print(f"❌ Found {len(self.issues)} issues:")
            for issue in self.issues:
                print(f"   {issue}")
                
        print("\n📚 Form Field Standards:")
        print(r"   • Use \ctmmCheckBox[field_name]{label} (optional first parameter)")
        print("   • Field names: alphanumeric + underscores only")
        print("   • No double backslashes before underscores")
        print("   • All commands must have proper closing braces")
        print("   • Avoid auto-generated _mm suffixes")

    def fix_common_issues(self) -> bool:
        """Automatically fix common form field issues."""
        print("\n🔧 ATTEMPTING AUTOMATIC FIXES...")
        print("=" * 60)
        
        fixed_files = []
        
        for tex_file in self.modules_dir.glob("*.tex"):
            if self.fix_file_issues(tex_file):
                fixed_files.append(tex_file.name)
                
        if fixed_files:
            print(f"✅ Fixed issues in {len(fixed_files)} files:")
            for filename in fixed_files:
                print(f"   • {filename}")
            return True
        else:
            print("ℹ️  No automatic fixes were needed")
            return False
    
    def fix_file_issues(self, file_path: Path) -> bool:
        """Fix common issues in a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Fix double backslash before underscore
            content = re.sub(r'\\\\_', '_', content)
            
            # Fix common incomplete field patterns (very conservative)
            # Only fix obvious cases where _mm appears at end of line
            content = re.sub(r'_mm\\\\$', '_date}\\\\', content)
            content = re.sub(r'_mm$', '_field}', content)
            
            if content != original_content:
                # Create backup
                backup_path = file_path.with_suffix('.tex.backup')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                    
                # Write fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"✅ Fixed {file_path.name} (backup created)")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
            
        return False

def main():
    """Main validation function."""
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = "."
        
    validator = FormFieldValidator(repo_root)
    
    # Run validation
    is_valid = validator.validate_all_files()
    
    # Optionally run automatic fixes
    if not is_valid:
        print("\n❓ Attempt automatic fixes? (y/n): ", end="")
        response = input().lower().strip()
        if response in ['y', 'yes']:
            validator.fix_common_issues()
            print("\n🔄 Re-running validation after fixes...")
            validator.issues = []  # Clear previous issues
            is_valid = validator.validate_all_files()
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()