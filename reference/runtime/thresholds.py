"""RFC-003 threshold profile utilities."""
from typing import Dict

THRESHOLD_FLOORS: Dict[str, float] = {
    "strict": 0.95,
    "balanced": 0.90,
    "exploratory": 0.82,
}


def floor_for(profile: str) -> float:
    if profile not in THRESHOLD_FLOORS:
        raise ValueError(f"unknown threshold profile: {profile}")
    return THRESHOLD_FLOORS[profile]
