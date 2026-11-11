# TASK-<n>: <title>

- status: todo
- story: [STORY-<n>](../stories/STORY-<n>.md)
- type: <frontend | backend>
- complexity: <standard | complex>   <!-- complex = started on a stronger model -->
- migration: <no | yes>              <!-- yes = changes the database schema -->
- depends on: <TASK-… that must be done first, or none>
- owner: lead

## Goal

<Two or three sentences: what changes and why. A dev with no other context must understand it.>

## Acceptance criteria

<The story ACs this task delivers, restated so they can be tested at this level.>

- AC-1 (story AC-1): …
- AC-2 (story AC-3): …

## Unit tests to write

Written first, and failing, before any implementation. One or more per acceptance criterion.

| Test (file::name) | Covers | Kind |
|---|---|---|
| `<test file>::<test name>` | AC-1 | <unit / integration> |
| `<test file>` › "<case>" | AC-2 | <…> |

## Files this task may touch

Nothing outside this list may be created or edited. Need another file → stop, report blocked.

- `<path>` — <new | edit>: <what>
- `<path>` — <new | edit>: <what>

## Read first

<Only what is needed, to keep the dev inside a 100k context. Point at sections, not whole files.>

- `<path>` — <function / lines / what to look for>
- Pattern to copy: `<path>`
- Project rules that apply: <the relevant lines from `.team/config.md` → Project rules>

## Out of scope

- <…>

## Questions

<!-- Q1 (dev, <date>): …
     A1 (lead|product, <date>): … -->

## Dev report

<!-- dev appends one block per run:
### Run <n> — <date> — slot <k>
status · files changed · test command · last lines of output -->

## Review

<!-- lead appends one block per review:
### Review <n> — <date> — approve | rework
AC coverage · test result · scope check · rework notes (numbered, specific) -->
