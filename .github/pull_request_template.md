# Pull Request Template

## Description
Briefly describe what this PR accomplishes and why it's needed.

## Type of Changes
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] LaTeX/therapy content update

## Changes Made
- [ ] Added/modified LaTeX modules in `modules/`
- [ ] Updated style files in `style/`
- [ ] Modified build system (`ctmm_build.py`, `build_system.py`)
- [ ] Updated documentation (README, etc.)
- [ ] Added/updated tests
- [ ] Other: _______________

## Pre-submission Checklist
- [ ] My code follows the project's coding standards
- [ ] I have run `python3 ctmm_build.py` and it passes
- [ ] I have tested my changes locally
- [ ] My changes generate no new warnings/errors
- [ ] I have added documentation where necessary
- [ ] My LaTeX follows the CTMM conventions (packages in preamble, proper macros)

## Testing Done
Describe the testing you performed to verify your changes work correctly.

## For LaTeX Changes
- [ ] Tested compilation with `make build` (if pdflatex available)
- [ ] Verified German text encoding is correct
- [ ] Followed therapeutic content guidelines
- [ ] Used proper CTMM macros and styling

## Related Issues
Fixes #(issue number)

## Additional Notes
Any additional information that reviewers should know.

---
**Note for Reviewers**: This PR should contain substantive changes for effective Copilot review. Empty PRs with no file changes cannot be reviewed by Copilot.