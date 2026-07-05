# Harness Framework

A learning framework for **Harness Engineering + Multi-Agent Orchestration + Memory (Second Brain)**.

It works with most coding agents — Claude Code, Codex, Cursor, OpenCode, Antigravite — and contains **no application code**. Bring your own project; the framework governs *how agents work on it*.

## What's inside

- `AGENTS.md` — the contract every agent reads first.
- `harness/` — role prompts, workflows, rules, CLI adapters.
- `memory/` — the "second brain" scaffolding (decisions, conventions, learnings).
- `tools/` — generators that turn prompts into CLI-specific config, plus a safety hook.
- `.claude.template/` — copy into `.claude/` to wire Claude Code.
- `challenge/` — a sample project brief to practice the harness on.
- `docs/GUIDE.html` — the illustrated guide (open it in a browser).

## Quickstart (3 minutes)

1. Copy this folder into your own project (or start a new one here).
2. Open `docs/GUIDE.html` and read the workflow.
3. For Claude Code: `cp -r .claude.template .claude` then run `python tools/gen_subagents.py`.
4. For Cursor: `python tools/gen_cursor_rules.py`.
5. Pick the `challenge/` brief (or your own task) and let the harness drive.

## The core idea

> The model is the engine; the harness is the steering wheel, brakes, and map.

Without a harness, an agent freelances. With it, the agent works in a **role**, follows a **workflow**, leaves a **memory trail**, and respects **guardrails**.

See `docs/GUIDE.html` for the full picture.
