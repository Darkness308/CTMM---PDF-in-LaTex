# CTMM LaTeX Framework

CTMM (Catch-Track-Map-Match) is a modular LaTeX framework for generating German therapy materials with interactive PDF forms. The system provides 14 therapy modules covering depression, trigger management, relationship dynamics, and therapeutic documentation.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Dependencies
- Install LaTeX with German language support:
  ```bash
  sudo apt update
  sudo apt install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german texlive-science
  ```
- Install Python dependencies:
  ```bash
  pip install chardet
  ```

### Build the Project
Choose any of these build methods (all complete in 1-3 seconds):

**Method 1: CTMM Build System (Recommended)**
```bash
python3 ctmm_build.py
```
- Checks dependencies and missing files
- Creates templates for missing modules automatically
- Takes ~1.7 seconds

**Method 2: Make Build**
```bash
make build
```
- Runs pdflatex twice for cross-references
- Takes ~2.2 seconds

**Method 3: VS Code Build Task**
```bash
mkdir -p build
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex
```
- Fastest option (~1.1 seconds)
- Outputs to `build/` directory with SyncTeX support

### Test the Build System
```bash
make test
```
- Quick validation of build system
- Takes ~1.7 seconds

### Clean Build Artifacts
```bash
make clean
```
- Removes *.aux, *.log, *.out, *.toc, *.pdf files
- Cleans temporary build files

## Validation

### Build Success Indicators
- PDF generation: `main.pdf` (27 pages, ~430KB) or `build/main.pdf`
- No LaTeX compilation errors in logs
- Exit code 0 from build commands

### Manual Validation Steps
After making changes, always verify:
1. Run the build system: `python3 ctmm_build.py`
2. Check PDF is generated with correct page count
3. Verify no new LaTeX errors in build logs
4. Test any new modules by including them in `main.tex`

### Development Environment Testing
- **GitHub Codespaces**: Pre-configured with devcontainer.json
- **VS Code**: Use Ctrl+Shift+P → "Tasks: Run Task" → "CTMM: Kompilieren"
- **Local development**: Ensure German language pack is installed

## Common Tasks

### Adding New Modules
1. Add reference in main.tex:
   ```latex
   \input{modules/new-module-name}
   ```
2. Run build system to auto-generate template:
   ```bash
   python3 ctmm_build.py
   ```
3. Edit the generated `modules/new-module-name.tex`
4. Remove the `modules/TODO_new-module-name.md` when complete

### Troubleshooting LaTeX Errors
- **"Unknown option 'ngerman'"**: Install `texlive-lang-german`
- **"Undefined control sequence"**: Check if new macros are defined in preamble, not in modules
- **Package loading errors**: Only load packages in main.tex preamble, never in modules
- **Build failures**: Run `python3 build_system.py --verbose` for detailed analysis

### Project Structure Navigation
```
/
├── main.tex              # Main document entry point
├── Makefile              # Build automation
├── ctmm_build.py         # Primary build system (use this)
├── build_system.py       # Advanced analysis tool
├── style/                # LaTeX style packages
│   ├── ctmm-design.sty   # Main design system
│   ├── form-elements.sty # Interactive PDF forms
│   └── ctmm-diagrams.sty # TikZ diagrams
├── modules/              # Therapy content modules (14 files)
│   ├── depression.tex
│   ├── triggermanagement.tex
│   ├── bindungsleitfaden.tex
│   └── [11 other modules]
├── build/                # VS Code build output
├── .devcontainer/        # GitHub Codespaces configuration
├── .vscode/tasks.json    # VS Code build tasks
└── .github/workflows/    # CI/CD automation
```

### Key Build System Features
- **Automatic dependency checking**: Scans main.tex for missing references
- **Template generation**: Creates structured templates for new modules
- **Incremental testing**: Tests modules individually to isolate issues
- **Encoding detection**: Handles UTF-8 and other text encodings automatically
- **Error isolation**: Identifies problematic modules without breaking the build

### GitHub Actions Integration
The project includes automated builds via `.github/workflows/latex-build.yml`:
- Runs on push/PR to main branch
- Validates build system and generates PDF artifact
- Uploads build logs on failure

### Best Practices for LaTeX Development
- **Package loading**: Only use `\usepackage{}` in main.tex preamble
- **Macro definitions**: Define custom commands centrally, not in modules
- **Checkbox symbols**: Use `\checkbox` and `\checkedbox` macros, never direct symbols
- **Module content**: Keep modules focused on content, not package/macro definitions
- **Cross-references**: LaTeX may need two passes to resolve references correctly

### Common Commands Reference
```bash
# Quick build validation
make test

# Full build with analysis  
python3 build_system.py --verbose

# Standard build methods
make build                    # Make-based build
python3 ctmm_build.py        # CTMM build system
make clean                   # Clean artifacts

# VS Code build (fastest)
mkdir -p build && pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex
```

## Critical Success Factors
- German language LaTeX packages are essential for compilation
- Build times are very fast (1-3 seconds) - no long waits expected
- PDF generation with 27 pages confirms successful build
- Multiple build methods provide flexibility for different development environments
- Custom build system handles missing files gracefully by generating templates