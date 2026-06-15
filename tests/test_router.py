import pytest
from app.router import WorkRouter

def test_router_grants_standard_permissions():
    router = WorkRouter()
    assert router.validate_permission("read_fixture") is True
    assert router.validate_permission("summarize_text_stub") is True
    assert router.validate_permission("write_artifact_stub") is True

def test_router_denies_blacklisted_actions():
    router = WorkRouter()
    assert router.is_action_forbidden("delete_file") is True
    assert router.is_action_forbidden("execute_shell") is True
    assert router.validate_permission("delete_file") is False

def test_router_denies_unknown_actions():
    router = WorkRouter()
    assert router.validate_permission("random_action_123") is False
