"""Resonance Canary Suite evaluator."""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from reference.runtime.aria_ica import semantic_similarity


def run_canary_suite(path: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text())
    cases_out: List[Dict[str, Any]] = []
    for c in data.get("cases", []):
        sim = semantic_similarity(c["source"], c["received"])
        cases_out.append({
            "id": c["id"],
            "similarity": sim,
            "expected_min": c.get("expected_min", 0.0),
            "pass": sim >= c.get("expected_min", 0.0),
        })
    avg = mean([c["similarity"] for c in cases_out]) if cases_out else 0.0
    status = "pass" if all(c["pass"] for c in cases_out) else "fail"
    return {
        "suite_id": data.get("suite_id", "canary-suite"),
        "baseline_version": data.get("baseline_version", "unknown"),
        "candidate_version": data.get("candidate_version", "unknown"),
        "status": status,
        "cases": cases_out,
        "summary": {"count": len(cases_out), "avg_similarity": avg},
    }
