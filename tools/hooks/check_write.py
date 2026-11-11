"""PreToolUse hook (Claude Code): block writes to forbidden paths.

Reads the tool-call JSON from stdin. Exits 0 to allow, 2 to block
(stderr is shown to the agent).

Forbidden (safety rule + DB integrity):
  - .env files (secrets)        except .env.example
  - *.sqlite / *.sqlite-*       the live database

Delivery-team scope (harness/workflows/team.md): when the call comes from a
sub-agent whose type is a team role (product, lead, pm, qalead, dev, qa), the
write must also be inside what that role owns — see team_scope.py. Set
HARNESS_TEAM_SCOPE=off to disable that check only.

This is the first tooth of the harness. Extend the denylist here.

Wire it in .claude/settings.json with matcher Write|Edit|NotebookEdit and
command:  python "${CLAUDE_PROJECT_DIR}/tools/hooks/check_write.py"
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import team_scope


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
    # agent_id is present only inside a sub-agent; the main session (the
    # coordinator, or any ordinary session) is never team-scoped.
    if data.get("agent_id") and os.environ.get("HARNESS_TEAM_SCOPE", "").lower() != "off":
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
        reason = team_scope.check(data.get("agent_type"), file_path, project_dir)
        if reason:
            print(reason, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
