"""Mini multi-hop chain PoC with intentional drift injection and semantic ACKs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from reference.runtime.aria_ica import semantic_similarity
from reference.runtime.execution_specialist import ExecutionSpecialist
from reference.runtime.rrc import emit_rrc_capsule
from reference.runtime.accountability import create_accountability_event, sign_event


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
) -> Dict:
    specialist = ExecutionSpecialist()
    hop_results: List[HopResult] = []
    rrc_hops: List[Dict] = []
    events: List[Dict] = []

    previous = dict(source_atoms)
    for i in range(1, hops + 1):
        current = _drifted_atoms(previous, i)
        sim = semantic_similarity(source_atoms, current)
        ack = specialist.semantic_ack(str(sim), "1.0", profile=profile)
        drift_delta = 1.0 - sim

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
            }
        )
        evt = create_accountability_event(
            event_type=ack.status,
            agent_id=f"agent-{i}",
            chain_depth=i,
            mission_fingerprint=mission_fingerprint,
            metadata={"similarity": sim, "drift_delta": drift_delta},
        )
        evt["signature"] = sign_event(evt, secret="aria-hop-chain-secret")
        events.append(evt)
        previous = current

    final_outcome = "completed" if all(h.ack_status == "ack_confirmed" for h in hop_results) else "escalated"
    capsule = emit_rrc_capsule(
        capsule_id="rrc-hop-chain-001",
        mission_fingerprint=mission_fingerprint,
        hop_sequence=rrc_hops,
        final_outcome=final_outcome,
        audit_signature="audit-hop-chain",
        accountability_events=events,
    )

    return {
        "final_outcome": final_outcome,
        "hops": [h.__dict__ for h in hop_results],
        "rrc_capsule": capsule,
    }
