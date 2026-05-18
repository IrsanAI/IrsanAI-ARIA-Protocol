import json
import subprocess
import sys

from reference.runtime.lineage import build_intent_lineage_graph


def test_lineage_graph_shape():
    hops = [
        {"agent_id": "a1", "similarity": 1.0, "drift_delta": 0.0, "guardrail_mode": "allow"},
        {"agent_id": "a2", "similarity": 0.8, "drift_delta": 0.2, "guardrail_mode": "review"},
    ]
    g = build_intent_lineage_graph("mf-x", hops, "strict")
    assert g["graph_id"].startswith("ilg-")
    assert len(g["nodes"]) == 3
    assert len(g["edges"]) == 2


def test_cli_lineage_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "lineage",
            "--mission-fingerprint",
            "mf-hop",
            "--hops",
            "fixtures/interop/hop_demo_hops.json",
            "--profile",
            "strict",
        ],
        text=True,
    )
    data = json.loads(out)
    assert "nodes" in data and "edges" in data
    assert len(data["edges"]) == 3
