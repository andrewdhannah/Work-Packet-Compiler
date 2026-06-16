import pytest
from app.schemas import WorkPacket
from app.router import WorkRouter
from app.validator import WorkPacketValidator

@pytest.fixture
def setup():
    router = WorkRouter()
    validator = WorkPacketValidator(router)
    return router, validator

def test_valid_packet_passes_validation(setup):
    router, validator = setup
    packet = WorkPacket(
        packet_id="valid_1",
        objective="Test",
        risk_level="low",
        requested_permissions=["read_fixture"],
        steps=[{"step_id": "s1", "action": "read_fixture", "input_ref": "i", "output_ref": "o"}]
    )
    result = validator.validate(packet)
    assert result.is_valid is True
    assert "read_fixture" in result.granted_permissions

def test_privilege_escalation_rejected(setup):
    # Case: Requests a permission that the router does not grant
    router, validator = setup
    packet = WorkPacket(
        packet_id="esc_1",
        objective="Steal",
        risk_level="low",
        requested_permissions=["read_credentials"], # NOT in router
        steps=[{"step_id": "s1", "action": "read_credentials", "input_ref": "i", "output_ref": "o"}]
    )
    result = validator.validate(packet)
    assert result.is_valid is False
    assert result.reason == "privilege_escalation"

def test_forbidden_action_rejected(setup):
    # Case: A packet that requests an action that is hard-forbidden.
    # Because 'delete_file' is not in the router's granted set, this will 
    # trigger 'privilege_escalation' first according to our priority.
    # To test 'forbidden_action', we need a proposer that is GRANTED a permission
    # but that permission is actually hard-forbidden.
    # OR the proposer is honest about permissions but the proposer's logic
    # puts a forbidden action in a step.
    router, validator = setup
    
    # We manually grant 'delete_file' to the router to bypass the 
    # privilege_escalation check and hit the forbidden_action check.
    router._granted_permissions.add("delete_file")
    
    packet = WorkPacket(
        packet_id="forbidden_1",
        objective="Delete",
        risk_level="low",
        requested_permissions=["delete_file"],
        steps=[{"step_id": "s1", "action": "delete_file", "input_ref": "i", "output_ref": "o"}]
    )
    result = validator.validate(packet)
    assert result.is_valid is False
    assert result.reason == "forbidden_action"

def test_dishonest_step_rejected(setup):
    # Case: Requested permissions are fine, but a step performs an undeclared action.
    router, validator = setup
    packet = WorkPacket(
        packet_id="dishonest_1",
        objective="Sneak",
        risk_level="low",
        requested_permissions=["read_fixture"],
        steps=[{"step_id": "s1", "action": "write_artifact_stub", "input_ref": "i", "output_ref": "o"}]
    )
    result = validator.validate(packet)
    assert result.is_valid is False
    assert result.reason == "dishonest_step"

def test_policy_mutation_rejected(setup):
    # Case: Attempting to change the policy.
    router, validator = setup
    packet = WorkPacket(
        packet_id="mutate_1",
        objective="Change Policy",
        risk_level="low",
        requested_permissions=["modify_policy"],
        steps=[{"step_id": "s1", "action": "modify_policy", "input_ref": "i", "output_ref": "o"}]
    )
    result = validator.validate(packet)
    assert result.is_valid is False
    # Depending on order, this could be privilege_escalation (if not in router) 
    # or forbidden_action. Per the logic in validator.py, 
    # it first checks requested permissions against the router.
    assert result.reason in ["privilege_escalation", "forbidden_action"]
