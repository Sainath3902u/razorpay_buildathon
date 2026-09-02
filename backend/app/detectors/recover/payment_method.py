import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


def detect_payment_method_risk(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "payment_method_id",
        "payment_method_expiry",
        "payment_method",
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

    data["payment_method_expiry"] = (
        pd.to_datetime(
            data["payment_method_expiry"],
            errors="coerce"
        )
    )

    data["amount"] = pd.to_numeric(
        data["amount"],
        errors="coerce"
    )

    today = pd.Timestamp.now().normalize()

    expiry_window = (
        today
        +
        pd.Timedelta(days=30)
    )

    risky = data[
        (
            data["payment_method_expiry"]
            <= expiry_window
        )
        &
        (
            data["payment_method_expiry"]
            >= today
        )
        &
        (data["amount"] > 0)
    ]

    opportunities = []

    for _, row in risky.iterrows():

        amount = float(
            row["amount"]
        )

        probability = 0.55

        expected = calculate_expected_value(
            amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"PM-RISK-"
                    f"{row['payment_method_id']}"
                ),

                category="RECOVER",

                opportunity_type=(
                    "PAYMENT_METHOD_RISK"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=amount,

                probability=probability,

                expected_value=expected,

                reason=(
                    f"Payment method "
                    f"{row['payment_method_id']} "
                    f"is approaching expiry."
                ),

                recommended_action=(
                    "UPDATE_PAYMENT_METHOD"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=True,

                recovery_reason=(
                    "Payment method update can "
                    "prevent payment interruption."
                ),

                source_detector=(
                    "PAYMENT_METHOD_RISK"
                ),
            )
        )

    return opportunities[:20]