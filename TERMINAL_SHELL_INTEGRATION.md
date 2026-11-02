# Terminal Shell Integration

## Overview

This repository is configured with VS Code's **terminal shell integration** enabled by default. This provides enhanced terminal features for developers working on the CTMM LaTeX project.

## What is Shell Integration?

Shell integration allows VS Code's terminal to "understand" what's happening inside your shell, enabling additional features that improve the development experience.

## Features Enabled

When shell integration is active, you get:

- **Command Detection & Navigation**: Easily scroll and jump between commands in the terminal
- **Exit Code Decorations**: Visual indicators showing whether commands succeeded or failed
- **Enhanced Command Suggestions**: Better autocompletion in the terminal
- **Working Directory Detection**: VS Code automatically tracks your current directory
- **Sticky Scroll**: Commands stay visible at the top when scrolling
- **Quick Fixes**: Suggestions for fixing common terminal errors

## Supported Shells

Shell integration works automatically with these shells:

- **Linux/macOS**: bash, zsh, fish, pwsh (PowerShell)
- **Windows**: PowerShell, Git Bash, Command Prompt (limited)

## Configuration

The setting is configured in `.vscode/settings.json`:

```json
{
  "terminal.integrated.shellIntegration.enabled": true
}
```

## How It Works

When you open a terminal in VS Code, the editor automatically injects shell integration scripts into supported shells. This happens transparently and doesn't require any manual setup.

## Advanced Usage

### Manual Integration

For advanced scenarios where automatic injection doesn't work (e.g., SSH sessions, sub-shells, or complex shell setups), you can manually enable shell integration by adding this to your shell's configuration file:

**Bash** (`.bashrc` or `.bash_profile`):
```bash
[[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path bash)"
```

**Zsh** (`.zshrc`):
```zsh
[[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path zsh)"
```

**PowerShell** (`$PROFILE`):
```powershell
if ($env:TERM_PROGRAM -eq "vscode") { . "$(code --locate-shell-integration-path pwsh)" }
```

**Fish** (`~/.config/fish/config.fish`):
```fish
string match -q "$TERM_PROGRAM" "vscode"
and . (code --locate-shell-integration-path fish)
```

### Disabling Shell Integration

If you prefer a pure shell environment or experience conflicts with custom shell configurations:

1. Set the configuration to `false` in `.vscode/settings.json`:
```json
{
  "terminal.integrated.shellIntegration.enabled": false
}
```

2. Or add this to your User Settings in VS Code (affects all projects):
   - Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Type "Preferences: Open User Settings (JSON)"
   - Add the setting there

## Troubleshooting

### Shell integration not working?

1. **Check your shell version**: Ensure you're using a recent version of your shell
2. **Check for conflicts**: Look for errors in your shell's initialization files (`.bashrc`, `.zshrc`, etc.)
3. **Restart VS Code**: Sometimes a restart is needed after changing settings
4. **Check the output**: Open the "Terminal" output channel in VS Code to see any errors

### Performance issues?

If you notice slow terminal startup:
1. Check your shell's initialization files for slow operations
2. Consider using a lighter shell configuration for development
3. If issues persist, you can disable shell integration

## Benefits for CTMM Development

For working on this LaTeX project, shell integration provides:

- **Better build feedback**: Easily see when `pdflatex` or `make` commands succeed or fail
- **Command history navigation**: Quickly jump to previous build commands
- **Error visibility**: Failed commands are clearly marked in the terminal
- **Improved workflow**: Better integration between terminal and editor

### Practical Examples

**Building the PDF:**
```bash
# Without shell integration: Just text output
$ make build
pdflatex main.tex
...

# With shell integration: Visual indicators show success
$ make build  ✓ (green checkmark)
pdflatex main.tex
...
```

**Failed Compilation:**
```bash
# Failed builds are immediately visible with red markers
$ pdflatex main.tex  ✗ (red X, exit code 1)
! LaTeX Error: ...
```

**Command Navigation:**
- Use Ctrl+↑ / Ctrl+↓ (Cmd+↑ / Cmd+↓ on Mac) to jump between commands
- Click on command decorations to scroll to that command
- Failed commands are highlighted in red, successful in green

**Common CTMM Commands with Integration:**
```bash
# Build system check - see success/failure status at a glance
$ python3 ctmm_build.py  ✓

# Unit tests - quickly identify test failures
$ make unit-test  ✓

# PDF generation - visual feedback on compilation status  
$ make build  ✓

# Validation - immediate feedback on issues
$ make validate-pr  ✓
```

## References

- [VS Code Terminal Shell Integration Documentation](https://code.visualstudio.com/docs/terminal/shell-integration)
- [Terminal Advanced Topics](https://code.visualstudio.com/docs/terminal/advanced)

## Related Files

- `.vscode/settings.json` - Contains the shell integration configuration
- `.vscode/tasks.json` - Build tasks that benefit from shell integration
- `Makefile` - Common commands that work well with shell integration features
