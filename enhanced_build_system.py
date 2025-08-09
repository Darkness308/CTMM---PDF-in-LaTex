#!/usr/bin/env python3
"""
Enhanced CTMM LaTeX Build System
Production-ready document processing pipeline with quality assurance features.

Features:
- Multi-pass compilation with error handling
- PDF verification and quality checks
- Advanced error analysis with actionable recommendations
- Code optimization suggestions
- Integration with converted documents
"""

import os
import re
import subprocess
import sys
from pathlib import Path
import logging
import shutil
import tempfile
from typing import List, Dict, Optional, Tuple
import argparse
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_build.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PDFAnalyzer:
    """Analyze PDF output for quality and completeness."""
    
    def __init__(self):
        self.pdf_info = {}
        self.quality_issues = []
        self.recommendations = []
    
    def analyze_pdf(self, pdf_path: Path) -> Dict:
        """Analyze PDF file for quality and completeness."""
        logger.info(f"Analyzing PDF: {pdf_path}")
        
        analysis = {
            'file_exists': pdf_path.exists(),
            'file_size': 0,
            'page_count': 0,
            'has_bookmarks': False,
            'has_forms': False,
            'quality_score': 0,
            'issues': [],
            'recommendations': []
        }
        
        if not pdf_path.exists():
            analysis['issues'].append("PDF file not generated")
            return analysis
        
        try:
            # Basic file info
            analysis['file_size'] = pdf_path.stat().st_size
            
            # Use pdfinfo if available
            try:
                result = subprocess.run(
                    ['pdfinfo', str(pdf_path)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Parse pdfinfo output
                for line in result.stdout.split('\n'):
                    if line.startswith('Pages:'):
                        analysis['page_count'] = int(line.split(':')[1].strip())
                    elif 'Form:' in line and 'AcroForm' in line:
                        analysis['has_forms'] = True
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.warning("pdfinfo not available, skipping detailed PDF analysis")
            
            # Quality assessment
            analysis['quality_score'] = self._calculate_quality_score(analysis)
            analysis['issues'] = self._identify_quality_issues(analysis)
            analysis['recommendations'] = self._generate_recommendations(analysis)
            
        except Exception as e:
            logger.error(f"Error analyzing PDF: {e}")
            analysis['issues'].append(f"Analysis error: {e}")
        
        return analysis
    
    def _calculate_quality_score(self, analysis: Dict) -> int:
        """Calculate quality score (0-100)."""
        score = 100
        
        if analysis['file_size'] < 1000:  # Very small file
            score -= 30
        elif analysis['file_size'] > 50 * 1024 * 1024:  # Very large file
            score -= 10
        
        if analysis['page_count'] == 0:
            score -= 50
        elif analysis['page_count'] < 5:
            score -= 10
        
        if not analysis['has_forms']:
            score -= 20  # CTMM documents should have interactive forms
        
        return max(0, score)
    
    def _identify_quality_issues(self, analysis: Dict) -> List[str]:
        """Identify potential quality issues."""
        issues = []
        
        if analysis['file_size'] < 1000:
            issues.append("PDF file unusually small - possible compilation error")
        
        if analysis['page_count'] == 0:
            issues.append("No pages in PDF")
        elif analysis['page_count'] > 200:
            issues.append("Very large document - consider splitting")
        
        if not analysis['has_forms']:
            issues.append("No interactive forms detected - CTMM documents should be interactive")
        
        return issues
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        if analysis['quality_score'] < 70:
            recommendations.append("Review compilation logs for errors")
        
        if not analysis['has_forms']:
            recommendations.append("Add interactive form elements using form-elements.sty")
        
        if analysis['page_count'] > 100:
            recommendations.append("Consider splitting into multiple documents")
        
        return recommendations


class ErrorAnalyzer:
    """Analyze LaTeX compilation errors and provide actionable recommendations."""
    
    def __init__(self):
        self.error_patterns = {
            'undefined_control_sequence': {
                'pattern': r'Undefined control sequence\\?\s*(.+)',
                'severity': 'high',
                'description': 'Command not defined or package not loaded'
            },
            'file_not_found': {
                'pattern': r'File `([^\']+)\' not found',
                'severity': 'high',
                'description': 'Referenced file missing'
            },
            'package_error': {
                'pattern': r'Package (\w+) Error:(.+)',
                'severity': 'medium',
                'description': 'Package-specific error'
            },
            'missing_begin_document': {
                'pattern': r'Missing \\begin\{document\}',
                'severity': 'high',
                'description': 'Document structure error'
            },
            'math_mode_error': {
                'pattern': r'Missing \$ inserted',
                'severity': 'medium',
                'description': 'Math mode syntax error'
            }
        }
    
    def analyze_log(self, log_path: Path) -> Dict:
        """Analyze LaTeX log file for errors and warnings."""
        logger.info(f"Analyzing log file: {log_path}")
        
        analysis = {
            'errors': [],
            'warnings': [],
            'recommendations': [],
            'error_count': 0,
            'warning_count': 0,
            'critical_issues': []
        }
        
        if not log_path.exists():
            analysis['critical_issues'].append("Log file not found")
            return analysis
        
        try:
            with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
                log_content = f.read()
            
            # Find errors
            analysis['errors'] = self._extract_errors(log_content)
            analysis['warnings'] = self._extract_warnings(log_content)
            analysis['error_count'] = len(analysis['errors'])
            analysis['warning_count'] = len(analysis['warnings'])
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_error_recommendations(analysis['errors'])
            analysis['critical_issues'] = self._identify_critical_issues(analysis['errors'])
            
        except Exception as e:
            logger.error(f"Error analyzing log: {e}")
            analysis['critical_issues'].append(f"Log analysis failed: {e}")
        
        return analysis
    
    def _extract_errors(self, log_content: str) -> List[Dict]:
        """Extract errors from log content."""
        errors = []
        lines = log_content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('!'):
                error = {
                    'line_number': i + 1,
                    'message': line,
                    'type': 'unknown',
                    'severity': 'medium',
                    'context': []
                }
                
                # Classify error type
                for error_type, pattern_info in self.error_patterns.items():
                    if re.search(pattern_info['pattern'], line):
                        error['type'] = error_type
                        error['severity'] = pattern_info['severity']
                        error['description'] = pattern_info['description']
                        break
                
                # Get context lines
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                error['context'] = lines[start:end]
                
                errors.append(error)
        
        return errors
    
    def _extract_warnings(self, log_content: str) -> List[str]:
        """Extract warnings from log content."""
        warnings = []
        for line in log_content.split('\n'):
            if 'Warning:' in line or 'warning:' in line:
                warnings.append(line.strip())
        return warnings
    
    def _generate_error_recommendations(self, errors: List[Dict]) -> List[str]:
        """Generate specific recommendations based on errors."""
        recommendations = []
        
        for error in errors:
            error_type = error.get('type', 'unknown')
            
            if error_type == 'undefined_control_sequence':
                recommendations.append("Check if required packages are loaded in preamble")
                recommendations.append("Verify command spelling and syntax")
            elif error_type == 'file_not_found':
                recommendations.append("Run conversion pipeline to generate missing files")
                recommendations.append("Check file paths and names for typos")
            elif error_type == 'package_error':
                recommendations.append("Update package usage or check package documentation")
            elif error_type == 'math_mode_error':
                recommendations.append("Check math mode delimiters ($...$ or \\[...\\])")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _identify_critical_issues(self, errors: List[Dict]) -> List[str]:
        """Identify critical issues that prevent compilation."""
        critical = []
        
        for error in errors:
            if error.get('severity') == 'high':
                critical.append(error['message'])
        
        return critical


class EnhancedBuildSystem:
    """Enhanced build system with comprehensive error handling and quality assurance."""
    
    def __init__(self, main_tex: str = "main.tex"):
        self.main_tex = Path(main_tex)
        self.build_dir = Path("build")
        self.pdf_analyzer = PDFAnalyzer()
        self.error_analyzer = ErrorAnalyzer()
        self.build_stats = {
            'start_time': None,
            'end_time': None,
            'total_time': 0,
            'passes': 0,
            'errors': 0,
            'warnings': 0
        }
    
    def multi_pass_compilation(self, passes: int = 3) -> bool:
        """Perform multi-pass LaTeX compilation."""
        logger.info(f"Starting multi-pass compilation ({passes} passes)")
        self.build_stats['start_time'] = datetime.now()
        
        # Create build directory
        self.build_dir.mkdir(exist_ok=True)
        
        success = True
        for pass_num in range(1, passes + 1):
            logger.info(f"Pass {pass_num}/{passes}")
            
            result = self._single_pass_compilation(pass_num)
            self.build_stats['passes'] = pass_num
            
            if not result:
                logger.error(f"Compilation failed on pass {pass_num}")
                success = False
                break
            
            # Check if we can stop early (no changes in aux files)
            if pass_num > 1 and self._check_convergence():
                logger.info(f"Compilation converged after {pass_num} passes")
                break
        
        self.build_stats['end_time'] = datetime.now()
        self.build_stats['total_time'] = (
            self.build_stats['end_time'] - self.build_stats['start_time']
        ).total_seconds()
        
        return success
    
    def _single_pass_compilation(self, pass_num: int) -> bool:
        """Perform a single compilation pass."""
        try:
            cmd = [
                'pdflatex',
                '-interaction=nonstopmode',
                '-output-directory=build',
                str(self.main_tex)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',  # Handle encoding issues gracefully
                check=False,
                timeout=300  # 5 minute timeout
            )
            
            # Copy log file for analysis
            log_src = self.build_dir / f"{self.main_tex.stem}.log"
            log_dst = f"build_pass_{pass_num}.log"
            if log_src.exists():
                shutil.copy2(log_src, log_dst)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error(f"Compilation timeout on pass {pass_num}")
            return False
        except Exception as e:
            logger.error(f"Compilation error on pass {pass_num}: {e}")
            return False
    
    def _check_convergence(self) -> bool:
        """Check if compilation has converged (aux files unchanged)."""
        # This would compare aux files between passes
        # Simplified implementation
        return False
    
    def verify_pdf_output(self) -> Dict:
        """Verify PDF output quality and completeness."""
        pdf_path = self.build_dir / f"{self.main_tex.stem}.pdf"
        
        if pdf_path.exists():
            # Copy PDF to main directory
            shutil.copy2(pdf_path, f"{self.main_tex.stem}.pdf")
        
        return self.pdf_analyzer.analyze_pdf(pdf_path)
    
    def analyze_compilation_errors(self) -> Dict:
        """Analyze compilation errors and provide recommendations."""
        log_path = self.build_dir / f"{self.main_tex.stem}.log"
        return self.error_analyzer.analyze_log(log_path)
    
    def generate_optimization_report(self) -> Dict:
        """Generate code optimization recommendations."""
        recommendations = {
            'performance': [],
            'quality': [],
            'maintenance': []
        }
        
        # Analyze main.tex for optimization opportunities
        if self.main_tex.exists():
            with open(self.main_tex, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for common optimization opportunities
            if '\\input{converted/' in content:
                recommendations['performance'].append(
                    "Consider organizing converted modules into logical groups"
                )
            
            if content.count('\\usepackage') > 20:
                recommendations['performance'].append(
                    "Many packages loaded - consider consolidating or lazy loading"
                )
            
            if '\\begin{document}' not in content:
                recommendations['quality'].append(
                    "Document structure issue detected"
                )
        
        return recommendations
    
    def full_build_pipeline(self) -> Dict:
        """Run the complete enhanced build pipeline."""
        logger.info("Starting enhanced CTMM build pipeline")
        
        pipeline_result = {
            'compilation_success': False,
            'pdf_analysis': {},
            'error_analysis': {},
            'optimization_report': {},
            'build_stats': {},
            'overall_success': False
        }
        
        try:
            # Multi-pass compilation
            compilation_success = self.multi_pass_compilation()
            pipeline_result['compilation_success'] = compilation_success
            
            # PDF verification
            pipeline_result['pdf_analysis'] = self.verify_pdf_output()
            
            # Error analysis
            pipeline_result['error_analysis'] = self.analyze_compilation_errors()
            
            # Optimization recommendations
            pipeline_result['optimization_report'] = self.generate_optimization_report()
            
            # Build statistics
            pipeline_result['build_stats'] = self.build_stats
            
            # Overall success determination
            pipeline_result['overall_success'] = (
                compilation_success and 
                pipeline_result['pdf_analysis'].get('file_exists', False) and
                len(pipeline_result['error_analysis'].get('critical_issues', [])) == 0
            )
            
            logger.info(f"Pipeline complete. Success: {pipeline_result['overall_success']}")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            pipeline_result['error'] = str(e)
        
        return pipeline_result
    
    def generate_comprehensive_report(self, pipeline_result: Dict) -> str:
        """Generate a comprehensive build report."""
        report = f"""
# Enhanced CTMM Build System Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Build Summary
- **Overall Success**: {pipeline_result.get('overall_success', False)}
- **Compilation Success**: {pipeline_result.get('compilation_success', False)}
- **Build Time**: {pipeline_result.get('build_stats', {}).get('total_time', 0):.2f} seconds
- **Passes Completed**: {pipeline_result.get('build_stats', {}).get('passes', 0)}

## PDF Analysis
"""
        
        pdf_analysis = pipeline_result.get('pdf_analysis', {})
        if pdf_analysis:
            report += f"""- **File Generated**: {pdf_analysis.get('file_exists', False)}
- **File Size**: {pdf_analysis.get('file_size', 0):,} bytes
- **Page Count**: {pdf_analysis.get('page_count', 0)}
- **Quality Score**: {pdf_analysis.get('quality_score', 0)}/100
- **Interactive Forms**: {pdf_analysis.get('has_forms', False)}

### Quality Issues
"""
            for issue in pdf_analysis.get('issues', []):
                report += f"- {issue}\n"
            
            report += "\n### PDF Recommendations\n"
            for rec in pdf_analysis.get('recommendations', []):
                report += f"- {rec}\n"
        
        report += "\n## Error Analysis\n"
        error_analysis = pipeline_result.get('error_analysis', {})
        if error_analysis:
            report += f"""- **Errors**: {error_analysis.get('error_count', 0)}
- **Warnings**: {error_analysis.get('warning_count', 0)}
- **Critical Issues**: {len(error_analysis.get('critical_issues', []))}

### Critical Issues
"""
            for issue in error_analysis.get('critical_issues', []):
                report += f"- {issue}\n"
            
            report += "\n### Error Recommendations\n"
            for rec in error_analysis.get('recommendations', []):
                report += f"- {rec}\n"
        
        report += "\n## Optimization Recommendations\n"
        optimization = pipeline_result.get('optimization_report', {})
        for category, recommendations in optimization.items():
            if recommendations:
                report += f"\n### {category.title()}\n"
                for rec in recommendations:
                    report += f"- {rec}\n"
        
        report += "\n## Next Steps\n"
        if pipeline_result.get('overall_success'):
            report += "✅ Build successful! PDF generated and ready for use.\n"
        else:
            report += "❌ Build issues detected. Review errors and recommendations above.\n"
        
        return report


def main():
    """Run the enhanced CTMM build system."""
    parser = argparse.ArgumentParser(description='Enhanced CTMM LaTeX Build System')
    parser.add_argument('--main-tex', default='main.tex', help='Main LaTeX file')
    parser.add_argument('--passes', type=int, default=3, help='Number of compilation passes')
    parser.add_argument('--output-report', default='enhanced_build_report.md', 
                       help='Output report filename')
    
    args = parser.parse_args()
    
    # Install PDF tools if available
    try:
        subprocess.run(['which', 'pdfinfo'], check=True, capture_output=True)
        logger.info("PDF analysis tools available")
    except subprocess.CalledProcessError:
        logger.warning("pdfinfo not available - limited PDF analysis")
    
    # Run enhanced build system
    build_system = EnhancedBuildSystem(args.main_tex)
    pipeline_result = build_system.full_build_pipeline()
    
    # Generate and save report
    report = build_system.generate_comprehensive_report(pipeline_result)
    with open(args.output_report, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"Enhanced build complete. Report saved to {args.output_report}")
    print(report)
    
    return 0 if pipeline_result.get('overall_success') else 1


if __name__ == "__main__":
    sys.exit(main())