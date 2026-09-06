# ROADMAP.md

## Objective

Turn Report Automator into a reliable, testable, locally production-ready Python
automation pipeline, while keeping its scope small and understandable for a
portfolio project, and while practicing a disciplined Claude Code workflow.

## Priorities (in order)

1. Portfolio quality: demonstrable correctness, tests, and clear documentation.
2. Local production readiness: reliable execution on Windows without manual
   babysitting.
3. Claude Code workflow practice: enforcement, agents, atomic commits.
4. Cloud preparation is explicitly deferred (see "Future" section below).

## Phase 1 - Governance, state, and diagnosis

Status: complete

- [x] Create `.claude/settings.json` with allow/ask/deny permission rules.
- [x] Create `block-dangerous-commands.ps1` hook (PreToolUse).
- [x] Create `protect-project-files.ps1` hook (PreToolUse, protects
      AGENTS.md and CLAUDE.md).
- [x] Create `validate-after-edit.ps1` hook (PostToolUse, runs py_compile
      on edited Python files).
- [x] Validate all hooks functionally:
      dangerous command denied, safe command allowed, protected files denied,
      and Python syntax validation passed.
- [x] Commit enforcement layer (`5dc67bb`).
- [x] Create `quick-explorer`, `writer`, `quick-reviewer`,
      `architecture-reviewer`, and `code-reviewer` agent definitions.
- [x] Assign explicit models:
      quick-explorer=haiku, writer=sonnet, quick-reviewer=haiku,
      architecture-reviewer=opus, code-reviewer=sonnet.
- [x] Update `CLAUDE.md` with session-start order, project priorities,
      agent workflow, and enforcement rules.
- [x] Update `AGENTS.md` with module boundaries, validation order,
      protected information rules, and agent workflow.
- [x] Create `SESSION_STATE.md` as the single source of truth for project state.
- [x] Create `ROADMAP.md`.
- [x] Run the baseline diagnosis:
      all five application modules pass py_compile;
      the existing pytest suite passes with 6 tests;
      Ruff is not installed and has no project configuration.
- [x] Commit agent definitions (`5fac46d`).
- [x] Commit governance documentation (`75918f1`).

Acceptance criteria:

- Enforcement layer is active and functionally tested.
- All five agents have valid frontmatter with name, description, model, and tools.
- Reviewer agents are read-only.
- `writer` has no commit or push capability.
- `CLAUDE.md` and `AGENTS.md` reflect the project workflow and priorities.
- `SESSION_STATE.md` contains verified facts rather than assumptions.
- No application code was changed during this phase.

## Phase 2 - Automated quality

Status: complete

### Baseline diagnosis

- [x] Compile all application modules with `py_compile`.
- [x] Confirm `main.py` compiles.
- [x] Confirm `config.py` compiles.
- [x] Confirm `data_processor.py` compiles.
- [x] Confirm `pdf_generator.py` compiles.
- [x] Confirm `email_sender.py` compiles.
- [x] Confirm the existing pytest suite runs successfully.
- [x] Confirm the baseline suite result: 6 passed, 0 failed, 0 skipped.
- [x] Map the existing `data_processor.py` test coverage.
- [x] Confirm there is no `tests/` directory.
- [x] Confirm the existing test file is `test_data_processor.py` at repository root.
- [x] Confirm `test_load_data_xlsx` is currently a no-op placeholder.
- [x] Check Ruff availability.
- [x] Install Ruff as a development dependency.
- [x] Add Ruff configuration in `pyproject.toml`.
- [x] Record and review the initial Ruff baseline.
- [x] Resolve the reviewed Ruff findings without broad global ignores.

### Configuration tests

- [x] Add `test_config.py`.
- [x] Test default configuration values.
- [x] Test environment variable overrides.
- [x] Test comma-separated recipient parsing.
- [x] Test empty and single-recipient behavior.
- [x] Run focused configuration tests: 4 passed.
- [x] Run the combined suite after configuration tests: 10 passed,
      0 failed, 0 skipped.
- [x] Confirm no application configuration logic was modified.

### PDF generator tests

- [x] Add `test_pdf_generator.py`.
- [x] Test PDF generation with a numeric summary and chart.
- [x] Test PDF generation with a numeric summary and no chart.
- [x] Test output-directory creation in a temporary directory.
- [x] Test that the generated PDF is non-empty.
- [x] Test the `%PDF` file signature.
- [x] Use temporary paths and avoid the real `output/` directory.
- [x] Confirm no network, SMTP, `.env`, or secret dependency.
- [x] Run focused PDF tests: 3 passed.
- [x] Run the combined suite after PDF tests: 13 passed,
      0 failed, 0 skipped.
- [x] Confirm `pdf_generator.py` was not modified.
- [x] Confirm quick-reviewer returned PASS.
- [x] Confirm code-reviewer returned APPROVE FOR COMMIT.

### Email sender tests

- [x] Add `test_email_sender.py`.
- [x] Test missing sender configuration.
- [x] Test missing password configuration.
- [x] Test empty recipient configuration.
- [x] Test missing PDF file behavior.
- [x] Test successful SMTP interaction with mocked `SMTP_SSL`.
- [x] Test SMTP failure behavior without real network calls.
- [x] Run focused email tests: 6 passed.
- [x] Run the accumulated suite after email tests: 19 passed,
      0 failed, 0 skipped.
- [x] Confirm `email_sender.py` was not modified.
- [x] Confirm no real credentials, `.env`, network, or SMTP server were used.
- [x] Confirm quick-reviewer returned PASS.

### XLSX and edge-case tests (Phase 2.3)

Status: complete

- [x] Replace the no-op `test_load_data_xlsx` placeholder.
- [x] Add a real temporary XLSX loading test.
- [x] Add empty-dataset coverage.
- [x] Add missing-file coverage.
- [x] Add malformed CSV coverage.
- [x] Add malformed XLSX coverage.
- [x] Verify numeric and non-numeric behavior remains stable.
- [x] Run the focused suite: 10 passed.
- [x] Run the accumulated suite: 23 passed.
- [x] Confirm no production logic changed.

### Pipeline integration tests (Phase 2.4)

Status: complete

- [x] Add integration coverage for `main.run_report()`.
- [x] Mock email delivery.
- [x] Verify successful report generation and delivery.
- [x] Verify current email-failure semantics.
- [x] Verify processing-exception semantics.
- [x] Keep network and SMTP calls disabled.
- [x] Run the accumulated suite: 26 passed.
- [x] Confirm no production logic changed.
- [x] Commit Phase 2.4 implementation as `7e2e7cd`.

### Remaining automated quality work

- [x] Review whether the test suite should move into a `tests/` package. DONE 2026-09-06, commit 53533d2 (test-suite-relocation). See SESSION_STATE.md incident log.

Acceptance criteria:

- [x] `pytest` passes with 0 failures across the currently implemented test modules.
- [x] `data_processor.py` has meaningful baseline coverage.
- [x] `config.py` has automated coverage.
- [x] `pdf_generator.py` has automated coverage.
- [x] `email_sender.py` has mocked SMTP coverage.
- [x] The XLSX path has a real test.
- [x] Pipeline integration behavior is covered.
- [x] Cover current email failure semantics at the pipeline level.
- [x] Ruff is installed, configured, and passes.
- [ ] The test suite has been evaluated for migration into a `tests/` package.

## Phase 2 evidence log

### Baseline diagnosis

- Date: 2026-08-23
- Result: 5 application modules compiled successfully.
- Result: existing test suite passed with 6 tests.
- Result: Ruff was unavailable and unconfigured.
- Source of evidence: delegated `quick-explorer` report.

### Configuration tests (2.2a)

- Date: 2026-08-23
- File added: `test_config.py`.
- Focused result: 4 passed.
- Combined result: 10 passed.
- Application logic changed: none.
- Review result: `quick-reviewer` PASS.
- Source of evidence: writer and quick-reviewer reports.

### PDF generator tests (2.2b)

- Date: 2026-08-23
- File added: `test_pdf_generator.py`.
- Focused result: 3 passed.
- Combined result: 13 passed.
- Application logic changed: none.
- Review result: `quick-reviewer` PASS.
- Final review result: `code-reviewer` APPROVE FOR COMMIT.
- Source of evidence: writer, quick-reviewer, and code-reviewer reports.

### Email sender tests (2.2c)

- Date: 2026-08-23
- File added: `test_email_sender.py`.
- Focused result: 6 passed.
- Combined result: 19 passed.
- Application logic changed: none.
- SMTP behavior tested with mocks; no real network or credentials used.
- Review result: quick-reviewer PASS.
- Source of evidence: writer and quick-reviewer reports.

### Phase 2.3 evidence

- Date: 2026-08-23
- File changed: `test_data_processor.py`.
- Tests added or replaced:
  - real XLSX loading;
  - empty dataset;
  - missing file;
  - malformed CSV;
  - malformed XLSX.
- Focused result: 10 passed.
- Accumulated result: 23 passed.
- Production logic changed: none.
- Input exception behavior verified in the current pandas/openpyxl environment.

### Phase 2.4 evidence

- Date: 2026-08-23
- File added: `test_main.py`.
- Tests added:
  - successful pipeline;
  - email delivery failure;
  - processing exception.
- Focused result: 3 passed.
- Accumulated result: 26 passed.
- Production logic changed: none.
- External services: SMTP and network disabled through mocks.
- Commit: `7e2e7cd`.

### Phase 2.5 evidence

- Date: 2026-08-24
- Tool: Ruff 0.16.4 installed in the project virtual environment.
- Configuration: `pyproject.toml`.
- Implementation commit: `e209fa8`.
- Initial baseline: 69 findings.
- Final result: `ruff check . --output-format=concise` passed with no findings.
- Rules addressed: I001, F401, RUF013, RUF059, LOG015, S110, DTZ005, BLE001,
  G201, and RUF100.
- Tests after cleanup: 26 passed.
- Compilation after cleanup: passed for all five application modules.
- Functional behavior: preserved according to the existing test suite.
- Observable output: error-path `print()` calls were migrated to logging.
- Top-level `except Exception` remains intentional in `main.py` and logs with
  `logger.exception`.
- Source of evidence: terminal verification performed on 2026-08-24.

### Current cumulative test count

- `data_processor.py`: 10 tests.
- `config.py`: 4 tests.
- `pdf_generator.py`: 3 tests.
- `email_sender.py`: 6 tests.
- `main.py`: 3 tests.
- Total currently passing: 26 tests.

### Phase 2.2 completion

Status: complete

Phase 2.2 included:
- 2.2a: `config.py` tests.
- 2.2b: `pdf_generator.py` tests.
- 2.2c: `email_sender.py` tests.

The accumulated suite passes with 19 tests. No application logic was changed.
The single accumulated Phase 2.2 test commit has been created.

### Phase 2.3 completion

Status: complete

Phase 2.3 included:
- Replaced the no-op XLSX test.
- Added empty-dataset coverage.
- Added missing-file coverage.
- Added malformed CSV coverage.
- Added malformed XLSX coverage.

The focused `data_processor.py` suite passed with 10 tests. No application logic
was changed. The Phase 2.3 implementation was committed as `38e1193`.

### Phase 2.4 completion

Status: complete

Phase 2.4 included:
- Added `test_main.py`.
- Covered successful pipeline execution.
- Covered current email-failure semantics.
- Covered processing-exception semantics.

The accumulated suite passed with 26 tests. No application logic was changed.
The Phase 2.4 implementation was committed as `7e2e7cd`.

### Phase 2.5 completion

Status: complete

Phase 2.5 included:

- Added Ruff 0.16.4 as a development dependency in `requirements.txt`.
- Added project Ruff configuration in `pyproject.toml`.
- Resolved import-order and unused-import findings.
- Corrected Optional annotations and the unused chart variable.
- Migrated root logger calls in `main.py` to a module-specific logger.
- Replaced silent chart-insertion failure with warning logging.
- Replaced application error-path `print()` calls with logging.
- Resolved timezone findings with local timezone-aware datetime values.
- Preserved the intentional top-level exception boundary in `main.py`.
- Resolved the final `BLE001`, `G201`, and `RUF100` findings.

Verification:

- All five application modules passed `py_compile`.
- The accumulated suite passed with 26 tests, 0 failures, and 0 skips.
- `ruff check . --output-format=concise` passed with no findings.
- No broad global Ruff ignore was added.
- Functional return values and tested control flow were preserved.
- Error-path output changed from stdout printing to logging.

Implementation commit: `e209fa8`.

No application feature scope was added in Phase 2.5.

## Phase 3 - Domain robustness

Status: complete (R2, R3, structured run result + exit codes, and
safe-generated-file-paths all done)

- [x] Add explicit configuration validation in config.py (required vs optional
      values, valid SCHEDULE_TIME format, valid recipient list).
- [x] Decouple "PDF generated successfully" from "email delivered successfully"
      in the run result (see AGENTS.md Regla 5).
- [x] Replace any remaining print statements with structured logging.
      (Verified already resolved by Phase 2.5 / R12; no print() remained in
      any of the five application modules as of 2026-09-03.)
- [x] Define a structured run result (files produced, email status, timing).
- [x] Improve CLI exit codes to distinguish partial success from full failure.
- [x] Handle temporary/generated files (chart.png, report.pdf) safely, avoiding
      collisions between runs.

Acceptance criteria:
- A failed email delivery does not cause a valid PDF run to be reported as failed.
- Configuration errors are caught early with a clear message.
- No print statements remain in application code.

### Phase 3 R2 evidence -- Configuration validation

- Date: 2026-08-25
- Files changed: config.py, main.py, test_config.py.
- config.py: EMAIL_RECIPIENTS filters empty/whitespace entries at load time
  ([] instead of ['']). New validate_config() validates SCHEDULE_TIME
  format only (24-hour HH:MM); email credential validation intentionally
  untouched in email_sender.py (Regla 5).
- main.py: validate_config() called once at startup; exits non-zero with a
  logged message on ValueError. run_report() unchanged in this commit.
- test_config.py: extended to 8 tests (4 new for validate_config, 2
  existing assertions updated).
- Focused result: 8 passed (test_config.py).
- Full suite result: 30 passed, 0 failed, 0 skipped.
- Ruff: clean.
- Review chain: writer -> quick-reviewer (PASS) -> architecture-reviewer
  (blocked by provider rate limiting; equivalent manual review performed,
  verdict APPROVE) -> code-reviewer (APPROVE FOR COMMIT).
- Commit: `660e7c7`.

### Phase 3 R3 evidence -- Email failure semantics

- Date: 2026-09-03
- Files changed: main.py, test_main.py.
- main.py: `run_report()` now returns `True` whenever the PDF was built
  successfully, regardless of email delivery result. Email failure still
  logged at ERROR level.
- test_main.py: renamed and updated `test_run_report_email_failure` to
  `test_run_report_email_failure_reports_success`; added caplog assertion.
- Focused result: 3 passed (test_main.py).
- Full suite result: 30 passed, 0 failed, 0 skipped.
- Ruff: clean.
- Process note: this task's orchestrating session made several
  unauthorized file modifications outside main.py/test_main.py; all were
  discarded before commit (see SESSION_STATE.md 2026-09-03 session log).
- Minor debt: docstring dropped and a duplicated comment line left in the
  committed test body (cosmetic only, not corrected in this commit).
- Commit: `a1894e7`.

### Phase 3 - Structured run result and CLI exit codes evidence

- Date: 2026-09-05
- Files changed: result.py (new), main.py, test_main.py.
- result.py: new RunResult dataclass (pdf_generated, pdf_path, chart_path,
  email_sent, error) and log_run_outcome() helper centralizing outcome
  logging across all 5 call sites in main.py.
- main.py: run_report() returns RunResult instead of bool, preserving
  existing try/except structure and R3's email-failure semantics unchanged.
  --run-now and default branches now sys.exit() with 0 (full success) / 2
  (partial success, PDF ok email failed) / 1 (full failure, no PDF). The
  three schedule.every()...do(...) branches wrapped to call log_run_outcome()
  without ever calling sys.exit(), since they run inside the long-lived
  scheduler loop.
- test_main.py: rewrote the 3 run_report() tests to assert RunResult fields;
  renamed test_run_report_email_failure_reports_success to
  test_run_report_email_failure_partial_success.
- Verification: py_compile clean; full suite 30/30; ruff check clean.
- Review chain: writer -> quick-reviewer (session 1, clean) ->
  architecture-reviewer (session 2, APPROVE, but see process note below) ->
  code-reviewer (session 3, APPROVE FOR COMMIT).
- Process note: in both the architecture-reviewer and code-reviewer sessions,
  the orchestrating CLI session did not wait passively for the backgrounded
  subagent - it narrated its own guessed/duplicated text before or alongside
  the real agent output, making the pasted terminal transcript unreliable as
  a clean verbatim report on both occasions. File scope stayed correct in
  both sessions (confirmed via git status before and after). The
  architecture review was treated as a documented manual deviation: the user
  and the planning assistant independently reviewed the same diff outside
  Claude Code and found no blocking issues. This is a new failure pattern,
  distinct from the R3 file-scope-creep incident, worth watching in future
  sessions with these NIM-routed aliases.
- Commit: `51d48f7`.

### Phase 3 - Safe generated file paths evidence

- Date: 2026-09-06
- Files changed: data_processor.py, pdf_generator.py, main.py,
  test_data_processor.py, test_pdf_generator.py, test_main.py.
- data_processor.py: generate_chart() writes to a UUID-suffixed temp file
  in the same directory as the final output_path, then finalizes with
  os.replace(). Cleans up the temp file on any exception before returning
  None, preserving existing behavior.
- pdf_generator.py: build_pdf() gained a new output_path parameter
  (defaults to OUTPUT_PDF). Fixed a pre-existing bug where the output
  directory was hardcoded to "output" instead of being derived from the
  actual output path. Writes to a UUID-suffixed temp file, finalizes via
  os.replace(), cleans up and re-raises on exception. Returns the final
  output_path instead of the OUTPUT_PDF constant.
- main.py: run_report() generates one run_id (timestamp + short uuid) per
  execution and passes explicit, unique output_path values to both
  generate_chart() and build_pdf(), preventing filename collisions between
  overlapping process invocations.
- Tests: added temp-file-safety and exception-cleanup coverage in
  test_data_processor.py and test_pdf_generator.py. Updated test_main.py's
  existing call-argument assertions to match the new output_path
  parameter, since the production call signature legitimately changed.
- Verification: py_compile clean; full suite 34/34 passed, 0 failed, 0
  skipped; ruff check clean.
- Review: performed manually (file-by-file diff review against the
  approved design, plus independent terminal re-verification of all
  validation commands) instead of via architecture-reviewer/code-reviewer,
  due to process issues during the writer-agent stage (see SESSION_STATE.md
  2026-09-06 entry for full detail).
- Commit: `157e922`.

Phase 3 is now complete.

## Phase 4 - CLI and local production readiness

Status: pending

- [x] Add `--dry-run` (build the report but skip email delivery). DONE 2026-09-06, commit 6e3710d (dry-run-flag). See SESSION_STATE.md incident log for the code-reviewer orchestration failure on this item.
- [ ] Add `--no-email` as an explicit alternative/alias if useful.
- [ ] Add a `validate-config` command that checks .env without running the pipeline.
- [ ] Document Windows Task Scheduler as an alternative to the in-process
      `schedule` loop for unattended execution.
- [ ] Document normal execution, dry-run execution, and scheduled execution
      in README.md.
- [ ] Verify behavior when two runs could overlap (basic guard or documented
      limitation).

Acceptance criteria:
- The project can be demoed end-to-end without a real SMTP account, using
  `--dry-run`.
- README.md accurately describes only implemented, validated behavior.
- Local scheduling options are documented with real trade-offs.

## Future - Distribution and cloud preparation (deferred, backlog only)

Not part of the current implementation phases. Do not implement without a new
explicit approval and a new phase definition.

- [ ] Decouple report distribution behind an interface (SMTP, file, webhook,
      S3, etc.).
- [ ] Persist execution history (database or structured log store).
- [ ] Evaluate a queue/worker model (Celery, RQ) for concurrent report runs.
- [ ] Evaluate cloud storage for generated artifacts (S3, Supabase Storage).
- [ ] Evaluate a managed scheduler (AWS EventBridge, GitHub Actions) instead
      of the in-process `schedule` loop.
- [ ] Evaluate containerization (Docker) for consistent local/cloud parity.

## Rule

Nothing in this file may be described in README.md as already implemented
until it is merged and validated. This prevents documentation drift between
planned work and actual behavior.
