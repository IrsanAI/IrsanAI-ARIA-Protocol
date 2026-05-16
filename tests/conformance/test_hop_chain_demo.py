import json
import subprocess
import sys

from reference.runtime.hop_chain import run_hop_chain


def test_hop_chain_generates_rrc_and_events():
    source = {
        "core_intent": "buy apple stock",
        "constraints": "max 10000 eur blue chips only",
        "context_dependencies": "portfolio state risk class",
        "success_condition": "order executed confirmed",
        "failure_condition": "halt on unrecoverable error",
    }
    report = run_hop_chain(source_atoms=source, hops=4, profile="strict")
    assert "rrc_capsule" in report
    observed_hops = len(report["hops"])
    assert report["rrc_capsule"]["chain_depth_max"] == observed_hops
    assert len(report["rrc_capsule"]["accountability_events"]) == observed_hops


def test_cli_hop_demo():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "hop-demo",
            "--source",
            "fixtures/interop/hop_demo_source_atoms.json",
            "--hops",
            "4",
            "--profile",
            "strict",
        ],
        text=True,
    )
    data = json.loads(out)
    assert "hops" in data
    assert 1 <= len(data["hops"]) <= 4
