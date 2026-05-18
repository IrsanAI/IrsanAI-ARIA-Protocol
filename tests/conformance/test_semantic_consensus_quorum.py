import json
import subprocess
import sys

from reference.runtime.quorum import evaluate_quorum, quorum_for_tier


def test_quorum_confirmed_for_finance_default():
    votes = [
        {"status": "ack_confirmed"},
        {"status": "ack_confirmed"},
        {"status": "ack_drift_detected"},
    ]
    report = evaluate_quorum(votes, quorum_for_tier("finance"))
    assert report["outcome"] in {"quorum_confirmed", "quorum_degraded"}


def test_quorum_cli_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "quorum",
            "--tier",
            "finance",
            "--votes",
            "fixtures/interop/quorum_votes.json",
        ],
        text=True,
    )
    data = json.loads(out)
    assert "outcome" in data
    assert data["total_votes"] == 3
