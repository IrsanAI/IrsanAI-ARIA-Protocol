import json
from pathlib import Path

from reference.runtime.aria_ica import compute_intent_checksum, semantic_similarity


def test_compute_intent_checksum_shape():
    atoms = {
        "core_intent": "execute equity purchase",
        "constraints": "max 10k",
        "context_dependencies": "portfolio state",
        "success_condition": "order confirmed",
        "failure_condition": "halt on error",
    }
    result = compute_intent_checksum(atoms)
    assert 0 <= result.score <= 1
    assert set(result.atoms.keys()) == {
        "core_intent",
        "constraints",
        "context_dependencies",
        "success_condition",
        "failure_condition",
    }


def test_goldenset_semantic_similarity_ranges():
    data = json.loads(Path("tests/goldensets/semantic_equivalence_and_drift.json").read_text())
    for case in data["cases"]:
        sim = semantic_similarity(case["source"], case["received"])
        if "expected_min_similarity" in case:
            assert sim >= case["expected_min_similarity"], f"{case['id']} below min"
        if "expected_max_similarity" in case:
            assert sim <= case["expected_max_similarity"], f"{case['id']} above max"
