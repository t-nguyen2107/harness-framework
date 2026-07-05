# Workflow — Bugfix

Reproduce → isolate → fix → verify → close.

## Trigger
A reported bug or a failing test.

## Steps

| # | Role | Action | Gate |
|---|------|--------|------|
| 1 | QA/QC | Reproduce with minimal steps; write a failing test. | Bug reproduces reliably. |
| 2 | Manager | Triage; assign a fix owner (usually Senior Dev or Senior Database). | Owner chosen. |
| 3 | Senior Dev / DB | Isolate root cause; apply minimal fix. | Failing test now passes; no regression. |
| 4 | QA/QC | Re-run full suite; confirm fix. | Green, evidence captured. |
| 5 | Manager | Record a learning in `memory/learnings/`. | Closed. |

## Rules
- Never fix symptoms without a root-cause note.
- Never weaken a test to make it pass.
- One bug, one commit when practical.
