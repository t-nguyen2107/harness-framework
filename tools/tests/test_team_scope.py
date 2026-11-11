"""Tests for the delivery-team write scope (tools/hooks/team_scope.py).

Run from the framework root:   python -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "hooks"))

import team_scope  # noqa: E402

TASK = """# TASK-{n}: example

- status: {status}
- story: [STORY-1](../stories/STORY-1.md)
- type: backend

## Files this task may touch

Nothing outside this list may be created or edited.

- `{a}` — edit: handler
- `{b}` — new: test
- `<path>` — <new | edit>: placeholder left from the template

## Read first

- `src/not_allowed.py` — only to read
"""

TC = """# TC-{n}: example

- status: {status}
- level: api
- test file: `{test}`
- helper files: {helpers}
"""


class TeamScopeCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        for d in ("stories", "tasks", "testcases"):
            (self.root / ".team" / d).mkdir(parents=True)
        (self.root / ".team" / "board.md").write_text("# Board\n")
        self.task(1, "in-progress", "src/api/a.py", "tests/test_a.py")
        self.task(2, "todo", "src/api/b.py", "tests/test_b.py")
        self.tc(1, "in-progress", "tests/test_tc1_flow.py", "`tests/helpers/flow.py`")
        self.tc(2, "todo", "tests/test_tc2_other.py", "none")

    def tearDown(self):
        self._tmp.cleanup()

    def task(self, n, status, a, b):
        (self.root / ".team" / "tasks" / f"TASK-{n}.md").write_text(
            TASK.format(n=n, status=status, a=a, b=b)
        )

    def tc(self, n, status, test, helpers):
        (self.root / ".team" / "testcases" / f"TC-{n}.md").write_text(
            TC.format(n=n, status=status, test=test, helpers=helpers)
        )

    def check(self, role, rel):
        return team_scope.check(role, str(self.root / rel), str(self.root))

    def assertAllowed(self, role, rel):
        self.assertIsNone(self.check(role, rel), f"{role} should be allowed to write {rel}")

    def assertBlocked(self, role, rel):
        reason = self.check(role, rel)
        self.assertIsNotNone(reason, f"{role} should be blocked from writing {rel}")
        self.assertIn(rel, reason)


class DevScope(TeamScopeCase):
    def test_dev_may_write_files_of_an_in_progress_task(self):
        self.assertAllowed("dev", "src/api/a.py")
        self.assertAllowed("dev", "tests/test_a.py")

    def test_dev_is_blocked_from_files_of_a_task_that_is_not_in_progress(self):
        self.assertBlocked("dev", "src/api/b.py")

    def test_dev_is_blocked_from_files_no_task_lists(self):
        self.assertBlocked("dev", "src/api/other.py")

    def test_read_first_paths_do_not_grant_write(self):
        self.assertBlocked("dev", "src/not_allowed.py")

    def test_dev_may_write_task_files_but_not_board_stories_or_testcases(self):
        self.assertAllowed("dev", ".team/tasks/TASK-1.md")
        self.assertBlocked("dev", ".team/board.md")
        self.assertBlocked("dev", ".team/stories/STORY-1.md")
        self.assertBlocked("dev", ".team/testcases/TC-1.md")

    def test_dev_with_no_task_in_progress_is_blocked_everywhere_in_code(self):
        self.task(1, "review", "src/api/a.py", "tests/test_a.py")
        reason = self.check("dev", "src/api/a.py")
        self.assertIsNotNone(reason)
        self.assertIn("in-progress", reason)

    def test_status_with_trailing_detail_still_counts(self):
        self.task(2, "in-progress  ", "src/api/b.py", "tests/test_b.py")
        self.assertAllowed("dev", "src/api/b.py")

    def test_directory_entries_allow_everything_below(self):
        self.task(3, "in-progress", "src/widgets/", "tests/widgets/**")
        self.assertAllowed("dev", "src/widgets/button.py")
        self.assertAllowed("dev", "tests/widgets/deep/test_button.py")
        self.assertBlocked("dev", "src/widgets_other/x.py")

    def test_path_outside_the_project_is_blocked(self):
        self.assertIsNotNone(team_scope.check("dev", "/tmp/elsewhere.py", str(self.root)))

    def test_relative_and_dotted_paths_are_normalised(self):
        self.assertIsNone(team_scope.check("dev", "./src/api/a.py", str(self.root)))
        self.assertIsNotNone(team_scope.check("dev", "src/api/../api/b.py", str(self.root)))


class QaScope(TeamScopeCase):
    def test_qa_may_write_test_and_helper_of_an_in_progress_tc(self):
        self.assertAllowed("qa", "tests/test_tc1_flow.py")
        self.assertAllowed("qa", "tests/helpers/flow.py")

    def test_qa_is_blocked_from_application_code_even_if_a_task_lists_it(self):
        self.assertBlocked("qa", "src/api/a.py")

    def test_qa_is_blocked_from_a_tc_that_is_not_in_progress(self):
        self.assertBlocked("qa", "tests/test_tc2_other.py")

    def test_qa_may_write_tc_files_but_not_task_files(self):
        self.assertAllowed("qa", ".team/testcases/TC-1.md")
        self.assertBlocked("qa", ".team/tasks/TASK-1.md")


class PlanningRoles(TeamScopeCase):
    def test_no_planning_role_may_write_code(self):
        for role in ("product", "lead", "pm", "qalead"):
            self.assertBlocked(role, "src/api/a.py")

    def test_product_writes_stories_and_answers_in_tasks_and_tcs(self):
        self.assertAllowed("product", ".team/stories/STORY-2.md")
        self.assertAllowed("product", ".team/tasks/TASK-1.md")
        self.assertAllowed("product", ".team/testcases/TC-1.md")
        self.assertBlocked("product", ".team/board.md")

    def test_lead_writes_tasks_not_the_board(self):
        self.assertAllowed("lead", ".team/tasks/TASK-9.md")
        self.assertAllowed("lead", ".team/stories/STORY-1.md")
        self.assertBlocked("lead", ".team/board.md")
        self.assertBlocked("lead", ".team/decision.md")

    def test_qalead_writes_testcases_not_tasks(self):
        self.assertAllowed("qalead", ".team/testcases/TC-9.md")
        self.assertBlocked("qalead", ".team/tasks/TASK-1.md")

    def test_pm_owns_board_and_decision_log_and_status_lines(self):
        self.assertAllowed("pm", ".team/board.md")
        self.assertAllowed("pm", ".team/decision.md")
        self.assertAllowed("pm", ".team/tasks/TASK-1.md")
        self.assertAllowed("pm", ".team/testcases/TC-1.md")
        self.assertBlocked("pm", ".team/stories/STORY-1.md")
        self.assertBlocked("pm", ".team/config.md")


class NotApplicable(TeamScopeCase):
    def test_other_agents_are_not_restricted(self):
        self.assertIsNone(self.check("senior-dev", "src/api/other.py"))
        self.assertIsNone(self.check("", "src/api/other.py"))
        self.assertIsNone(self.check(None, "src/api/other.py"))

    def test_project_without_team_folder_is_not_restricted(self):
        with tempfile.TemporaryDirectory() as bare:
            self.assertIsNone(team_scope.check("dev", str(Path(bare) / "x.py"), bare))


class HookEndToEnd(TeamScopeCase):
    """check_write.py as Claude Code calls it: JSON on stdin, exit 0 / 2."""

    def run_hook(self, payload, env_extra=None):
        import os

        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)}
        env.pop("HARNESS_TEAM_SCOPE", None)
        env.update(env_extra or {})
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / "hooks" / "check_write.py")],
            input=json.dumps(payload), capture_output=True, text=True, env=env,
        )

    def payload(self, rel, **extra):
        return {"tool_name": "Edit", "tool_input": {"file_path": str(self.root / rel)},
                "cwd": str(self.root), **extra}

    def test_subagent_dev_out_of_scope_exits_2_with_reason(self):
        r = self.run_hook(self.payload("src/api/other.py", agent_id="a1", agent_type="dev"))
        self.assertEqual(r.returncode, 2)
        self.assertIn("src/api/other.py", r.stderr)

    def test_subagent_dev_in_scope_exits_0(self):
        r = self.run_hook(self.payload("src/api/a.py", agent_id="a1", agent_type="dev"))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_main_thread_is_never_scoped(self):
        # No agent_id: the coordinator / an ordinary session.
        r = self.run_hook(self.payload("src/api/other.py"))
        self.assertEqual(r.returncode, 0, r.stderr)
        r = self.run_hook(self.payload("src/api/other.py", agent_type="dev"))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_env_file_is_still_blocked_for_everyone(self):
        r = self.run_hook(self.payload(".env"))
        self.assertEqual(r.returncode, 2)

    def test_kill_switch_disables_team_scope_only(self):
        off = {"HARNESS_TEAM_SCOPE": "off"}
        r = self.run_hook(self.payload("src/api/other.py", agent_id="a1", agent_type="dev"), off)
        self.assertEqual(r.returncode, 0, r.stderr)
        r = self.run_hook(self.payload(".env", agent_id="a1", agent_type="dev"), off)
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
