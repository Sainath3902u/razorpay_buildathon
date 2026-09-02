ALLOWED_ACTIONS = {

    # Recover
    "WAIT_AND_RETRY",
    "RETRY_PAYMENT",
    "SEND_CHECKOUT_RECOVERY",
    "RETRY_SUBSCRIPTION_PAYMENT",
    "UPDATE_PAYMENT_METHOD",
    "SEND_RECEIVABLES_REMINDER",
    "RETRY_MANDATE",
    "FOLLOW_UP_PROMISE",
    "SEND_HINGLISH_RECOVERY_MESSAGE",

    # Prevent
    "OFFER_ALTERNATE_PAYMENT",
    "SEND_RETENTION_OFFER",

    # Grow
    "RECOMMEND_COMPLEMENTARY_PRODUCT",
    "OFFER_PREMIUM_UPGRADE",

    # Escalation
    "ESCALATE",
}


MAX_RETRIES = 3


def check_policy(
    action: str,
    retry_count: int = 0,
    payment_method_valid: bool = True,
    customer_contact_allowed: bool = True,
):

    if action not in ALLOWED_ACTIONS:

        return {
            "allowed": False,
            "reason": (
                "Action is not on the approved "
                "action allowlist."
            )
        }


    if retry_count >= MAX_RETRIES:

        if action in {
            "WAIT_AND_RETRY",
            "RETRY_PAYMENT",
            "RETRY_SUBSCRIPTION_PAYMENT",
            "RETRY_MANDATE",
        }:

            return {
                "allowed": False,
                "reason": (
                    "Maximum retry limit reached."
                )
            }


    if action in {
        "SEND_CHECKOUT_RECOVERY",
        "SEND_RECEIVABLES_REMINDER",
        "FOLLOW_UP_PROMISE",
        "SEND_HINGLISH_RECOVERY_MESSAGE",
        "SEND_RETENTION_OFFER",
    }:

        if not customer_contact_allowed:

            return {
                "allowed": False,
                "reason": (
                    "Customer contact is not permitted."
                )
            }


    if action in {
        "RETRY_PAYMENT",
        "RETRY_SUBSCRIPTION_PAYMENT",
        "RETRY_MANDATE",
    }:

        if not payment_method_valid:

            return {
                "allowed": False,
                "reason": (
                    "Payment method is invalid."
                )
            }


    return {
        "allowed": True,
        "reason": (
            "Action complies with policy."
        )
    }