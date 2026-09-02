import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


MAX_RETRIES = 3


def detect_mandate_retry(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "mandate_id",
        "mandate_status",
        "retry_count",
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

    data["retry_count"] = pd.to_numeric(
        data["retry_count"],
        errors="coerce"
    ).fillna(0)

    data["subscription_amount"] = pd.to_numeric(
        data["subscription_amount"],
        errors="coerce"
    ).fillna(0)

    status = (
        data["mandate_status"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    failed = data[
        status.isin({
            "FAILED",
            "PAUSED",
            "EXPIRED",
        })
        &
        (data["retry_count"] < MAX_RETRIES)
        &
        (data["subscription_amount"] > 0)
    ]

    opportunities = []

    for _, row in failed.iterrows():

        amount = float(
            row["subscription_amount"]
        )

        probability = 0.70

        expected = calculate_expected_value(
            amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"MANDATE-"
                    f"{row['mandate_id']}"
                ),

                category="RECOVER",

                opportunity_type=(
                    "MANDATE_RETRY"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=amount,

                probability=probability,

                expected_value=expected,

                reason=(
                    f"Mandate "
                    f"{row['mandate_id']} "
                    f"has failed with "
                    f"{int(row['retry_count'])} "
                    f"previous retries."
                ),

                recommended_action=(
                    "RETRY_MANDATE"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=(
                    row["retry_count"]
                    < MAX_RETRIES
                ),

                recovery_reason=(
                    "Retry count remains within "
                    "the bounded retry limit."
                ),

                source_detector=(
                    "MANDATE_RETRY"
                ),
            )
        )

    return opportunities[:20]