# harness/workflows/

Multi-role orchestration flows. Each has a **trigger**, ordered **steps** (role → action), a **gate** to advance, and a **memory touch** at start and end.

| File | When to use |
|------|-------------|
| `feature.md` | Ship a feature end-to-end |
| `bugfix.md` | Fix a reported bug |
| `explore.md` | Read-only recon before a big change |
