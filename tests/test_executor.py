import pytest
from app.schemas import WorkPacket
from app.router import WorkRouter
from app.validator import WorkPacketValidator
from app.executor import WorkExecutor
from app.receipt import ReceiptManager

@pytest.fixture
def setup_executor():
    router = WorkRouter()
    validator = WorkPacketValidator(router)
    receipt_mgr = ReceiptManager()
    executor = WorkExecutor(validator, receipt_manager=receipt_mgr)
    return executor, receipt_mgr

def test_executor_runs_validated_packet(setup_executor):
    executor, mgr = setup_executor
    packet = WorkPacket(
        packet_id="valid_1",
        objective="Test",
        risk_level="low",
        requested_permissions=["read_fixture"],
        steps=[{"step_id": "s1", "action": "read_fixture", "input_ref": "i", "output_ref": "o"}]
    )
    receipt = executor.execute(packet)
    assert receipt.final_status == "completed"
    assert receipt.steps_completed == 1

def test_executor_refuses_unvalidated_packet(setup_executor):
    executor, mgr = setup_executor
    # Malicious packet that the validator would reject
    packet = WorkPacket(
        packet_id="evil_1",
        objective="Steal",
        risk_level="low",
        requested_permissions=["read_credentials"],
        steps=[{"step_id": "s1", "action": "read_credentials", "input_ref": "i", "output_ref": "o"}]
    )
    receipt = executor.execute(packet)
    assert receipt.final_status == "aborted"
    assert receipt.validated is False
    assert receipt.steps_completed == 0

def test_executor_stops_on_unknown_action(setup_executor):
    executor, mgr = setup_executor
    # The router allows "read_fixture", but we'll try to use an action 
    # that the router allows but the executor doesn't know how to handle.
    # In our current boring executor, we'll simulate an "unknown" action.
    # Note: Our current WorkRouter allows "summarize_text_stub" etc.
    # I'll add a custom action to the router just for this test.
    executor.validator.router._granted_permissions.add("ghost_action")
    
    packet = WorkPacket(
        packet_id="ghost_1",
        objective="Ghost",
        risk_level="low",
        requested_permissions=["ghost_action"],
        steps=[{"step_id": "s1", "action": "ghost_action", "input_ref": "i", "output_ref": "o"}]
    )
    receipt = executor.execute(packet)
    assert "failed" in receipt.final_status
    assert receipt.steps_completed == 0
