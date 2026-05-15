import json
import subprocess
import sys

from reference.runtime.aria_ica import semantic_similarity
from reference.runtime.calibration import evaluate_tier_matrix


def test_domain_tier_matrix_minimums_hold():
    data = json.load(open("tests/goldensets/domain_tier_matrix.json", "r", encoding="utf-8"))
    for tier in data["tiers"]:
        for case in tier["cases"]:
            sim = semantic_similarity(case["source"], case["received"])
            assert sim >= tier["min_similarity"], f"{tier['tier']}::{case['id']} below min"


def test_calibration_cli_outputs_report():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "calibrate",
            "--matrix",
            "tests/goldensets/domain_tier_matrix.json",
        ],
        text=True,
    )
    data = json.loads(out)
    assert "finance" in data
    assert "recommended_floor" in data["finance"]


def test_calibration_module_report_shape():
    report = evaluate_tier_matrix("tests/goldensets/domain_tier_matrix.json")
    assert "critical_safety" in report
    assert report["critical_safety"]["mean_similarity"] >= 0
