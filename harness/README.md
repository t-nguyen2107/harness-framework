# harness/

The orchestration layer — separate from your application runtime.

> Application code never imports from this folder. The harness governs *how agents work*, not what the app does.

## Layout

| Folder | Purpose |
|--------|---------|
| `agents/` | System prompts for the 6 roles |
| `workflows/` | Multi-role orchestration flows |
| `rules/` | Binding conventions + guardrails |
| `adapters/` | Per-CLI wiring (Claude Code, Cursor, ...) |

## Principles

1. **Agent-agnostic** — no hard dependency on one CLI. Each CLI gets an adapter.
2. **Role-based** — one agent may play several roles; one role may run on several CLIs.
3. **Tool-scoped** — each role limits its tools and owned paths explicitly.
