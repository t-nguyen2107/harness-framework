# Team guide — the delivery team

A board-driven, six-role team for shipping a story: small tasks, parallel developers, an
independent review on everything, and files as the only memory. Works in any CLI that can
read files, edit files and run commands.

```
you ──► coordinator (main session)
          ├─ product  → .team/stories/STORY-n.md      what + acceptance criteria
          ├─ lead     → .team/tasks/TASK-n.md         how, split small; reviews dev
          ├─ qalead   → .team/testcases/TC-n.md       how it is proven; reviews qa
          └─ pm       → .team/board.md, decision.md   moves work
                ├─ dev ×(up to 4, parallel)           code + unit tests, TDD
                └─ qa  ×1                              automation for one TC
```

## Which team do I use?

| | Lane team (`feature.md`, `bugfix.md`) | Delivery team (`team.md`) |
|---|---|---|
| Roles | manager, senior-database, senior-dev, senior-design, qa-qc, devops | product, lead, pm, qalead, dev, qa |
| Split by | area of the codebase | step of the process |
| State | the conversation + `memory/` | `.team/` files — resumable, shareable across CLIs |
| Parallelism | by lane | up to 4 devs on non-overlapping file lists |
| Good for | a change one session can hold | a story too big for one context, cheap models for the bulk work |

They do not mix inside one run: pick one workflow per request.

## Install

```bash
# 1. In your project (with the harness already dropped in):
cp -r team.template .team

# 2. Wire your CLI
python tools/gen_subagents.py       # Claude Code: .claude/agents/*.md + .claude/rules/team-coordinator.md
python tools/gen_cursor_rules.py    # Cursor: .cursor/rules/*.mdc

# 3. Restart the CLI so it loads the new agents.
```

Then fill in `.team/config.md` — or leave the `<FILL IN>` markers and the coordinator detects
the commands on the first kickoff and tells you what it could not find. The two that matter
most:

- **Isolation slots.** If your tests share a database, cache or port, parallel devs need one
  each. No slots → set `max_parallel_devs` to 1.
- **Project rules.** The handful of invariants a reviewer must fail a task on.

## Use

Kickoff:

```
Team mode. Read harness/workflows/team.md and act as the coordinator.

Story: <what you want, who it is for, and why>
Constraints: <out of scope / deadline / "none">

Run the workflow until the story is done or something is blocked on me.
```

Resume (new session, another CLI, after a crash):

```
Team mode: resume. Read harness/workflows/team.md and .team/board.md,
then continue from the board.
```

Also: `Team mode: status` · `Team mode: answer — TASK-7 Q1: <your answer>` ·
`Team mode: stop after this round`.

You will be asked for: sign-off on the acceptance criteria, questions product and lead cannot
answer, a task that failed review twice, and anything about commit / push / deploy. Nothing is
committed unless `commit_after_approval` is `yes`; nothing is ever pushed.

## How a story flows

1. product writes the story with numbered acceptance criteria → **you approve them**.
2. lead splits it into tasks (frontend / backend, exact file list, tests to write, sized for a
   100k context). qalead writes test cases from the same story.
3. pm puts everything on the board.
4. pm runs a dispatch round: up to 4 devs in parallel on tasks whose file lists do not overlap.
5. lead reviews each task: every criterion has a test, tests pass, code stays in scope.
6. pm records `done` or `rework`. A second rework → `blocked`, escalated to you.
7. QA: one test case at a time — qa automates, qalead reviews, pm records.
8. Closure: lead runs the full gate, product checks each criterion, and you get a report that
   also lists what was not verified.

## Rules that make it work

- **Files are the memory.** Agents remember nothing; every report names the files it updated.
- **One writer per file.** product → stories, lead → tasks, qalead → test cases, pm → board
  and decision log, dev/qa → only the files their task or TC lists.
- **Only devs run in parallel**, only pm starts them, and never on overlapping files.
- **A question stops the work.** It is written into the file, status `blocked: question`,
  answered in the same file; significant answers go to `.team/decision.md`.
- **Author ≠ reviewer**, and a second failed review goes to a human.

## Per-CLI notes

- **Claude Code** — roles are sub-agents; the workflow is a rule scoped to `.team/**`, so it
  stays out of ordinary sessions. `dev` and `qa` get `autoCompactWindow: 100000` in their
  frontmatter; it is a Claude Code *settings* key and is not confirmed to take effect per
  agent, so rely on task sizing to keep them inside 100k. If your version does not let a
  sub-agent start sub-agents, pm returns a `DISPATCH` list and the coordinator starts the devs.
- **Cursor** — roles become rules; run them one after another in one chat, or one chat per
  task for parallel devs.
- **Codex, Gemini CLI, OpenCode, others** — no generator needed: "Act as `lead` per
  `harness/agents/lead.md` on STORY-3". Sequential by default; open one terminal per task
  after pm has set them `in-progress` to go parallel.
- **Mixing CLIs** works because the state is in files. Tell the coordinator "TASK-4 goes to
  Codex"; pm marks Assignee `dev:codex`; in the other CLI: "You are dev. Your task file is
  `.team/tasks/TASK-4.md`. Your slot is 2. Read `harness/agents/dev.md` and follow it."
  A review by a different tool or model than the author is the most useful mix.

Model names in `.team/config.md` are tiers: `haiku` = your CLI's fast model, `sonnet` = its
standard one.

## Limits

- One working tree per team. Do not run a second team, or another session that edits code, in
  the same checkout at the same time.
- Lane discipline for dev and qa (listed files only) is prompt-enforced plus lead's scope
  check — not hook-enforced. `tools/hooks/check_write.py` is where to add a hard wall.
- This is a protocol, not a runtime: no locks, no retries, no checkpointing beyond the files.
