# Workflow — Feature

Ship a feature end-to-end, from request to deploy-ready.

## Trigger
A request for a new capability that touches product code.

## Memory touch (start)
- Manager reads `memory/MEMORY.md` + ADRs in the feature's area.
- If none exist, decide whether a new ADR is warranted.

## Steps

| # | Role | Action | Gate to next |
|---|------|--------|--------------|
| 1 | Manager | Decompose into tasks with acceptance criteria; assign roles. | Task list exists, each with owner + criteria. |
| 2 | Senior Database | Schema/migration if new data is needed. | Migration runs on a fresh database. |
| 3 | Senior Design | UI spec + tokens (parallel with Dev if independent). | Spec is concrete enough to implement. |
| 4 | Senior Dev | Implement logic/UI per spec; add tests. | Code works locally; new tests pass. |
| 5 | QA/QC | Turn criteria into a test matrix; run tests; capture evidence. | All criteria pass, or blockers are filed. |
| 6 | DevOps | Scripts/CI/env if the feature needs them. | Dev script still boots; CI green. |
| 7 | Manager | Synthesize; write ADR if non-obvious; update `MEMORY.md`. | Sign-off recorded. |

## Rules during the run
- Authoring ≠ review: the Dev at step 4 cannot sign off step 5.
- Stay in lane: each role only touches owned paths.
- Honest reporting: each step states what it did and whether tests pass.

## Memory touch (end)
- Manager appends a line to `MEMORY.md` if a new ADR was written.
- QA/QC records any gotcha under `memory/learnings/`.

## Done when
- Acceptance criteria met with evidence, or blockers documented.
