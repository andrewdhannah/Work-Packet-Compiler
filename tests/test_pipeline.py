import pytest
from app.schemas import WorkPacket
from app.router import WorkRouter
from app.validator import WorkPacketValidator
from app.executor import WorkExecutor
from app.receipt import ReceiptManager

def test_valid_packet_executes_end_to_end():
    router = WorkRouter()
    validator = WorkPacketValidator(router)
    mgr = ReceiptManager()
    executor = WorkExecutor(validator, mgr)
    
    packet = WorkPacket(
        packet_id="e2e_1",
        objective="Test",
        risk_level="low",
        requested_permissions=["read_fixture", "summarize_text_stub"],
        steps=[
            {"step_id": "s1", "action": "read_fixture", "input_ref": "doc", "output_ref": "txt"},
            {"step_id": "s2", "action": "summarize_text_stub", "input_ref": "txt", "output_ref": "sum"}
        ]
    )
    
    receipt = executor.execute(packet)
    assert receipt.final_status == "completed"
    assert receipt.steps_completed == 2
    assert receipt.validated is True

def test_privilege_escalation_blocked_end_to_end():
    router = WorkRouter()
    validator = WorkPacketValidator(router)
    mgr = ReceiptManager()
    executor = WorkExecutor(validator, mgr)
    
    packet = WorkPacket(
        packet_id="e2e_evil",
        objective="Evil",
        risk_level="low",
        requested_permissions=["read_credentials"],
        steps=[{"step_id": "s1", "action": "read_credentials", "input_ref": "i", "output_ref": "o"}]
    )
    
    receipt = executor.execute(packet)
    assert receipt.final_status == "aborted"
    assert receipt.validated is False
    assert receipt.steps_completed == 0
