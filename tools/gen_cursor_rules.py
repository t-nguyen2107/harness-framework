"""Generate Cursor rules from the harness role prompts.

Reads:  harness/agents/*.md
Writes: .cursor/rules/*.mdc  (Cursor rule files with frontmatter)

Run from the framework root:   python tools/gen_cursor_rules.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "harness" / "agents"
OUT = ROOT / ".cursor" / "rules"

ROOT_DESC = "Harness root contract - read AGENTS.md and follow role/workflow rules."

ROLES = {
    "manager":         {"globs": "docs/**, memory/**"},
    "senior-database": {"globs": "**/migrations/**, **/db.py, **/models.py"},
    "senior-dev":      {"globs": "**/routes/**, **/services/**, src/**, app/**"},
    "senior-design":   {"globs": "src/**, app/**, web/**"},
    "qa-qc":          {"globs": "**/tests/**, **/*.test.*"},
    "devops":          {"globs": "scripts/**, .github/**, Dockerfile, .env.example"},
}


def en_section(text: str) -> str:
    parts = re.split(r"\n---\n", text, maxsplit=1)
    return parts[0]


def render_mdc(description, globs, always_apply, body, slug):
    fm = "---\n"
    fm += "description: " + description + "\n"
    if globs:
        fm += "globs: " + globs + "\n"
    fm += "alwaysApply: " + ("true" if always_apply else "false") + "\n"
    fm += "---\n\n"
    note = "> Auto-generated from harness/agents/" + slug + ".md by tools/gen_cursor_rules.py.\n"
    note += "> Do not edit here - edit the source and re-run the generator.\n\n"
    return fm + note + body.strip() + "\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = []

    root_body = (
        "# Harness - root rule\n\n"
        "Read AGENTS.md at the repo root. Adopt exactly one role per task, "
        "follow the matching workflow in harness/workflows/, respect the rules "
        "in harness/rules/, and keep memory/MEMORY.md updated."
    )
    (OUT / "harness.mdc").write_text(
        render_mdc(ROOT_DESC, "", True, root_body, "_root"), encoding="utf-8"
    )
    written.append("harness (root, alwaysApply)")

    for slug, meta in ROLES.items():
        src = SRC / (slug + ".md")
        if not src.exists():
            print("SKIP " + slug + ": source missing")
            continue
        body = en_section(src.read_text(encoding="utf-8"))
        first = body.strip().splitlines()[0]
        desc = first.lstrip("# ").strip() or slug
        (OUT / (slug + ".mdc")).write_text(
            render_mdc(desc, meta["globs"], False, body, slug), encoding="utf-8"
        )
        written.append(slug)

    print("Wrote " + str(len(written)) + " cursor rules: " + ", ".join(written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
