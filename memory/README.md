# memory/ — Second Brain

Long-term project memory. Version-controlled. Read and edited by both humans and agents.

## Layout

| Path | Purpose |
|------|---------|
| `MEMORY.md` | Index — one-line pointer per entry. Loaded every session. |
| `decisions/` | ADRs — one file per non-obvious decision |
| `conventions/` | Project-specific conventions |
| `learnings/` | Lessons, gotchas, feedback |

## Rules (see `harness/rules/memory.md`)
1. Read `MEMORY.md` first every session.
2. The index holds pointers only — never full content.
3. Dedup before write; update rather than duplicate.
4. Never store what code or git already records.
