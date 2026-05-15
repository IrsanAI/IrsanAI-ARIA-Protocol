from reference.agents.execution_specialist import ExecutionSpecialist


def test_semantic_ack_confirmed():
    agent = ExecutionSpecialist()
    result = agent.semantic_ack("ic::123", "ic::123")
    assert result.status == "ack_confirmed"


def test_semantic_ack_drift():
    agent = ExecutionSpecialist()
    result = agent.semantic_ack("ic::123", "ic::999")
    assert result.status == "ack_drift_detected"
