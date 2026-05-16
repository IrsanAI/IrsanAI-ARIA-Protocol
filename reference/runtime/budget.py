"""Resonance Budget Envelope (RBE) tracking."""
from __future__ import annotations

from typing import Dict


def budget_for_tier(tier: str) -> float:
    defaults = {
        "critical_safety": 0.35,
        "healthcare": 0.45,
        "finance": 0.55,
        "legal": 0.60,
        "business": 0.75,
        "creative": 1.10,
    }
    return defaults.get(tier, 0.70)


def update_budget(*, budget_max: float, budget_used: float, drift_delta: float) -> Dict:
    used = budget_used + max(0.0, drift_delta)
    rem = budget_max - used
    if rem <= 0:
        status = "exhausted"
    elif rem <= budget_max * 0.25:
        status = "warning"
    else:
        status = "within_budget"
    return {
        "budget_max": budget_max,
        "budget_used": used,
        "budget_remaining": rem,
        "status": status,
    }
