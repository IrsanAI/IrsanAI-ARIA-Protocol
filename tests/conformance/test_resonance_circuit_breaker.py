import json
import subprocess
import sys

from reference.runtime.circuit_breaker import circuit_threshold_for_tier, next_circuit_state


def test_circuit_opens_on_threshold():
    th = circuit_threshold_for_tier("finance")
    state = next_circuit_state(
        current_state="closed",
        event_count=th - 1,
        threshold=th,
        cooldown_remaining=0,
        risk_event=True,
    )
    assert state["state"] == "open"


def test_circuit_cli_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "circuit",
            "--tier",
            "finance",
            "--state",
            "closed",
            "--event-count",
            "1",
            "--risk-event",
        ],
        text=True,
    )
    data = json.loads(out)
    assert data["state"] in {"closed", "open", "half_open"}
