"""Mini multi-hop chain PoC with intentional drift injection and semantic ACKs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from reference.runtime.aria_ica import semantic_similarity
from reference.runtime.execution_specialist import ExecutionSpecialist
from reference.runtime.rrc import emit_rrc_capsule
from reference.runtime.accountability import create_accountability_event, sign_event
from reference.runtime.guardrails import guardrail_decision
from reference.runtime.budget import budget_for_tier, update_budget


@dataclass
class HopResult:
    hop: int
    agent_id: str
    ack_status: str
    similarity: float
    drift_delta: float


def _drifted_atoms(atoms: Dict[str, str], hop: int) -> Dict[str, str]:
    out = dict(atoms)
    # deterministic intentional drift after hop 2
    if hop >= 2:
        out["constraints"] = out.get("constraints", "") + " flexible budget"
    if hop >= 3:
        out["core_intent"] = "increase technology exposure"
    return out


def run_hop_chain(
    source_atoms: Dict[str, str],
    hops: int = 4,
    profile: str = "strict",
    mission_fingerprint: str = "mf-hop-chain",
    tier: str = "finance",
) -> Dict:
    specialist = ExecutionSpecialist()
    hop_results: List[HopResult] = []
    rrc_hops: List[Dict] = []
    events: List[Dict] = []

    previous = dict(source_atoms)
    drift_history: List[float] = []
    budget = {"budget_max": budget_for_tier(tier), "budget_used": 0.0, "budget_remaining": budget_for_tier(tier), "status": "within_budget"}
    for i in range(1, hops + 1):
        current = _drifted_atoms(previous, i)
        sim = semantic_similarity(source_atoms, current)
        ack = specialist.semantic_ack(str(sim), "1.0", profile=profile)
        drift_delta = 1.0 - sim

        moving_drift = (sum(drift_history) / len(drift_history)) if drift_history else drift_delta
        guard = guardrail_decision(
            similarity=sim,
            profile=profile,
            tier=tier,
            chain_depth=i,
            moving_drift=moving_drift,
        )

        hop_results.append(
            HopResult(
                hop=i,
                agent_id=f"agent-{i}",
                ack_status=ack.status,
                similarity=sim,
                drift_delta=drift_delta,
            )
        )
        rrc_hops.append(
            {
                "agent_id": f"agent-{i}",
                "received_ic": f"sim::{sim:.6f}",
                "recomputed_ic": "sim::1.000000",
                "ack_status": ack.status,
                "delta_score": drift_delta,
                "chain_depth": i,
                "guardrail_mode": guard["mode"],
            }
        )
        budget = update_budget(
            budget_max=budget["budget_max"],
            budget_used=budget["budget_used"],
            drift_delta=drift_delta,
        )

        evt = create_accountability_event(
            event_type=f"{ack.status}:{guard["mode"]}",
            agent_id=f"agent-{i}",
            chain_depth=i,
            mission_fingerprint=mission_fingerprint,
            metadata={"similarity": sim, "drift_delta": drift_delta, "budget": budget},
        )
        evt["signature"] = sign_event(evt, secret="aria-hop-chain-secret")
        events.append(evt)
        drift_history.append(drift_delta)
        previous = current
        if guard["mode"] == "block" or budget["status"] == "exhausted":
            break

    final_outcome = "completed" if all(h.ack_status == "ack_confirmed" for h in hop_results) else "escalated"
    capsule = emit_rrc_capsule(
        capsule_id="rrc-hop-chain-001",
        mission_fingerprint=mission_fingerprint,
        hop_sequence=rrc_hops,
        final_outcome=final_outcome,
        audit_signature="audit-hop-chain",
        accountability_events=events,
    )

    capsule["resonance_budget"] = budget
    return {
        "final_outcome": final_outcome,
        "hops": [h.__dict__ for h in hop_results],
        "rrc_capsule": capsule,
        "resonance_budget": budget,
    }
