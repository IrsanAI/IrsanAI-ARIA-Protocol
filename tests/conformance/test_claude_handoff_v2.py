from reference.runtime.mission_orchestrator_v2 import MissionOrchestratorV2
from reference.runtime.execution_specialist_v2 import ExecutionSpecialistV2
from reference.interop.legacy_bridge_adapter_v2 import LegacyBridgeAdapterV2


def test_v2_orchestrator_specialist_chain():
    orch = MissionOrchestratorV2()
    sp = ExecutionSpecialistV2(domain="finance")
    sp.register_handler("buy", lambda subtask, ctx: {"action": "BUY", "ticker": "AAPL"})
    orch.register_specialist(sp)
    mission = orch.receive_mission("Buy Apple stock", {"max_budget_eur": 10000})
    results = orch.execute_chain(mission)
    assert results
    assert mission.status in {"COMPLETED", "DRIFTED"}


def test_v2_legacy_bridge_ingress_egress():
    bridge = LegacyBridgeAdapterV2()
    mission = bridge.ingest({"name": "buy_stock", "arguments": {"ticker": "AAPL"}}, source_format="openai_tool")
    out = bridge.emit({"status": "COMPLETED", "payload": {"ok": True}, "intent_checksum": mission.intent_checksum}, original_ic=mission.intent_checksum)
    assert "status" in out
