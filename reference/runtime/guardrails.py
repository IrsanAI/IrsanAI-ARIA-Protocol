"""Resonance Guardrails Gateway (RGG) policy engine."""
from __future__ import annotations

from typing import Dict, Literal

from reference.runtime.thresholds import floor_for

GuardMode = Literal["allow", "review", "block"]


TIER_RISK_BUMP = {
    "critical_safety": 0.08,
    "healthcare": 0.06,
    "finance": 0.04,
    "legal": 0.04,
    "business": 0.02,
    "creative": 0.0,
}


def guardrail_decision(
    *,
    similarity: float,
    profile: str,
    tier: str,
    chain_depth: int,
    moving_drift: float,
) -> Dict:
    floor = floor_for(profile)
    dynamic_floor = min(1.0, floor + TIER_RISK_BUMP.get(tier, 0.03) + min(0.05, moving_drift * 0.2))

    if similarity < dynamic_floor - 0.08:
        return {
            "mode": "block",
            "reason": "similarity below dynamic safety floor",
            "similarity": similarity,
            "profile": profile,
            "tier": tier,
            "chain_depth": chain_depth,
        }
    if similarity < dynamic_floor:
        return {
            "mode": "review",
            "reason": "similarity near safety boundary",
            "similarity": similarity,
            "profile": profile,
            "tier": tier,
            "chain_depth": chain_depth,
        }
    return {
        "mode": "allow",
        "reason": "similarity within safe operating envelope",
        "similarity": similarity,
        "profile": profile,
        "tier": tier,
        "chain_depth": chain_depth,
    }
