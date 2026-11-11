# Harness Framework

A **prompt + hook overlay** that turns any coding agent into a role-based, multi-agent team with a memory layer. CLI-portable. No runtime. Bring your own project.

> The model is the engine. The harness is the **steering wheel, the brakes, and the map**.

---

## 📖 Pick your path

| You want to… | Read this | Time |
|---|---|---|
| Understand the framework before using it | [**Learning Guide**](https://t-nguyen2107.github.io/harness-framework/LEARNING_GUIDE.html) | 30 min read |
| Wire it into your CLI, write roles, build hooks | [**Developer Guide**](https://t-nguyen2107.github.io/harness-framework/DEV_GUIDE.html) | 30 min read + run |
| Just see what the code looks like | [`harness/agents/`](./harness/agents/) | 5 min skim |

Both guides are standalone HTML — open them in any browser, no build step.

---

## ⚡ What you get

- **6 role prompts** (Manager, Senior DB, Senior Dev, Senior Design, QA/QC, DevOps) with strict owned-paths discipline.
- **3 workflows** (feature, bugfix, explore) that gate every step.
- **A delivery team** (product, lead, pm, qalead, dev, qa) with a file-based board in `.team/`: small tasks, up to 4 parallel devs on cheap models, independent review, resumable from any CLI. See the [Team guide](./docs/TEAM_GUIDE.md).
- **A safety hook** that blocks writes to `.env`, `*.db`, secrets — exit 2, machine-enforced, not prompt-soft.
- **Versioned memory**: `memory/MEMORY.md` index + `decisions/`, `conventions/`, `learnings/` — read at session start, written at session end.
- **CLI-portable**: same prompts drive Claude Code, Cursor, Codex, OpenCode. Swap CLIs without losing memory.
- **No new runtime, no new dependency**. It steers an existing model; it does not become one.

---

## 🚀 Install in 5 minutes

```bash
# 1. Drop the framework into your project (or clone this repo).
git clone https://github.com/t-nguyen2107/harness-framework.git
cd harness-framework

# 2. Read AGENTS.md + memory/MEMORY.md at the repo root — they're mandatory.
cat AGENTS.md
cat memory/MEMORY.md

# 3. Wire your CLI.

# Claude Code
cp -r .claude.template .claude
python tools/gen_subagents.py

# Cursor
python tools/gen_cursor_rules.py

# Optional: the delivery team (board-driven, parallel devs)
cp -r team.template .team        # then see docs/TEAM_GUIDE.md

# 4. Open a fresh session, ask the agent:
#    "List the six roles defined here and their owned paths."

# 5. Run the safety probe:
#    Ask the agent: "Reset my sqlite database file."
#    The hook MUST block it. If it doesn't, see the Developer Guide → Hooks.
```

---

## 🗂 Repo layout

```
harness-framework/
├── AGENTS.md              # contract every agent reads first
├── harness/               # orchestration layer (source of truth)
│   ├── agents/            # 6 lane roles + 6 delivery-team roles (.md)
│   ├── workflows/         # feature / bugfix / explore / team
│   ├── rules/             # code-style / commit / memory / safety
│   └── adapters/          # per-CLI mapping (claude-code / cursor)
├── memory/                # second brain (versioned)
│   ├── MEMORY.md          # one-line index, loaded each session
│   └── decisions/         # ADRs
├── team.template/         # copy to .team/ — board, config, story/task/TC templates
├── tools/                 # generators + the safety hook
│   ├── gen_subagents.py   # role .md → .claude/agents/
│   ├── gen_cursor_rules.py
│   ├── hooks/check_write.py
│   ├── hooks/team_scope.py  # delivery team: each role writes only what it owns
│   └── tests/
├── challenge/             # practice brief
└── docs/
    ├── LEARNING_GUIDE.html
    ├── DEV_GUIDE.html
    └── TEAM_GUIDE.md      # delivery team: install, kickoff prompt, per-CLI notes
```

**Read order for every session:** `AGENTS.md` → `memory/MEMORY.md` → relevant ADRs → your role prompt.

---

## 🧠 Core principles

1. **Prompts steer, hooks enforce.** A prompt is a suggestion; a hook is a wall. Critical safety lives in hooks, not prose.
2. **Edit the source, regenerate the derived.** Never hand-edit `.claude/agents/` — the generator overwrites it. The role prompt in `harness/agents/` is the single source of truth.
3. **One role per commit, one ADR per non-obvious decision.** Memory is cheap; rediscovering a decision 6 months later is expensive.
4. **Authoring is not review.** The author commits; a different lane (QA/QC or another role) signs off. No self-approval.
5. **CLI-agnostic by design.** The framework does not know which CLI is running. Swap agents; keep memory.

---

## 🆚 When NOT to use this

| Better alternative | If you need |
|---|---|
| **LangGraph / AutoGen / CrewAI** | Strong runtime guarantees, programmatic orchestration, checkpointed state |
| **SWE-agent / Devin** | End-to-end autonomous task execution as a product |
| **Raw prompts + your judgement** | One-off tasks, prototypes, exploration with no repeatability need |

This framework trades runtime guarantees for portability. If you need hard-coded locks and reproducible state machines, use a runtime framework instead.

---

## 🧪 Try the challenge

```bash
cd challenge/
cat README.md   # pick one of three briefs, ship it end-to-end
```

Or bring your own project and apply the 3-step quickstart above.

---

## 📚 Further reading

- [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — reasoning + acting loop
- [Reflexion (Shinn et al., 2023)](https://arxiv.org/abs/2303.11381) — verbal reinforcement
- [AutoGen (Wu et al., 2023)](https://arxiv.org/abs/2308.08155) — multi-agent conversation
- [SWE-agent (Yang et al., 2024)](https://arxiv.org/abs/2405.15793) — agent-computer interfaces

---

## License

MIT.