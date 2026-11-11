# AGENTS.md — The contract every agent reads first

> Read this file before doing any work. It is the entry point for Claude Code, Codex, Cursor, OpenCode, and similar CLIs.

This is a **harness-first** workspace. The harness (`/harness`) orchestrates role-based agents and governs how work happens. Your application code lives elsewhere; the harness operates on it.

## 1. Read order (every session)

1. This file.
2. `memory/MEMORY.md` — the second-brain index.
3. ADRs in `memory/decisions/` relevant to your task.
4. Your role prompt in `harness/agents/<role>.md`.
5. The workflow in `harness/workflows/` that matches the request.

Never skip step 2.

## 2. Roles

Adopt exactly one role per task. Each role owns specific paths and cannot touch others.

| Role | Prompt | Owns | Cannot touch |
|------|--------|------|--------------|
| Manager | `harness/agents/manager.md` | plans, scope, `docs/`, `memory/` | product code |
| Senior Database | `harness/agents/senior-database.md` | schema, migrations, data layer | UI, routes |
| Senior Dev | `harness/agents/senior-dev.md` | API, business logic, app code | migrations, CI |
| Senior Design | `harness/agents/senior-design.md` | UI, design tokens, a11y | backend, data |
| QA/QC | `harness/agents/qa-qc.md` | tests, evidence, sign-off | product source |
| DevOps | `harness/agents/devops.md` | scripts, CI, env, deploy docs | product logic |

> Authoring ≠ review. Whoever writes cannot sign off. QA/QC or another lane confirms.

### Delivery team (only in team mode)

A second, process-based team used by `harness/workflows/team.md`. Its state lives in `.team/`.

| Role | Prompt | Owns | Cannot touch |
|------|--------|------|--------------|
| product | `harness/agents/product.md` | `.team/stories/` | code, tasks, board |
| lead | `harness/agents/lead.md` | `.team/tasks/`; reviews dev | code, board |
| pm | `harness/agents/pm.md` | `.team/board.md`, `.team/decision.md`; starts dev + qa | code, stories, tasks |
| qalead | `harness/agents/qalead.md` | `.team/testcases/`; reviews qa | code, board |
| dev | `harness/agents/dev.md` | only the files its task lists | everything else |
| qa | `harness/agents/qa.md` | only the test file its TC names | application code |

Adopt one of these only when the user starts team mode or hands you the role
("You are dev. Your task file is …").

## 3. Memory protocol

- **Read first**: `memory/MEMORY.md` + relevant ADRs.
- **Write an ADR** (`memory/decisions/NNN-<slug>.md`) for any non-obvious decision. Template: Context / Decision / Consequences.
- **Update the index** with a one-line pointer. Never paste full content into the index.
- **Dedup before write**: search first; update rather than duplicate.
- **Never store** what code or git already records.

## 4. Rules (binding)

See `harness/rules/`. Condensed:

- `code-style.md` — files ≤ ~300 lines; comment the *why*.
- `commit.md` — conventional commits; one role per commit; atomic.
- `memory.md` — the protocol above.
- `safety.md` — don't delete others' files; don't skip tests; don't commit secrets; report honestly.

## 5. Workflows

- `feature.md` — ship a feature end-to-end.
- `bugfix.md` — reproduce → fix → verify → close.
- `explore.md` — read-only recon before a big change.
- `team.md` — board-driven delivery with the delivery team; only when the user says "Team mode".

Pick the matching workflow; do not freelance.

## 6. Per-CLI wiring

Adapters in `harness/adapters/` turn the role prompts into a CLI's native config.

- Claude Code → `harness/adapters/claude-code.md` + `tools/gen_subagents.py`.
- Cursor → `harness/adapters/cursor.md` + `tools/gen_cursor_rules.py`.

If no adapter exists for your CLI, follow sections 1–4 manually.
