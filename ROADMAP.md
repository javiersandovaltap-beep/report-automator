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

Status: in progress

- [x] Create .claude/settings.json with allow/ask/deny permission rules.
- [x] Create block-dangerous-commands.ps1 hook (PreToolUse).
- [x] Create protect-project-files.ps1 hook (PreToolUse, protects AGENTS.md/CLAUDE.md).
- [x] Create validate-after-edit.ps1 hook (PostToolUse, py_compile on Python edits).
- [x] Validate all hooks functionally (dangerous command denied, safe command
      allowed, protected files denied, Python syntax check passes).
- [x] Commit enforcement layer (5dc67bb).
- [x] Create quick-explorer, writer, quick-reviewer, architecture-reviewer,
      and code-reviewer agent definitions.
- [x] Update CLAUDE.md with session-start order, agent workflow, and priorities.
- [x] Update AGENTS.md with architecture, agent workflow, and validation order.
- [x] Create SESSION_STATE.md as the single source of truth for project state.
- [x] Create this ROADMAP.md.
- [ ] Run the baseline diagnosis (py_compile all modules, run pytest, run
      ruff check) and record real results in SESSION_STATE.md.
- [ ] Commit governance files (agents, CLAUDE.md, AGENTS.md, SESSION_STATE.md,
      ROADMAP.md) as separate atomic commits.

Acceptance criteria:
- Enforcement layer is active and tested.
- All five agents exist with valid frontmatter (name, description, model, tools).
- Reviewer agents cannot Edit or Write.
- writer cannot commit or push.
- CLAUDE.md and AGENTS.md reflect the actual agent workflow and priorities.
- SESSION_STATE.md contains verified facts, not assumptions.
- No application code was changed during this phase.

## Phase 2 - Automated quality

Status: pending

- [ ] Confirm actual syntax integrity of all Python modules (py_compile).
- [ ] Confirm existing pytest suite scope (know what data_processor tests cover).
- [ ] Add missing tests: config loading, pdf_generator, email_sender (mocked
      SMTP, no real network calls), and a full pipeline integration test.
- [ ] Cover numeric and non-numeric datasets, empty datasets, missing files,
      and invalid Excel/CSV input.
- [ ] Add ruff configuration and run `ruff check .` cleanly.
- [ ] Record final test and lint status in SESSION_STATE.md.

Acceptance criteria:
- `pytest` passes with 0 failures across all modules.
- `ruff check .` passes cleanly.
- Non-numeric dataset behavior is covered by an explicit test.
- Email sending is tested without making real network/SMTP calls.

## Phase 3 - Domain robustness

Status: pending

- [ ] Add explicit configuration validation in config.py (required vs optional
      values, valid SCHEDULE_TIME format, valid recipient list).
- [ ] Decouple "PDF generated successfully" from "email delivered successfully"
      in the run result (see AGENTS.md Regla 5).
- [ ] Replace any remaining print statements with structured logging.
- [ ] Define a structured run result (files produced, email status, timing).
- [ ] Improve CLI exit codes to distinguish partial success from full failure.
- [ ] Handle temporary/generated files (chart.png, report.pdf) safely, avoiding
      collisions between runs.

Acceptance criteria:
- A failed email delivery does not cause a valid PDF run to be reported as failed.
- Configuration errors are caught early with a clear message.
- No print statements remain in application code.

## Phase 4 - CLI and local production readiness

Status: pending

- [ ] Add `--dry-run` (build the report but skip email delivery).
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
