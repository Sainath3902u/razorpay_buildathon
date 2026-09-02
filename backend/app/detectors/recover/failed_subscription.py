import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


def detect_failed_subscriptions(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "subscription_id",
        "subscription_status",
        "subscription_amount",
    ]

    missing = [
        x for x in required
        if x not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    data = df.copy()

    data["subscription_amount"] = pd.to_numeric(
        data["subscription_amount"],
        errors="coerce"
    )

    status = (
        data["subscription_status"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    failed = data[
        status.isin({
            "FAILED",
            "PAST_DUE",
            "PAYMENT_FAILED",
        })
        &
        (data["subscription_amount"] > 0)
    ]

    opportunities = []

    for _, row in failed.iterrows():

        amount = float(
            row["subscription_amount"]
        )

        probability = 0.72

        expected = calculate_expected_value(
            amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"SUB-FAIL-"
                    f"{row['subscription_id']}"
                ),

                category="RECOVER",

                opportunity_type=(
                    "FAILED_SUBSCRIPTION"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=amount,

                probability=probability,

                expected_value=expected,

                reason=(
                    f"Subscription "
                    f"{row['subscription_id']} "
                    f"has a failed payment status."
                ),

                recommended_action=(
                    "RETRY_SUBSCRIPTION_PAYMENT"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=True,

                recovery_reason=(
                    "Failed subscription is "
                    "eligible for bounded renewal recovery."
                ),

                source_detector=(
                    "FAILED_SUBSCRIPTION"
                ),
            )
        )

    return opportunities[:20]