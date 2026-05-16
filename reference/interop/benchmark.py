"""Interop benchmark harness: legacy -> ARIA -> legacy roundtrip drift report."""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from reference.interop.legacy_bridge_adapter import aria_to_legacy, legacy_to_aria
from reference.runtime.semantic import cosine_similarity_text


def _constraint_similarity(a: List[str], b: List[str]) -> float:
    return cosine_similarity_text(" ".join(a), " ".join(b))


def evaluate_roundtrip_case(case: Dict[str, Any]) -> Dict[str, Any]:
    legacy_in = case["legacy_input"]
    aria_packet = legacy_to_aria(legacy_in)
    legacy_out = aria_to_legacy(aria_packet)

    goal_sim = cosine_similarity_text(legacy_in.get("goal", ""), legacy_out.get("goal", ""))
    constraint_sim = _constraint_similarity(
        legacy_in.get("constraints", []), legacy_out.get("constraints", [])
    )
    overall = (goal_sim + constraint_sim) / 2.0

    return {
        "id": case.get("id", "unknown"),
        "goal_similarity": goal_sim,
        "constraint_similarity": constraint_sim,
        "overall_similarity": overall,
        "drift_delta": 1.0 - overall,
    }


def evaluate_roundtrip_suite(fixtures_path: str) -> Dict[str, Any]:
    data = json.loads(Path(fixtures_path).read_text())
    results = [evaluate_roundtrip_case(case) for case in data.get("cases", [])]
    avg_overall = mean([r["overall_similarity"] for r in results]) if results else 0.0
    avg_drift = mean([r["drift_delta"] for r in results]) if results else 0.0
    return {
        "suite": Path(fixtures_path).name,
        "cases": results,
        "summary": {
            "count": len(results),
            "average_similarity": avg_overall,
            "average_drift_delta": avg_drift,
        },
    }
