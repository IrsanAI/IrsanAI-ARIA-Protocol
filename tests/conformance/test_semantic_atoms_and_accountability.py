from reference.runtime.accountability import create_accountability_event, sign_event
from reference.runtime.semantic import cosine_similarity_text, per_atom_drift_score


def test_cosine_similarity_text_partial_overlap():
    sim = cosine_similarity_text("buy apple stock max 10k", "buy apple shares max 10k")
    assert 0.5 < sim < 1.0


def test_per_atom_drift_scoring():
    source = {
        "core_intent": "execute equity purchase",
        "constraints": "max 10k blue chips only",
        "context_dependencies": "portfolio state risk class",
        "success_condition": "order executed confirmed",
        "failure_condition": "halt on unrecoverable error",
    }
    received = {
        "core_intent": "execute equity purchase",
        "constraints": "max 50k",
        "context_dependencies": "portfolio state risk class",
        "success_condition": "order executed confirmed",
        "failure_condition": "halt on unrecoverable error",
    }
    drift = per_atom_drift_score(source, received)
    assert drift["core_intent"] == 0.0
    assert drift["constraints"] > 0.0


def test_accountability_event_signature():
    event = create_accountability_event(
        event_type="ack_drift_detected",
        agent_id="agent-b",
        chain_depth=2,
        mission_fingerprint="mf-42",
        metadata={"delta": 0.2},
    )
    sig = sign_event(event, secret="aria-secret")
    assert isinstance(sig, str)
    assert len(sig) == 64
