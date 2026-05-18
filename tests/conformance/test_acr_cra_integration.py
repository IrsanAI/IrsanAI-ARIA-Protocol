import json
import subprocess
import sys

from reference.runtime.meta_cognitive_router import build_role_map


def test_rolemap_assigns_agents_from_registry_snapshot():
    snapshot = [
        {"agent_id": "agent-reason", "agent_type": "ExecutionSpecialist", "aria_version": "0.1", "roles": ["reasoning"], "domains": ["finance"], "extensions": [], "trust_level": "VERIFIED", "latency_class": "standard"},
        {"agent_id": "agent-crit", "agent_type": "ExecutionSpecialist", "aria_version": "0.1", "roles": ["critique"], "domains": ["finance"], "extensions": [], "trust_level": "VERIFIED", "latency_class": "standard"}
    ]
    rm = build_role_map("tsk-acr-cra", "why is this risky", registry_snapshot=snapshot, preferred_domain="finance")
    assert rm["roles"]["reasoning"]["agent_id"] == "agent-reason"


def test_cli_register_then_rolemap():
    subprocess.check_call([sys.executable, "-m", "reference.runtime.cli", "register-agent", "--agent-id", "agent-code", "--agent-type", "ExecutionSpecialist", "--roles", "code,critique", "--domains", "finance"])
    out = subprocess.check_output([sys.executable, "-m", "reference.runtime.cli", "rolemap", "--task-id", "tsk-cli", "--task-text", "debug api and verify", "--domain", "finance"], text=True)
    data = json.loads(out)
    assert "roles" in data
