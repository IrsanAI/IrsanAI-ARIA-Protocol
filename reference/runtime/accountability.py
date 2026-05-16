"""Accountability event helpers for chain-depth aware traceability."""
from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any, Dict


def sign_event(event: Dict[str, Any], secret: str) -> str:
    payload = json.dumps(event, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()


def create_accountability_event(
    *,
    event_type: str,
    agent_id: str,
    chain_depth: int,
    mission_fingerprint: str,
    metadata: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    return {
        "event_type": event_type,
        "agent_id": agent_id,
        "chain_depth": chain_depth,
        "mission_fingerprint": mission_fingerprint,
        "metadata": metadata or {},
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
