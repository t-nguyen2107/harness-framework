# Adapter — Claude Code

How to wire the harness into Claude Code.

## Mechanism
- Claude Code auto-reads `AGENTS.md` at the repo root.
- It loads subagent definitions from `.claude/agents/*.md`.
- We use both: `AGENTS.md` is the global contract; each role becomes a subagent.

## Role → subagent mapping
Each `harness/agents/<role>.md` maps to `.claude/agents/<role>.md` with frontmatter:

```yaml
---
name: <role-slug>                 # e.g. senior-dev
description: <one-line role summary>
model: <opus | sonnet | haiku>    # see routing below
tools: <comma-separated allowlist>
---
```

The body is the role prompt (English section).

## Model routing (default)
| Role | model | why |
|------|-------|-----|
| manager | opus | planning, judgment |
| senior-database | sonnet | precise schema reasoning |
| senior-dev | sonnet | standard implementation |
| senior-design | sonnet | UI / a11y |
| qa-qc | sonnet | test design + verification |
| devops | sonnet | scripts + CI |

Use `opus` for the hardest planning/review step; `haiku` only for trivial lookups.

## Tool allowance
Restrict the `tools` field per role to enforce lane discipline at the API level. Path-scoped write limits are reinforced by the role prompt and the safety rule (and by a hook — see below).

## Hooks (hard enforcement)
Add a `PreToolUse` hook in `.claude/settings.json` to block forbidden writes. The framework ships a starter hook at `tools/hooks/check_write.py` that blocks `.env` and database files.

> Always reference the hook script with `${CLAUDE_PROJECT_DIR}/...` so the path resolves regardless of the agent's current directory.

## Generation
```bash
python tools/gen_subagents.py    # reads harness/agents/*.md, writes .claude/agents/*.md
```
Re-run after editing a role prompt. Idempotent.
