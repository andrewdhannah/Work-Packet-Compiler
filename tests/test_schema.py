import pytest
from pydantic import ValidationError
from app.schemas import WorkPacket, WorkStep

def test_schema_valid_packet():
    data = {
        "packet_id": "wp_001",
        "objective": "Test",
        "risk_level": "low",
        "requested_permissions": ["read_fixture"],
        "steps": [
            {"step_id": "s1", "action": "read_fixture", "input_ref": "i", "output_ref": "o"}
        ]
    }
    packet = WorkPacket(**data)
    assert packet.packet_id == "wp_001"

def test_schema_missing_required_fields():
    # Missing objective and steps
    data = {"packet_id": "wp_002"}
    with pytest.raises(ValidationError):
        WorkPacket(**data)

def test_schema_invalid_types():
    data = {
        "packet_id": "wp_003",
        "objective": "Test",
        "risk_level": "low",
        "steps": "Not a list"
    }
    with pytest.raises(ValidationError):
        WorkPacket(**data)

def test_step_schema_validation():
    with pytest.raises(ValidationError):
        WorkStep(step_id="s1") # missing action, input_ref, output_ref
