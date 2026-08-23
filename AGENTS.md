# AGENTS.md

## Project purpose

This project automates data reading, PDF report generation, and email delivery.
It is a local Python pipeline, not a distributed or cloud service.

## Working goal

- Understand the real workflow before changing files.
- Make small, safe, well-justified changes.
- Prioritize clarity, maintainability, and validation over new features.
- Keep the project scope appropriate for a portfolio project: small, understandable,
  and demonstrably correct.

## Architecture (module boundaries)

```
main.py
 |-- data_processor.py   -> data loading, summary generation, chart generation
 |-- pdf_generator.py    -> PDF construction
 |-- email_sender.py     -> email validation and delivery attempt
 `-- config.py           -> centralized environment configuration
```

Rules:
- Regla 1 (Separation): never mix the data/processing layer with orchestration
  or delivery logic. Each module keeps its single responsibility above.
- Regla 2 (Error handling): never use print in application code. Use the
  structured logger configured in main.py.
- Regla 3 (Configuration): all environment variables are loaded through
  config.py. Do not read os.environ directly from other modules.
- Regla 4 (Numeric tolerance): datasets without numeric columns must still
  produce a valid summary and PDF. Chart generation is optional and may
  return None without breaking the pipeline.
- Regla 5 (Delivery independence): PDF generation must not depend on email
  delivery succeeding. A generated PDF with a failed email is a partial
  success, not a pipeline failure.
- Regla 6 (No premature cloud): do not introduce AWS, Celery, Redis, S3,
  SES, Supabase, or any distributed infrastructure. This is explicitly
  deferred; see ROADMAP.md "Future" section.

## Required workflow

1. Read SESSION_STATE.md, ROADMAP.md, README.md, and this file before
   changing anything.
2. Explain the real program flow based on the code, not assumptions.
3. Propose a short plan before editing.
4. Delegate according to the agent workflow below.
5. Make the smallest change necessary.
6. Summarize exactly what changed and how it was verified.
7. Update SESSION_STATE.md after every accepted commit.

## Agent workflow

| Step | Agent | Model | Purpose |
|---|---|---|---|
| 1 | quick-explorer | haiku | Read-only discovery before planning |
| 2 | writer | sonnet | Implements the approved plan |
| 3 | quick-reviewer | haiku | Fast sanity check after implementation |
| 4 | architecture-reviewer | opus | Structural review (only when module boundaries, config flow, or dependencies change) |
| 5 | code-reviewer | sonnet | Final pre-commit gate |

Do not skip quick-reviewer. Only invoke architecture-reviewer when the change
affects boundaries listed above. code-reviewer is required before every commit.

## Validation order

1. `python -m py_compile <changed files>`
2. Focused `pytest` for the affected module
3. Full `pytest` before commit
4. `ruff check .`
5. quick-reviewer
6. architecture-reviewer (only for boundary changes)
7. code-reviewer

## Evidence before hypothesis

State which command will verify a hypothesis before proposing a fix. Do not
propose the same unverified hypothesis twice without new evidence.

## Change rules

- Do not modify unrelated files.
- Do not refactor unnecessarily if it does not help the current goal.
- Do not assume behavior that is not confirmed in the code or by a test run.
- If context is missing, ask before continuing.
- If a change affects multiple files, explain why.
- Never edit AGENTS.md or CLAUDE.md without explicit user approval in the
  current session.

## Protected information

Never read, in any circumstance:
- .env, .env.*
- secrets/**
- credentials, private keys
- ~/.aws/**, ~/.ssh/**

If a task appears to require reading one of these, stop and ask the user first.

## Commands and Git

Commands permitted without asking (reference for permission rules):
- `pytest`, `python -m py_compile`, `ruff check`, `git status`, `git diff`, `git log`

Commands that always require manual approval:
- `git commit`, `git push`

Commands that are always denied:
- `git push --force`, `git push -f`, recursive destructive delete, destructive SQL
  (`DROP TABLE`, `TRUNCATE TABLE`)

Each commit must be atomic: one logical change per commit, with a clear message
describing what changed and how it was verified.

## Validation

- Describe how to test the change manually.
- Name the exact pytest/ruff commands to run.
- Report residual risks, or explicitly say "none".

## Required completion format

- [Files Changed]
- [Logic Altered]
- [Verification Method]
- [Residual Risks]
