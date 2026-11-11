# Board

Owned by **pm** — nobody else edits this file. One table per story, newest story on top.
The board is the status of record; pm copies each status into the `status:` line of the
task/TC file in the same edit. If the two disagree, pm reconciles before doing anything else
(a `blocked: …` set by the working agent in its own file wins).

Statuses: `todo` · `in-progress` · `review` · `rework` · `done` · `blocked`
(`blocked: question`, `blocked: needs file`, `blocked: rework limit`, …).

Assignee: `<role>` or `<role>:<tool>` when the work was done outside Claude
(e.g. `dev:codex`, `qa:cursor`). Notes: slot number while in progress, then one line of outcome.

<!--
## STORY-1 — <title>  (story status: in-progress)

| Task | Type | Files | Assignee | Status | Rework count | Notes |
|---|---|---|---|---|---|---|
| TASK-1 | backend | api/routes/x.py, tests/test_x.py | dev | todo | 0 | |
| TASK-2 | frontend | web/lib/x.ts, web/lib/x.test.ts | dev | todo | 0 | after TASK-1 |
| TC-1 | qa:api | tests/test_tc1_x.py | qa | todo | 0 | needs TASK-1 |
-->

_No stories yet._
