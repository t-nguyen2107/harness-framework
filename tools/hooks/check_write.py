"""PreToolUse hook (Claude Code): block writes to forbidden paths.

Reads the tool-call JSON from stdin. Exits 0 to allow, 2 to block
(stderr is shown to the agent).

Forbidden (safety rule + DB integrity):
  - .env files (secrets)        except .env.example
  - *.sqlite / *.sqlite-*       the live database

This is the first tooth of the harness. Extend the denylist or add
per-role path enforcement here.

Wire it in .claude/settings.json with matcher Write|Edit|NotebookEdit and
command:  python "${CLAUDE_PROJECT_DIR}/tools/hooks/check_write.py"
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _forbidden(path_str):
    name = Path(path_str).name
    if name == ".env":
        return "Refusing to write to .env (secrets). Use .env.example."
    if name.startswith(".env.") and not name.endswith(".example"):
        return "Refusing to write to " + name + " (possible secret)."
    if name.endswith(".sqlite") or ".sqlite-" in name:
        return "Refusing to write to " + name + " (live database file)."
    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    file_path = (data.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return 0
    reason = _forbidden(file_path)
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
