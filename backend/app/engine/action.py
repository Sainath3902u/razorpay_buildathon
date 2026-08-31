def execute_action(
    action: str,
    probability: float,
    recovery_eligible: bool = True,
):
    """
    Simulate execution of a revenue recovery action.

    IMPORTANT:
    This does not perform a real payment.

    The recovery_eligible flag represents synthetic
    ground truth generated for the buildathon.
    """

    recoverable_actions = {
        "WAIT_AND_RETRY",
        "RETRY_PAYMENT",
    }

    # ---------------------------------------------------------
    # Non-recovery actions
    # ---------------------------------------------------------

    if action not in recoverable_actions:

        return {
            "action": action,
            "status": "EXECUTED",
            "success": False,
            "recovered": False,
            "message": (
                "Action executed, but this action "
                "does not directly recover payment."
            )
        }

    # ---------------------------------------------------------
    # Ground-truth recovery check
    # ---------------------------------------------------------

    if not recovery_eligible:

        return {
            "action": action,
            "status": "FAILED",
            "success": False,
            "recovered": False,
            "message": (
                "Recovery was not eligible for "
                "this synthetic scenario."
            )
        }

    # ---------------------------------------------------------
    # Eligible recovery
    # ---------------------------------------------------------

    return {
        "action": action,
        "status": "SUCCESS",
        "success": True,
        "recovered": True,
        "message": (
            "Payment successfully recovered "
            "through the simulated recovery action."
        )
    }