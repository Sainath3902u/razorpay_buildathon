import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


MIN_CART_VALUE = 5000
MAX_OPPORTUNITIES = 20


def _bool(value):

    if pd.isna(value):
        return False

    if isinstance(value, bool):
        return value

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "y",
    }


def detect_checkout_dropoff(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "order_id",
        "timestamp",
        "checkout_started",
        "checkout_completed",
        "cart_value",
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

    data["cart_value"] = pd.to_numeric(
        data["cart_value"],
        errors="coerce"
    )

    data["checkout_started"] = (
        data["checkout_started"]
        .apply(_bool)
    )

    data["checkout_completed"] = (
        data["checkout_completed"]
        .apply(_bool)
    )

    data = data.dropna(
        subset=[
            "customer_id",
            "order_id",
            "cart_value",
        ]
    )

    dropoffs = data[
        (data["checkout_started"])
        &
        (~data["checkout_completed"])
        &
        (data["cart_value"] >= MIN_CART_VALUE)
    ]

    opportunities = []

    for _, row in dropoffs.iterrows():

        amount = float(
            row["cart_value"]
        )

        probability = 0.60

        if amount >= 10000:
            probability += 0.05

        if amount >= 25000:
            probability += 0.05

        if amount >= 50000:
            probability += 0.05

        probability = min(
            probability,
            0.90
        )

        expected = calculate_expected_value(
            amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"CHK-DROP-"
                    f"{row['order_id']}"
                ),

                category="RECOVER",

                opportunity_type=(
                    "CHECKOUT_DROPOFF"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=round(
                    amount,
                    2
                ),

                probability=round(
                    probability,
                    2
                ),

                expected_value=expected,

                reason=(
                    f"Checkout was started but "
                    f"not completed. Cart value "
                    f"is ₹{amount:,.2f}."
                ),

                recommended_action=(
                    "SEND_CHECKOUT_RECOVERY"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=True,

                recovery_reason=(
                    "High-value abandoned checkout "
                    "is eligible for bounded recovery."
                ),

                source_detector=(
                    "CHECKOUT_DROPOFF"
                ),
            )
        )

    opportunities.sort(
        key=lambda x: x.expected_value,
        reverse=True
    )

    return opportunities[
        :MAX_OPPORTUNITIES
    ]