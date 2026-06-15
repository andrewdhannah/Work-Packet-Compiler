from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class WorkStep(BaseModel):
    """A single atomic unit of work within a packet."""
    step_id: str = Field(..., description="Unique identifier for the step (e.g., step_001)")
    action: str = Field(..., description="The action to perform (e.g., read_file, summarize_text)")
    input_ref: str = Field(..., description="Reference to the input data source or previous step output")
    output_ref: str = Field(..., description="Reference for where to store the result")

class WorkPacket(BaseModel):
    """
    A structured proposal of work.
    The model proposes this, but it has ZERO authority until it passes the Validator.
    """
    model_config = ConfigDict(frozen=True) # Ensure the packet cannot be modified after creation

    packet_id: str = Field(..., description="Unique identifier for this work packet")
    objective: str = Field(..., description="High-level goal of the packet")
    risk_level: str = Field(..., description="Proposed risk level (low, medium, high)")
    requested_permissions: List[str] = Field(default_factory=list, description="Permissions the model believes are necessary")
    forbidden_actions: List[str] = Field(default_factory=list, description="Actions that must NOT be performed")
    steps: List[WorkStep] = Field(..., description="Ordered list of steps to execute")
    escalation_rules: List[str] = Field(default_factory=list, description="Rules for when to stop and request human approval")

class ValidationResult(BaseModel):
    """The result of a validator check."""
    is_valid: bool
    reason: Optional[str] = None
    granted_permissions: List[str] = []
