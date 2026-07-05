# Rule — Safety (Guardrails)

These are blockers, not suggestions. Violating any of them stops the work.

1. **Don't delete files you didn't create.** If deletion is needed, surface it and ask first.
2. **Authoring ≠ review.** The role that wrote code cannot sign it off.
3. **Don't skip tests.** If a test fails, fix the cause — never delete or weaken the test.
4. **Don't modify product source to make a test pass.** File a bug instead.
5. **Stay in your lane.** Only touch the paths your role owns.
6. **Secrets never committed.** Only `.env.example` is tracked.
7. **Irreversible actions need confirmation.** Deletes, force-pushes, deploys, and external publishes ask first.
8. **Report honestly.** If a step was skipped or a test fails, say so plainly.
