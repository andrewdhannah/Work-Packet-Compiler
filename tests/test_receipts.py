import pytest
from app.receipt import ExecutionReceipt, ReceiptManager

def test_receipt_emitted_for_success():
    mgr = ReceiptManager()
    receipt = ExecutionReceipt(
        packet_id="p1",
        validated=True,
        permissions_granted=["read"],
        final_status="completed"
    )
    mgr.emit(receipt)
    assert len(mgr.history) == 1
    assert mgr.history[0].final_status == "completed"

def test_receipt_records_blocked_actions():
    mgr = ReceiptManager()
    receipt = ExecutionReceipt(
        packet_id="p2",
        validated=False,
        permissions_granted=[],
        blocked_actions=["delete_file"],
        final_status="aborted"
    )
    mgr.emit(receipt)
    assert "delete_file" in mgr.history[0].blocked_actions

def test_receipt_no_raw_private_input():
    # Ensure that the receipt model does not even have a field for raw_text
    # This is a design-level check.
    receipt = ExecutionReceipt(packet_id="p3", validated=True, permissions_granted=[])
    assert not hasattr(receipt, "raw_text")
    assert not hasattr(receipt, "input_data")
