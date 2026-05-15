"""Core runtime interfaces for ARIA reference implementations."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Protocol

AckStatus = Literal["ack_confirmed", "ack_drift_detected", "retransmit_requested", "mission_escalated"]


@dataclass
class AriaPacket:
    aria_version: str
    channel_id: str
    origin_type: str
    mission_core: str
    constraints: List[str] = field(default_factory=list)
    context_snapshot: Dict[str, Any] = field(default_factory=dict)
    intent_checksum: str = ""
    chain_depth: int = 0
    timestamp_utc: str = ""


@dataclass
class SemanticAck:
    status: AckStatus
    similarity_score: float
    threshold_profile: Literal["strict", "balanced", "exploratory"] = "balanced"


class AriaRuntime(Protocol):
    """Minimum runtime contract (aligned with ARIA-AGENT-RFC-001)."""

    def ingest_mission(self, packet: AriaPacket) -> AriaPacket:
        ...

    def compute_intent_checksum(self, packet: AriaPacket) -> str:
        ...

    def semantic_ack(self, received_checksum: str, recomputed_checksum: str) -> SemanticAck:
        ...

    def emit_accountability_event(self, event: Dict[str, Any]) -> None:
        ...

    def handoff(self, packet: AriaPacket) -> AriaPacket:
        ...
