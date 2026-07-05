# Rule — Commits

- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `perf:`.
- One role per commit. The body may name the role.
- Atomic: one logical change per commit; tests ship with the code they cover.
- Subject ≤ 72 chars, imperative mood.
- Never commit: secrets, `.env`, build artifacts, dependencies, local databases.
- Reference the ADR or task when relevant.
