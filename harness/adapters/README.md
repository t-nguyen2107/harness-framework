# harness/adapters/

Adapters translate the harness's roles + workflows into each agent CLI's native config.

> This is what makes the framework CLI-portable: the same `harness/agents/*.md` source drives Claude Code, Cursor, and beyond — without changing the prompts.

## Principles

- One file = one CLI.
- Each adapter documents: role → config mapping, tool scope, memory read/write, the init command.
- Adapters describe and generate config; they do not run inside the app.

## Files

| File | CLI | Generator |
|------|-----|-----------|
| `claude-code.md` | Claude Code | `tools/gen_subagents.py` → `.claude/agents/*.md` + `.claude/rules/team-coordinator.md` |
| `cursor.md` | Cursor | `tools/gen_cursor_rules.py` → `.cursor/rules/*.mdc` |
