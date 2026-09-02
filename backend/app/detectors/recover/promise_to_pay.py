import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


def detect_promise_to_pay(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "invoice_id",
        "invoice_amount",
        "promise_date",
        "promise_status",
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

    data["invoice_amount"] = pd.to_numeric(
        data["invoice_amount"],
        errors="coerce"
    )

    data["promise_date"] = pd.to_datetime(
        data["promise_date"],
        errors="coerce"
    )

    status = (
        data["promise_status"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    today = pd.Timestamp.now().normalize()

    broken = data[
        (data["promise_date"] < today)
        &
        (~status.isin({
            "PAID",
            "FULFILLED",
            "COMPLETED",
        }))
        &
        (data["invoice_amount"] > 0)
    ]

    opportunities = []

    for _, row in broken.iterrows():

        amount = float(
            row["invoice_amount"]
        )

        probability = 0.60

        expected = calculate_expected_value(
            amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"PTP-"
                    f"{row['invoice_id']}"
                ),

                category="RECOVER",

                opportunity_type=(
                    "PROMISE_TO_PAY"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=amount,

                probability=probability,

                expected_value=expected,

                reason=(
                    f"Promise-to-pay for invoice "
                    f"{row['invoice_id']} "
                    f"was not fulfilled."
                ),

                recommended_action=(
                    "FOLLOW_UP_PROMISE"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=True,

                recovery_reason=(
                    "Broken promise is eligible "
                    "for bounded follow-up."
                ),

                source_detector=(
                    "PROMISE_TO_PAY"
                ),
            )
        )

    return opportunities[:20]