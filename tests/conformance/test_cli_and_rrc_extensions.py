import json
import subprocess
import sys
from pathlib import Path


def test_cli_ack_command():
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "reference.runtime.cli",
            "ack",
            "--received",
            "ic::alpha",
            "--recomputed",
            "ic::alpha",
            "--profile",
            "balanced",
        ],
        text=True,
    )
    data = json.loads(out)
    assert data["status"] == "ack_confirmed"


def test_cli_validate_packet(tmp_path: Path):
    packet = {
        "aria_version": "0.1",
        "channel_id": "003",
        "origin_type": "AGENT",
        "mission_core": "execute order",
        "constraints": ["max 10k"],
        "context_snapshot": {},
        "intent_checksum": "ic::123",
        "chain_depth": 0,
        "timestamp_utc": "2026-05-15T00:00:00Z",
    }
    f = tmp_path / "packet.json"
    f.write_text(json.dumps(packet))
    out = subprocess.check_output(
        [sys.executable, "-m", "reference.runtime.cli", "validate", "packet", str(f)],
        text=True,
    ).strip()
    assert out == "valid"
