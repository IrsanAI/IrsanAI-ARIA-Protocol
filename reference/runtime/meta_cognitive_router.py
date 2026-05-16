"""Meta-Cognitive Router: task -> Cognitive Role Map (CRA)."""
from __future__ import annotations

from typing import Dict


def assess_dimensions(task_text: str) -> Dict[str, float]:
    t = (task_text or "").lower()
    dims = {
        "perception": 0.4,
        "memory": 0.2,
        "reasoning": 0.2,
        "creativity": 0.1,
        "code": 0.0,
        "critique": 0.1,
        "synthesis": 0.0,
    }
    if any(k in t for k in ["why", "because", "if", "therefore", "risk"]):
        dims["reasoning"] += 0.5
    if any(k in t for k in ["create", "write", "draft", "idea"]):
        dims["creativity"] += 0.5
    if any(k in t for k in ["code", "debug", "function", "api"]):
        dims["code"] += 0.7
    if any(k in t for k in ["verify", "check", "correct", "audit"]):
        dims["critique"] += 0.5
    if any(k in t for k in ["history", "context", "previous", "retrieve"]):
        dims["memory"] += 0.5
    return {k: min(1.0, v) for k, v in dims.items()}


def build_role_map(task_id: str, task_text: str, activation_threshold: float = 0.3) -> Dict:
    dims = assess_dimensions(task_text)
    roles = {r: {"confidence": c} for r, c in dims.items() if c >= activation_threshold}
    if len(roles) > 1:
        roles["synthesis"] = {"confidence": max(0.6, dims.get("reasoning", 0.0))}

    high_conf = all(v["confidence"] >= 0.95 for v in roles.values()) if roles else False
    if not high_conf and "critique" not in roles:
        roles["critique"] = {"confidence": 0.6}

    return {
        "task_id": task_id,
        "roles": roles,
        "execution_mode": "parallel" if len(roles) > 2 else "sequential",
        "self_assessment": {
            "role_coverage": min(1.0, sum(v["confidence"] for v in roles.values()) / max(1, len(roles))),
            "missing_roles": [],
            "recommendation": "PROCEED" if roles else "REVIEW",
        },
    }
