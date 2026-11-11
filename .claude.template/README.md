# .claude.template/

Copy this folder to `.claude/` to wire the harness into Claude Code.

```bash
cp -r .claude.template .claude
python tools/gen_subagents.py    # generates .claude/agents/*.md from harness/agents/*.md
```

What it contains:
- `settings.json` — a `PreToolUse` hook that calls `tools/hooks/check_write.py` to block writes to `.env` and database files.

What the generator adds:
- `.claude/agents/*.md` — one subagent per role: the six lane roles (manager, senior-database, senior-dev, senior-design, qa-qc, devops) and the six delivery-team roles (product, lead, pm, qalead, dev, qa).
- `.claude/rules/team-coordinator.md` — the team workflow, loaded only when a session touches `.team/`.

Re-run `gen_subagents.py` whenever you edit a role prompt in `harness/agents/` or `harness/workflows/team.md`.
