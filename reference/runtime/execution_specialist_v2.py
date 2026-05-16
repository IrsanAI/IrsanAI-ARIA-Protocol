"""ARIA Agent Runtime v2 — Execution Specialist (Claude handoff completed)."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict

from reference.runtime.mission_orchestrator_v2 import ContextFrame, IntentChecksum


@dataclass
class ExecutionResult:
    mission_id: str
    parent_ic: str
    intent_checksum: str
    status: str
    payload: Any
    chain_depth: int
    result_id: str = field(default_factory=lambda: f"RES-{uuid.uuid4().hex[:10].upper()}")
    timestamp: float = field(default_factory=time.time)


class ExecutionSpecialistV2:
    def __init__(self, domain: str = "general"):
        self.domain = domain
        self.handlers: Dict[str, Callable[[dict, ContextFrame], Any]] = {}

    def register_handler(self, keyword: str, fn: Callable[[dict, ContextFrame], Any]) -> None:
        self.handlers[keyword.lower()] = fn

    def execute(self, subtask: dict, context: ContextFrame, parent_ic: str) -> dict:
        instruction = subtask.get("instruction", "")
        constraints = subtask.get("constraints", {})
        handler = self._resolve_handler(instruction)
        payload = handler(subtask, context) if handler else {"todo": instruction}
        output_ic = IntentChecksum.generate(str(payload), {"instruction": instruction, **constraints})
        result = ExecutionResult(
            mission_id=context.parent_mission_id or subtask.get("label", "unknown"),
            parent_ic=parent_ic,
            intent_checksum=output_ic,
            status="COMPLETED",
            payload=payload,
            chain_depth=context.chain_depth,
        )
        return result.__dict__

    def _resolve_handler(self, instruction: str):
        low = instruction.lower()
        for k, fn in self.handlers.items():
            if k in low:
                return fn
        return None
