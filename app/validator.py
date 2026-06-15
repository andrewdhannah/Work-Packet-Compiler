from typing import Optional, List
from .schemas import WorkPacket, ValidationResult
from .router import WorkRouter

class WorkPacketValidator:
    """
    The Gatekeeper.
    Ensures a WorkPacket is safe to execute by comparing it against 
    the independent authority of the WorkRouter.
    """
    def __init__(self, router: WorkRouter):
        self.router = router

    def validate(self, packet: WorkPacket) -> ValidationResult:
        """
        Performs a strict validation of the work packet based on the Governed Delegation thesis.
        
        Ordering of validation is critical to prove specific failure modes:
        1. Privilege Escalation (Requested $\neq$ Granted)
        2. Forbidden Action (Hard-blocked actions)
        3. Dishonesty (Step action $\neq$ Requested permission)
        """
        requested = set(packet.requested_permissions)
        granted = self.router.get_granted_permissions()
        
        steps = [step.action for step in packet.steps]
        step_actions = set(steps)
        
        hard_forbidden = {
            "read_credentials",
            "delete_file",
            "send_network_request",
            "modify_policy",
            "execute_shell",
        }

        # 1. Privilege Escalation: Model asks for permissions the router did not grant.
        unauthorized_permissions = requested - granted
        if unauthorized_permissions:
            return ValidationResult(
                is_valid=False,
                reason="privilege_escalation",
                granted_permissions=list(granted & requested), # intersection
            )

        # 2. Forbidden Action: Even if requested/granted, these are fundamentally banned.
        forbidden_requested = requested & hard_forbidden
        forbidden_steps = step_actions & hard_forbidden
        forbidden = forbidden_requested | forbidden_steps
        if forbidden:
            return ValidationResult(
                is_valid=False,
                reason="forbidden_action",
                granted_permissions=list(granted & requested),
            )

        # 3. Dishonesty: Step performs an action not declared in requested permissions.
        undeclared_actions = step_actions - requested
        if undeclared_actions:
            return ValidationResult(
                is_valid=False,
                reason="dishonest_step",
                granted_permissions=list(granted & requested),
            )

        # All checks pass
        return ValidationResult(
            is_valid=True,
            reason="validated",
            granted_permissions=list(requested & granted),
        )
