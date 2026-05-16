"""Intent Lineage Graph builder for branching/mergeable semantic traces."""
from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class LineageNode:
    node_id: str
    agent_id: str
    chain_depth: int
    state_hash: str


@dataclass
class LineageEdge:
    edge_id: str
    from_node: str
    to_node: str
    similarity: float
    drift_delta: float
    guardrail_mode: str
    profile: str


def _state_hash(payload: Dict[str, Any]) -> str:
    return sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def build_intent_lineage_graph(
    mission_fingerprint: str,
    hops: List[Dict[str, Any]],
    profile: str,
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    prev_node_id = "root"
    nodes.append({"node_id": prev_node_id, "agent_id": "origin", "chain_depth": 0, "state_hash": _state_hash({"m": mission_fingerprint})})

    for idx, hop in enumerate(hops, start=1):
        node_id = f"n{idx}"
        nodes.append(
            {
                "node_id": node_id,
                "agent_id": hop.get("agent_id", f"agent-{idx}"),
                "chain_depth": idx,
                "state_hash": _state_hash(hop),
            }
        )
        edges.append(
            {
                "edge_id": f"e{idx}",
                "from": prev_node_id,
                "to": node_id,
                "similarity": hop.get("similarity", 0.0),
                "drift_delta": hop.get("drift_delta", 1.0),
                "guardrail_mode": hop.get("guardrail_mode", "review"),
                "profile": profile,
            }
        )
        prev_node_id = node_id

    return {
        "graph_id": f"ilg-{mission_fingerprint}",
        "mission_fingerprint": mission_fingerprint,
        "nodes": nodes,
        "edges": edges,
    }
