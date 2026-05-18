import json
import subprocess
import sys

from reference.runtime.canary import run_canary_suite


def test_canary_suite_passes():
    report = run_canary_suite("tests/goldensets/resonance_canary_suite.json")
    assert report["status"] in {"pass", "fail"}
    assert report["summary"]["count"] == 2


def test_cli_canary_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "canary",
            "--suite",
            "tests/goldensets/resonance_canary_suite.json",
        ],
        text=True,
    )
    data = json.loads(out)
    assert "cases" in data
    assert len(data["cases"]) == 2
