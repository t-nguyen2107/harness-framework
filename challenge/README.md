# Challenge — Reading List Tracker

A small brief to practice the harness. It exercises every role and every workflow stage without being large.

> You bring the code. The harness governs how you produce it.

## The brief

Build a **Reading List Tracker**: a single-user app to track books you want to read.

### Functional requirements

| ID | Requirement |
|----|-------------|
| R1 | Add a book: title, author, status (`want` / `reading` / `done`), optional notes. |
| R2 | List books, filterable by status. |
| R3 | Change a book's status. |
| R4 | Delete a book. |
| R5 | Search books by title or author (substring, case-insensitive). |

### Non-functional

- Any stack you like (the harness is stack-agnostic). Suggestion: the same SQLite + Python + Next.js you saw, or whatever you know best.
- Single user, local. No auth.
- Tests for the core logic.

## Acceptance criteria (used by QA/QC)

1. R1–R5 each have at least one passing test.
2. The five statuses round-trip: add as `want`, move to `reading`, move to `done`.
3. Search returns the right books and is case-insensitive.
4. `scripts/dev` (or your equivalent) boots the app in one command.
5. At least one ADR exists explaining a non-obvious choice (e.g. how you model status).

## How to run it through the harness

1. Start a fresh agent session in this folder.
2. Give it this brief as the request.
3. Watch which path it takes — see `docs/GUIDE.html` → "How to use".

## What to look for (the actual lesson)

- Did the agent read `AGENTS.md` and `memory/MEMORY.md` first?
- Did it decompose into roles (Manager) or freelance?
- Did it write an ADR for the status-modeling choice?
- Did a different lane verify the work (authoring ≠ review)?
- Did it boot the app and capture real evidence, or claim success without running anything?

The output app is secondary. The point is to see the harness shape the process.
