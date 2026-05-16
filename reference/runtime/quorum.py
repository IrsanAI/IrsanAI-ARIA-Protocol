"""Semantic Consensus Quorum (SCQ) evaluator."""
from __future__ import annotations

from typing import Dict, List


def quorum_for_tier(tier: str) -> float:
    return {
        "critical_safety": 0.90,
        "healthcare": 0.85,
        "finance": 0.80,
        "legal": 0.75,
        "business": 0.67,
        "creative": 0.60,
    }.get(tier, 0.67)


def evaluate_quorum(votes: List[Dict], quorum_ratio: float) -> Dict:
    total = max(1, len(votes))
    confirmed = sum(1 for v in votes if v.get("status") == "ack_confirmed")
    ratio = confirmed / total

    if ratio >= quorum_ratio:
        outcome = "quorum_confirmed"
    elif ratio >= max(0.5, quorum_ratio - 0.2):
        outcome = "quorum_degraded"
    else:
        outcome = "quorum_rejected"

    return {
        "quorum_ratio": quorum_ratio,
        "total_votes": total,
        "confirmed_votes": confirmed,
        "observed_ratio": ratio,
        "outcome": outcome,
        "votes": votes,
    }
