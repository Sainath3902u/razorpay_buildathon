import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


def detect_cross_sell(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "product_id",
        "product_category",
        "product_price",
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

    data["product_price"] = pd.to_numeric(
        data["product_price"],
        errors="coerce"
    )

    customer_products = (
        data
        .groupby("customer_id")
        ["product_category"]
        .nunique()
    )

    customers = customer_products[
        customer_products == 1
    ].index

    opportunities = []

    for customer_id in customers:

        customer_rows = data[
            data["customer_id"]
            == customer_id
        ]

        amount = float(
            customer_rows[
                "product_price"
            ].sum()
        )

        opportunity_amount = (
            amount * 0.25
        )

        probability = 0.35

        expected = calculate_expected_value(
            opportunity_amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"GROW-XSELL-"
                    f"{customer_id}"
                ),

                category="GROW",

                opportunity_type=(
                    "CROSS_SELL"
                ),

                customer_id=str(
                    customer_id
                ),

                amount_at_risk=(
                    opportunity_amount
                ),

                probability=probability,

                expected_value=expected,

                reason=(
                    "Customer purchases are "
                    "concentrated in one product "
                    "category, creating a potential "
                    "cross-sell opportunity."
                ),

                recommended_action=(
                    "RECOMMEND_COMPLEMENTARY_PRODUCT"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=False,

                recovery_reason=(
                    "Growth opportunity, not recovery."
                ),

                source_detector=(
                    "CROSS_SELL"
                ),
            )
        )

    return opportunities[:20]