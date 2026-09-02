import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


def detect_receivables(
    df: pd.DataFrame
):

    required = [
        "customer_id",
        "invoice_id",
        "invoice_amount",
        "invoice_due_date",
        "invoice_status",
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

    data["invoice_due_date"] = pd.to_datetime(
        data["invoice_due_date"],
        errors="coerce"
    )

    status = (
        data["invoice_status"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    today = pd.Timestamp.now().normalize()

    overdue = data[
        (data["invoice_due_date"] < today)
        &
        (data["invoice_amount"] > 0)
        &
        (
            ~status.isin({
                "PAID",
                "SETTLED",
            })
        )
    ]

    opportunities = []

    for _, row in overdue.iterrows():

        amount = float(
            row["invoice_amount"]
        )

        probability = 0.65

        expected = calculate_expected_value(
            amount,
            probability
        )

        opportunities.append(
            Opportunity(

                opportunity_id=(
                    f"AR-"
                    f"{row['invoice_id']}"
                ),

                category="RECOVER",

                opportunity_type=(
                    "B2B_RECEIVABLE"
                ),

                customer_id=str(
                    row["customer_id"]
                ),

                amount_at_risk=amount,

                probability=probability,

                expected_value=expected,

                reason=(
                    f"Invoice "
                    f"{row['invoice_id']} "
                    f"is overdue."
                ),

                recommended_action=(
                    "SEND_RECEIVABLES_REMINDER"
                ),

                priority=calculate_priority(
                    expected
                ),

                recovery_eligible=True,

                recovery_reason=(
                    "Overdue receivable is "
                    "eligible for compliant follow-up."
                ),

                source_detector=(
                    "B2B_RECEIVABLE"
                ),
            )
        )

    return opportunities[:20]