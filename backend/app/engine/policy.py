def check_policy(
    action: str,
    retry_count: int = 0,
    payment_method_valid: bool = True,
    customer_contact_allowed: bool = True
):

    # ------------------------------------------
    # Retry limits
    # ------------------------------------------

    if action in {
        "RETRY_PAYMENT",
        "WAIT_AND_RETRY"
    }:

        if retry_count >= 2:

            return {
                "allowed": False,
                "reason":
                    "Maximum retry limit reached."
            }

        if not payment_method_valid:

            return {
                "allowed": False,
                "reason":
                    "Payment method is invalid or expired."
            }

    # ------------------------------------------
    # Communication policy
    # ------------------------------------------

    if action in {
        "SEND_PAYMENT_LINK",
        "SEND_REMINDER"
    }:

        if not customer_contact_allowed:

            return {
                "allowed": False,
                "reason":
                    "Customer contact is not permitted."
            }

    return {
        "allowed": True,
        "reason": "Action complies with policy."
    }