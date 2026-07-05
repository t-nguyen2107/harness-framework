# harness/rules/

Binding conventions + guardrails applied to every agent and every role.

Unlike `agents/*.md` (which describe roles), `rules/` defines **shared laws**.

| File | Content |
|------|---------|
| `code-style.md` | Formatting, naming, file-size cap |
| `commit.md` | Conventional commits, atomic per role |
| `memory.md` | Memory read/write protocol |
| `safety.md` | Hard blockers: deletions, secrets, honesty |
