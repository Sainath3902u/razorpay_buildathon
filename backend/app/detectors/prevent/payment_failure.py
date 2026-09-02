import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


def detect_payment_failure_prevention(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "transaction_status",
        "amount",
        "failure_reason",
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

    data["amount"] = pd.to_numeric(
        data["amount"],
        errors="coerce"
    )

    failed = data[
        data["transaction_status"]
        .astype(str)
        .str.upper()
        .eq("FAILED")
    ]

    customer_failures = (
        failed
        .groupby("customer_id")
        .agg(
            failures=(
                "transaction_status",
                "count"
            ),
            amount=(
                "amount",
                "sum"
            )
        )
        .reset_index()
    )

    risky = customer_failures[
        customer_failures["failures"] >= 2
    ]

    opportunities = []

    for _, row in risky.iterrows():

        amount = float(
            row["amount"]
        )

        probability = 0.65

        expected = calculate_expected_value(
            amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"PREVENT-PAY-"
                    f"{row['customer_id']}"
                ),

                category="PREVENT",

                opportunity_type=(
                    "PAYMENT_FAILURE_PREVENTION"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=amount,

                probability=probability,

                expected_value=expected,

                reason=(
                    f"Customer has "
                    f"{int(row['failures'])} "
                    "recent failed payments."
                ),

                recommended_action=(
                    "OFFER_ALTERNATE_PAYMENT"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=False,

                recovery_reason=(
                    "Preventive intervention "
                    "should occur before another failure."
                ),

                source_detector=(
                    "PAYMENT_FAILURE_PREVENTION"
                ),
            )
        )

    return opportunities[:20]