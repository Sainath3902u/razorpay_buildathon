import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


def detect_churn_risk(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "timestamp",
        "amount",
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

    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce"
    )

    data["amount"] = pd.to_numeric(
        data["amount"],
        errors="coerce"
    )

    customer = (
        data
        .groupby("customer_id")
        .agg(
            purchases=(
                "transaction_id",
                "nunique"
            ),
            spending=(
                "amount",
                "sum"
            ),
            last_purchase=(
                "timestamp",
                "max"
            )
        )
        .reset_index()
    )

    today = data["timestamp"].max()

    customer["days_since_purchase"] = (
        today
        -
        customer["last_purchase"]
    ).dt.days

    risky = customer[
        (
            customer["days_since_purchase"]
            >= 60
        )
        &
        (
            customer["purchases"]
            >= 2
        )
    ]

    opportunities = []

    for _, row in risky.iterrows():

        amount = float(
            row["spending"]
        )

        probability = 0.50

        expected = calculate_expected_value(
            amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"PREVENT-CHURN-"
                    f"{row['customer_id']}"
                ),

                category="PREVENT",

                opportunity_type=(
                    "CHURN_RISK"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=amount,

                probability=probability,

                expected_value=expected,

                reason=(
                    f"Customer has not purchased "
                    f"for {int(row['days_since_purchase'])} "
                    "days despite having prior purchases."
                ),

                recommended_action=(
                    "SEND_RETENTION_OFFER"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=False,

                recovery_reason=(
                    "Preventive retention action."
                ),

                source_detector=(
                    "CHURN_RISK"
                ),
            )
        )

    return opportunities[:20]