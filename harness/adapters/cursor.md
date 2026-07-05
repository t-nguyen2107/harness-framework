# Adapter — Cursor

How to wire the harness into Cursor.

## Mechanism
- Cursor loads rules from `.cursor/rules/*.mdc`.
- Each rule has frontmatter: `description`, `globs` (path patterns), `alwaysApply` (boolean).
- A rule with `alwaysApply: true` is loaded into every session; others activate when their `globs` match the file being edited.

## Role → rule mapping
- One `alwaysApply: true` root rule that summarizes `AGENTS.md`.
- One rule per role, with `globs` matching the role's owned paths.

Suggested globs (adapt to your layout):

| Role | globs |
|------|-------|
| manager | `docs/**, memory/**` |
| senior-database | `**/migrations/**, **/db.py, **/models.py` |
| senior-dev | `**/routes/**, **/services/**, <frontend>/**` |
| senior-design | `<frontend>/**` |
| qa-qc | `**/tests/**, **/*.test.*` |
| devops | `scripts/**, .github/**, Dockerfile, .env.example` |

## Tool allowance
Cursor does not restrict tools per rule; lane discipline is advisory (prompt + safety rule), same as Claude Code today.

## Generation
```bash
python tools/gen_cursor_rules.py    # reads harness/agents/*.md, writes .cursor/rules/*.mdc
```
Idempotent. Re-run after editing a role prompt or when you change the path globs.
