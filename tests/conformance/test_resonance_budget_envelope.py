import json
import subprocess
import sys

from reference.runtime.budget import budget_for_tier, update_budget
from reference.runtime.hop_chain import run_hop_chain


def test_budget_transitions_to_warning_or_exhausted():
    bmax = budget_for_tier("finance")
    b = update_budget(budget_max=bmax, budget_used=0.0, drift_delta=bmax * 0.9)
    assert b["status"] in {"warning", "exhausted"}


def test_hop_chain_includes_resonance_budget():
    source = {
        "core_intent": "buy apple stock",
        "constraints": "max 10000 eur blue chips only",
        "context_dependencies": "portfolio state risk class",
        "success_condition": "order executed confirmed",
        "failure_condition": "halt on unrecoverable error",
    }
    report = run_hop_chain(source_atoms=source, hops=5, profile="strict", tier="finance")
    assert "resonance_budget" in report
    assert "status" in report["resonance_budget"]


def test_cli_budget_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "budget",
            "--tier",
            "finance",
            "--drift-delta",
            "0.2",
        ],
        text=True,
    )
    d = json.loads(out)
    assert "budget_remaining" in d
