"""Interop benchmark v2 with compatibility profiles and lossy mutation simulation."""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from reference.interop.legacy_bridge_adapter import aria_to_legacy, legacy_to_aria
from reference.runtime.semantic import cosine_similarity_text


def _constraint_similarity(a: List[str], b: List[str]) -> float:
    return cosine_similarity_text(" ".join(a), " ".join(b))


def _apply_mutations(legacy_out: Dict[str, Any], mutations: Dict[str, Any], profile: str) -> Dict[str, Any]:
    out = dict(legacy_out)
    # bridge-safe preserves semantics: no lossy mutation applied.
    if profile == "bridge-safe":
        return out

    # bridge-legacy simulates common lossy transformations.
    if "drop_constraints_after_roundtrip" in mutations:
        drops = set(mutations["drop_constraints_after_roundtrip"])
        out["constraints"] = [c for c in out.get("constraints", []) if c not in drops]
    if "rewrite_goal_after_roundtrip" in mutations:
        out["goal"] = mutations["rewrite_goal_after_roundtrip"]
    return out


def evaluate_case(case: Dict[str, Any], profile: str) -> Dict[str, Any]:
    legacy_in = case["legacy_input"]
    aria_packet = legacy_to_aria(legacy_in)
    legacy_out = aria_to_legacy(aria_packet)
    legacy_out = _apply_mutations(legacy_out, case.get("mutations", {}), profile)

    goal_sim = cosine_similarity_text(legacy_in.get("goal", ""), legacy_out.get("goal", ""))
    cons_sim = _constraint_similarity(legacy_in.get("constraints", []), legacy_out.get("constraints", []))
    overall = (goal_sim + cons_sim) / 2.0

    return {
        "id": case.get("id", "unknown"),
        "profile": profile,
        "goal_similarity": goal_sim,
        "constraint_similarity": cons_sim,
        "overall_similarity": overall,
        "drift_delta": 1.0 - overall,
    }


def evaluate_suite(fixtures_path: str, profile: str) -> Dict[str, Any]:
    data = json.loads(Path(fixtures_path).read_text())
    cases = [evaluate_case(c, profile) for c in data.get("cases", [])]
    return {
        "profile": profile,
        "suite": Path(fixtures_path).name,
        "cases": cases,
        "summary": {
            "count": len(cases),
            "average_similarity": mean([c["overall_similarity"] for c in cases]) if cases else 0.0,
            "average_drift_delta": mean([c["drift_delta"] for c in cases]) if cases else 0.0,
        },
    }


def compare_profiles(fixtures_path: str) -> Dict[str, Any]:
    safe = evaluate_suite(fixtures_path, "bridge-safe")
    legacy = evaluate_suite(fixtures_path, "bridge-legacy")
    return {
        "suite": safe["suite"],
        "bridge_safe": safe,
        "bridge_legacy": legacy,
        "delta": {
            "similarity_gain_safe_over_legacy": safe["summary"]["average_similarity"] - legacy["summary"]["average_similarity"],
            "drift_reduction_safe_over_legacy": legacy["summary"]["average_drift_delta"] - safe["summary"]["average_drift_delta"],
        },
    }
