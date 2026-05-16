"""ARIA Legacy Bridge Adapter v2 (Claude handoff completed)."""
from __future__ import annotations

from typing import Any, Dict

from reference.runtime.mission_orchestrator_v2 import ARIAChannel, IntentChecksum, MissionContract


class LegacyBridgeAdapterV2:
    def ingest(self, payload: Any, source_format: str = "raw_string") -> MissionContract:
        raw_text, constraints = self._to_mission_parts(payload, source_format)
        return MissionContract(raw_text=raw_text, constraints=constraints, channel=ARIAChannel.HYBRID_AUTHORIZED).seal()

    def emit(self, result: Dict[str, Any], target_format: str = "raw_string", original_ic: str = "") -> Any:
        drift = None
        if original_ic and result.get("intent_checksum"):
            drift = IntentChecksum.drift_delta(original_ic, result["intent_checksum"])
        if target_format == "mcp_response":
            return {
                "type": "tool_result",
                "content": [{"type": "text", "text": str(result.get("payload"))}],
                "_aria": {"status": result.get("status"), "drift_delta": drift},
            }
        return {"status": result.get("status"), "payload": result.get("payload"), "drift_delta": drift}

    def _to_mission_parts(self, payload: Any, source_format: str):
        if source_format == "openai_tool":
            name = payload.get("name", "unknown")
            args = payload.get("arguments", {})
            return f"{name}: {args}", args
        if source_format == "mcp_request":
            tool = payload.get("tool", "unknown")
            inp = payload.get("input", {})
            return f"{tool}: {inp}", inp
        if isinstance(payload, dict):
            return payload.get("content", str(payload)), payload.get("metadata", {})
        return str(payload), {}
