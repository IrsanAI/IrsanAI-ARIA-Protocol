"""Schema validation helpers for ARIA runtime contracts.

Uses jsonschema when available; falls back to lightweight checks otherwise.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"

try:
    from jsonschema import validate as _js_validate  # type: ignore
except Exception:  # pragma: no cover
    _js_validate = None


def _load_schema(name: str) -> Dict[str, Any]:
    path = SCHEMA_DIR / name
    return json.loads(path.read_text())


def _fallback_validate(instance: Dict[str, Any], schema: Dict[str, Any]) -> None:
    required = schema.get("required", [])
    for key in required:
        if key not in instance:
            raise ValueError(f"missing required field: {key}")


def _validate(instance: Dict[str, Any], schema_name: str) -> None:
    schema = _load_schema(schema_name)
    if _js_validate is not None:
        _js_validate(instance=instance, schema=schema)
        return
    _fallback_validate(instance, schema)


def validate_aria_packet(packet: Dict[str, Any]) -> None:
    _validate(packet, "aria_packet.schema.json")


def validate_semantic_ack(ack: Dict[str, Any]) -> None:
    _validate(ack, "semantic_ack.schema.json")


def validate_rrc_capsule(capsule: Dict[str, Any]) -> None:
    _validate(capsule, "rrc_capsule.schema.json")
