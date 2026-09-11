# Changelog

## [2.0.0] - 2026-09-11

### Added
- Automated test suite (pytest) covering data loading, summary generation,
  chart generation, PDF generation, email delivery (mocked SMTP), and
  CLI/pipeline integration — 49 tests total.
- Ruff linting configured via `pyproject.toml`; codebase passes with no findings.
- Configuration validation: `validate_config()` checks `SCHEDULE_TIME` format
  at startup; a dedicated `--validate-config` CLI command performs a full
  configuration check without running the pipeline.
- `--dry-run` flag to build the report without sending email; `--no-email`
  as an alias.
- Structured `RunResult` dataclass replacing the previous boolean return
  value from `run_report()`, with distinct CLI exit codes for full success,
  partial success (PDF generated, email failed), and full failure.
- File-locking guard (`lock.py`) preventing two overlapping report runs
  (e.g. a manual run colliding with a scheduled run) from executing
  concurrently.
- Atomic, collision-safe output writes: chart and PDF files are written to
  a unique temporary path per run and finalized with `os.replace()`.
- Documentation for using Windows Task Scheduler as an alternative to the
  in-process scheduler loop.

### Changed
- `run_report()` no longer treats a failed email delivery as an overall run
  failure; a successfully generated PDF is reported as success even if
  email delivery fails (email errors are still logged).
- `EMAIL_RECIPIENTS` parsing now filters empty/whitespace entries.
- `build_pdf()` accepts an explicit `output_path` parameter instead of
  relying solely on a fixed constant.

### Fixed
- Removed corrupted byte sequences from scheduler log messages.
- Corrected a bug where the PDF output directory was hardcoded instead of
  derived from the actual output path.
- Corrected the sample data file path to match the documented default
  (`sample_data/sales_data.csv`).

## [1.0.0] - Initial release
- Initial CSV/XLSX -> summary -> chart -> PDF -> email pipeline.
