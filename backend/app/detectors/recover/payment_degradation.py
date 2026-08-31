# import pandas as pd

# from app.engine.opportunity import (
#     Opportunity,
#     calculate_expected_value,
#     calculate_priority,
# )


# # ============================================================
# # CONFIGURATION
# # ============================================================

# MIN_TRANSACTIONS = 30

# # More sensitive than the previous 2.0 / 1.8 thresholds.
# MIN_FAILURE_MULTIPLE = 1.5
# MIN_DEGRADATION_RATIO = 1.5

# # Don't flood the agent with hundreds of opportunities.
# MAX_OPPORTUNITIES = 20


# # ============================================================
# # PAYMENT METHODS
# # ============================================================

# NORMAL_PAYMENT_METHODS = {
#     "UPI",
#     "CARD",
#     "NETBANKING",
#     "WALLET",
#     "CREDIT_CARD",
#     "DEBIT_CARD",
# }


# def detect_payment_degradation(
#     df: pd.DataFrame
# ):
#     """
#     Detect unusual payment failure degradation.

#     Detection dimensions:

#         bank
#         payment_method
#         hour
#         failure_rate
#         baseline_failure_rate
#         dominant_failure_reason

#     The detector produces structured Opportunities.

#     The AI Agent will later:
#         diagnose the cause
#         choose the intervention
#         apply policy
#         execute the recovery action
#     """

#     opportunities = []


#     # ========================================================
#     # 1. REQUIRED COLUMNS
#     # ========================================================

#     required_columns = [
#         "transaction_status",
#         "payment_method",
#         "bank",
#         "timestamp",
#         "amount",
#         "failure_reason",
#     ]

#     missing = [
#         column
#         for column in required_columns
#         if column not in df.columns
#     ]

#     if missing:

#         raise ValueError(
#             f"Missing required columns: {missing}"
#         )


#     # ========================================================
#     # 2. COPY + CLEAN
#     # ========================================================

#     data = df.copy()


#     data["timestamp"] = pd.to_datetime(
#         data["timestamp"],
#         errors="coerce"
#     )


#     data["amount"] = pd.to_numeric(
#         data["amount"],
#         errors="coerce"
#     )


#     data["transaction_status"] = (
#         data["transaction_status"]
#         .astype(str)
#         .str.upper()
#         .str.strip()
#     )


#     data["payment_method"] = (
#         data["payment_method"]
#         .astype(str)
#         .str.upper()
#         .str.strip()
#     )


#     data["bank"] = (
#         data["bank"]
#         .astype(str)
#         .str.strip()
#     )


#     data = data.dropna(
#         subset=[
#             "timestamp",
#             "amount",
#             "payment_method",
#             "bank",
#         ]
#     )


#     if data.empty:
#         return []


#     # ========================================================
#     # 3. FAILED TRANSACTION FLAG
#     # ========================================================

#     data["is_failed"] = (
#         data["transaction_status"]
#         == "FAILED"
#     )


#     # ========================================================
#     # 4. HOUR
#     # ========================================================

#     data["hour"] = (
#         data["timestamp"]
#         .dt.hour
#     )


#     # ========================================================
#     # 5. OVERALL FAILURE RATE
#     # ========================================================

#     overall_failure_rate = (
#         data["is_failed"].mean()
#     )


#     # Prevent division problems.
#     if overall_failure_rate <= 0:

#         return []


#     # ========================================================
#     # 6. BASELINE BY BANK + PAYMENT METHOD
#     # ========================================================

#     baseline = (
#         data
#         .groupby(
#             [
#                 "bank",
#                 "payment_method",
#             ]
#         )
#         .agg(
#             baseline_transactions=(
#                 "transaction_status",
#                 "count"
#             ),

#             baseline_failed=(
#                 "is_failed",
#                 "sum"
#             ),

#             baseline_amount=(
#                 "amount",
#                 "sum"
#             )
#         )
#         .reset_index()
#     )


#     baseline["baseline_failure_rate"] = (
#         baseline["baseline_failed"]
#         /
#         baseline["baseline_transactions"]
#     )


#     # ========================================================
#     # 7. HOURLY ANALYSIS
#     # ========================================================

#     hourly = (
#         data
#         .groupby(
#             [
#                 "bank",
#                 "payment_method",
#                 "hour",
#             ]
#         )
#         .agg(
#             total_transactions=(
#                 "transaction_status",
#                 "count"
#             ),

#             failed_transactions=(
#                 "is_failed",
#                 "sum"
#             ),

#             total_amount=(
#                 "amount",
#                 "sum"
#             )
#         )
#         .reset_index()
#     )


#     hourly["failure_rate"] = (
#         hourly["failed_transactions"]
#         /
#         hourly["total_transactions"]
#     )


#     # ========================================================
#     # 8. MERGE BASELINE
#     # ========================================================

#     hourly = hourly.merge(

#         baseline[
#             [
#                 "bank",
#                 "payment_method",
#                 "baseline_failure_rate",
#             ]
#         ],

#         on=[
#             "bank",
#             "payment_method",
#         ],

#         how="left"
#     )


#     # ========================================================
#     # 9. DEGRADATION RATIO
#     # ========================================================

#     hourly["degradation_ratio"] = (

#         hourly["failure_rate"]

#         /

#         hourly["baseline_failure_rate"]
#         .replace(0, 0.0001)
#     )


#     # ========================================================
#     # 10. FIND SUSPICIOUS WINDOWS
#     # ========================================================

#     suspicious = hourly[
#         (
#             hourly["total_transactions"]
#             >= MIN_TRANSACTIONS
#         )
#         &
#         (
#             hourly["failure_rate"]
#             >= (
#                 overall_failure_rate
#                 * MIN_FAILURE_MULTIPLE
#             )
#         )
#         &
#         (
#             hourly["degradation_ratio"]
#             >= MIN_DEGRADATION_RATIO
#         )
#     ].copy()


#     if suspicious.empty:

#         return []


#     # ========================================================
#     # 11. PROCESS EACH OPPORTUNITY
#     # ========================================================

#     for _, row in suspicious.iterrows():

#         bank = row["bank"]

#         method = row["payment_method"]

#         hour = int(row["hour"])


#         # ----------------------------------------------------
#         # Failed transactions in this window
#         # ----------------------------------------------------

#         affected = data[
#             (data["bank"] == bank)
#             &
#             (data["payment_method"] == method)
#             &
#             (data["hour"] == hour)
#             &
#             (data["is_failed"])
#         ]


#         if affected.empty:
#             continue


#         # ----------------------------------------------------
#         # Dominant failure reason
#         # ----------------------------------------------------

#         reason_counts = (
#             affected["failure_reason"]
#             .fillna("unknown")
#             .astype(str)
#             .str.lower()
#             .value_counts()
#         )


#         dominant_reason = (
#             reason_counts.index[0]
#         )


#         # ----------------------------------------------------
#         # Dominant reason percentage
#         # ----------------------------------------------------

#         dominant_reason_count = (
#             reason_counts.iloc[0]
#         )


#         dominant_reason_rate = (
#             dominant_reason_count
#             /
#             len(affected)
#         )


#         # ----------------------------------------------------
#         # Expected failures at baseline
#         # ----------------------------------------------------

#         expected_failed_transactions = (
#             row["total_transactions"]
#             *
#             row["baseline_failure_rate"]
#         )


#         actual_failed_transactions = (
#             row["failed_transactions"]
#         )


#         excess_failed_transactions = max(
#             0,
#             actual_failed_transactions
#             -
#             expected_failed_transactions
#         )


#         # ----------------------------------------------------
#         # Estimate amount at risk
#         # ----------------------------------------------------

#         average_failed_amount = (
#             affected["amount"].mean()
#         )


#         amount_at_risk = (
#             excess_failed_transactions
#             *
#             average_failed_amount
#         )


#         amount_at_risk = max(
#             0,
#             float(amount_at_risk)
#         )


#         if amount_at_risk <= 0:
#             continue


#         # ====================================================
#         # 12. ESTIMATE RECOVERY PROBABILITY
#         # ====================================================

#         # This is NOT the AI's decision.
#         #
#         # It is an initial quantitative estimate.
#         # The AI will use the evidence to make the
#         # intervention decision.

#         probability = 0.50


#         # Network/provider errors are generally more
#         # suitable for retry than permanent declines.

#         if dominant_reason in {
#             "network_error",
#             "timeout",
#             "gateway_timeout",
#             "temporary_error",
#             "server_error",
#         }:

#             probability += 0.20


#         # Strong degradation signal.

#         if row["degradation_ratio"] >= 2.0:

#             probability += 0.10


#         if row["degradation_ratio"] >= 3.0:

#             probability += 0.05


#         # High concentration of one temporary reason.

#         if dominant_reason_rate >= 0.70:

#             probability += 0.05


#         probability = min(
#             0.95,
#             probability
#         )


#         # ====================================================
#         # 13. EXPECTED VALUE
#         # ====================================================

#         expected_value = (
#             calculate_expected_value(
#                 amount_at_risk,
#                 probability
#             )
#         )


#         priority = calculate_priority(
#             expected_value
#         )


#         # ====================================================
#         # 14. PAYMENT TYPE
#         # ====================================================

#         if method == "MANDATE":

#             opportunity_type = (
#                 "MANDATE_PAYMENT_DEGRADATION"
#             )

#         else:

#             opportunity_type = (
#                 "PAYMENT_DEGRADATION"
#             )


#         # ====================================================
#         # 15. RECOMMENDED ACTION
#         # ====================================================

#         if dominant_reason in {
#             "network_error",
#             "timeout",
#             "gateway_timeout",
#             "temporary_error",
#             "server_error",
#         }:

#             recommended_action = (
#                 "WAIT_AND_RETRY"
#             )

#         else:

#             recommended_action = (
#                 "IDENTIFY_ROOT_CAUSE"
#             )


#         # ====================================================
#         # 16. CREATE OPPORTUNITY
#         # ====================================================

#         opportunity_id = (
#             f"PAY-DEG-"
#             f"{bank}-"
#             f"{method}-"
#             f"{hour:02d}"
#         )


#         reason = (

#             f"{bank} + {method} experienced "
#             f"a payment failure spike during "
#             f"{hour:02d}:00-{hour:02d}:59. "

#             f"Observed failure rate: "
#             f"{row['failure_rate']:.1%}. "

#             f"Baseline failure rate: "
#             f"{row['baseline_failure_rate']:.1%}. "

#             f"Degradation: "
#             f"{row['degradation_ratio']:.2f}x. "

#             f"Dominant failure reason: "
#             f"{dominant_reason} "
#             f"({dominant_reason_rate:.1%} "
#             f"of failed transactions)."
#         )


#         opportunity = Opportunity(

#             opportunity_id=opportunity_id,

#             category="RECOVER",

#             opportunity_type=opportunity_type,

#             customer_id=None,

#             amount_at_risk=round(
#                 amount_at_risk,
#                 2
#             ),

#             probability=round(
#                 probability,
#                 2
#             ),

#             expected_value=round(
#                 expected_value,
#                 2
#             ),

#             reason=reason,

#             recommended_action=recommended_action,

#             priority=priority,
#         )


#         opportunities.append(
#             opportunity
#         )


#     # ========================================================
#     # 17. REMOVE DUPLICATES
#     # ========================================================

#     unique_opportunities = {}

#     for opportunity in opportunities:

#         unique_opportunities[
#             opportunity.opportunity_id
#         ] = opportunity


#     opportunities = list(
#         unique_opportunities.values()
#     )


#     # ========================================================
#     # 18. RANK BY EXPECTED VALUE
#     # ========================================================

#     opportunities.sort(
#         key=lambda opportunity:
#             opportunity.expected_value,

#         reverse=True
#     )


#     # ========================================================
#     # 19. LIMIT OPPORTUNITIES
#     # ========================================================

#     return opportunities[
#         :MAX_OPPORTUNITIES
#     ]




import pandas as pd

from app.engine.opportunity import (
    Opportunity,
    calculate_expected_value,
    calculate_priority,
)


# ============================================================
# CONFIGURATION
# ============================================================

MIN_TRANSACTIONS = 30

# Sensitivity thresholds
MIN_FAILURE_MULTIPLE = 1.5
MIN_DEGRADATION_RATIO = 1.5

# Maximum number of opportunities returned
MAX_OPPORTUNITIES = 20


# ============================================================
# PAYMENT METHODS
# ============================================================

NORMAL_PAYMENT_METHODS = {
    "UPI",
    "CARD",
    "NETBANKING",
    "WALLET",
    "CREDIT_CARD",
    "DEBIT_CARD",
}


# ============================================================
# PAYMENT DEGRADATION DETECTOR
# ============================================================

def detect_payment_degradation(
    df: pd.DataFrame
):
    """
    Detect unusual payment failure degradation.

    Looks for:

        bank
        payment_method
        hour
        failure_rate
        baseline_failure_rate
        dominant_failure_reason

    Returns:

        list[Opportunity]

    The detector identifies suspicious revenue situations.

    The AI Agent later:

        1. Diagnoses the situation
        2. Chooses the intervention
        3. Policy Engine validates the action
        4. Action Engine executes the bounded action
        5. Recovery Engine calculates actual recovery
        6. Audit Engine records the decision
    """

    opportunities = []


    # ========================================================
    # 1. REQUIRED COLUMNS
    # ========================================================

    required_columns = [
        "transaction_status",
        "payment_method",
        "bank",
        "timestamp",
        "amount",
        "failure_reason",
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
    # 2. COPY + CLEAN DATA
    # ========================================================

    data = df.copy()


    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce"
    )


    data["amount"] = pd.to_numeric(
        data["amount"],
        errors="coerce"
    )


    data["transaction_status"] = (
        data["transaction_status"]
        .astype(str)
        .str.upper()
        .str.strip()
    )


    data["payment_method"] = (
        data["payment_method"]
        .astype(str)
        .str.upper()
        .str.strip()
    )


    data["bank"] = (
        data["bank"]
        .astype(str)
        .str.strip()
    )


    data = data.dropna(
        subset=[
            "timestamp",
            "amount",
            "payment_method",
            "bank",
        ]
    )


    if data.empty:

        return []


    # ========================================================
    # 3. FAILED TRANSACTION FLAG
    # ========================================================

    data["is_failed"] = (
        data["transaction_status"]
        == "FAILED"
    )


    # ========================================================
    # 4. EXTRACT HOUR
    # ========================================================

    data["hour"] = (
        data["timestamp"]
        .dt.hour
    )


    # ========================================================
    # 5. OVERALL FAILURE RATE
    # ========================================================

    overall_failure_rate = (
        data["is_failed"].mean()
    )


    # Prevent division problems
    if overall_failure_rate <= 0:

        return []


    # ========================================================
    # 6. BASELINE BY BANK + PAYMENT METHOD
    # ========================================================

    baseline = (
        data
        .groupby(
            [
                "bank",
                "payment_method",
            ]
        )
        .agg(
            baseline_transactions=(
                "transaction_status",
                "count"
            ),

            baseline_failed=(
                "is_failed",
                "sum"
            ),

            baseline_amount=(
                "amount",
                "sum"
            )
        )
        .reset_index()
    )


    baseline["baseline_failure_rate"] = (
        baseline["baseline_failed"]
        /
        baseline["baseline_transactions"]
    )


    # ========================================================
    # 7. HOURLY FAILURE ANALYSIS
    # ========================================================

    hourly = (
        data
        .groupby(
            [
                "bank",
                "payment_method",
                "hour",
            ]
        )
        .agg(
            total_transactions=(
                "transaction_status",
                "count"
            ),

            failed_transactions=(
                "is_failed",
                "sum"
            ),

            total_amount=(
                "amount",
                "sum"
            )
        )
        .reset_index()
    )


    hourly["failure_rate"] = (
        hourly["failed_transactions"]
        /
        hourly["total_transactions"]
    )


    # ========================================================
    # 8. MERGE BASELINE WITH HOURLY DATA
    # ========================================================

    hourly = hourly.merge(

        baseline[
            [
                "bank",
                "payment_method",
                "baseline_failure_rate",
            ]
        ],

        on=[
            "bank",
            "payment_method",
        ],

        how="left"
    )


    # ========================================================
    # 9. DEGRADATION RATIO
    # ========================================================

    hourly["degradation_ratio"] = (

        hourly["failure_rate"]

        /

        hourly["baseline_failure_rate"]
        .replace(
            0,
            0.0001
        )
    )


    # ========================================================
    # 10. FIND SUSPICIOUS WINDOWS
    # ========================================================

    suspicious = hourly[
        (
            hourly["total_transactions"]
            >= MIN_TRANSACTIONS
        )

        &

        (
            hourly["failure_rate"]
            >= (
                overall_failure_rate
                *
                MIN_FAILURE_MULTIPLE
            )
        )

        &

        (
            hourly["degradation_ratio"]
            >= MIN_DEGRADATION_RATIO
        )
    ].copy()


    if suspicious.empty:

        return []


    # ========================================================
    # 11. PROCESS EACH SUSPICIOUS WINDOW
    # ========================================================

    for _, row in suspicious.iterrows():

        bank = row["bank"]

        method = row["payment_method"]

        hour = int(row["hour"])


        # ----------------------------------------------------
        # Failed transactions in this window
        # ----------------------------------------------------

        affected = data[
            (data["bank"] == bank)

            &

            (data["payment_method"] == method)

            &

            (data["hour"] == hour)

            &

            (data["is_failed"])
        ]


        if affected.empty:

            continue


        # ----------------------------------------------------
        # Dominant failure reason
        # ----------------------------------------------------

        reason_counts = (
            affected["failure_reason"]
            .fillna("unknown")
            .astype(str)
            .str.lower()
            .str.strip()
            .value_counts()
        )


        dominant_reason = (
            reason_counts.index[0]
        )


        # ----------------------------------------------------
        # Dominant reason percentage
        # ----------------------------------------------------

        dominant_reason_count = (
            reason_counts.iloc[0]
        )


        dominant_reason_rate = (
            dominant_reason_count
            /
            len(affected)
        )


        # ====================================================
        # 12. RECOVERY GROUND TRUTH
        # ====================================================

        # These failure reasons are considered temporarily
        # recoverable through a bounded retry.

        recoverable_reasons = {
            "network_error",
            "timeout",
            "gateway_timeout",
            "temporary_error",
            "server_error",
        }


        recovery_eligible = (
            dominant_reason
            in recoverable_reasons
        )


        if recovery_eligible:

            recovery_reason = (
                f"Failure reason "
                f"'{dominant_reason}' "
                "is considered temporarily "
                "recoverable through a "
                "bounded retry."
            )

        else:

            recovery_reason = (
                f"Failure reason "
                f"'{dominant_reason}' "
                "is not eligible for "
                "automatic retry."
            )


        # ====================================================
        # 13. EXPECTED FAILURES AT BASELINE
        # ====================================================

        expected_failed_transactions = (
            row["total_transactions"]
            *
            row["baseline_failure_rate"]
        )


        actual_failed_transactions = (
            row["failed_transactions"]
        )


        excess_failed_transactions = max(
            0,
            actual_failed_transactions
            -
            expected_failed_transactions
        )


        # ====================================================
        # 14. ESTIMATE AMOUNT AT RISK
        # ====================================================

        average_failed_amount = (
            affected["amount"].mean()
        )


        amount_at_risk = (
            excess_failed_transactions
            *
            average_failed_amount
        )


        amount_at_risk = max(
            0,
            float(amount_at_risk)
        )


        if amount_at_risk <= 0:

            continue


        # ====================================================
        # 15. INITIAL RECOVERY PROBABILITY
        # ====================================================

        # This is an initial quantitative estimate.
        #
        # It is NOT the final AI decision.
        #
        # The OpenAI Agent receives the evidence and
        # independently recommends the intervention.

        probability = 0.50


        # Temporary/provider errors are more recoverable.

        if dominant_reason in {
            "network_error",
            "timeout",
            "gateway_timeout",
            "temporary_error",
            "server_error",
        }:

            probability += 0.20


        # Strong degradation signal.

        if row["degradation_ratio"] >= 2.0:

            probability += 0.10


        if row["degradation_ratio"] >= 3.0:

            probability += 0.05


        # Strong concentration of one failure reason.

        if dominant_reason_rate >= 0.70:

            probability += 0.05


        # Non-recoverable ground truth should not have
        # a high automatic recovery probability.

        if not recovery_eligible:

            probability = min(
                probability,
                0.30
            )


        probability = min(
            0.95,
            max(
                0.05,
                probability
            )
        )


        # ====================================================
        # 16. EXPECTED VALUE
        # ====================================================

        expected_value = (
            calculate_expected_value(
                amount_at_risk,
                probability
            )
        )


        priority = calculate_priority(
            expected_value
        )


        # ====================================================
        # 17. PAYMENT TYPE
        # ====================================================

        if method == "MANDATE":

            opportunity_type = (
                "MANDATE_PAYMENT_DEGRADATION"
            )

        else:

            opportunity_type = (
                "PAYMENT_DEGRADATION"
            )


        # ====================================================
        # 18. INITIAL RECOMMENDED ACTION
        # ====================================================

        if dominant_reason in {
            "network_error",
            "timeout",
            "gateway_timeout",
            "temporary_error",
            "server_error",
        }:

            recommended_action = (
                "WAIT_AND_RETRY"
            )

        else:

            recommended_action = (
                "IDENTIFY_ROOT_CAUSE"
            )


        # ====================================================
        # 19. OPPORTUNITY ID
        # ====================================================

        opportunity_id = (
            f"PAY-DEG-"
            f"{bank}-"
            f"{method}-"
            f"{hour:02d}"
        )


        # ====================================================
        # 20. HUMAN-READABLE REASON
        # ====================================================

        reason = (

            f"{bank} + {method} experienced "
            f"a payment failure spike during "
            f"{hour:02d}:00-{hour:02d}:59. "

            f"Observed failure rate: "
            f"{row['failure_rate']:.1%}. "

            f"Baseline failure rate: "
            f"{row['baseline_failure_rate']:.1%}. "

            f"Degradation: "
            f"{row['degradation_ratio']:.2f}x. "

            f"Dominant failure reason: "
            f"{dominant_reason} "

            f"({dominant_reason_rate:.1%} "
            f"of failed transactions)."
        )


        # ====================================================
        # 21. CREATE OPPORTUNITY
        # ====================================================

        opportunity = Opportunity(

            opportunity_id=(
                opportunity_id
            ),

            category="RECOVER",

            opportunity_type=(
                opportunity_type
            ),

            customer_id=None,

            amount_at_risk=round(
                amount_at_risk,
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

            # ------------------------------------------------
            # Recovery ground truth
            # ------------------------------------------------

            recovery_eligible=(
                recovery_eligible
            ),

            recovery_reason=(
                recovery_reason
            ),

            # ------------------------------------------------
            # Detector provenance
            # ------------------------------------------------

            source_detector=(
                "PAYMENT_DEGRADATION"
            ),
        )


        opportunities.append(
            opportunity
        )


    # ========================================================
    # 22. REMOVE DUPLICATES
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
    # 23. RANK BY EXPECTED VALUE
    # ========================================================

    opportunities.sort(

        key=lambda opportunity:
            opportunity.expected_value,

        reverse=True
    )


    # ========================================================
    # 24. LIMIT RESULTS
    # ========================================================

    return opportunities[
        :MAX_OPPORTUNITIES
    ]