# CTMM-System: Interaktive Therapie-Materialien in LaTeX

Ein umfassendes System zur Erstellung professioneller Therapiematerialien mit ausfüllbaren Formularen, speziell entwickelt für neurodiverse Paare und Personen mit psychischen Herausforderungen.

## 🚀 Quick Start

### Automated Build Management

The CTMM project includes a comprehensive automated build management system:

```bash
# Run comprehensive build analysis
python3 build_manager.py
# or
make check

# Build the PDF
make build        # Builds main.tex
make build-ci     # Builds main_final.tex for CI

# Clean up
make clean        # Remove build artifacts
make clean-all    # Remove all generated files
```

### Key Features

- **🔧 Automated Build Management**: Scans `main.tex` for dependencies and creates missing templates
- **📋 Template Generation**: Automatically creates structured `.sty` and `.tex` templates
- **🧪 Incremental Testing**: Isolates module-specific build errors through systematic testing
- **📊 Comprehensive Reporting**: Generates detailed `build_report.md` with analysis and recommendations
- **🛠️ Installation Guidance**: Provides helpful error messages and installation instructions

## 📖 Detailed Documentation

- **[BUILD_GUIDE.md](BUILD_GUIDE.md)**: Comprehensive quick-start guide and troubleshooting
- **[build_report.md](build_report.md)**: Generated analysis report (created after running build system)

## 🏗️ Build System Architecture

### Core Components

- **`build_manager.py`**: Main comprehensive build management system
- **`ctmm_build.py`**: Simplified build system for basic operations
- **`build_system.py`**: Detailed module analysis and testing
- **`main_final.tex`**: Dedicated CI build target
- **`Makefile`**: Intuitive command interface

### Workflow

1. **Dependency Scanning**: Analyzes `main.tex` for all `\usepackage{style/...}` and `\input{modules/...}`
2. **Template Generation**: Creates minimal templates for missing files with TODO guidelines
3. **Incremental Testing**: Tests modules one by one to isolate build errors
4. **Error Reporting**: Generates comprehensive reports and specific error logs
5. **Build Optimization**: Provides recommendations for resolving issues

## 📁 Project Structure

```
├── main.tex                    # Main document (development)
├── main_final.tex             # CI build target
├── build_manager.py           # Comprehensive build management
├── ctmm_build.py             # Simplified build system
├── build_system.py           # Detailed analysis system
├── Makefile                   # Build commands
├── BUILD_GUIDE.md            # Quick start documentation
├── style/                     # LaTeX style files
│   ├── ctmm-design.sty      # CTMM design elements
│   ├── form-elements.sty    # Interactive form components
│   └── ctmm-diagrams.sty    # Custom diagrams
├── modules/                   # Therapy content modules
│   ├── arbeitsblatt-*.tex   # Worksheets
│   ├── trigger*.tex         # Trigger management
│   └── *.tex               # Other therapy modules
└── .github/workflows/        # CI/CD automation
```

## 🛠️ Available Commands

| Command | Description |
|---------|-------------|
| `make check` | Run build manager analysis |
| `make build` | Build main PDF (main.tex) |
| `make build-ci` | Build CI PDF (main_final.tex) |
| `make analyze` | Run comprehensive analysis |
| `make test` | Quick build system test |
| `make clean` | Remove build artifacts |
| `make clean-all` | Remove all generated files |
| `make help` | Show available commands |

### Build Manager Options

```bash
python3 build_manager.py              # Basic analysis
python3 build_manager.py --verbose    # Detailed logging
python3 build_manager.py --test-file main_final.tex  # Test specific file
```

## 🧠 Content Overview

### Therapeutic Focus Areas

- **Depression und Stimmungsstörungen**
- **Trigger-Management und Bewältigungsstrategien**
- **Borderline-Persönlichkeitsstörung (BPS)**
- **ADHS und Autismus-Spektrum-Störung (ASS)**
- **Komplexe PTBS (KPTBS)**
- **Beziehungsdynamiken und Bindungsmuster**

### Interactive Features

- ✅ **Ausfüllbare PDF-Formulare** mit Checkboxen und Textfeldern
- 🎨 **CTMM-Farbschema** für konsistente Gestaltung
- 📱 **QR-Codes** für digitale Ressourcen
- 🧭 **Navigationssystem** mit FontAwesome-Icons
- 📋 **Strukturierte Arbeitsblätter** für Selbstreflexion

## ⚙️ Installation

### Prerequisites

**LaTeX Distribution:**
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-lang-german

# macOS (Homebrew)
brew install --cask mactex

# Windows
# Download MiKTeX from https://miktex.org/
```

**Python Dependencies:**
```bash
pip install chardet
```

### Verification

```bash
# Test installation
python3 build_manager.py --verbose

# Check LaTeX packages
make deps
```

## 🔄 Development Workflow

### Adding New Content

1. **Add reference in main.tex:**
   ```latex
   \input{modules/my-new-module}
   ```

2. **Run build system:**
   ```bash
   python3 build_manager.py
   ```

3. **Complete generated template:**
   - Edit the created `.tex` file
   - Follow guidelines in `TODO_*.md`
   - Remove TODO file when complete

### Build Testing

```bash
# Test your changes
make check

# Build PDF
make build

# Check for issues
cat build_report.md
```

## 📊 Understanding Output

### Build Status

- ✅ **SUCCESS**: All systems operational
- ⚠️ **WARNING**: Minor issues detected
- ❌ **FAILED**: Build errors need attention

### Generated Files

- `build_report.md`: Comprehensive analysis and recommendations
- `build_manager.log`: Detailed operation log
- `TODO_*.md`: Task lists for new templates
- `build_error_*.log`: Specific error diagnostics

## 🆘 Troubleshooting

### Common Issues

**Missing LaTeX Packages:**
```bash
# Install missing packages
sudo apt-get install texlive-lang-german
sudo apt-get install texlive-fonts-extra
```

**Build Failures:**
```bash
# Check detailed error logs
cat build_error_modulename.log

# Clean and retry
make clean-all
python3 build_manager.py
```

**Template Completion:**
```bash
# List incomplete templates
ls TODO_*.md

# Complete templates and remove TODO files
rm TODO_*.md  # after completing content
```

## 🤝 Contributing

1. **Run build system** before making changes
2. **Add new content** through main.tex references
3. **Complete generated templates** following guidelines
4. **Test builds** with `make build`
5. **Check reports** in `build_report.md`

## 📄 License

Dieses Projekt steht unter der [MIT License](LICENSE).

## 🙏 Acknowledgments

Entwickelt für die therapeutische Arbeit mit neurodiversen Paaren und Personen mit komplexen psychischen Herausforderungen.

---

💡 **Tip**: Start with `python3 build_manager.py` to analyze your system and get recommendations for next steps.