"""Legacy bridge adapter scaffold for ARIA envelopes."""
from typing import Any, Dict


def legacy_to_aria(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "aria_version": "0.1",
        "channel_id": payload.get("channel_id", "003"),
        "origin_type": payload.get("origin_type", "AGENT"),
        "mission_core": payload.get("goal", ""),
        "constraints": payload.get("constraints", []),
        "context_snapshot": payload.get("context", {}),
        "intent_checksum": payload.get("intent_checksum", ""),
        "chain_depth": payload.get("chain_depth", 0),
        "timestamp_utc": payload.get("timestamp_utc", ""),
    }


def aria_to_legacy(packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "goal": packet.get("mission_core", ""),
        "constraints": packet.get("constraints", []),
        "context": packet.get("context_snapshot", {}),
        "intent_checksum": packet.get("intent_checksum", ""),
        "chain_depth": packet.get("chain_depth", 0),
    }
