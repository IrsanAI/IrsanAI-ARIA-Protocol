"""Resonance Circuit Breaker (RCB) for repeated semantic risk events."""
from __future__ import annotations

from typing import Dict


def circuit_threshold_for_tier(tier: str) -> int:
    return {
        "critical_safety": 1,
        "healthcare": 2,
        "finance": 2,
        "legal": 2,
        "business": 3,
        "creative": 4,
    }.get(tier, 3)


def next_circuit_state(
    *,
    current_state: str,
    event_count: int,
    threshold: int,
    cooldown_remaining: int,
    risk_event: bool,
) -> Dict:
    if current_state == "open":
        if cooldown_remaining > 0:
            return {
                "state": "open",
                "event_count": event_count,
                "threshold": threshold,
                "cooldown_remaining": cooldown_remaining - 1,
            }
        return {
            "state": "half_open",
            "event_count": event_count,
            "threshold": threshold,
            "cooldown_remaining": 0,
        }

    next_count = event_count + (1 if risk_event else 0)
    if next_count >= threshold:
        return {
            "state": "open",
            "event_count": next_count,
            "threshold": threshold,
            "cooldown_remaining": 2,
        }

    return {
        "state": "closed" if current_state != "half_open" else "half_open",
        "event_count": next_count,
        "threshold": threshold,
        "cooldown_remaining": 0,
    }
