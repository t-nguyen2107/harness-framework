"""Write scope for the delivery team (harness/workflows/team.md).

Turns "each role only writes what it owns" from a prompt rule into a wall.
Called by check_write.py for every Write / Edit made by a sub-agent.

Who may write what:

  product   .team/stories/, and answers in .team/tasks/ and .team/testcases/
  lead      .team/tasks/, .team/stories/, .team/testcases/
  qalead    .team/testcases/, .team/stories/
  pm        .team/board.md, .team/decision.md, .team/tasks/, .team/testcases/
  dev       .team/tasks/TASK-*.md + the "Files this task may touch" of every
            task whose status is in-progress
  qa        .team/testcases/TC-*.md + the "test file" / "helper files" of
            every test case whose status is in-progress

Devs run in parallel and the hook cannot tell which dev holds which task, so a
dev is held to the union of all in-flight tasks. Staying inside its *own* task
is still checked by lead's review.

Not covered: files changed through the shell (sed -i, redirects). The hook only
sees Write / Edit tool calls; lead's `git status` scope check catches the rest.

Any other agent, and any project without a .team/ folder, is not restricted.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

TEAM_DIR = ".team"

# Planning roles: fixed path prefixes (a trailing "/" means "everything below").
STATIC_SCOPE = {
    "product": [".team/stories/", ".team/tasks/", ".team/testcases/"],
    "lead": [".team/tasks/", ".team/stories/", ".team/testcases/"],
    "qalead": [".team/testcases/", ".team/stories/"],
    "pm": [".team/board.md", ".team/decision.md", ".team/tasks/", ".team/testcases/"],
}
# Working roles: their own folder + whatever the in-progress files list.
DYNAMIC_SCOPE = {
    "dev": {"own": ".team/tasks/", "glob": "tasks/TASK-*.md"},
    "qa": {"own": ".team/testcases/", "glob": "testcases/TC-*.md"},
}
TEAM_ROLES = set(STATIC_SCOPE) | set(DYNAMIC_SCOPE)

_STATUS = re.compile(r"^- status:\s*(.+?)\s*$", re.M)
_BACKTICKED = re.compile(r"`([^`]+)`")
_FILES_HEADING = "## Files this task may touch"


def _in_progress(text):
    m = _STATUS.search(text)
    return bool(m) and m.group(1).startswith("in-progress")


def _clean(entry):
    """A listed path as a comparable prefix, or None for template placeholders."""
    entry = entry.strip()
    if not entry or "<" in entry:
        return None
    if entry.endswith("/**"):
        entry = entry[:-2]  # keep the trailing slash
    return os.path.normpath(entry) + ("/" if entry.endswith("/") else "")


def _task_files(text):
    """Paths under '## Files this task may touch' (first backticked item per bullet)."""
    if _FILES_HEADING not in text:
        return []
    section = text.split(_FILES_HEADING, 1)[1]
    section = re.split(r"^## ", section, maxsplit=1, flags=re.M)[0]
    out = []
    for line in section.splitlines():
        if line.lstrip().startswith("- "):
            m = _BACKTICKED.search(line)
            if m:
                out.append(m.group(1))
    return out


def _tc_files(text):
    """Backticked paths on the '- test file:' and '- helper files:' lines."""
    out = []
    for line in text.splitlines():
        if line.startswith("- test file:") or line.startswith("- helper files:"):
            out.extend(_BACKTICKED.findall(line))
    return out


def _active_files(project_dir, role):
    """Allowed code paths for dev / qa: lists from every in-progress file."""
    extract = _task_files if role == "dev" else _tc_files
    allowed = []
    for path in sorted((project_dir / TEAM_DIR).glob(DYNAMIC_SCOPE[role]["glob"])):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if _in_progress(text):
            allowed.extend(filter(None, (_clean(e) for e in extract(text))))
    return allowed


def _matches(rel, allowed):
    for entry in allowed:
        if entry.endswith("/"):
            if rel.startswith(entry):
                return True
        elif rel == entry:
            return True
    return False


def check(agent_type, file_path, project_dir):
    """Return None to allow the write, or a reason string to block it."""
    if agent_type not in TEAM_ROLES:
        return None
    root = Path(project_dir).resolve()
    if not (root / TEAM_DIR).is_dir():
        return None

    target = Path(file_path)
    if not target.is_absolute():
        target = root / target
    target = Path(os.path.normpath(str(target)))
    try:
        rel = target.relative_to(root).as_posix()
    except ValueError:
        return (
            "Team scope: " + agent_type + " may not write outside the project (" + str(target) + ")."
        )

    if agent_type in STATIC_SCOPE:
        allowed = STATIC_SCOPE[agent_type]
        if _matches(rel, allowed):
            return None
        return (
            "Team scope: " + agent_type + " may not write " + rel + ". It owns only: "
            + ", ".join(allowed) + ". If the work needs this file, report it instead of editing."
        )

    if rel.startswith(DYNAMIC_SCOPE[agent_type]["own"]):
        return None
    allowed = _active_files(root, agent_type)
    if _matches(rel, allowed):
        return None
    kind = "task" if agent_type == "dev" else "test case"
    if not allowed:
        return (
            "Team scope: " + agent_type + " may not write " + rel + ": no " + kind
            + " is in-progress (pm sets the status before starting you)."
        )
    return (
        "Team scope: " + agent_type + " may not write " + rel + ": it is not listed in any in-progress "
        + kind + ". Allowed now: " + ", ".join(allowed) + ". If the work needs this file, stop and "
        + "report 'blocked: needs file' — do not edit it."
    )
