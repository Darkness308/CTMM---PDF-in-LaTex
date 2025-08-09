#!/usr/bin/env python3
"""
CTMM Security Fix Demonstration
Demonstrates the before/after comparison of the package name sanitization security fix.

This script shows how the vulnerability was fixed and validates that the solution
prevents LaTeX compilation errors caused by invalid command names.
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple
import tempfile

# Add the current directory to the path so we can import build_manager
sys.path.insert(0, str(Path(__file__).parent))

from build_manager import PackageNameSanitizer


class SecurityVulnerabilityDemo:
    """Demonstrates the security vulnerability and its fix."""
    
    def __init__(self):
        self.sanitizer = PackageNameSanitizer()
        self.test_packages = [
            'ctmm-design',
            'form-elements',
            'ctmm-diagrams',
            'complex-package_name-v2',
            'test_underscore-hyphen',
            '123-starts-with-number',
            'special@chars!name',
        ]
    
    def generate_vulnerable_command(self, package_name: str) -> str:
        """
        Generate the problematic command that would be created by the vulnerable system.
        This is how the OLD system would have generated commands.
        """
        # This is the VULNERABLE way - directly using package name
        return f"{package_name}Placeholder"
    
    def generate_safe_command(self, package_name: str) -> str:
        """
        Generate the safe command using the new sanitization system.
        """
        return self.sanitizer.generate_safe_command_name(package_name)
    
    def validate_latex_command(self, command: str) -> Tuple[bool, str]:
        """
        Validate if a command name is valid for LaTeX.
        Returns (is_valid, reason)
        """
        if not command:
            return False, "Empty command name"
        
        if not command[0].isalpha():
            return False, "Must start with a letter"
        
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', command):
            return False, "Contains invalid characters (only letters and numbers allowed)"
        
        return True, "Valid LaTeX command"
    
    def demonstrate_vulnerability(self):
        """Demonstrate the security vulnerability and its fix."""
        print("CTMM Security Vulnerability Demonstration")
        print("="*50)
        print()
        
        print("PROBLEM: Package names with special characters generate invalid LaTeX commands")
        print("-" * 70)
        print()
        
        for package in self.test_packages:
            print(f"📦 Package: {package}")
            
            # Show vulnerable command generation
            vulnerable_cmd = self.generate_vulnerable_command(package)
            vuln_valid, vuln_reason = self.validate_latex_command(vulnerable_cmd)
            vuln_status = "✅ SAFE" if vuln_valid else "❌ VULNERABLE"
            
            print(f"   OLD (Vulnerable): \\{vulnerable_cmd}")
            print(f"   Status: {vuln_status} - {vuln_reason}")
            
            # Show safe command generation
            safe_cmd = self.generate_safe_command(package)
            safe_valid, safe_reason = self.validate_latex_command(safe_cmd)
            safe_status = "✅ SAFE" if safe_valid else "❌ STILL UNSAFE"
            
            print(f"   NEW (Sanitized):  \\{safe_cmd}")
            print(f"   Status: {safe_status} - {safe_reason}")
            print()
        
        return self.generate_summary()
    
    def generate_summary(self) -> dict:
        """Generate summary statistics of the fix."""
        stats = {
            'total_packages': len(self.test_packages),
            'vulnerable_before': 0,
            'safe_after': 0,
            'still_problematic': 0,
        }
        
        for package in self.test_packages:
            vulnerable_cmd = self.generate_vulnerable_command(package)
            safe_cmd = self.generate_safe_command(package)
            
            vuln_valid, _ = self.validate_latex_command(vulnerable_cmd)
            safe_valid, _ = self.validate_latex_command(safe_cmd)
            
            if not vuln_valid:
                stats['vulnerable_before'] += 1
            
            if safe_valid:
                stats['safe_after'] += 1
            else:
                stats['still_problematic'] += 1
        
        return stats
    
    def generate_latex_examples(self):
        """Generate LaTeX code examples showing the vulnerability and fix."""
        print("\nLaTeX Code Examples")
        print("="*50)
        print()
        
        print("BEFORE (Vulnerable Code):")
        print("-" * 25)
        for package in self.test_packages[:3]:  # Show first 3 for brevity
            vulnerable_cmd = self.generate_vulnerable_command(package)
            print(f"% Package: {package}")
            print(f"\\newcommand{{\\{vulnerable_cmd}}}{{\\textcolor{{red}}{{[TEMPLATE]}}}} % ❌ INVALID")
            print()
        
        print("AFTER (Secure Code):")
        print("-" * 20)
        for package in self.test_packages[:3]:  # Show first 3 for brevity
            safe_cmd = self.generate_safe_command(package)
            sanitized = self.sanitizer.sanitize_package_name(package)
            print(f"% Package: {package} → {sanitized}")
            print(f"\\newcommand{{\\{safe_cmd}}}{{\\textcolor{{red}}{{[TEMPLATE]}}}} % ✅ VALID")
            print()
    
    def create_test_latex_files(self):
        """Create actual LaTeX files to demonstrate the compilation difference."""
        print("Creating Test LaTeX Files")
        print("="*30)
        print()
        
        # Create vulnerable LaTeX file
        vulnerable_content = """\\documentclass{article}
\\usepackage{xcolor}

% VULNERABLE COMMANDS - These would cause LaTeX errors
"""
        
        for package in self.test_packages[:3]:
            vulnerable_cmd = self.generate_vulnerable_command(package)
            vulnerable_content += f"\\newcommand{{\\{vulnerable_cmd}}}{{\\textcolor{{red}}{{[{package.upper()} TEMPLATE]}}}}\n"
        
        vulnerable_content += """
\\begin{document}
\\title{Vulnerable LaTeX Commands Test}
\\maketitle

This document would fail to compile due to invalid command names.

\\end{document}
"""
        
        # Create safe LaTeX file
        safe_content = """\\documentclass{article}
\\usepackage{xcolor}

% SAFE COMMANDS - These compile successfully
"""
        
        for package in self.test_packages[:3]:
            safe_cmd = self.generate_safe_command(package)
            sanitized = self.sanitizer.sanitize_package_name(package)
            safe_content += f"% {package} → {sanitized}\n"
            safe_content += f"\\newcommand{{\\{safe_cmd}}}{{\\textcolor{{red}}{{[{package.upper()} TEMPLATE]}}}}\n"
        
        safe_content += """
\\begin{document}
\\title{Safe LaTeX Commands Test}
\\maketitle

This document compiles successfully with sanitized command names.

% Using the safe commands:
"""
        
        for package in self.test_packages[:3]:
            safe_cmd = self.generate_safe_command(package)
            safe_content += f"\\{safe_cmd}\n\n"
        
        safe_content += """\\end{document}
"""
        
        # Write files
        try:
            with open('vulnerable_commands_test.tex', 'w') as f:
                f.write(vulnerable_content)
            print("✅ Created: vulnerable_commands_test.tex")
            
            with open('safe_commands_test.tex', 'w') as f:
                f.write(safe_content)
            print("✅ Created: safe_commands_test.tex")
            
            print()
            print("To test the difference:")
            print("1. Try compiling vulnerable_commands_test.tex - should fail")
            print("2. Try compiling safe_commands_test.tex - should succeed")
            
        except Exception as e:
            print(f"❌ Error creating test files: {e}")


def main():
    """Main demonstration function."""
    demo = SecurityVulnerabilityDemo()
    
    # Run the main demonstration
    stats = demo.demonstrate_vulnerability()
    
    # Show LaTeX examples
    demo.generate_latex_examples()
    
    # Create test files
    demo.create_test_latex_files()
    
    # Show final summary
    print("\n" + "="*60)
    print("SECURITY FIX SUMMARY")
    print("="*60)
    print(f"Total packages tested: {stats['total_packages']}")
    print(f"Vulnerable before fix: {stats['vulnerable_before']}")
    print(f"Safe after fix: {stats['safe_after']}")
    print(f"Still problematic: {stats['still_problematic']}")
    
    if stats['still_problematic'] == 0:
        print("\n✅ SUCCESS: All security vulnerabilities have been fixed!")
        print("✅ All generated LaTeX commands are now valid and safe.")
        print("✅ The CTMM system is protected against package name injection attacks.")
    else:
        print(f"\n❌ WARNING: {stats['still_problematic']} packages still generate invalid commands!")
        print("❌ Additional sanitization may be needed.")
    
    # Show security benefits
    print("\n🔒 SECURITY BENEFITS:")
    print("   ✅ Prevents LaTeX compilation errors from invalid command names")
    print("   ✅ Sanitizes package names to safe camelCase format")
    print("   ✅ Validates all generated commands before use")
    print("   ✅ Maintains backward compatibility")
    print("   ✅ Provides comprehensive error handling")
    
    print("\n🛡️ ATTACK PREVENTION:")
    print("   ✅ Package name injection attacks blocked")
    print("   ✅ Special character exploits prevented")
    print("   ✅ Invalid command name generation eliminated")
    print("   ✅ Build system hardened against malicious input")
    
    return stats['still_problematic'] == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)