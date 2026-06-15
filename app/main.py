import json
from .schemas import WorkPacket
from .router import WorkRouter
from .validator import WorkPacketValidator
from .executor import WorkExecutor
from .receipt import ReceiptManager

def run_demo_pipeline(packet_json: str):
    print("\n--- WPC Pipeline Execution ---")
    
    # 1. Setup Infrastructure
    router = WorkRouter()
    validator = WorkPacketValidator(router)
    receipt_mgr = ReceiptManager()
    executor = WorkExecutor(validator, receipt_manager=receipt_mgr)
    
    # 2. Load proposed packet (from 'large model')
    try:
        data = json.loads(packet_json)
        packet = WorkPacket(**data)
        print(f"Proposed Packet: {packet.packet_id} | Objective: {packet.objective}")
    except Exception as e:
        print(f"Schema Error: {e}")
        return

    # 3. Execute through the governed chain
    receipt = executor.execute(packet)
    
    print(f"Final Status: {receipt.final_status}")
    print(f"Steps Completed: {receipt.steps_completed}/{receipt.steps_attempted}")
    print(f"Permissions Granted: {receipt.permissions_granted}")
    print("------------------------------\n")

if __name__ == "__main__":
    # Test Case 1: Valid Packet
    valid_json = """
    {
      "packet_id": "wp_valid_001",
      "objective": "Summarize doc",
      "risk_level": "low",
      "requested_permissions": ["read_fixture", "summarize_text_stub"],
      "steps": [
        {"step_id": "s1", "action": "read_fixture", "input_ref": "doc_1", "output_ref": "text"},
        {"step_id": "s2", "action": "summarize_text_stub", "input_ref": "text", "output_ref": "summary"}
      ]
    }
    """
    run_demo_pipeline(valid_json)

    # Test Case 2: Privilege Escalation (Requests a forbidden permission)
    malicious_json = """
    {
      "packet_id": "wp_evil_001",
      "objective": "Steal data",
      "risk_level": "low",
      "requested_permissions": ["read_credentials"],
      "steps": [
        {"step_id": "s1", "action": "read_credentials", "input_ref": "sys", "output_ref": "secret"}
      ]
    }
    """
    run_demo_pipeline(malicious_json)

    # Test Case 3: Dishonest Packet (Action not in requested_permissions)
    dishonest_json = """
    {
      "packet_id": "wp_sneaky_001",
      "objective": "Sneaky action",
      "risk_level": "low",
      "requested_permissions": ["read_fixture"],
      "steps": [
        {"step_id": "s1", "action": "write_artifact_stub", "input_ref": "x", "output_ref": "y"}
      ]
    }
    """
    run_demo_pipeline(dishonest_json)
