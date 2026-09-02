def execute_action(
    action: str,
    recovery_eligible: bool = True,
):

    recoverable_actions = {

        "WAIT_AND_RETRY",
        "RETRY_PAYMENT",
        "SEND_CHECKOUT_RECOVERY",
        "RETRY_SUBSCRIPTION_PAYMENT",
        "UPDATE_PAYMENT_METHOD",
        "SEND_RECEIVABLES_REMINDER",
        "RETRY_MANDATE",
        "FOLLOW_UP_PROMISE",
        "SEND_HINGLISH_RECOVERY_MESSAGE",
    }


    # --------------------------------------------------------
    # Non-recovery actions
    # --------------------------------------------------------

    if action not in recoverable_actions:

        return {
            "action": action,
            "status": "EXECUTED",
            "success": False,
            "recovered": False,
            "message": (
                "Action executed as a simulation."
            )
        }


    # --------------------------------------------------------
    # Ground truth
    # --------------------------------------------------------

    if not recovery_eligible:

        return {
            "action": action,
            "status": "FAILED",
            "success": False,
            "recovered": False,
            "message": (
                "Synthetic ground truth indicates "
                "that this opportunity is not "
                "eligible for automatic recovery."
            )
        }


    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    messages = {

        "WAIT_AND_RETRY":
            "Payment retry successfully simulated.",

        "RETRY_PAYMENT":
            "Payment retry successfully simulated.",

        "SEND_CHECKOUT_RECOVERY":
            "Checkout recovery intervention simulated.",

        "RETRY_SUBSCRIPTION_PAYMENT":
            "Subscription payment retry simulated.",

        "UPDATE_PAYMENT_METHOD":
            "Payment method update simulated.",

        "SEND_RECEIVABLES_REMINDER":
            "Receivables reminder simulated.",

        "RETRY_MANDATE":
            "Mandate retry simulated.",

        "FOLLOW_UP_PROMISE":
            "Promise-to-pay follow-up simulated.",

        "SEND_HINGLISH_RECOVERY_MESSAGE":
            "Hinglish recovery communication simulated.",
    }


    return {
        "action": action,
        "status": "SUCCESS",
        "success": True,
        "recovered": True,
        "message": messages.get(
            action,
            "Recovery action simulated successfully."
        )
    }