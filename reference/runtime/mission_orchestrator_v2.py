"""ARIA Agent Runtime v2 — Mission Orchestrator (Claude handoff completed)."""
from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class ARIAChannel(str, Enum):
    HUMAN_ORIGIN = "001"
    VERIFIED_HUMAN = "002"
    AGENT_TO_AGENT = "003"
    SYSTEM_AUTONOMOUS = "004"
    HYBRID_AUTHORIZED = "005"
    EMERGENCY_OVERRIDE = "006"
    GOVERNANCE = "007"


class MissionStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DRIFTED = "DRIFTED"
    FAILED = "FAILED"


class IntentChecksum:
    @staticmethod
    def generate(text: str, constraints: Dict[str, Any]) -> str:
        payload = json.dumps({"intent": (text or "").lower().strip(), "constraints": constraints}, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    @staticmethod
    def drift_delta(a: str, b: str) -> float:
        if a == b:
            return 0.0
        oa = bin(int(a, 16))[2:].zfill(256)
        ob = bin(int(b, 16))[2:].zfill(256)
        return sum(x != y for x, y in zip(oa, ob)) / 256.0


@dataclass
class MissionContract:
    mission_id: str = field(default_factory=lambda: f"MSN-{uuid.uuid4().hex[:10].upper()}")
    raw_text: str = ""
    constraints: Dict[str, Any] = field(default_factory=dict)
    intent_checksum: str = ""
    channel: ARIAChannel = ARIAChannel.HUMAN_ORIGIN
    status: MissionStatus = MissionStatus.PENDING

    def seal(self) -> "MissionContract":
        self.intent_checksum = IntentChecksum.generate(self.raw_text, self.constraints)
        return self


@dataclass
class ContextFrame:
    known_facts: Dict[str, Any] = field(default_factory=dict)
    chain_depth: int = 0
    parent_mission_id: str | None = None


class MissionOrchestratorV2:
    DRIFT_THRESHOLD = 0.15

    def __init__(self):
        self.specialists: List[Any] = []
        self.accountability: List[Dict[str, Any]] = []

    def register_specialist(self, specialist: Any) -> None:
        self.specialists.append(specialist)

    def receive_mission(self, raw_text: str, constraints: Dict[str, Any] | None = None, channel: ARIAChannel = ARIAChannel.HUMAN_ORIGIN) -> MissionContract:
        m = MissionContract(raw_text=raw_text, constraints=constraints or {}, channel=channel).seal()
        m.status = MissionStatus.ACTIVE
        self._record(m.mission_id, "MISSION_RECEIVED", f"ICA={m.intent_checksum[:16]}…", 0)
        return m

    def execute_chain(self, mission: MissionContract) -> List[Dict[str, Any]]:
        if not self.specialists:
            mission.status = MissionStatus.FAILED
            return []
        subtask = {
            "label": f"subtask-1:{mission.mission_id}",
            "instruction": mission.raw_text,
            "constraints": mission.constraints,
            "parent_ic": mission.intent_checksum,
        }
        ctx = ContextFrame(chain_depth=1, parent_mission_id=mission.mission_id)
        results = []
        for specialist in self.specialists:
            result = specialist.execute(subtask=subtask, context=ctx, parent_ic=mission.intent_checksum)
            results.append(result)
            delta = IntentChecksum.drift_delta(mission.intent_checksum, result.get("intent_checksum", mission.intent_checksum))
            self._record(mission.mission_id, "SEMANTIC_ACK", f"delta={delta:.3f}", ctx.chain_depth)
            if delta > self.DRIFT_THRESHOLD:
                mission.status = MissionStatus.DRIFTED
        if mission.status != MissionStatus.DRIFTED:
            mission.status = MissionStatus.COMPLETED
        return results

    def _record(self, mission_id: str, action: str, rationale: str, chain_depth: int):
        self.accountability.append({
            "ts": time.time(), "mission_id": mission_id, "action": action, "rationale": rationale, "chain_depth": chain_depth
        })
