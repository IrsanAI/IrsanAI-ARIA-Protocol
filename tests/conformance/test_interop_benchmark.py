import json
import subprocess
import sys

from reference.interop.benchmark import evaluate_roundtrip_suite


def test_interop_benchmark_report_shape():
    report = evaluate_roundtrip_suite("fixtures/interop/legacy_roundtrip_cases.json")
    assert "summary" in report
    assert report["summary"]["count"] >= 2
    assert 0 <= report["summary"]["average_similarity"] <= 1


def test_cli_interop_benchmark():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "interop-benchmark",
            "--fixtures",
            "fixtures/interop/legacy_roundtrip_cases.json",
        ],
        text=True,
    )
    data = json.loads(out)
    assert "cases" in data
    assert len(data["cases"]) >= 2
