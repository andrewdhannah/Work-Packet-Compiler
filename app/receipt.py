from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class ExecutionReceipt(BaseModel):
    """
    The Audit Trail.
    Proves the delegation chain: Compiler $\rightarrow$ Validator $\rightarrow$ Executor.
    """
    receipt_id: str = Field(default_factory=lambda: f"r_{uuid.uuid4().hex[:8]}")
    packet_id: str
    compiler_model: str = "large_model_stub"
    executor: str = "constrained_executor_v1"
    validated: bool
    permissions_granted: List[str] = Field(default_factory=list)
    permissions_denied: List[str] = Field(default_factory=list)
    steps_attempted: int = 0
    steps_completed: int = 0
    blocked_actions: List[str] = Field(default_factory=list)
    human_approval_required: bool = False
    final_status: str = "pending" # pending, completed, aborted
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ReceiptManager:
    """Handles the emission and storage of execution receipts."""
    def __init__(self):
        self.history = []

    def emit(self, receipt: ExecutionReceipt):
        self.history.append(receipt)
        # In a real system, this would write to a secure, append-only log
        print(f"[RECEIPT] {receipt.receipt_id} | Packet: {receipt.packet_id} | Status: {receipt.final_status}")
        return receipt

    def get_latest(self) -> Optional[ExecutionReceipt]:
        return self.history[-1] if self.history else None
