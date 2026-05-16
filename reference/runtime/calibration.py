"""Calibration helpers for domain-tier threshold recommendations."""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Dict, List

from reference.runtime.aria_ica import semantic_similarity
from reference.runtime.thresholds import floor_for


def evaluate_tier_matrix(path: str) -> Dict[str, Dict[str, float]]:
    data = json.loads(Path(path).read_text())
    report: Dict[str, Dict[str, float]] = {}
    for tier in data["tiers"]:
        sims: List[float] = []
        for c in tier["cases"]:
            sims.append(semantic_similarity(c["source"], c["received"]))
        current_floor = floor_for(tier["profile"])
        report[tier["tier"]] = {
            "mean_similarity": mean(sims) if sims else 0.0,
            "profile_floor": current_floor,
            "recommended_floor": max(0.0, min(1.0, (mean(sims) if sims else 0.0) - 0.05)),
            "min_required": tier["min_similarity"],
        }
    return report
