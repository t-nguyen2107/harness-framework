# Workflow — Team (board-driven delivery)

Ship a story with a six-role delivery team: stories → small tasks → parallel developers →
independent review → QA automation → closure. State lives in `.team/` files, so any CLI can
play any role and a run can be resumed by a different session or a different tool.

## Trigger
The user starts or resumes team mode ("Team mode. …", "run the team on …", "resume the team").
In every other session, ignore this workflow and work normally — do not turn an ordinary
request into a story.

## Who you are
The main session is the **coordinator**. You route work between the six roles and talk to the
user. You do not write stories, tasks, test cases, code or reviews yourself, and you do not
edit `.team/board.md` or `.team/decision.md` — those belong to pm. In team mode use only the
delivery-team roles below.

## Roles

| Role | Owns | Prompt |
|---|---|---|
| product | `.team/stories/STORY-<n>.md`; answers business questions | `harness/agents/product.md` |
| lead | `.team/tasks/TASK-<n>.md`; reviews dev work; answers technical questions | `harness/agents/lead.md` |
| pm | `.team/board.md`, `.team/decision.md`; starts dev and qa | `harness/agents/pm.md` |
| qalead | `.team/testcases/TC-<n>.md`; reviews qa work | `harness/agents/qalead.md` |
| dev | code + unit tests, only in its task's listed files | `harness/agents/dev.md` |
| qa | automation test code for one TC | `harness/agents/qa.md` |

## Rules for everyone

- **Statuses:** `todo`, `in-progress`, `review`, `rework`, `done`, `blocked`.
- **IDs:** each owner numbers its own files: highest existing number + 1.
- **One at a time:** never run two product, lead, qalead, pm or qa agents at once. Only devs
  run in parallel, only pm starts them, and devs never start agents.
- **No memory:** agents remember nothing between runs. Everything they need is in `.team/`
  files, and every report says which files it updated. Give each agent file paths, not a
  retelling.
- **Questions:** an agent writes its question under `## Questions` in its own file, sets the
  status to `blocked: question` and stops. You send business questions to product and technical
  questions to lead; a question neither can answer goes to the user. The answer is written into
  the same file. pm logs significant answers in `.team/decision.md` (date, decision, made by,
  reason, links).
- **Errors are reported, never hidden:** no skipped tests, no placeholder implementations, no
  silent fallbacks. A blocker is written down with evidence and the agent stops.
- **Author ≠ reviewer:** whoever wrote something does not approve it.
- **Git:** no agent pushes, merges, deploys, stashes or switches branch. Commits follow
  `commit_after_approval` in `.team/config.md`.
- `harness/rules/` applies throughout.

## Memory touch (start) — kickoff and every resume

1. Read `memory/MEMORY.md` and `.team/config.md`. If config still has `<FILL IN>` commands,
   detect them from the repo (package scripts, Makefile, CI workflow, compose file), write
   them in, and tell the user what you could not detect. Do not start work with a missing
   unit-test command.
2. Run the preflight in `.team/config.md` §0. If it fails, stop and tell the user.
3. Read `.team/board.md`. If a story is in flight, continue from the board; anything left
   `in-progress` by an interrupted run goes back through pm first.

## Steps

| # | Role | Action | Gate to next |
|---|---|---|---|
| 1 | product | Write `STORY-<n>` with numbered acceptance criteria. | **User approves the criteria.** |
| 2 | lead, then qalead | lead splits the story into `TASK-<n>` files (type `frontend` or `backend`): story link, acceptance criteria, unit tests to write, files it may touch, sized for a 100k context. qalead writes `TC-<n>` files from the same story. | Every story AC is covered by a task and a TC. |
| 3 | pm | Add the tasks and TCs to `board.md`. | Board matches the files. |
| 4 | pm | **Dispatch round:** pick up to 4 ready tasks whose file lists do not overlap, set them `in-progress`, start one dev per task in parallel, collect the reports, set the tasks to `review`, return a short summary. | Reports are in the task files. |
| 5 | lead | Review each task (one at a time): tests cover every acceptance criterion, tests pass with the command in `.team/config.md`, code matches the task and stays inside its file list. Verdict `approve`, or `rework` with notes in the task file. | Verdict written. |
| 6 | pm | Set each task to `done` or `rework`. A second rework sets it to `blocked` and is escalated to the user. | Repeat 4–6 until no task is `todo` or `rework`. |
| 7 | pm → qa → qalead → pm | QA works the same way, **one TC at a time**: pm starts qa on a ready TC, qalead reviews, pm updates the board. An application bug found by qa becomes a new bug-fix TASK written by lead (back to step 3); qa never edits application code. | Every TC `done` or `manual`. |
| 8 | lead, then product | lead runs the closure gate (lint, typecheck, full suites). product fills in `## Closure` in the story, AC by AC. | Report sent to the user. |

**If pm cannot start agents** in this CLI (some do not let a sub-agent start sub-agents; some
have none): pm returns a `DISPATCH` list (task, slot, model, prompt) instead. Start exactly
those agents yourself — devs in parallel — then hand the reports back to pm with "close the
dispatch round". Change nothing in the list. With no sub-agents at all, play the roles one
after another in this session, finishing and writing the files before switching role.

## Handling blocked work

| Status | Coordinator does |
|---|---|
| `blocked: question` | Route it (business → product, technical → lead, neither → user). Once answered, pm sets the item back to `todo`. |
| `blocked: needs file` | lead widens the task's file list or splits off a new task; pm resets it. |
| `blocked: rework limit` | Escalate to the user with the task file. Do not dispatch again without their decision. |
| dev or qa returned nothing usable | pm notes a failed run and sets the item back to `todo`; twice in a row → escalate. |

## Talking to the user
Report at the end of each round in a few lines: what moved, what is blocked and on whom, what
is next. Ask the user only for: sign-off on acceptance criteria, questions product and lead
cannot answer, rework-limit escalations, and anything involving commit, push or deploy.

## Memory touch (end)
- Decisions in `.team/decision.md` that will outlive the story become ADRs in
  `memory/decisions/`, with a one-line pointer in `memory/MEMORY.md`.
- Gotchas found during the run (flaky tests, environment traps) go to `memory/learnings/`.

## Done when
Every task and TC is `done`, the closure gate output is reported as it is, the story's
`## Closure` maps each AC to its proof, and the user has the list of what was **not** verified.
