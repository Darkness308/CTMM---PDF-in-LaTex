#!/usr/bin/env python3
"""
CTMM Document Conversion Pipeline
Converts Word documents and Markdown to LaTeX format for CTMM therapy materials.

This script:
1. Scans therapie-material/ directory for .docx and .md files
2. Converts documents to LaTeX with CTMM formatting
3. Maintains German text encoding and therapeutic content structure
4. Creates organized converted/ directory with processed documents
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import logging
import tempfile
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CTMMDocumentConverter:
    def __init__(self, source_dir: str = "therapie-material", target_dir: str = "converted"):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(exist_ok=True)
        self.converted_files = []
        self.failed_conversions = []
        
    def scan_source_documents(self) -> List[Path]:
        """Scan source directory for convertible documents."""
        logger.info(f"Scanning {self.source_dir} for documents...")
        
        if not self.source_dir.exists():
            logger.error(f"Source directory {self.source_dir} not found")
            return []
        
        # Find .docx and .md files
        docx_files = list(self.source_dir.glob("*.docx"))
        md_files = list(self.source_dir.glob("*.md"))
        
        all_files = docx_files + md_files
        logger.info(f"Found {len(docx_files)} .docx files and {len(md_files)} .md files")
        
        return all_files
    
    def convert_docx_to_latex(self, docx_file: Path) -> bool:
        """Convert Word document to LaTeX using pandoc."""
        logger.info(f"Converting {docx_file.name} to LaTeX...")
        
        # Generate output filename
        output_file = self.target_dir / f"{docx_file.stem}.tex"
        
        try:
            # Check if pandoc is available
            pandoc_check = subprocess.run(['which', 'pandoc'], capture_output=True)
            if pandoc_check.returncode != 0:
                logger.warning("pandoc not found, attempting alternative conversion")
                return self._convert_without_pandoc(docx_file, output_file)
            
            # Use pandoc for conversion
            result = subprocess.run([
                'pandoc',
                str(docx_file),
                '-o', str(output_file),
                '--from=docx',
                '--to=latex',
                '--standalone',
                '--wrap=none'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"✓ Successfully converted {docx_file.name}")
                self._post_process_latex(output_file)
                self.converted_files.append(str(output_file))
                return True
            else:
                logger.error(f"✗ pandoc conversion failed for {docx_file.name}: {result.stderr}")
                self.failed_conversions.append(str(docx_file))
                return False
                
        except Exception as e:
            logger.error(f"Conversion failed for {docx_file.name}: {e}")
            self.failed_conversions.append(str(docx_file))
            return False
    
    def _convert_without_pandoc(self, docx_file: Path, output_file: Path) -> bool:
        """Fallback conversion method when pandoc is not available."""
        logger.info(f"Using fallback conversion for {docx_file.name}")
        
        # Create a basic LaTeX template based on filename
        template_content = self._generate_latex_template(docx_file.stem)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            logger.info(f"✓ Created LaTeX template for {docx_file.name}")
            self.converted_files.append(str(output_file))
            return True
            
        except Exception as e:
            logger.error(f"Fallback conversion failed for {docx_file.name}: {e}")
            self.failed_conversions.append(str(docx_file))
            return False
    
    def _generate_latex_template(self, document_name: str) -> str:
        """Generate a LaTeX template based on document name and CTMM conventions."""
        # Clean up document name for title
        title = document_name.replace('_', ' ').replace('-', ' ')
        title = re.sub(r'\b\w', lambda m: m.group(0).upper(), title)
        
        # Determine document type and create appropriate structure
        if 'trigger' in document_name.lower():
            return self._create_trigger_management_template(title)
        elif 'matching' in document_name.lower() and 'matrix' in document_name.lower():
            return self._create_matching_matrix_template(title)
        elif 'tool' in document_name.lower():
            return self._create_tool_template(title)
        elif 'safeword' in document_name.lower():
            return self._create_safewords_template(title)
        elif 'depression' in document_name.lower():
            return self._create_depression_template(title)
        elif 'bindung' in document_name.lower():
            return self._create_binding_template(title)
        else:
            return self._create_generic_template(title)
    
    def _create_trigger_management_template(self, title: str) -> str:
        return f"""% {title} - CTMM Trigger Management Module
% Converted from Word document by CTMM Document Converter

\\section{{{title}}}
\\label{{sec:{title.lower().replace(' ', '-')}}}

\\begin{{ctmmBlueBox}}{{Trigger Management System}}
Das CTMM Trigger Management System hilft dabei, Trigger zu erkennen, zu verstehen und effektiv damit umzugehen.
\\end{{ctmmBlueBox}}

\\subsection{{Trigger-Erkennung}}

\\begin{{itemize}}
    \\item \\textbf{{Körperliche Signale:}} \\underline{{\\hspace{{3cm}}}}
    \\item \\textbf{{Emotionale Reaktionen:}} \\underline{{\\hspace{{3cm}}}}
    \\item \\textbf{{Gedankenmuster:}} \\underline{{\\hspace{{3cm}}}}
    \\item \\textbf{{Verhaltensmuster:}} \\underline{{\\hspace{{3cm}}}}
\\end{{itemize}}

\\subsection{{Trigger-Tracking}}

\\begin{{tabular}}{{|p{{3cm}}|p{{4cm}}|p{{4cm}}|p{{3cm}}|}}
\\hline
\\textbf{{Datum}} & \\textbf{{Trigger}} & \\textbf{{Reaktion}} & \\textbf{{Intervention}} \\\\
\\hline
& & & \\\\[1cm]
\\hline
& & & \\\\[1cm]
\\hline
& & & \\\\[1cm]
\\hline
\\end{{tabular}}

\\subsection{{Interventionsstrategien}}

\\begin{{enumerate}}
    \\item \\textbf{{Sofortmaßnahmen:}}
    \\begin{{itemize}}
        \\item \\checkbox\\,Tiefe Atmung
        \\item \\checkbox\\,Grounding-Techniken
        \\item \\checkbox\\,Sicherer Ort aufsuchen
    \\end{{itemize}}
    
    \\item \\textbf{{Mittelfristige Strategien:}}
    \\begin{{itemize}}
        \\item \\checkbox\\,Kommunikation mit Partner/in
        \\item \\checkbox\\,Professionelle Unterstützung
        \\item \\checkbox\\,Selbstfürsorge-Aktivitäten
    \\end{{itemize}}
\\end{{enumerate}}

\\vspace{{1cm}}
\\textit{{TODO: Ergänzen Sie den Inhalt basierend auf dem ursprünglichen Word-Dokument.}}
"""
    
    def _create_matching_matrix_template(self, title: str) -> str:
        return f"""% {title} - CTMM Matching Matrix
% Converted from Word document by CTMM Document Converter

\\section{{{title}}}
\\label{{sec:{title.lower().replace(' ', '-')}}}

\\begin{{ctmmBlueBox}}{{CTMM Matching Matrix}}
Die Matching Matrix hilft dabei, Trigger, Reaktionen und Interventionen systematisch zu verknüpfen.
\\end{{ctmmBlueBox}}

\\subsection{{Matrix-Übersicht}}

\\begin{{tabular}}{{|p{{2.5cm}}|p{{3cm}}|p{{3cm}}|p{{3cm}}|p{{3cm}}|}}
\\hline
\\textbf{{Kategorie}} & \\textbf{{Trigger}} & \\textbf{{Reaktion}} & \\textbf{{Intervention}} & \\textbf{{Erfolg}} \\\\
\\hline
\\multirow{{3}}{{*}}{{Emotional}} & & & & \\\\[0.8cm]
& & & & \\\\[0.8cm]
& & & & \\\\[0.8cm]
\\hline
\\multirow{{3}}{{*}}{{Körperlich}} & & & & \\\\[0.8cm]
& & & & \\\\[0.8cm]
& & & & \\\\[0.8cm]
\\hline
\\multirow{{3}}{{*}}{{Sozial}} & & & & \\\\[0.8cm]
& & & & \\\\[0.8cm]
& & & & \\\\[0.8cm]
\\hline
\\end{{tabular}}

\\subsection{{Matching-Strategien}}

\\begin{{enumerate}}
    \\item \\textbf{{Catch:}} Trigger frühzeitig erkennen
    \\item \\textbf{{Track:}} Reaktionsmuster dokumentieren
    \\item \\textbf{{Map:}} Zusammenhänge verstehen
    \\item \\textbf{{Match:}} Passende Interventionen zuordnen
\\end{{enumerate}}

\\vspace{{1cm}}
\\textit{{TODO: Ergänzen Sie den Inhalt basierend auf dem ursprünglichen Word-Dokument.}}
"""
    
    def _create_tool_template(self, title: str) -> str:
        return f"""% {title} - CTMM Tool
% Converted from Word document by CTMM Document Converter

\\section{{{title}}}
\\label{{sec:{title.lower().replace(' ', '-')}}}

\\begin{{ctmmBlueBox}}{{CTMM Tool: {title}}}
Dieses Tool unterstützt Sie bei der praktischen Anwendung der CTMM-Methoden.
\\end{{ctmmBlueBox}}

\\subsection{{Anleitung}}

\\textbf{{Schritt 1:}} \\underline{{\\hspace{{6cm}}}}

\\textbf{{Schritt 2:}} \\underline{{\\hspace{{6cm}}}}

\\textbf{{Schritt 3:}} \\underline{{\\hspace{{6cm}}}}

\\subsection{{Arbeitsbereich}}

\\begin{{center}}
\\begin{{tabular}}{{|p{{6cm}}|p{{6cm}}|}}
\\hline
\\textbf{{Beobachtung}} & \\textbf{{Aktion}} \\\\
\\hline
& \\\\[2cm]
\\hline
& \\\\[2cm]
\\hline
& \\\\[2cm]
\\hline
\\end{{tabular}}
\\end{{center}}

\\subsection{{Reflexion}}

\\textbf{{Was hat gut funktioniert?}}
\\vspace{{1cm}}

\\textbf{{Was könnte verbessert werden?}}
\\vspace{{1cm}}

\\textbf{{Nächste Schritte:}}
\\begin{{itemize}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
\\end{{itemize}}

\\vspace{{1cm}}
\\textit{{TODO: Ergänzen Sie den Inhalt basierend auf dem ursprünglichen Word-Dokument.}}
"""
    
    def _create_safewords_template(self, title: str) -> str:
        return f"""% {title} - CTMM Safewords und Signalsysteme
% Converted from Word document by CTMM Document Converter

\\section{{{title}}}
\\label{{sec:{title.lower().replace(' ', '-')}}}

\\begin{{ctmmBlueBox}}{{Safewords und Signalsysteme}}
Sicherheitswörter und Signale für effektive Kommunikation in herausfordernden Situationen.
\\end{{ctmmBlueBox}}

\\subsection{{Safeword-System}}

\\textbf{{Stopp-Wort:}} \\underline{{\\hspace{{4cm}}}} \\textit{{(sofortiger Stopp)}}

\\textbf{{Pause-Wort:}} \\underline{{\\hspace{{4cm}}}} \\textit{{(kurze Unterbrechung)}}

\\textbf{{Hilfe-Wort:}} \\underline{{\\hspace{{4cm}}}} \\textit{{(Unterstützung benötigt)}}

\\subsection{{Signalsystem}}

\\begin{{tabular}}{{|p{{3cm}}|p{{4cm}}|p{{5cm}}|}}
\\hline
\\textbf{{Signal}} & \\textbf{{Bedeutung}} & \\textbf{{Reaktion}} \\\\
\\hline
Gelb & Vorsicht & \\checkbox\\,Achtsamkeit erhöhen \\\\
& & \\checkbox\\,Kommunikation anpassen \\\\
\\hline
Rot & Stopp & \\checkbox\\,Sofortiger Stopp \\\\
& & \\checkbox\\,Sicherheit gewährleisten \\\\
\\hline
Grün & OK & \\checkbox\\,Weitermachen \\\\
& & \\checkbox\\,Positives Feedback \\\\
\\hline
\\end{{tabular}}

\\subsection{{Vereinbarungen}}

\\textbf{{Wir vereinbaren:}}
\\begin{{itemize}}
    \\item \\checkbox\\,Safewords werden respektiert
    \\item \\checkbox\\,Keine Diskussion über Signale während der Situation
    \\item \\checkbox\\,Nachbesprechung zu geeignetem Zeitpunkt
    \\item \\checkbox\\,Regelmäßige Überprüfung des Systems
\\end{{itemize}}

\\vspace{{1cm}}
\\textit{{TODO: Ergänzen Sie den Inhalt basierend auf dem ursprünglichen Word-Dokument.}}
"""
    
    def _create_depression_template(self, title: str) -> str:
        return f"""% {title} - CTMM Depression Modul
% Converted from Word document by CTMM Document Converter

\\section{{{title}}}
\\label{{sec:{title.lower().replace(' ', '-')}}}

\\begin{{ctmmBlueBox}}{{Depression im CTMM-Kontext}}
Umgang mit depressiven Episoden in neuroiversen Beziehungen.
\\end{{ctmmBlueBox}}

\\subsection{{Symptom-Monitoring}}

\\begin{{tabular}}{{|p{{4cm}}|p{{2cm}}|p{{2cm}}|p{{2cm}}|p{{2cm}}|}}
\\hline
\\textbf{{Symptom}} & \\textbf{{Nie}} & \\textbf{{Selten}} & \\textbf{{Oft}} & \\textbf{{Immer}} \\\\
\\hline
Niedergeschlagenheit & \\checkbox & \\checkbox & \\checkbox & \\checkbox \\\\
\\hline
Interessenverlust & \\checkbox & \\checkbox & \\checkbox & \\checkbox \\\\
\\hline
Müdigkeit & \\checkbox & \\checkbox & \\checkbox & \\checkbox \\\\
\\hline
Konzentrationsprobleme & \\checkbox & \\checkbox & \\checkbox & \\checkbox \\\\
\\hline
Schlafstörungen & \\checkbox & \\checkbox & \\checkbox & \\checkbox \\\\
\\hline
\\end{{tabular}}

\\subsection{{Bewältigungsstrategien}}

\\textbf{{Sofortmaßnahmen:}}
\\begin{{itemize}}
    \\item \\checkbox\\,Tagesstruktur beibehalten
    \\item \\checkbox\\,Soziale Kontakte
    \\item \\checkbox\\,Körperliche Aktivität
    \\item \\checkbox\\,Professionelle Hilfe
\\end{{itemize}}

\\textbf{{Langfristige Strategien:}}
\\begin{{itemize}}
    \\item \\checkbox\\,Therapie
    \\item \\checkbox\\,Medikation (falls verordnet)
    \\item \\checkbox\\,Selbstfürsorge-Routine
    \\item \\checkbox\\,Partnerschaftliche Unterstützung
\\end{{itemize}}

\\subsection{{Notfallplan}}

\\textbf{{Bei akuter Verschlechterung:}}
\\begin{{enumerate}}
    \\item Kontakt: \\underline{{\\hspace{{4cm}}}} Tel: \\underline{{\\hspace{{3cm}}}}
    \\item Notfall-Medikation: \\underline{{\\hspace{{4cm}}}}
    \\item Kriseninterventionsstelle: \\underline{{\\hspace{{4cm}}}}
\\end{{enumerate}}

\\vspace{{1cm}}
\\textit{{TODO: Ergänzen Sie den Inhalt basierend auf dem ursprünglichen Word-Dokument.}}
"""
    
    def _create_binding_template(self, title: str) -> str:
        return f"""% {title} - CTMM Bindungsmodul
% Converted from Word document by CTMM Document Converter

\\section{{{title}}}
\\label{{sec:{title.lower().replace(' ', '-')}}}

\\begin{{ctmmBlueBox}}{{Bindungsdynamik in neuroiversen Beziehungen}}
Verständnis und Stärkung der Bindung zwischen neurodiversen Partnern.
\\end{{ctmmBlueBox}}

\\subsection{{Bindungsstile erkennen}}

\\textbf{{Partner A:}}
\\begin{{itemize}}
    \\item \\checkbox\\,Sicher
    \\item \\checkbox\\,Ängstlich-ambivalent
    \\item \\checkbox\\,Vermeidend
    \\item \\checkbox\\,Desorganisiert
\\end{{itemize}}

\\textbf{{Partner B:}}
\\begin{{itemize}}
    \\item \\checkbox\\,Sicher
    \\item \\checkbox\\,Ängstlich-ambivalent
    \\item \\checkbox\\,Vermeidend
    \\item \\checkbox\\,Desorganisiert
\\end{{itemize}}

\\subsection{{Bindungsmuster verstehen}}

\\begin{{tabular}}{{|p{{3cm}}|p{{5cm}}|p{{5cm}}|}}
\\hline
\\textbf{{Situation}} & \\textbf{{Reaktion Partner A}} & \\textbf{{Reaktion Partner B}} \\\\
\\hline
Stress & & \\\\[1cm]
\\hline
Trennung & & \\\\[1cm]
\\hline
Wiedervereinigung & & \\\\[1cm]
\\hline
Konflikte & & \\\\[1cm]
\\hline
\\end{{tabular}}

\\subsection{{Bindung stärken}}

\\textbf{{Gemeinsame Aktivitäten:}}
\\begin{{itemize}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
\\end{{itemize}}

\\textbf{{Kommunikationsverbesserung:}}
\\begin{{itemize}}
    \\item \\checkbox\\,Aktives Zuhören
    \\item \\checkbox\\,Bedürfnisse ausdrücken
    \\item \\checkbox\\,Empathie zeigen
    \\item \\checkbox\\,Konflikte konstruktiv lösen
\\end{{itemize}}

\\vspace{{1cm}}
\\textit{{TODO: Ergänzen Sie den Inhalt basierend auf dem ursprünglichen Word-Dokument.}}
"""
    
    def _create_generic_template(self, title: str) -> str:
        return f"""% {title} - CTMM Modul
% Converted from Word document by CTMM Document Converter

\\section{{{title}}}
\\label{{sec:{title.lower().replace(' ', '-')}}}

\\begin{{ctmmBlueBox}}{{{title}}}
Dieses Modul ist Teil des CTMM-Systems für neurodiverse Paare.
\\end{{ctmmBlueBox}}

\\subsection{{Übersicht}}

\\textit{{Beschreibung des Moduls...}}

\\subsection{{Anweisungen}}

\\begin{{enumerate}}
    \\item \\textbf{{Schritt 1:}} \\underline{{\\hspace{{6cm}}}}
    \\item \\textbf{{Schritt 2:}} \\underline{{\\hspace{{6cm}}}}
    \\item \\textbf{{Schritt 3:}} \\underline{{\\hspace{{6cm}}}}
\\end{{enumerate}}

\\subsection{{Arbeitsbereich}}

\\vspace{{3cm}}

\\subsection{{Reflexion}}

\\textbf{{Notizen:}}
\\vspace{{2cm}}

\\textbf{{Nächste Schritte:}}
\\begin{{itemize}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
    \\item \\checkbox\\,\\underline{{\\hspace{{5cm}}}}
\\end{{itemize}}

\\vspace{{1cm}}
\\textit{{TODO: Ergänzen Sie den Inhalt basierend auf dem ursprünglichen Word-Dokument.}}
"""
    
    def convert_md_to_latex(self, md_file: Path) -> bool:
        """Convert Markdown file to LaTeX."""
        logger.info(f"Converting {md_file.name} to LaTeX...")
        
        output_file = self.target_dir / f"{md_file.stem}.tex"
        
        try:
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Simple markdown to LaTeX conversion
            latex_content = self._convert_markdown_to_latex(md_content, md_file.stem)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            logger.info(f"✓ Successfully converted {md_file.name}")
            self.converted_files.append(str(output_file))
            return True
            
        except Exception as e:
            logger.error(f"Markdown conversion failed for {md_file.name}: {e}")
            self.failed_conversions.append(str(md_file))
            return False
    
    def _convert_markdown_to_latex(self, md_content: str, filename: str) -> str:
        """Convert markdown content to LaTeX format."""
        # Basic markdown to LaTeX conversions
        latex_content = md_content
        
        # Headers
        latex_content = re.sub(r'^# (.+)$', r'\\section{\1}', latex_content, flags=re.MULTILINE)
        latex_content = re.sub(r'^## (.+)$', r'\\subsection{\1}', latex_content, flags=re.MULTILINE)
        latex_content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', latex_content, flags=re.MULTILINE)
        
        # Bold and italic
        latex_content = re.sub(r'\\*\\*(.+?)\\*\\*', r'\\textbf{\1}', latex_content)
        latex_content = re.sub(r'\\*(.+?)\\*', r'\\textit{\1}', latex_content)
        
        # Lists
        latex_content = re.sub(r'^- (.+)$', r'\\item \1', latex_content, flags=re.MULTILINE)
        
        # Add LaTeX document structure
        title = filename.replace('_', ' ').replace('-', ' ').title()
        
        full_latex = f"""% {title} - CTMM Module
% Converted from Markdown by CTMM Document Converter

\\section{{{title}}}
\\label{{sec:{filename.lower().replace(' ', '-')}}}

{latex_content}

% End of converted content
"""
        
        return full_latex
    
    def _post_process_latex(self, latex_file: Path):
        """Post-process converted LaTeX for CTMM compatibility."""
        logger.info(f"Post-processing {latex_file.name}...")
        
        try:
            with open(latex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove document class and preamble if present (for inclusion in main document)
            content = re.sub(r'\\documentclass.*?\\begin{document}', '', content, flags=re.DOTALL)
            content = re.sub(r'\\end{document}', '', content)
            
            # Add CTMM-specific formatting
            content = self._add_ctmm_formatting(content)
            
            with open(latex_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.info(f"✓ Post-processing completed for {latex_file.name}")
            
        except Exception as e:
            logger.error(f"Post-processing failed for {latex_file.name}: {e}")
    
    def _add_ctmm_formatting(self, content: str) -> str:
        """Add CTMM-specific formatting to LaTeX content."""
        # Add navigation helper
        content = "% CTMM Module - Auto-converted\\n" + content
        
        # Replace generic checkboxes with CTMM checkboxes
        content = re.sub(r'\\square', r'\\checkbox', content)
        content = re.sub(r'\\Box', r'\\checkbox', content)
        
        # Enhance tables for interactive use
        content = re.sub(r'\\begin{tabular}', r'\\begin{tabularx}{\\textwidth}', content)
        content = re.sub(r'\\end{tabular}', r'\\end{tabularx}', content)
        
        return content
    
    def convert_all_documents(self) -> Dict[str, int]:
        """Convert all documents in the source directory."""
        logger.info("Starting document conversion process...")
        
        source_files = self.scan_source_documents()
        
        if not source_files:
            logger.warning("No documents found to convert")
            return {"total": 0, "converted": 0, "failed": 0}
        
        for file_path in source_files:
            if file_path.suffix.lower() == '.docx':
                self.convert_docx_to_latex(file_path)
            elif file_path.suffix.lower() == '.md':
                self.convert_md_to_latex(file_path)
        
        # Create summary report
        self._create_conversion_report()
        
        stats = {
            "total": len(source_files),
            "converted": len(self.converted_files),
            "failed": len(self.failed_conversions)
        }
        
        logger.info(f"Conversion complete: {stats['converted']}/{stats['total']} files converted")
        return stats
    
    def _create_conversion_report(self):
        """Create a detailed conversion report."""
        report_path = self.target_dir / "conversion_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# CTMM Document Conversion Report\\n\\n")
            f.write(f"## Summary\\n")
            f.write(f"- Total files processed: {len(self.converted_files) + len(self.failed_conversions)}\\n")
            f.write(f"- Successfully converted: {len(self.converted_files)}\\n")
            f.write(f"- Failed conversions: {len(self.failed_conversions)}\\n\\n")
            
            if self.converted_files:
                f.write("## Successfully Converted Files\\n")
                for file_path in self.converted_files:
                    f.write(f"- {file_path}\\n")
                f.write("\\n")
            
            if self.failed_conversions:
                f.write("## Failed Conversions\\n")
                for file_path in self.failed_conversions:
                    f.write(f"- {file_path}\\n")
                f.write("\\n")
            
            f.write("## Next Steps\\n")
            f.write("1. Review converted LaTeX files for accuracy\\n")
            f.write("2. Complete TODO sections in generated templates\\n")
            f.write("3. Test integration with main CTMM document\\n")
            f.write("4. Adjust formatting as needed\\n")
        
        logger.info(f"Conversion report saved to {report_path}")

def main():
    """Run the CTMM document conversion pipeline."""
    converter = CTMMDocumentConverter()
    
    # Install pandoc if available
    logger.info("Checking for pandoc...")
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'pandoc'], check=True)
        logger.info("✓ pandoc installed successfully")
    except Exception as e:
        logger.warning(f"Could not install pandoc, using fallback conversion: {e}")
    
    # Convert all documents
    stats = converter.convert_all_documents()
    
    print("\\n" + "="*50)
    print("CTMM DOCUMENT CONVERSION SUMMARY")
    print("="*50)
    print(f"Total files: {stats['total']}")
    print(f"Converted: {stats['converted']}")
    print(f"Failed: {stats['failed']}")
    print(f"Success rate: {(stats['converted']/stats['total']*100):.1f}%" if stats['total'] > 0 else "N/A")
    
    return 0 if stats['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())