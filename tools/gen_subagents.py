"""Generate Claude Code subagents from the harness role prompts.

Reads:  harness/agents/*.md
Writes: .claude/agents/*.md  (subagent definitions with frontmatter)

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
}


def en_section(text: str) -> str:
    parts = re.split(r"\n---\n", text, maxsplit=1)
    return parts[0]


def render(slug: str, meta: dict, body: str) -> str:
    fm = "---\n"
    fm += "name: " + slug + "\n"
    fm += "description: " + meta["description"] + "\n"
    fm += "model: " + meta["model"] + "\n"
    fm += "tools: " + meta["tools"] + "\n"
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
