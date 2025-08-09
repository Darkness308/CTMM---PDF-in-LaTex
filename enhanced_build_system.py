#!/usr/bin/env python3
"""
Enhanced CTMM Build System
Advanced LaTeX compilation with multi-pass, error analysis, and optimization.

This enhanced build system provides:
1. Multi-pass compilation for references and cross-references
2. Advanced error detection and analysis with actionable recommendations
3. PDF verification and quality metrics
4. Code optimization suggestions
5. Performance monitoring and reporting
6. Integration with document conversion pipeline
"""

import os
import re
import subprocess
import sys
import tempfile
import shutil
import time
from pathlib import Path
from typing import List, Tuple, Dict, Set, Optional
import argparse
import logging
import json
from datetime import datetime
import hashlib

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

class AdvancedErrorAnalyzer:
    """Advanced LaTeX error analysis with actionable recommendations."""
    
    def __init__(self):
        self.error_patterns = {
            # Package and command errors
            r"Package (\w+) Error: (.+)": {
                "type": "Package Error",
                "severity": "high",
                "action": "Check package documentation or update packages"
            },
            r"Undefined control sequence.*\\(\w+)": {
                "type": "Undefined Command",
                "severity": "high", 
                "action": "Define command in preamble or check spelling"
            },
            r"File `([^']+)' not found": {
                "type": "Missing File",
                "severity": "high",
                "action": "Create missing file or check file path"
            },
            
            # Font and encoding issues
            r"Font shape .* undefined": {
                "type": "Font Issue",
                "severity": "medium",
                "action": "Install missing fonts or use alternative font family"
            },
            r"Package inputenc Error: (.+)": {
                "type": "Encoding Error",
                "severity": "medium",
                "action": "Check file encoding or use UTF-8"
            },
            
            # Reference and citation errors
            r"Reference `([^']+)' on page \d+ undefined": {
                "type": "Missing Reference",
                "severity": "medium",
                "action": "Define label or check reference name"
            },
            r"Citation `([^']+)' on page \d+ undefined": {
                "type": "Missing Citation",
                "severity": "medium",
                "action": "Add bibliography entry or check citation key"
            },
            
            # Layout and formatting warnings
            r"Overfull \\hbox.*": {
                "type": "Layout Warning",
                "severity": "low",
                "action": "Adjust line breaks or use smaller font"
            },
            r"Underfull \\hbox.*": {
                "type": "Layout Warning", 
                "severity": "low",
                "action": "Add content or adjust spacing"
            },
            
            # CTMM-specific issues
            r"Unknown option 'ngerman'": {
                "type": "Language Package",
                "severity": "high",
                "action": "Install texlive-lang-german package"
            },
            r"Package fontawesome5 Error": {
                "type": "Font Package",
                "severity": "high",
                "action": "Install texlive-fonts-extra package"
            }
        }
    
    def analyze_log(self, log_content: str) -> Dict:
        """Analyze LaTeX log for errors, warnings, and optimization opportunities."""
        analysis = {
            "errors": [],
            "warnings": [],
            "optimizations": [],
            "performance_metrics": {},
            "recommendations": []
        }
        
        lines = log_content.split('\n')
        
        for i, line in enumerate(lines):
            # Check against error patterns
            for pattern, info in self.error_patterns.items():
                match = re.search(pattern, line)
                if match:
                    error_info = {
                        "line_number": i + 1,
                        "content": line.strip(),
                        "type": info["type"],
                        "severity": info["severity"],
                        "action": info["action"],
                        "match": match.groups() if match.groups() else None
                    }
                    
                    if info["severity"] == "high":
                        analysis["errors"].append(error_info)
                    else:
                        analysis["warnings"].append(error_info)
        
        # Extract performance metrics
        analysis["performance_metrics"] = self._extract_performance_metrics(log_content)
        
        # Generate optimization recommendations
        analysis["optimizations"] = self._generate_optimizations(log_content, analysis)
        
        # Generate general recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _extract_performance_metrics(self, log_content: str) -> Dict:
        """Extract compilation performance metrics from log."""
        metrics = {}
        
        # Memory usage
        memory_match = re.search(r'(\d+) words of memory out of (\d+)', log_content)
        if memory_match:
            used, total = memory_match.groups()
            metrics["memory_usage"] = {
                "used": int(used),
                "total": int(total),
                "percentage": round(int(used) / int(total) * 100, 2)
            }
        
        # Font info
        font_match = re.search(r'(\d+) words of font info for (\d+) fonts', log_content)
        if font_match:
            font_words, font_count = font_match.groups()
            metrics["font_info"] = {
                "words": int(font_words),
                "fonts": int(font_count)
            }
        
        # Pages
        page_match = re.search(r'Output written on [^(]*\((\d+) page', log_content)
        if page_match:
            metrics["pages"] = int(page_match.group(1))
        
        return metrics
    
    def _generate_optimizations(self, log_content: str, analysis: Dict) -> List[Dict]:
        """Generate optimization suggestions based on analysis."""
        optimizations = []
        
        # Check for redundant packages
        packages = re.findall(r'Package: (\w+)', log_content)
        if len(packages) > len(set(packages)):
            optimizations.append({
                "type": "Package Optimization",
                "issue": "Duplicate package loading detected",
                "action": "Remove redundant \\usepackage commands",
                "impact": "Faster compilation and reduced memory usage"
            })
        
        # Check for many warnings
        if len(analysis["warnings"]) > 10:
            optimizations.append({
                "type": "Warning Cleanup",
                "issue": f"{len(analysis['warnings'])} warnings detected",
                "action": "Address layout and formatting warnings",
                "impact": "Better document quality and faster compilation"
            })
        
        # Memory usage optimization
        if "memory_usage" in analysis.get("performance_metrics", {}):
            memory_pct = analysis["performance_metrics"]["memory_usage"]["percentage"]
            if memory_pct > 80:
                optimizations.append({
                    "type": "Memory Optimization", 
                    "issue": f"High memory usage: {memory_pct}%",
                    "action": "Consider splitting document or reducing package usage",
                    "impact": "Improved compilation stability"
                })
        
        return optimizations
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate general recommendations based on analysis."""
        recommendations = []
        
        error_count = len(analysis["errors"])
        warning_count = len(analysis["warnings"])
        
        if error_count == 0 and warning_count == 0:
            recommendations.append("✅ Document compiles cleanly with no errors or warnings")
        elif error_count == 0:
            recommendations.append(f"⚠️ Document compiles successfully but has {warning_count} warnings to address")
        else:
            recommendations.append(f"❌ Document has {error_count} errors that must be fixed before compilation")
        
        if len(analysis["optimizations"]) > 0:
            recommendations.append(f"🔧 {len(analysis['optimizations'])} optimization opportunities identified")
        
        return recommendations

class EnhancedCTMMBuildSystem:
    """Enhanced build system with advanced features."""
    
    def __init__(self, main_tex_path: str = "main.tex"):
        self.main_tex_path = Path(main_tex_path)
        self.error_analyzer = AdvancedErrorAnalyzer()
        self.build_stats = {
            "start_time": None,
            "end_time": None,
            "duration": None,
            "passes": 0,
            "status": "pending"
        }
    
    def multi_pass_compile(self, tex_file: Path, max_passes: int = 3) -> Tuple[bool, Dict]:
        """Perform multi-pass compilation for proper cross-references."""
        logger.info(f"Starting multi-pass compilation of {tex_file}")
        self.build_stats["start_time"] = time.time()
        
        aux_file = tex_file.with_suffix('.aux')
        toc_file = tex_file.with_suffix('.toc')
        
        compilation_results = []
        
        for pass_num in range(1, max_passes + 1):
            logger.info(f"Compilation pass {pass_num}/{max_passes}")
            
            # Store checksums to detect changes
            aux_checksum_before = self._get_file_checksum(aux_file) if aux_file.exists() else None
            toc_checksum_before = self._get_file_checksum(toc_file) if toc_file.exists() else None
            
            # Compile
            success, log_content = self._compile_latex(tex_file)
            self.build_stats["passes"] = pass_num
            
            if not success:
                self.build_stats["status"] = "failed"
                compilation_results.append({
                    "pass": pass_num,
                    "success": False,
                    "log_analysis": self.error_analyzer.analyze_log(log_content)
                })
                break
            
            # Analyze log
            log_analysis = self.error_analyzer.analyze_log(log_content)
            compilation_results.append({
                "pass": pass_num,
                "success": True,
                "log_analysis": log_analysis
            })
            
            # Check if another pass is needed
            aux_checksum_after = self._get_file_checksum(aux_file) if aux_file.exists() else None
            toc_checksum_after = self._get_file_checksum(toc_file) if toc_file.exists() else None
            
            if (aux_checksum_before == aux_checksum_after and 
                toc_checksum_before == toc_checksum_after and 
                pass_num > 1):
                logger.info(f"Convergence achieved after {pass_num} passes")
                break
        
        self.build_stats["end_time"] = time.time()
        self.build_stats["duration"] = self.build_stats["end_time"] - self.build_stats["start_time"]
        
        final_success = compilation_results[-1]["success"] if compilation_results else False
        self.build_stats["status"] = "success" if final_success else "failed"
        
        return final_success, {
            "compilation_results": compilation_results,
            "build_stats": self.build_stats,
            "final_analysis": compilation_results[-1]["log_analysis"] if compilation_results else {}
        }
    
    def _get_file_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum of file."""
        if not file_path.exists():
            return ""
        
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _compile_latex(self, tex_file: Path) -> Tuple[bool, str]:
        """Compile single LaTeX pass."""
        try:
            cmd = [
                "pdflatex",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-synctex=1",
                str(tex_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=tex_file.parent
            )
            
            # Read log file
            log_file = tex_file.with_suffix('.log')
            log_content = ""
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                    log_content = f.read()
            
            return result.returncode == 0, log_content
            
        except subprocess.TimeoutExpired:
            logger.error(f"LaTeX compilation timed out for {tex_file}")
            return False, "Compilation timed out"
        except Exception as e:
            logger.error(f"LaTeX compilation failed: {str(e)}")
            return False, str(e)
    
    def verify_pdf_quality(self, pdf_file: Path) -> Dict:
        """Verify PDF quality and extract metrics."""
        if not pdf_file.exists():
            return {"status": "error", "message": "PDF file not found"}
        
        verification = {
            "status": "success",
            "file_size": pdf_file.stat().st_size,
            "file_size_mb": round(pdf_file.stat().st_size / 1024 / 1024, 2),
            "created": datetime.fromtimestamp(pdf_file.stat().st_mtime).isoformat()
        }
        
        # Try to get PDF info using pdfinfo if available
        try:
            result = subprocess.run(
                ["pdfinfo", str(pdf_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                info_lines = result.stdout.split('\n')
                for line in info_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower().replace(' ', '_')
                        verification[key] = value.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # pdfinfo not available or failed
            pass
        
        return verification
    
    def generate_build_report(self, results: Dict, output_file: Path = None) -> str:
        """Generate comprehensive build report."""
        if output_file is None:
            output_file = Path("build_report.md")
        
        report_lines = []
        report_lines.append("# CTMM Enhanced Build Report")
        report_lines.append("")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Build Statistics
        stats = results.get("build_stats", {})
        report_lines.append("## Build Statistics")
        report_lines.append("")
        report_lines.append(f"- **Status:** {stats.get('status', 'unknown').upper()}")
        report_lines.append(f"- **Compilation passes:** {stats.get('passes', 0)}")
        report_lines.append(f"- **Duration:** {stats.get('duration', 0):.2f} seconds")
        report_lines.append("")
        
        # Error Analysis
        final_analysis = results.get("final_analysis", {})
        
        if final_analysis.get("errors"):
            report_lines.append("## ❌ Errors")
            report_lines.append("")
            for error in final_analysis["errors"]:
                report_lines.append(f"- **{error['type']}:** {error['content']}")
                report_lines.append(f"  - *Action:* {error['action']}")
            report_lines.append("")
        
        if final_analysis.get("warnings"):
            report_lines.append("## ⚠️ Warnings")
            report_lines.append("")
            for warning in final_analysis["warnings"][:5]:  # Show first 5 warnings
                report_lines.append(f"- **{warning['type']}:** {warning['content']}")
            if len(final_analysis["warnings"]) > 5:
                report_lines.append(f"- *... and {len(final_analysis['warnings']) - 5} more warnings*")
            report_lines.append("")
        
        # Optimizations
        if final_analysis.get("optimizations"):
            report_lines.append("## 🔧 Optimization Opportunities")
            report_lines.append("")
            for opt in final_analysis["optimizations"]:
                report_lines.append(f"- **{opt['type']}:** {opt['issue']}")
                report_lines.append(f"  - *Action:* {opt['action']}")
                report_lines.append(f"  - *Impact:* {opt['impact']}")
            report_lines.append("")
        
        # Performance Metrics
        metrics = final_analysis.get("performance_metrics", {})
        if metrics:
            report_lines.append("## 📊 Performance Metrics")
            report_lines.append("")
            
            if "memory_usage" in metrics:
                mem = metrics["memory_usage"]
                report_lines.append(f"- **Memory Usage:** {mem['used']:,} words ({mem['percentage']}%)")
            
            if "font_info" in metrics:
                font = metrics["font_info"]
                report_lines.append(f"- **Font Info:** {font['words']:,} words for {font['fonts']} fonts")
            
            if "pages" in metrics:
                report_lines.append(f"- **Pages Generated:** {metrics['pages']}")
            
            report_lines.append("")
        
        # Recommendations
        recommendations = final_analysis.get("recommendations", [])
        if recommendations:
            report_lines.append("## 💡 Recommendations")
            report_lines.append("")
            for rec in recommendations:
                report_lines.append(f"- {rec}")
            report_lines.append("")
        
        report_content = '\n'.join(report_lines)
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"Build report saved to {output_file}")
        return report_content
    
    def build_with_converted_documents(self, include_converted: bool = True) -> Dict:
        """Build main document with option to include converted documents."""
        logger.info("Starting enhanced build process")
        
        # First, build main document
        main_success, main_results = self.multi_pass_compile(self.main_tex_path)
        
        results = {
            "main_document": {
                "success": main_success,
                "results": main_results
            },
            "converted_documents": {}
        }
        
        if include_converted and Path("converted").exists():
            logger.info("Building converted documents")
            converted_dir = Path("converted")
            
            for tex_file in converted_dir.glob("*.tex"):
                if tex_file.name == "README.tex":
                    continue  # Skip README
                
                logger.info(f"Building converted document: {tex_file.name}")
                success, build_result = self.multi_pass_compile(tex_file)
                
                results["converted_documents"][tex_file.name] = {
                    "success": success,
                    "results": build_result
                }
        
        # Verify main PDF
        main_pdf = self.main_tex_path.with_suffix('.pdf')
        if main_pdf.exists():
            results["main_document"]["pdf_verification"] = self.verify_pdf_quality(main_pdf)
        
        return results

def main():
    parser = argparse.ArgumentParser(description="Enhanced CTMM Build System")
    parser.add_argument("--main", "-m", default="main.tex",
                       help="Main LaTeX file to compile")
    parser.add_argument("--passes", "-p", type=int, default=3,
                       help="Maximum number of compilation passes")
    parser.add_argument("--include-converted", "-c", action="store_true",
                       help="Also build converted documents")
    parser.add_argument("--report", "-r", default="build_report.md",
                       help="Output file for build report")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    build_system = EnhancedCTMMBuildSystem(args.main)
    
    # Run enhanced build
    results = build_system.build_with_converted_documents(args.include_converted)
    
    # Generate report
    report_content = build_system.generate_build_report(
        results["main_document"]["results"], 
        Path(args.report)
    )
    
    # Print summary
    main_success = results["main_document"]["success"]
    logger.info("=== ENHANCED BUILD SUMMARY ===")
    logger.info(f"Main document: {'✅ SUCCESS' if main_success else '❌ FAILED'}")
    
    if args.include_converted:
        converted_results = results["converted_documents"]
        successful_converted = sum(1 for r in converted_results.values() if r["success"])
        total_converted = len(converted_results)
        logger.info(f"Converted documents: {successful_converted}/{total_converted} successful")
    
    if not main_success:
        sys.exit(1)

if __name__ == "__main__":
    main()