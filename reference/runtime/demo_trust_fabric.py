"""
Showcase Demo: ARIA Meta-Cognitive Trust Fabric in Action.
Demonstrates Mission Contracts, Capability Identity, and Drift Detection.
"""
from reference.runtime.trust_fabric import TrustFabric, CapabilityCard, TrustLevel, MissionContract, AuditCapsule
from reference.runtime.aria_ica import MetacognitiveICA

def run_demo():
    print("=== ARIA Meta-Cognitive Trust Fabric Demo ===\n")
    
    # 1. Initialize Trust Fabric
    fabric = TrustFabric()
    
    # 2. Register Agents with Capability Cards
    orchestrator_card = CapabilityCard(
        agent_id="AGENT-ORCH-001",
        capabilities=["orchestration", "planning"],
        trust_level=TrustLevel.ROOT
    )
    specialist_card = CapabilityCard(
        agent_id="AGENT-SPEC-001",
        capabilities=["data-analysis"],
        trust_level=TrustLevel.VERIFIED
    )
    
    fabric.register_agent(orchestrator_card)
    fabric.register_agent(specialist_card)
    print(f"Registered Agents: {orchestrator_card.agent_id}, {specialist_card.agent_id}")
    
    # 3. Create a Mission Contract
    mission = MissionContract(
        intent="Analyze Q1 financial reports for Apple Inc. and identify risks.",
        constraints=["Use only official SEC filings", "Max budget 50 tokens"],
        risk_level="MEDIUM",
        origin_agent_id="AGENT-ORCH-001"
    )
    mission.sign("private-key-123")
    print(f"\nCreated Mission: {mission.mission_id}")
    print(f"Intent: {mission.intent}")
    
    # 4. Compute Initial Intent Checksum (ICA)
    initial_ic = MetacognitiveICA.compute(mission)
    print(f"Initial IC Checksum: {initial_ic.checksum[:16]}... (Score: {initial_ic.score})")
    
    # 5. Simulate Handoff and Potential Drift
    print("\n--- Simulating Handoff to Specialist ---")
    
    # Specialist modifies the mission slightly (simulated drift)
    specialist_mission = MissionContract(
        intent="Review Apple's Q1 numbers and find some problems.", # Slightly drifted intent
        constraints=mission.constraints,
        risk_level=mission.risk_level,
        parent_mission_id=mission.mission_id,
        origin_agent_id="AGENT-SPEC-001"
    )
    
    current_ic = MetacognitiveICA.compute(specialist_mission)
    drift = MetacognitiveICA.detect_drift(initial_ic, current_ic)
    
    print(f"Current IC Checksum: {current_ic.checksum[:16]}...")
    print(f"Detected Semantic Drift: {drift:.4f}")
    
    # 6. Audit and Policy Check
    if drift > 0.1:
        print("⚠️ ALERT: Significant semantic drift detected!")
    
    is_authorized = fabric.verify_delegation("AGENT-ORCH-001", "AGENT-SPEC-001", specialist_mission)
    print(f"Delegation Authorized: {is_authorized}")
    
    # 7. Log Audit Capsule
    capsule = AuditCapsule(
        mission_id=mission.mission_id,
        agent_id="AGENT-SPEC-001",
        action="HANDOFF_RECEIVED",
        input_ic=initial_ic.checksum,
        output_ic=current_ic.checksum,
        drift_delta=drift,
        rationale="Specialist received mission and prepared for analysis."
    )
    fabric.log_audit(capsule)
    print(f"\nAudit Capsule Created: {capsule.capsule_id}")
    print(f"Rationale: {capsule.rationale}")

if __name__ == "__main__":
    run_demo()
