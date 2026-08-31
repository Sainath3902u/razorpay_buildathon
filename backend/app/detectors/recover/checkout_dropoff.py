import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


# ============================================================
# CONFIGURATION
# ============================================================

MIN_CART_VALUE = 5000

MAX_OPPORTUNITIES = 20


# ============================================================
# CHECKOUT DROP-OFF DETECTOR
# ============================================================

def detect_checkout_dropoff(
    df: pd.DataFrame
):
    """
    Detect high-value checkout sessions that were started
    but not completed.

    Detection logic:

        checkout_started = TRUE
        checkout_completed = FALSE
        cart_value >= MIN_CART_VALUE

    The detector creates RECOVER opportunities.

    The AI Agent later decides the appropriate intervention.
    """

    opportunities = []


    # ========================================================
    # 1. REQUIRED COLUMNS
    # ========================================================

    required_columns = [
        "customer_id",
        "order_id",
        "timestamp",
        "checkout_started",
        "checkout_completed",
        "cart_value",
    ]


    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]


    if missing:

        raise ValueError(
            f"Missing required columns: {missing}"
        )


    # ========================================================
    # 2. COPY DATA
    # ========================================================

    data = df.copy()


    # ========================================================
    # 3. CLEAN DATA
    # ========================================================

    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce"
    )


    data["cart_value"] = pd.to_numeric(
        data["cart_value"],
        errors="coerce"
    )


    # ========================================================
    # 4. NORMALIZE BOOLEAN COLUMNS
    # ========================================================

    def normalize_boolean(value):

        if pd.isna(value):
            return False

        if isinstance(value, bool):
            return value

        value = str(value).strip().lower()

        return value in {
            "true",
            "1",
            "yes",
            "y",
            "completed",
            "started",
        }


    data["checkout_started"] = (
        data["checkout_started"]
        .apply(normalize_boolean)
    )


    data["checkout_completed"] = (
        data["checkout_completed"]
        .apply(normalize_boolean)
    )


    # ========================================================
    # 5. REMOVE INVALID ROWS
    # ========================================================

    data = data.dropna(
        subset=[
            "customer_id",
            "order_id",
            "timestamp",
            "cart_value",
        ]
    )


    data = data[
        data["cart_value"] > 0
    ]


    if data.empty:

        return []


    # ========================================================
    # 6. DETECT CHECKOUT DROP-OFF
    # ========================================================

    dropoffs = data[
        (
            data["checkout_started"]
            == True
        )

        &

        (
            data["checkout_completed"]
            == False
        )

        &

        (
            data["cart_value"]
            >= MIN_CART_VALUE
        )
    ].copy()


    if dropoffs.empty:

        return []


    # ========================================================
    # 7. PROCESS EACH DROPOFF
    # ========================================================

    for _, row in dropoffs.iterrows():

        customer_id = str(
            row["customer_id"]
        )

        order_id = str(
            row["order_id"]
        )

        cart_value = float(
            row["cart_value"]
        )


        # ====================================================
        # RECOVERY GROUND TRUTH
        # ====================================================

        # For the synthetic buildathon dataset, high-value
        # abandoned carts are marked recoverable.
        #
        # The AI does NOT decide this.
        #
        # This represents synthetic ground truth used by
        # the action simulator.

        recovery_eligible = True


        recovery_reason = (
            "Checkout was started but not completed "
            "for a high-value cart. The synthetic "
            "scenario is eligible for a bounded "
            "checkout recovery intervention."
        )


        # ====================================================
        # RECOVERY PROBABILITY
        # ====================================================

        probability = 0.60


        # Higher-value abandoned carts receive a slightly
        # higher recovery opportunity score.

        if cart_value >= 10000:

            probability += 0.05


        if cart_value >= 25000:

            probability += 0.05


        if cart_value >= 50000:

            probability += 0.05


        probability = min(
            0.90,
            probability
        )


        # ====================================================
        # EXPECTED VALUE
        # ====================================================

        expected_value = (
            calculate_expected_value(
                cart_value,
                probability
            )
        )


        priority = calculate_priority(
            expected_value
        )


        # ====================================================
        # RECOMMENDED ACTION
        # ====================================================

        # This is only the detector's initial suggestion.
        # The OpenAI Agent makes the final decision.

        recommended_action = (
            "SEND_CHECKOUT_RECOVERY"
        )


        # ====================================================
        # OPPORTUNITY ID
        # ====================================================

        opportunity_id = (
            f"CHK-DROP-"
            f"{order_id}"
        )


        # ====================================================
        # REASON
        # ====================================================

        reason = (

            f"Customer {customer_id} started "
            f"a checkout for order {order_id} "
            f"but did not complete it. "

            f"Cart value: ₹{cart_value:,.2f}. "
            f"The cart exceeds the high-value "
            f"threshold of ₹{MIN_CART_VALUE:,.2f}."
        )


        # ====================================================
        # CREATE OPPORTUNITY
        # ====================================================

        opportunity = Opportunity(

            opportunity_id=(
                opportunity_id
            ),

            category="RECOVER",

            opportunity_type=(
                "CHECKOUT_DROPOFF"
            ),

            customer_id=(
                customer_id
            ),

            amount_at_risk=round(
                cart_value,
                2
            ),

            probability=round(
                probability,
                2
            ),

            expected_value=round(
                expected_value,
                2
            ),

            reason=reason,

            recommended_action=(
                recommended_action
            ),

            priority=priority,

            recovery_eligible=(
                recovery_eligible
            ),

            recovery_reason=(
                recovery_reason
            ),

            source_detector=(
                "CHECKOUT_DROPOFF"
            ),
        )


        opportunities.append(
            opportunity
        )


    # ========================================================
    # 8. REMOVE DUPLICATE ORDERS
    # ========================================================

    unique_opportunities = {}


    for opportunity in opportunities:

        unique_opportunities[
            opportunity.opportunity_id
        ] = opportunity


    opportunities = list(
        unique_opportunities.values()
    )


    # ========================================================
    # 9. RANK BY EXPECTED VALUE
    # ========================================================

    opportunities.sort(

        key=lambda opportunity:
            opportunity.expected_value,

        reverse=True
    )


    # ========================================================
    # 10. LIMIT RESULTS
    # ========================================================

    return opportunities[
        :MAX_OPPORTUNITIES
    ]