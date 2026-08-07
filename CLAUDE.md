# Project
Report Automator is a Python-based project that automates data reading from CSV/Excel files, generates PDF reports with metrics and visualizations, and attempts email delivery. The technical stack includes:
- pandas>=2.2.0 for data processing
- reportlab>=4.0.0 for PDF generation  
- matplotlib>=3.8.0 for chart creation
- python-dotenv>=1.0.0 for environment configuration
- schedule>=1.2.0 for job scheduling
- openpyxl>=3.1.0 for Excel support

The pipeline follows: data loading → summary generation → chart creation (when applicable) → PDF construction → email attempt → immediate or scheduled execution.

# Commands
## Environment Setup
```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execution
```bash
# Immediate execution (default behavior)
python main.py
# or explicitly
python main.py --run-now

# Schedule daily execution
python main.py --schedule daily

# Schedule weekly execution (Mondays)
python main.py --schedule weekly
```

## Configuration
Create `.env` file from `.env.example` with:
- EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENTS
- DATA_FILE (default: sample_data/sales_data.csv)
- REPORT_TITLE, COMPANY_NAME
- OUTPUT_PDF (default: output/report.pdf)
- SCHEDULE_TIME (default: 08:00)

# Code Style
- [Files Changed]
- [Logic Altered]
- [Verification Method]
- [Residual Risks]

# Git & GitHub Workflow
Make atomic, descriptive commits after each logical change that has been verified. When ready to share changes, use native git commands (`git add`, `git commit`, `git push`) or suggest using the `/commit-push-pr` skill in Claude Code for streamlined PR creation. Each commit should include a clear summary of what was changed and how it was verified, following the Code Style format above.