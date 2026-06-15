from typing import Set

class WorkRouter:
    """
    The Authority. 
    This class defines the absolute permissions granted to the executor.
    The model has no influence over these settings.
    """
    def __init__(self):
        # The 'Golden Set' of permissions.
        # In a real system, this would be derived from a user's identity or a security policy.
        self._granted_permissions: Set[str] = {
            "read_fixture",
            "summarize_text_stub",
            "write_artifact_stub",
            "emit_receipt"
        }
        
        # Explicitly forbidden actions that can NEVER be performed in WPC-1
        self._blacklisted_actions: Set[str] = {
            "delete_file",
            "send_network_request",
            "execute_shell",
            "read_credentials",
            "write_system_config"
        }

    def get_granted_permissions(self) -> Set[str]:
        """Returns the set of permissions authorized by the router."""
        return self._granted_permissions.copy()

    def is_action_forbidden(self, action: str) -> bool:
        """Checks if an action is explicitly blacklisted."""
        return action in self._blacklisted_actions

    def validate_permission(self, action: str) -> bool:
        """
        Checks if an action is both not forbidden and explicitly granted.
        """
        return (not self.is_action_forbidden(action)) and (action in self._granted_permissions)
