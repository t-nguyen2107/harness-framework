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

### Delivery team (`harness/workflows/team.md`)
| Role | model | tools | why |
|------|-------|-------|-----|
| product | sonnet | Read, Write, Edit, Glob, Grep | writes stories; no shell |
| lead | sonnet | + Bash | splits tasks, runs tests to review |
| pm | sonnet | Read, Write, Edit, Glob, Grep, Agent | the only role that starts agents |
| qalead | sonnet | + Bash | writes TCs, runs tests to review |
| dev | haiku | + Bash | one small, fully specified task; `autoCompactWindow: 100000` |
| qa | haiku | + Bash | one test case; `autoCompactWindow: 100000` |

pm overrides the model to `sonnet` for `complexity: complex` tasks and rework attempts
(`.team/config.md` → Policies).

The workflow itself is generated to `.claude/rules/team-coordinator.md` with
`paths: [".team/**"]`, so it loads only when a session touches team files — ordinary sessions
never see it.

Caveats: `autoCompactWindow` is a settings key and is not confirmed to apply from agent
frontmatter; and some Claude Code versions do not let a sub-agent start sub-agents — the
workflow has a fallback where pm returns a `DISPATCH` list and the main session starts the devs.

## Tool allowance
Restrict the `tools` field per role to enforce lane discipline at the API level. Path-scoped write limits are reinforced by the role prompt and the safety rule (and by a hook — see below).

## Hooks (hard enforcement)
Add a `PreToolUse` hook in `.claude/settings.json` to block forbidden writes. The framework ships a starter hook at `tools/hooks/check_write.py` that blocks `.env` and database files.

The same hook enforces the delivery team's write scope (`tools/hooks/team_scope.py`): Claude
Code passes `agent_id` / `agent_type` to the hook for sub-agent calls, so a `dev` can only
write files listed in an in-progress task, a `qa` only its test file, and the planning roles
only their `.team/` files. It covers Write / Edit, not shell commands. Disable with
`HARNESS_TEAM_SCOPE=off`.

> Always reference the hook script with `${CLAUDE_PROJECT_DIR}/...` so the path resolves regardless of the agent's current directory.

## Generation
```bash
python tools/gen_subagents.py    # reads harness/agents/*.md + workflows/team.md, writes .claude/agents/*.md + .claude/rules/team-coordinator.md
```
Re-run after editing a role prompt. Idempotent.
