# Team config

Commands and locations every delivery-team agent uses. This is the only project-specific file
in `.team/` — everything else is protocol.

**First kickoff:** the coordinator replaces every `<FILL IN>` by detecting it from the repo
(package scripts, Makefile, CI workflow, compose file), runs each command once to confirm it
works, and lists what it could not detect in §8. If a command here stops working, fix this
file — do not work around it.

## 0. Preflight (coordinator runs this at kickoff and on every resume)

```bash
git status --short --branch
```

- The branch must not be the default branch. Team work happens on a feature branch.
- The working tree must not contain someone else's uncommitted work.
- **The tests must run against the checkout being edited.** If tests run inside containers or
  a remote environment, check that it mounts / deploys *this* directory:
  `<FILL IN — a command that proves it, or "tests run directly in this checkout">`

If any check fails, stop and tell the user.

## 1. Build

| What | Command |
|---|---|
| Backend | `<FILL IN or "no build step">` |
| Frontend | `<FILL IN or "no build step">` |

Run builds at story closure only, unless they are safe alongside running developers.

## 2. Lint / typecheck

| Scope | Command |
|---|---|
| Backend | `<FILL IN>` |
| Frontend | `<FILL IN>` |

## 3. Unit tests

| Scope | One file / one test | Whole suite |
|---|---|---|
| Backend | `<FILL IN>` | `<FILL IN>` |
| Frontend | `<FILL IN>` | `<FILL IN>` |

Where unit tests live and how they are named: `<FILL IN>`

### Isolation slots (parallel devs)

Up to `max_parallel_devs` developers run tests at the same time in one working tree. If the
tests share anything mutable — a database, a cache, a port, a temp directory — each dev needs
its own copy, called a **slot** (`1..N`), and reviewers use the default environment.

- Shared mutable state in this project's tests: `<FILL IN — e.g. "test database + redis", or "none">`
- **Dev command for slot `<k>`:** `<FILL IN — the unit-test command with slot k's database / port / dir, or "same as above (no shared state)">`
- **Review command** (lead, qalead, qa — one at a time, default environment): `<FILL IN>`
- One-time slot setup: `<FILL IN or "none">`

If slots cannot be provided, set `max_parallel_devs` to 1.

## 4. E2E tests

| Key | Value |
|---|---|
| Available | `<FILL IN — yes | no>` |
| Run command | `<FILL IN>` |
| Location | `<FILL IN>` |
| Seed / auth setup | `<FILL IN>` |

If not available, qalead must not write `e2e` test cases; a flow that truly needs a browser
is written as `manual` and listed for the user at closure.

## 5. Where automation tests live (qa)

| TC level | Available | Location and naming | Runner |
|---|---|---|---|
| `api` | `<FILL IN>` | `<FILL IN — e.g. tests/test_tc<n>_<slug>.py>` | review command in §3 |
| `ui` | `<FILL IN>` | `<FILL IN>` | `<FILL IN>` |
| `e2e` | see §4 | `<FILL IN>` | `<FILL IN>` |
| `manual` | always | steps stay in the TC file | user |

## 6. Policies

| Key | Value | Meaning |
|---|---|---|
| `max_parallel_devs` | 4 | Hard cap on developers per dispatch round (= number of slots) |
| `dev_model` | haiku | Default model tier for dev |
| `dev_model_complex` | sonnet | Used for `complexity: complex` tasks and rework attempts |
| `qa_model` | haiku | Default model tier for qa |
| `migrations_per_round` | 1 | Tasks with `migration: yes` allowed in flight at once |
| `commit_after_approval` | no | `no`: nothing is committed, the user reviews the working tree. `yes`: the coordinator commits each approved task's files, following `harness/rules/commit.md` |
| `push` | never | No agent pushes, merges or deploys |

Model names are tiers, not vendors: map `haiku` to your CLI's fast model and `sonnet` to its
standard one.

## 7. Project rules

The invariants product writes into stories, devs follow, and lead fails a review on. Keep it
to the ten that matter; link to the doc for the rest.

- `<FILL IN — e.g. "every data lookup goes through the access-check helpers in <path>">`
- `<FILL IN — e.g. "UI copy in English only">`
- `<FILL IN — e.g. "no network calls in tests">`
- Full project guidance: `<FILL IN — AGENTS.md / CLAUDE.md / docs path>`

## 8. Could not detect

- `<the coordinator lists here what is still <FILL IN> and why>`
