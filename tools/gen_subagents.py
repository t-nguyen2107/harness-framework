"""Generate Claude Code subagents from the harness role prompts.

Reads:  harness/agents/*.md, harness/workflows/team.md
Writes: .claude/agents/*.md  (subagent definitions with frontmatter)
        .claude/rules/team-coordinator.md  (team workflow, path-scoped rule)

Why a generator: the harness is the single source of truth. Subagents are a
derived artifact for one specific CLI (Claude Code). Hand-writing them would
let the prompt and the subagent drift apart.

Run from the framework root:   python tools/gen_subagents.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "harness" / "agents"
OUT = ROOT / ".claude" / "agents"

ROLES = {
    "manager":         {"model": "opus",   "description": "Orchestrator: break down work, delegate to roles, decide scope.",  "tools": "Read, Glob, Grep, Task, Write"},
    "senior-database": {"model": "sonnet", "description": "Owns schema, migrations, indexes, query performance.",                "tools": "Read, Glob, Grep, Write, Edit, Bash"},
    "senior-dev":      {"model": "sonnet", "description": "Implements API, business logic, and UI wiring.",                      "tools": "Read, Glob, Grep, Write, Edit, Bash"},
    "senior-design":   {"model": "sonnet", "description": "UI/UX, design tokens, component layout, accessibility.",               "tools": "Read, Glob, Grep, Write, Edit"},
    "qa-qc":          {"model": "sonnet", "description": "Test plan, run tests, capture evidence, sign-off or block.",            "tools": "Read, Glob, Grep, Bash, Write"},
    "devops":          {"model": "sonnet", "description": "Scripts, env, CI/CD, containers, deployment docs.",                    "tools": "Read, Glob, Grep, Write, Edit, Bash"},
    # Delivery team (harness/workflows/team.md). Only pm may start agents.
    # "extra" lines are copied into the frontmatter as-is.
    "product": {"model": "sonnet", "description": "Delivery team: writes stories with acceptance criteria, answers business questions. Team mode only.", "tools": "Read, Write, Edit, Glob, Grep"},
    "lead":    {"model": "sonnet", "description": "Delivery team: splits stories into tasks, reviews dev work, answers technical questions. Team mode only.", "tools": "Read, Write, Edit, Glob, Grep, Bash"},
    "pm":      {"model": "sonnet", "description": "Delivery team: owns the board and decision log, starts dev and qa agents. Team mode only.", "tools": "Read, Write, Edit, Glob, Grep, Agent"},
    "qalead":  {"model": "sonnet", "description": "Delivery team: writes test cases from a story, reviews qa automation. Team mode only.", "tools": "Read, Write, Edit, Glob, Grep, Bash"},
    "dev":     {"model": "haiku",  "description": "Delivery team: implements one task with TDD inside its listed files. Started only by pm.", "tools": "Read, Write, Edit, Glob, Grep, Bash", "extra": ["autoCompactWindow: 100000"]},
    "qa":      {"model": "haiku",  "description": "Delivery team: automates one test case. Started only by pm.", "tools": "Read, Write, Edit, Glob, Grep, Bash", "extra": ["autoCompactWindow: 100000"]},
}

# The team workflow becomes a Claude Code rule that loads only when the
# session touches .team/ files, so ordinary sessions are not affected.
WORKFLOW_SRC = ROOT / "harness" / "workflows" / "team.md"
RULE_OUT = ROOT / ".claude" / "rules" / "team-coordinator.md"


def en_section(text: str) -> str:
    parts = re.split(r"\n---\n", text, maxsplit=1)
    return parts[0]


def render(slug: str, meta: dict, body: str) -> str:
    fm = "---\n"
    fm += "name: " + slug + "\n"
    fm += "description: " + meta["description"] + "\n"
    fm += "model: " + meta["model"] + "\n"
    fm += "tools: " + meta["tools"] + "\n"
    for line in meta.get("extra", []):
        fm += line + "\n"
    fm += "---\n\n"
    note = "> Auto-generated from harness/agents/" + slug + ".md by tools/gen_subagents.py.\n"
    note += "> Do not edit here - edit the source and re-run the generator.\n\n"
    return fm + note + body.strip() + "\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for slug, meta in ROLES.items():
        src = SRC / (slug + ".md")
        if not src.exists():
            print("SKIP " + slug + ": source missing")
            continue
        body = en_section(src.read_text(encoding="utf-8"))
        (OUT / (slug + ".md")).write_text(render(slug, meta, body), encoding="utf-8")
        written.append(slug)
    print("Wrote " + str(len(written)) + " subagents: " + ", ".join(written))
    if WORKFLOW_SRC.exists():
        RULE_OUT.parent.mkdir(parents=True, exist_ok=True)
        rule = '---\npaths:\n  - ".team/**"\n---\n\n'
        rule += "> Auto-generated from harness/workflows/team.md by tools/gen_subagents.py.\n"
        rule += "> Do not edit here - edit the source and re-run the generator.\n\n"
        rule += WORKFLOW_SRC.read_text(encoding="utf-8").strip() + "\n"
        RULE_OUT.write_text(rule, encoding="utf-8")
        print("Wrote rule: .claude/rules/team-coordinator.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
