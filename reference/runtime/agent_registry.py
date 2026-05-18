"""Agent Capability Registry (ACR) runtime helper."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class AgentCapabilityCard:
    agent_id: str
    agent_type: str
    aria_version: str
    roles: List[str]
    domains: List[str]
    extensions: List[str]
    trust_level: str = "VERIFIED"
    latency_class: str = "standard"


class AgentRegistry:
    def __init__(self):
        self._cards: Dict[str, AgentCapabilityCard] = {}

    def register(self, card: AgentCapabilityCard) -> None:
        self._cards[card.agent_id] = card

    def get(self, agent_id: str) -> Dict:
        return asdict(self._cards[agent_id])

    def find_by_role(self, role: str) -> List[Dict]:
        return [asdict(c) for c in self._cards.values() if role in c.roles]

    def find_by_domain(self, domain: str) -> List[Dict]:
        return [asdict(c) for c in self._cards.values() if domain in c.domains]

    def snapshot(self) -> List[Dict]:
        return [asdict(c) for c in self._cards.values()]
