"""Resonance Replay Capsule emitter (RFC-004 draft scaffold)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from reference.runtime.validation import validate_rrc_capsule


def emit_rrc_capsule(
    capsule_id: str,
    mission_fingerprint: str,
    hop_sequence: List[Dict],
    final_outcome: str,
    audit_signature: str,
    accountability_events: Optional[List[Dict]] = None,
) -> Dict:
    max_chain_depth = max((int(h.get("chain_depth", 0)) for h in hop_sequence), default=0)
    capsule = {
        "capsule_id": capsule_id,
        "mission_fingerprint": mission_fingerprint,
        "hop_sequence": hop_sequence,
        "final_outcome": final_outcome,
        "audit_signature": audit_signature,
        "chain_depth_max": max_chain_depth,
        "accountability_events": accountability_events or [],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    # schema currently does not include extension fields; validate canonical subset
    validate_rrc_capsule({
        "capsule_id": capsule["capsule_id"],
        "mission_fingerprint": capsule["mission_fingerprint"],
        "hop_sequence": capsule["hop_sequence"],
        "final_outcome": capsule["final_outcome"],
        "audit_signature": capsule["audit_signature"],
    })
    return capsule
