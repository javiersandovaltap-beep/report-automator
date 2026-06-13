# AGENTS.md

## Project purpose
This project automates data reading, PDF report generation, and email delivery.

## Working goal
- Understand the real workflow before changing files.
- Make small, safe, well-justified changes.
- Prioritize clarity, maintainability, and validation.

## Required workflow
1. Read README.md, this file, and CLAUDE.md before changing anything.
2. Explain the real program flow based on the code, not assumptions.
3. Propose a short plan before editing.
4. Make the smallest change necessary.
5. Summarize exactly what changed and how to verify it.

## Change rules
- Do not modify unrelated files.
- Do not refactor unnecessarily if it does not help the current goal.
- Do not assume behavior that is not confirmed in the code.
- If context is missing, ask before continuing.
- If a change affects multiple files, explain why.

## Validation
- Describe how to test the change manually.
- If scripts or tests are available, suggest which ones to run.
- Report residual risks, or explicitly say "none".

## Required completion format
- [Files Changed]
- [Logic Altered]
- [Verification Method]
- [Residual Risks]
