import json
import subprocess
import sys
from pathlib import Path


def test_cli_chain_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "chain",
            "--source",
            "fixtures/interop/hop_demo_source_atoms.json",
            "--hops",
            "4",
            "--profile",
            "strict",
            "--tier",
            "finance",
        ],
        text=True,
    )
    data = json.loads(out)
    assert "rrc_capsule" in data


def test_publish_scorecard_script():
    subprocess.check_call([sys.executable, "benchmarks/interop_report.py"])
    subprocess.check_call([sys.executable, "benchmarks/publish_scorecard.py"])
    p = Path("benchmarks/interop_scorecard.md")
    assert p.exists()
    assert "ARIA Interop Scorecard" in p.read_text()
