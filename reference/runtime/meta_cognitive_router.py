"""Meta-Cognitive Router: task -> Cognitive Role Map (CRA), registry-aware."""
from __future__ import annotations

from typing import Dict, List


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


def assign_roles_to_agents(
    role_conf: Dict[str, float],
    registry_snapshot: List[Dict],
    preferred_domain: str | None = None,
) -> Dict[str, Dict]:
    assignments: Dict[str, Dict] = {}
    for role, conf in role_conf.items():
        candidates = [c for c in registry_snapshot if role in c.get("roles", [])]
        if preferred_domain:
            domain_hits = [c for c in candidates if preferred_domain in c.get("domains", [])]
            if domain_hits:
                candidates = domain_hits
        if candidates:
            chosen = sorted(candidates, key=lambda c: (c.get("trust_level", ""), c.get("latency_class", "")), reverse=True)[0]
            assignments[role] = {
                "confidence": conf,
                "agent_id": chosen["agent_id"],
                "agent_type": chosen["agent_type"],
            }
        else:
            assignments[role] = {"confidence": conf, "agent_id": None, "agent_type": None}
    return assignments


def build_role_map(
    task_id: str,
    task_text: str,
    activation_threshold: float = 0.3,
    registry_snapshot: List[Dict] | None = None,
    preferred_domain: str | None = None,
) -> Dict:
    dims = assess_dimensions(task_text)
    active = {r: c for r, c in dims.items() if c >= activation_threshold}
    if len(active) > 1:
        active["synthesis"] = max(0.6, dims.get("reasoning", 0.0))

    high_conf = all(v >= 0.95 for v in active.values()) if active else False
    if not high_conf and "critique" not in active:
        active["critique"] = 0.6

    if registry_snapshot is None:
        roles = {r: {"confidence": c, "agent_id": None, "agent_type": None} for r, c in active.items()}
    else:
        roles = assign_roles_to_agents(active, registry_snapshot, preferred_domain=preferred_domain)

    missing_roles = [r for r, v in roles.items() if not v.get("agent_id")]
    return {
        "task_id": task_id,
        "roles": roles,
        "execution_mode": "parallel" if len(roles) > 2 else "sequential",
        "self_assessment": {
            "role_coverage": min(1.0, sum(v["confidence"] for v in roles.values()) / max(1, len(roles))),
            "missing_roles": missing_roles,
            "recommendation": "PROCEED" if not missing_roles else "REVIEW",
        },
    }
