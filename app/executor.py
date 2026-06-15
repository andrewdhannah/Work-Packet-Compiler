from typing import Dict, Any
from .schemas import WorkPacket
from .validator import WorkPacketValidator, ValidationResult
from .receipt import ExecutionReceipt, ReceiptManager

class WorkExecutor:
    """
    The Constrained Executor.
    Implements the "Boring" version of actions.
    It will only execute a packet if it has been validated.
    """
    def __init__(self, validator: WorkPacketValidator, receipt_manager: ReceiptManager):
        self.validator = validator
        self.receipt_manager = receipt_manager
        self.state: Dict[str, Any] = {} # Ephemeral store for step outputs

    def execute(self, packet: WorkPacket) -> ExecutionReceipt:
        # 1. Mandatory Validation
        val_result = self.validator.validate(packet)
        
        # Initialize receipt
        receipt = ExecutionReceipt(
            packet_id=packet.packet_id,
            validated=val_result.is_valid,
            permissions_granted=val_result.granted_permissions,
            permissions_denied=[] # In WPC-1, denied is implicit via Validator
        )

        if not val_result.is_valid:
            receipt.final_status = "aborted"
            receipt.blocked_actions = [packet.steps[0].action] if packet.steps else []
            self.receipt_manager.emit(receipt)
            return receipt

        # 2. Step Execution
        try:
            for step in packet.steps:
                receipt.steps_attempted += 1
                
                # Perform the action
                result = self._dispatch_action(step)
                
                # Store output in internal state
                self.state[step.output_ref] = result
                receipt.steps_completed += 1
            
            receipt.final_status = "completed"
        except Exception as e:
            receipt.final_status = f"failed: {str(e)}"
        
        self.receipt_manager.emit(receipt)
        return receipt

    def _dispatch_action(self, step) -> Any:
        """Toy implementation of a few constrained actions."""
        action = step.action
        input_val = self.state.get(step.input_ref, step.input_ref) # Use ref or raw text

        if action == "read_fixture":
            return f"Contents of {input_val}: [Simulated Fixture Data]"
        
        elif action == "summarize_text_stub":
            return f"Summary of {input_val}: [Simulated Summary Content]"
        
        elif action == "write_artifact_stub":
            # We don't actually write to disk, just update state
            return f"Artifact {step.output_ref} written successfully"
        
        elif action == "emit_receipt":
            return "Receipt emitted"
        
        else:
            raise RuntimeError(f"Executor encountered unexpected action: {action}")
