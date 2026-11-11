# TC-<n>: <title>

- status: todo
- story: [STORY-<n>](../stories/STORY-<n>.md)
- covers: <story AC-…>
- level: <api | ui | e2e | manual>   <!-- only levels marked available in .team/config.md §5 -->
- depends on: <TASK-… that must be done before this can be automated>
- test file: `<path from .team/config.md §5>`
- owner: qalead

## Purpose

<What user-visible behaviour this proves, in one or two sentences.>

## Preconditions / data

- <user, role, data, fixtures — and how the test creates them>

## Steps and expected results

| # | Step | Expected |
|---|---|---|
| 1 | … | … |
| 2 | … | … |

## Negative / edge cases

- <e.g. a user without access is refused; empty state; invalid input>

## Questions

<!-- Q1 (qa, <date>): …
     A1 (qalead|product|lead, <date>): … -->

## QA report

<!-- qa appends one block per run:
### Run <n> — <date>
status · files changed · test command · last lines of output · app bug found? (evidence) -->

## Review

<!-- qalead appends one block per review:
### Review <n> — <date> — approve | rework
steps covered · assertions are real · passes twice · rework notes (numbered, specific) -->
