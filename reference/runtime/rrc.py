"""Resonance Replay Capsule emitter (RFC-004 draft scaffold)."""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Dict, List

from reference.runtime.validation import validate_rrc_capsule


def emit_rrc_capsule(
    capsule_id: str,
    mission_fingerprint: str,
    hop_sequence: List[Dict],
    final_outcome: str,
    audit_signature: str,
) -> Dict:
    capsule = {
        "capsule_id": capsule_id,
        "mission_fingerprint": mission_fingerprint,
        "hop_sequence": hop_sequence,
        "final_outcome": final_outcome,
        "audit_signature": audit_signature,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    # remove non-schema key for now to keep strict schema compliance
    capsule.pop("generated_at")
    validate_rrc_capsule(capsule)
    return capsule
