import json
import subprocess
import sys

from reference.interop.benchmark_v2 import compare_profiles


def test_profile_comparison_shows_safe_advantage():
    report = compare_profiles("fixtures/interop/legacy_roundtrip_lossy_cases.json")
    assert report["delta"]["similarity_gain_safe_over_legacy"] >= 0
    assert report["delta"]["drift_reduction_safe_over_legacy"] >= 0


def test_cli_interop_compare_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "interop-compare",
            "--fixtures",
            "fixtures/interop/legacy_roundtrip_lossy_cases.json",
        ],
        text=True,
    )
    data = json.loads(out)
    assert "bridge_safe" in data and "bridge_legacy" in data
