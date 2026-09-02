import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


def detect_customer_expansion(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "amount",
        "timestamp",
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

    customer = (
        data
        .groupby("customer_id")
        .agg(
            transactions=(
                "transaction_id",
                "nunique"
            ),
            spending=(
                "amount",
                "sum"
            )
        )
        .reset_index()
    )

    # High-value customers
    threshold = customer[
        "spending"
    ].quantile(0.80)

    high_value = customer[
        (
            customer["spending"]
            >= threshold
        )
        &
        (
            customer["transactions"]
            >= 3
        )
    ]

    opportunities = []

    for _, row in high_value.iterrows():

        spending = float(
            row["spending"]
        )

        opportunity_amount = (
            spending * 0.20
        )

        probability = 0.30

        expected = calculate_expected_value(
            opportunity_amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"GROW-EXPAND-"
                    f"{row['customer_id']}"
                ),

                category="GROW",

                opportunity_type=(
                    "CUSTOMER_EXPANSION"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=(
                    opportunity_amount
                ),

                probability=probability,

                expected_value=expected,

                reason=(
                    "High-value customer with "
                    "multiple purchases represents "
                    "an expansion opportunity."
                ),

                recommended_action=(
                    "OFFER_PREMIUM_UPGRADE"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=False,

                recovery_reason=(
                    "Growth opportunity, not recovery."
                ),

                source_detector=(
                    "CUSTOMER_EXPANSION"
                ),
            )
        )

    return opportunities[:20]