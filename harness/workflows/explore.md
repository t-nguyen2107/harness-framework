# Workflow — Explore

Read-only reconnaissance before a large change.

## Trigger
A big or risky change is proposed and the codebase is not yet understood.

## Steps

| # | Role | Action | Gate |
|---|------|--------|------|
| 1 | Manager | Frame the question and the decision the exploration supports. | Question is specific. |
| 2 | Senior Dev / DB / Design | Read-only mapping: relevant files, data flow, touch points, risks. | Map written to a short note. |
| 3 | Manager | Decide: proceed, split the work, or write an ADR. | Decision recorded. |

## Rules
- Read-only. No edits to product code.
- Output is a note, not a refactor.
- Time-boxed; stop when the question is answered.
