import json
import subprocess
import sys

from reference.runtime.meta_cognitive_router import build_role_map


def test_build_role_map_includes_synthesis_when_multi_role():
    rm = build_role_map("tsk-1", "write and verify a strategy with risks")
    assert "roles" in rm
    assert "synthesis" in rm["roles"]


def test_cli_rolemap_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "rolemap",
            "--task-id",
            "tsk-2",
            "--task-text",
            "debug this api and verify correctness",
        ],
        text=True,
    )
    data = json.loads(out)
    assert data["task_id"] == "tsk-2"
    assert "roles" in data
