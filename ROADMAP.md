# ROADMAP.md

## Objective

Report Automator is a local Python pipeline that turns tabular data
(CSV/XLSX) into a PDF report with summary metrics and an optional chart,
then attempts email delivery. It is built as a portfolio project
demonstrating modular architecture, automated testing, defensive
configuration handling, and a disciplined AI-assisted development workflow
using Claude Code (see `.claude/` for agent and enforcement configuration).

## Status

| Area | Status |
|---|---|
| Core pipeline (load -> summarize -> chart -> PDF -> email) | Complete |
| Automated test suite (pytest + Ruff) | Complete -- 49 tests, no lint findings |
| Configuration validation | Complete |
| CLI: immediate run, scheduled run, dry-run, validate-config | Complete |
| Concurrent-run protection | Complete |

See `CHANGELOG.md` for the detailed history of what shipped in each release.

## Known limitations

- No stale-lock recovery: if the process is killed (SIGKILL) while holding
  the run lock, the lock file must be removed manually before the next run.
- Email delivery is SMTP-only; no alternate provider configuration.
- Scheduling runs in-process (`schedule` library) or via an external
  scheduler (e.g. Windows Task Scheduler calling `--run-now`); there is no
  built-in distributed or cloud scheduler.

## What's next

Future development directions are not yet scoped. This roadmap will be
updated with a new phase definition when work resumes.
