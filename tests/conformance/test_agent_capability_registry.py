from reference.runtime.agent_registry import AgentCapabilityCard, AgentRegistry


def test_registry_register_and_query():
    r = AgentRegistry()
    c = AgentCapabilityCard(
        agent_id="agent-x",
        agent_type="ExecutionSpecialist",
        aria_version="0.1",
        roles=["code", "reasoning"],
        domains=["finance"],
        extensions=["RFC-012"],
    )
    r.register(c)
    assert r.get("agent-x")["agent_type"] == "ExecutionSpecialist"
    assert len(r.find_by_role("code")) == 1
    assert len(r.find_by_domain("finance")) == 1
