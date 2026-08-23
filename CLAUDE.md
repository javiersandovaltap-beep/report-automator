# CLAUDE.md

## Project

Report Automator is a local Python pipeline that automates data reading, PDF report
generation, and email delivery. It loads CSV or XLSX data, generates summary metrics,
optionally builds a chart, constructs a PDF report, and attempts email delivery. It
supports immediate execution and daily, weekly, or monthly scheduling.

## Session start

Read, in this order, at the start of every new session:
1. SESSION_STATE.md (current state, confirmed facts, open risks)
2. ROADMAP.md (scope, phases, priorities)
3. AGENTS.md (architecture and workflow rules)
4. This file (CLAUDE.md)

SESSION_STATE.md is the single source of truth for what has actually been done and
verified. ROADMAP.md defines what is in scope and what is deferred.

## Project priorities (in order)

1. Portfolio quality.
2. Reliable local production use.
3. Practicing and applying the Claude Code workflow correctly.
4. Cloud preparation is explicitly deferred. Do not implement or design cloud
   infrastructure (AWS, workers, queues, external storage) in the current phases.

## Approved scope

Only Phases 1-4 in ROADMAP.md are currently approved for implementation:
1. Governance, state, and diagnosis.
2. Automated quality.
3. Domain robustness.
4. CLI and local production readiness.

Distribution and cloud preparation are backlog only ("Future" section of ROADMAP.md).

## Agent workflow

Report Automator uses five project-scoped agents under .claude/agents/, in addition
to the legacy reviewer_agent.md and the architecture_reviewer skill under .claude/skills/.

| Agent | Model | Role |
|---|---|---|
| quick-explorer | haiku | Read-only discovery before planning |
| writer | sonnet | Implements an approved, scoped plan |
| quick-reviewer | haiku | Fast read-only sanity check after implementation |
| architecture-reviewer | opus | Read-only structural review for boundary changes |
| code-reviewer | sonnet | Final read-only pre-commit gate |

Typical flow for a small change:

```
quick-explorer -> writer -> quick-reviewer -> tests -> code-reviewer -> commit
```

Typical flow for a change that affects module boundaries or configuration flow:

```
quick-explorer -> writer -> quick-reviewer -> architecture-reviewer -> code-reviewer -> commit
```

## Absolute rules

1. Read AGENTS.md before proposing any plan. It is the law of the project.
2. Do not refactor code unrelated to the current task.
3. Follow the flow: Plan -> Execute -> Verify (tests) -> Review -> Commit.
4. Never read .env, .env.*, secrets/, credentials, private keys, ~/.aws/, or ~/.ssh/,
   even if a tool would technically allow it. Stop and ask first.
5. Never edit AGENTS.md or CLAUDE.md without explicit user approval in the current
   session. Both files are protected by .claude/settings.json and hooks.
6. Never commit or push without explicit approval. git push --force is always denied.
7. Update SESSION_STATE.md after every accepted commit.
8. Do not claim a feature works until it has been validated with an actual command
   (py_compile, pytest, or a real execution), not just by reading the code.
9. Keep operational project files (this file, AGENTS.md, SESSION_STATE.md,
   ROADMAP.md, agent files, skills) in English. The user may communicate in Spanish.
10. Prefer ASCII-safe content in tracked Markdown files to avoid encoding corruption
    from automated edits.

## Environment

- OS: Windows 10/11
- Interactive shell: PowerShell
- Claude Code version: 2.1.240 (confirmed)
- Entry point: main.py
- Immediate run: `python main.py --run-now`
- Default run (no args): `python main.py`
- Scheduled run: `python main.py --schedule daily|weekly|monthly`

## Enforcement layer (already active)

- .claude/settings.json defines allow/ask/deny permission rules.
- .claude/hooks/block-dangerous-commands.ps1 blocks destructive commands
  (recursive delete, force push, destructive SQL) before execution.
- .claude/hooks/protect-project-files.ps1 blocks Edit/Write attempts against
  AGENTS.md and CLAUDE.md before execution.
- .claude/hooks/validate-after-edit.ps1 runs py_compile on any Python file
  after it is edited or written.

Do not weaken, bypass, or remove this enforcement layer without explicit approval.

## Completion format

When reporting completed work, use:

[Files Changed]
[Logic Altered]
[Tests Run]
[Verification Method]
[Residual Risks]
