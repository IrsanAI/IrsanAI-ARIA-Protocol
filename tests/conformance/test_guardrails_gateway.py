from reference.runtime.guardrails import guardrail_decision
from reference.runtime.hop_chain import run_hop_chain


def test_guardrail_blocks_low_similarity_for_critical_safety():
    d = guardrail_decision(
        similarity=0.5,
        profile="strict",
        tier="critical_safety",
        chain_depth=2,
        moving_drift=0.4,
    )
    assert d["mode"] in {"review", "block"}


def test_hop_chain_stops_on_block_when_drift_compounds():
    source = {
        "core_intent": "trigger emergency shutdown protocol",
        "constraints": "require dual verification",
        "context_dependencies": "sensor anomaly and plant state",
        "success_condition": "shutdown confirmed and logged",
        "failure_condition": "halt if verification fails",
    }
    report = run_hop_chain(source_atoms=source, hops=6, profile="strict", tier="critical_safety")
    assert len(report["hops"]) <= 6
    assert report["final_outcome"] in {"completed", "escalated"}
