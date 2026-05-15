from reference.runtime.execution_specialist import ExecutionSpecialist
from reference.runtime.rrc import emit_rrc_capsule
from reference.runtime.validation import validate_aria_packet, validate_semantic_ack


def test_threshold_profiles_strict_detects_drift():
    agent = ExecutionSpecialist()
    result = agent.semantic_ack("ic::1", "ic::2", profile="strict")
    assert result.status == "ack_drift_detected"


def test_schema_validation_packet_and_ack():
    packet = {
        "aria_version": "0.1",
        "channel_id": "003",
        "origin_type": "AGENT",
        "mission_core": "execute trade",
        "constraints": ["max 10k"],
        "context_snapshot": {},
        "intent_checksum": "ic::123",
        "chain_depth": 0,
        "timestamp_utc": "2026-05-15T00:00:00Z",
    }
    ack = {
        "status": "ack_confirmed",
        "similarity_score": 1.0,
        "threshold_profile": "balanced",
    }
    validate_aria_packet(packet)
    validate_semantic_ack(ack)


def test_rrc_capsule_emission():
    capsule = emit_rrc_capsule(
        capsule_id="rrc-1",
        mission_fingerprint="mf-1",
        hop_sequence=[
            {
                "agent_id": "agent-a",
                "received_ic": "ic::1",
                "recomputed_ic": "ic::1",
                "ack_status": "ack_confirmed",
                "delta_score": 0.0,
            }
        ],
        final_outcome="completed",
        audit_signature="sig-1",
    )
    assert capsule["capsule_id"] == "rrc-1"
