# team.template/

State files for the delivery team (`harness/workflows/team.md`). Copy this folder to `.team/`
in your project and commit it — the board is meant to be tracked, so every CLI and every
machine sees the same state.

```bash
cp -r team.template .team
```

| File | Owner | Purpose |
|---|---|---|
| `config.md` | you / coordinator | Build, lint, test commands; isolation slots; policies; project rules. The only project-specific file |
| `board.md` | pm | Status of every task and test case |
| `decision.md` | pm | Decisions that came out of questions |
| `stories/_template.md` | product | `STORY-<n>.md` |
| `tasks/_template.md` | lead | `TASK-<n>.md` |
| `testcases/_template.md` | qalead | `TC-<n>.md` |

Fill in `config.md` yourself, or let the coordinator detect it on the first kickoff.
Guide: [`docs/TEAM_GUIDE.md`](../docs/TEAM_GUIDE.md).
