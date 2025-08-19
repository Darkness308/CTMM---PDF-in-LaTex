# CTMM Module Generator Documentation

## Overview

The CTMM Module Generator is a comprehensive system for creating professional LaTeX therapeutic materials within the Catch-Track-Map-Match (CTMM) framework. It automates the creation of three main types of therapeutic modules while ensuring consistency with CTMM design patterns and German therapeutic standards.

## Quick Start

### Interactive Mode (Recommended)
```bash
./create-module.sh
```

### Command Line Mode
```bash
# Generate different module types
node module-generator.js arbeitsblatt taeglicher-stimmungscheck
node module-generator.js tool 5-4-3-2-1-grounding  
node module-generator.js notfallkarte panikattacken
```

### VS Code Integration
- **Ctrl+Shift+P** → "Tasks: Run Task" → "CTMM: Module Generator (Interactive)"
- Use individual generators: "CTMM: Generate Arbeitsblatt/Tool/Notfallkarte"

## Module Types

### 1. Arbeitsblatt (Worksheets)
**Purpose**: Interactive therapeutic worksheets for self-reflection and skill building.

**Features**:
- Personal information fields (name, date)
- Goal-setting sections
- Situation assessment areas
- Reflection and coping strategy sections
- Success documentation
- Learning points for future sessions

**Example Modules**:
- `arbeitsblatt-taeglicher-stimmungscheck` - Daily mood tracking
- `arbeitsblatt-trigger-analyse` - Trigger pattern analysis
- `arbeitsblatt-selbstreflexion` - Self-reflection exercises

**Generated Structure**:
```latex
% Header with module information
\newpage
\section*{\faEdit~MODULE_NAME}
\label{sec:arbeitsblatt-module-name}

% Main working area with CTMM blue box
\begin{ctmmBlueBox}{\faEdit~Arbeitsbereich}
  % Personal fields and goal setting
\end{ctmmBlueBox}

% Structured sections for therapeutic work
\subsection*{1. Situation erfassen}
\subsection*{2. Reflexion und Bewältigung}  
\subsection*{3. Erfolg dokumentieren}
```

### 2. Tool (Therapeutic Techniques)
**Purpose**: Step-by-step guides for specific therapeutic techniques and coping strategies.

**Features**:
- Tool number assignment (random 10-59)
- Contextual usage information
- Theoretical background
- Step-by-step instructions
- Personal practice area
- Effectiveness tracking
- Integration planning

**Example Modules**:
- `tool-5-4-3-2-1-grounding` - Grounding technique using five senses
- `tool-atemtechnik-4-7-8` - Breathing exercise for anxiety
- `tool-kommunikation-ich-botschaften` - Communication skills

**Generated Structure**:
```latex
% Header with tool number and title
\newpage
\section*{\textcolor{ctmmOrange}{\faTools~TOOL XX: TECHNIQUE_NAME}}
\label{sec:tool-technique-name}

% Inspirational quote and usage context
\begin{quote}
  % Motivational quote and when to use
\end{quote}

% Four main sections
\subsection*{1. Grundlagen}        % Theory and background
\subsection*{2. Anwendung}         % Step-by-step instructions  
\subsection*{3. Persönlicher Arbeitsbereich}  % Practice area
\subsection*{4. Integration in den Alltag}     % Daily life integration
```

### 3. Notfallkarte (Emergency Cards)
**Purpose**: Crisis management cards with immediate action steps and emergency contacts.

**Features**:
- Emergency contact information
- Immediate action protocols
- Personal safety strategies
- Warning sign identification
- Professional help guidelines
- Crisis hotline information

**Example Modules**:
- `notfallkarte-panikattacken` - Panic attack emergency protocol
- `notfallkarte-dissoziative-episoden` - Dissociation management
- `notfallkarte-selbstverletzung` - Self-harm prevention

**Generated Structure**:
```latex
% Header with emergency card title
\newpage
\section*{\textcolor{ctmmRed}{\faHeartbeat~NOTFALLKARTE: CRISIS_TYPE}}
\label{sec:notfall-crisis-type}

% Critical information warning
\begin{ctmmRedBox}{\faExclamationTriangle~WICHTIGE INFORMATION}
  % Usage instructions
\end{ctmmRedBox}

% Five main sections
\subsection*{\faPhoneAlt~NOTFALLKONTAKTE}      % Emergency contacts
\subsection*{\faFirstAid~SOFORTMASSNAHMEN}     % Immediate actions
\subsection*{\faShieldAlt~PERSÖNLICHE SICHERHEITSSTRATEGIE}  % Safety strategies
\subsection*{\faExclamationCircle~WARNSIGNALE} % Warning signs
```

## CTMM Design System Integration

### Color Scheme
The generator automatically applies CTMM's therapeutic color psychology:

- **ctmmBlue** (#003087) - Arbeitsblätter (trust, stability, reflection)
- **ctmmOrange** (#FF6200) - Tools (energy, motivation, action)
- **ctmmRed** (#D32F2F) - Notfallkarten (urgency, attention, safety)
- **ctmmGreen** (#4CAF50) - Success sections (growth, healing, progress)
- **ctmmPurple** (#7B1FA2) - Special elements (wisdom, transformation)
- **ctmmGray** (#757575) - Contact information (neutral, reliable)
- **ctmmYellow** (#FFC107) - Tips and warnings (attention, caution)

### Form Elements
All modules use CTMM's interactive form components:

```latex
% Text input fields
\ctmmTextField[width]{default text}{field_name}

% Multi-line text areas  
\ctmmTextArea[width]{lines}{label}{field_name}

% Checkboxes with therapeutic options
\ctmmCheckBox[field_name]{Label text}
```

### Box Components
Modules leverage CTMM's colored box system:

```latex
\begin{ctmmBlueBox}{Title}      % Information and working areas
\begin{ctmmGreenBox}{Title}     % Instructions and positive content  
\begin{ctmmOrangeBox}{Title}    % Techniques and methods
\begin{ctmmRedBox}{Title}       % Warnings and emergency information
\begin{ctmmPurpleBox}{Title}    % Special insights and reflections
\begin{ctmmGrayBox}{Title}      % Neutral information and contacts
\begin{ctmmYellowBox}{Title}    % Tips and important notes
```

### Typography and Icons
The system integrates FontAwesome icons and CTMM typography standards:

```latex
% Common therapeutic icons
\faEdit         % Worksheets and writing
\faTools        % Techniques and methods
\faHeartbeat    % Emergency and medical
\faExclamationCircle  % Triggers and attention
\faShieldAlt    % Safety and protection
\faPhoneAlt     % Contacts and communication
\faFirstAid     % Immediate help and crisis
```

## Content Generation Features

### Intelligent Content Adaptation
The generator analyzes module names to provide contextually appropriate content:

**Grounding Techniques**:
- Recognizes keywords: "grounding", "erdung", "5-4-3-2-1"
- Generates specific sensory-based steps
- Includes dissociation and overwhelm context

**Breathing Techniques**:
- Recognizes keywords: "atem", "breathing", "4-7-8"
- Provides structured breathing instructions
- Includes anxiety and stress context

**Communication Tools**:
- Recognizes keywords: "kommunikation", "gespräch"
- Focuses on relationship and expression skills
- Includes conflict resolution context

**Panic/Crisis Management**:
- Recognizes keywords: "panik", "notfall", "krise"
- Provides immediate action protocols
- Includes safety-first approaches

### German Therapeutic Terminology
All generated content uses professional German therapeutic language:

- **Du-Form**: Directly addressing the client in a supportive manner
- **Professional terminology**: Correct psychological and therapeutic terms
- **Empathetic language**: Non-judgmental, encouraging expressions
- **Cultural sensitivity**: Appropriate for German-speaking therapy contexts

### Therapeutic Best Practices
Content follows evidence-based therapeutic approaches:

- **Trauma-informed**: Safe, empowering language and approaches
- **Strength-based**: Focus on resources and capabilities
- **Collaborative**: Encourages active participation
- **Practical**: Concrete, actionable steps and strategies

## Technical Implementation

### File Structure
```
CTMM-Repository/
├── module-generator.js          # Core JavaScript generator
├── create-module.sh            # Interactive shell interface
├── modules/                    # Generated modules directory
│   ├── arbeitsblatt-*.tex     # Worksheet modules
│   ├── tool-*.tex             # Tool modules
│   └── notfallkarte-*.tex     # Emergency card modules
├── .vscode/tasks.json         # VS Code task integration
└── main.tex                   # Main LaTeX document
```

### Generator Architecture
```javascript
class CTMMModuleGenerator {
    // Module type validation and file management
    generateModule(type, name, options)
    
    // Content generation methods
    generateArbeitsblatt(name, options)
    generateTool(name, options)  
    generateNotfallkarte(name, options)
    
    // Content intelligence helpers
    generateToolQuote(name)
    generateToolUsage(name)
    generateEmergencySteps(name)
}
```

### Integration Points
The generator integrates seamlessly with existing CTMM infrastructure:

1. **Build System**: Compatible with `ctmm_build.py`
2. **Validation**: Passes `validate_latex_syntax.py` checks
3. **Style System**: Uses existing `.sty` files in `style/` directory
4. **Main Document**: Modules can be included via `\input{modules/...}`

## Usage Examples

### Creating a Daily Mood Tracking Worksheet
```bash
# Interactive mode
./create-module.sh
# Select: arbeitsblatt
# Name: taeglicher-stimmungscheck

# Command line mode  
node module-generator.js arbeitsblatt taeglicher-stimmungscheck
```

**Generated features**:
- Personal identification fields
- Mood assessment scales
- Trigger identification checkboxes
- Coping strategy documentation
- Daily goal setting area
- Success and learning sections

### Creating a Crisis Communication Tool
```bash
# Generate a tool for crisis communication
node module-generator.js tool krisenkommunikation-partner

# Generated features include:
# - When to use this communication approach
# - Step-by-step conversation guide
# - De-escalation techniques
# - Practice scenarios
# - Effectiveness tracking
```

### Creating an Emergency Self-Harm Prevention Card
```bash
# Generate emergency card for self-harm situations
node module-generator.js notfallkarte selbstverletzung-praevention

# Generated features include:
# - Immediate safety protocols
# - Emergency contact information
# - Alternative coping strategies
# - Warning sign identification
# - Professional help guidelines
```

## Customization Options

### Module Content Adaptation
After generation, modules can be customized for specific needs:

1. **Therapeutic Content**: Modify questions, instructions, and guidance
2. **Form Fields**: Adjust field sizes, labels, and validation
3. **Visual Design**: Change colors, icons, and layout elements
4. **Integration**: Add cross-references to other modules

### Template Modification
Advanced users can modify the generator templates:

1. **Content Templates**: Edit `generateArbeitsblatt()`, `generateTool()`, `generateNotfallkarte()` methods
2. **Design Elements**: Update color schemes and icon mappings
3. **Therapeutic Approaches**: Add new content generation patterns
4. **Language Localization**: Adapt for other languages (with appropriate therapeutic terminology)

## Integration Workflow

### Standard Module Development Process
1. **Generate Module**: Use generator to create base structure
2. **Review Content**: Validate therapeutic appropriateness
3. **Customize Details**: Adapt for specific client needs or therapeutic goals
4. **Add to Main Document**: Include in `main.tex` with `\input{modules/module-name}`
5. **Test Build**: Run `python3 ctmm_build.py` to validate
6. **Generate PDF**: Use `make build` for final document

### Quality Assurance Checklist
- [ ] **Therapeutic Content**: Appropriate, safe, evidence-based
- [ ] **Language Quality**: Professional German therapeutic terminology
- [ ] **LaTeX Syntax**: Valid syntax, proper escaping
- [ ] **CTMM Design**: Correct colors, fonts, and styling
- [ ] **Form Functionality**: Working interactive elements
- [ ] **Cross-References**: Proper navigation and linking
- [ ] **Accessibility**: Clear, readable, culturally appropriate

## Troubleshooting

### Common Issues

**Module Generation Fails**:
```bash
# Check Node.js installation
node --version

# Verify script permissions
chmod +x create-module.sh

# Check current directory
ls -la module-generator.js
```

**LaTeX Build Errors**:
```bash
# Run CTMM validation
python3 ctmm_build.py

# Check LaTeX syntax
python3 validate_latex_syntax.py

# Verify module content
cat modules/module-name.tex
```

**Missing Dependencies**:
```bash
# Install Node.js (Ubuntu/Debian)
sudo apt update && sudo apt install nodejs

# Install Python dependencies
pip install chardet

# Verify LaTeX installation
pdflatex --version
```

### Getting Help

**Community Support**:
- GitHub Issues: Report bugs and request features
- Documentation: Refer to CTMM comprehensive guides
- Examples: Study existing modules in `modules/` directory

**Development Support**:
- Build System: `python3 ctmm_build.py --help`
- Validation Tools: `python3 validate_latex_syntax.py`
- VS Code Tasks: Integrated workflows and problem matchers

## Advanced Features

### Batch Module Generation
Create multiple related modules efficiently:

```bash
# Generate a complete therapy module set
for module in "stimmungsregulation" "trigger-management" "kommunikation"; do
    node module-generator.js tool "$module"
done
```

### Custom Content Patterns
Add specialized content generation for specific therapeutic approaches:

```javascript
// Custom content for DBT modules
generateDBTTool(name, options) {
    // Dialectical Behavior Therapy specific content
    // Distress tolerance, emotion regulation, etc.
}

// Custom content for EMDR modules  
generateEMDRTool(name, options) {
    // Eye Movement Desensitization specific content
    // Resource installation, safe place, etc.
}
```

### Integration with External Systems
The generator can be extended for integration with:

- **Electronic Health Records (EHR)**: Export module data
- **Therapy Management Software**: Import progress tracking
- **Educational Platforms**: Create learning modules
- **Assessment Tools**: Generate evaluation instruments

## Future Development

### Planned Features
- **Multi-language Support**: English, French therapeutic terminology
- **Template Library**: Expandable content templates
- **AI Content Assistance**: GPT-based content suggestions
- **Interactive PDF Forms**: Enhanced digital interactivity
- **Progress Tracking Integration**: Automatic outcome measurement

### Contributing
The CTMM Module Generator is designed for community contribution:

1. **Content Templates**: Add new therapeutic approaches
2. **Design Elements**: Expand visual and interactive components
3. **Integration Tools**: Develop connections with therapy software
4. **Validation Systems**: Enhance quality assurance processes

---

**Version**: 1.0.0  
**Last Updated**: August 2024  
**License**: Open source under CTMM project terms  
**Support**: CTMM-Team via GitHub Issues