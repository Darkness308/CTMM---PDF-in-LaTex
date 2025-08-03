#!/usr/bin/env python3
"""
CTMM LaTeX Error Checker & Statistics Generator
Purpose: Analyze LaTeX logs, generate module statistics, check dependencies
Usage: python latex-helper.py [command] [args]
Copilot: Use for automated LaTeX project analysis and error detection
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
import argparse

class CTMMLaTeXHelper:
    def __init__(self):
        self.stats = {
            'modules': {},
            'packages': set(),
            'errors': [],
            'warnings': [],
            'total_pages': 0,
            'total_words': 0
        }
    
    def analyze_tex_file(self, filepath):
        """Analyze a single .tex file for content and structure"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count words (rough estimate)
            words = len(re.findall(r'\b\w+\b', content))
            
            # Find packages
            packages = re.findall(r'\\usepackage(?:\[.*?\])?\{([^}]+)\}', content)
            
            # Find sections
            sections = re.findall(r'\\(?:section|subsection|subsubsection)\*?\{([^}]+)\}', content)
            
            # Find form elements
            form_elements = len(re.findall(r'\\ctmm(?:TextField|CheckBox|RadioButton)', content))
            
            # Find CTMM color usage
            colors = re.findall(r'\\textcolor\{(ctmm\w+)\}', content)
            color_counts = Counter(colors)
            
            # Find tcolorbox usage
            tcolorboxes = len(re.findall(r'\\begin\{tcolorbox\}', content))
            
            return {
                'filepath': str(filepath),
                'words': words,
                'packages': packages,
                'sections': sections,
                'form_elements': form_elements,
                'colors': dict(color_counts),
                'tcolorboxes': tcolorboxes,
                'lines': len(content.split('\n'))
            }
            
        except Exception as e:
            return {'error': str(e), 'filepath': str(filepath)}
    
    def analyze_log_file(self, log_path):
        """Analyze LaTeX log file for errors and warnings"""
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                log_content = f.read()
            
            # Find errors
            errors = re.findall(r'! (.+)', log_content)
            
            # Find warnings
            warnings = re.findall(r'Warning: (.+)', log_content)
            
            # Find missing packages
            missing_packages = re.findall(r'Package (\w+) not found', log_content)
            
            # Find page count
            pages_match = re.search(r'Output written on .+ \((\d+) pages?', log_content)
            pages = int(pages_match.group(1)) if pages_match else 0
            
            return {
                'errors': errors,
                'warnings': warnings,
                'missing_packages': missing_packages,
                'pages': pages
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def scan_modules_directory(self, modules_dir):
        """Scan modules/ directory for all .tex files"""
        modules_dir = Path(modules_dir)
        tex_files = list(modules_dir.rglob('*.tex'))
        
        print(f"🔍 Scanning {len(tex_files)} .tex files in {modules_dir}")
        
        for tex_file in tex_files:
            analysis = self.analyze_tex_file(tex_file)
            if 'error' not in analysis:
                # Determine module category based on path
                relative_path = tex_file.relative_to(modules_dir)
                category = str(relative_path.parts[0]) if len(relative_path.parts) > 1 else 'root'
                
                if category not in self.stats['modules']:
                    self.stats['modules'][category] = []
                
                self.stats['modules'][category].append(analysis)
                self.stats['total_words'] += analysis['words']
                self.stats['packages'].update(analysis['packages'])
            else:
                self.stats['errors'].append(analysis)
    
    def generate_report(self, output_path=None):
        """Generate comprehensive report"""
        report = {
            'summary': {
                'total_modules': sum(len(modules) for modules in self.stats['modules'].values()),
                'total_words': self.stats['total_words'],
                'total_packages': len(self.stats['packages']),
                'categories': list(self.stats['modules'].keys())
            },
            'modules_by_category': {},
            'package_usage': list(self.stats['packages']),
            'ctmm_color_usage': defaultdict(int),
            'form_elements_total': 0
        }
        
        # Analyze by category
        for category, modules in self.stats['modules'].items():
            category_stats = {
                'count': len(modules),
                'total_words': sum(m['words'] for m in modules),
                'total_form_elements': sum(m['form_elements'] for m in modules),
                'modules': []
            }
            
            for module in modules:
                category_stats['modules'].append({
                    'name': Path(module['filepath']).stem,
                    'words': module['words'],
                    'sections': len(module['sections']),
                    'form_elements': module['form_elements'],
                    'colors': module['colors']
                })
                
                # Count color usage
                for color, count in module['colors'].items():
                    report['ctmm_color_usage'][color] += count
                
                report['form_elements_total'] += module['form_elements']
            
            report['modules_by_category'][category] = category_stats
        
        # Convert defaultdict to regular dict for JSON serialization
        report['ctmm_color_usage'] = dict(report['ctmm_color_usage'])
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"📊 Report saved to: {output_path}")
        
        return report
    
    def print_summary(self):
        """Print a nice summary to console"""
        print("\n🧩 CTMM LaTeX Project Analysis")
        print("=" * 50)
        
        total_modules = sum(len(modules) for modules in self.stats['modules'].values())
        print(f"📁 Module gefunden: {total_modules}")
        print(f"📝 Wörter gesamt: {self.stats['total_words']:,}")
        print(f"📦 Packages verwendet: {len(self.stats['packages'])}")
        
        print(f"\n📂 Module nach Kategorien:")
        for category, modules in self.stats['modules'].items():
            total_words = sum(m['words'] for m in modules)
            total_forms = sum(m['form_elements'] for m in modules)
            print(f"  • {category}: {len(modules)} Module, {total_words:,} Wörter, {total_forms} Formularfelder")
        
        # Color usage analysis
        all_colors = defaultdict(int)
        for modules in self.stats['modules'].values():
            for module in modules:
                for color, count in module['colors'].items():
                    all_colors[color] += count
        
        if all_colors:
            print(f"\n🎨 CTMM-Farben Verwendung:")
            for color, count in sorted(all_colors.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {color}: {count}x")
        
        if self.stats['errors']:
            print(f"\n❌ Fehler gefunden: {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                print(f"  • {error}")

def main():
    parser = argparse.ArgumentParser(description='CTMM LaTeX Helper Tool')
    parser.add_argument('command', choices=['analyze', 'check-errors', 'stats', 'module-detail'], 
                       help='What to do')
    parser.add_argument('--modules-dir', default='modules/', 
                       help='Path to modules directory')
    parser.add_argument('--build-dir', default='build/', 
                       help='Path to build directory')
    parser.add_argument('--output', '-o', 
                       help='Output file for reports')
    parser.add_argument('--module', 
                       help='Specific module name for detail analysis')
    
    args = parser.parse_args()
    
    helper = CTMMLaTeXHelper()
    
    if args.command == 'analyze':
        print("🔍 Analyzing CTMM LaTeX project...")
        helper.scan_modules_directory(args.modules_dir)
        helper.print_summary()
        
        if args.output:
            helper.generate_report(args.output)
    
    elif args.command == 'check-errors':
        log_files = list(Path(args.build_dir).glob('*.log'))
        if not log_files:
            print(f"❌ No log files found in {args.build_dir}")
            return
        
        print(f"🔍 Checking {len(log_files)} log files for errors...")
        for log_file in log_files:
            log_analysis = helper.analyze_log_file(log_file)
            if log_analysis.get('errors'):
                print(f"\n❌ Errors in {log_file.name}:")
                for error in log_analysis['errors']:
                    print(f"  • {error}")
            if log_analysis.get('warnings'):
                print(f"\n⚠️  Warnings in {log_file.name}:")
                for warning in log_analysis['warnings'][:5]:  # Limit to 5 warnings
                    print(f"  • {warning}")
    
    elif args.command == 'stats':
        helper.scan_modules_directory(args.modules_dir)
        report = helper.generate_report(args.output)
        
        print("\n📊 Detailed Statistics:")
        print(f"Total LaTeX words: {report['summary']['total_words']:,}")
        print(f"Total form elements: {report['form_elements_total']}")
        print(f"Most used color: {max(report['ctmm_color_usage'].items(), key=lambda x: x[1]) if report['ctmm_color_usage'] else 'None'}")
    
    elif args.command == 'module-detail':
        if not args.module:
            print("❌ Please specify --module <name> for detail analysis")
            return
        
        helper.scan_modules_directory(args.modules_dir)
        
        # Find the specific module
        found_module = None
        for category, modules in helper.stats['modules'].items():
            for module in modules:
                if args.module.lower() in Path(module['filepath']).stem.lower():
                    found_module = module
                    break
            if found_module:
                break
        
        if not found_module:
            print(f"❌ Module '{args.module}' not found")
            return
        
        print(f"\n🔍 Detailed Analysis: {Path(found_module['filepath']).stem}")
        print("=" * 60)
        print(f"📄 File: {found_module['filepath']}")
        print(f"📝 Words: {found_module['words']}")
        print(f"📏 Lines: {found_module['lines']}")
        print(f"📋 Sections: {len(found_module['sections'])}")
        print(f"🎨 Form elements: {found_module['form_elements']}")
        print(f"📦 tcolorboxes: {found_module['tcolorboxes']}")
        
        if found_module['sections']:
            print(f"\n📑 Sections found:")
            for i, section in enumerate(found_module['sections'], 1):
                print(f"  {i}. {section}")
        
        if found_module['colors']:
            print(f"\n🎨 CTMM Colors used:")
            for color, count in sorted(found_module['colors'].items(), key=lambda x: x[1], reverse=True):
                print(f"  • {color}: {count}x")
        
        if found_module['packages']:
            print(f"\n📦 Packages used:")
            for package in found_module['packages']:
                print(f"  • {package}")
        
        # Quality suggestions
        print(f"\n💡 Quality Assessment:")
        if found_module['form_elements'] > 0:
            print(f"  ✅ Interactive elements present ({found_module['form_elements']} form fields)")
        else:
            print(f"  ⚠️  No form elements found - consider adding interactive elements")
        
        if found_module['colors']:
            print(f"  ✅ CTMM color system used consistently")
        else:
            print(f"  ⚠️  No CTMM colors found - check color consistency")
        
        if found_module['tcolorboxes'] > 0:
            print(f"  ✅ Structured content with {found_module['tcolorboxes']} colored boxes")
        
        words_per_section = found_module['words'] / max(len(found_module['sections']), 1)
        if words_per_section > 200:
            print(f"  ⚠️  Sections might be too long (avg {words_per_section:.0f} words/section)")
        elif words_per_section > 100:
            print(f"  ✅ Good section length (avg {words_per_section:.0f} words/section)")
        else:
            print(f"  ✅ Concise sections (avg {words_per_section:.0f} words/section)")

if __name__ == '__main__':
    main()
