# from dataclasses import dataclass
# from typing import Optional


# @dataclass
# class Opportunity:

#     # ---------------------------------------------------------
#     # Identity
#     # ---------------------------------------------------------

#     opportunity_id: str

#     # RECOVER / PREVENT / GROW
#     category: str

#     # Specific opportunity type
#     opportunity_type: str

#     # Customer may not always be available
#     customer_id: Optional[str] = None

#     # ---------------------------------------------------------
#     # Financial impact
#     # ---------------------------------------------------------

#     # Revenue currently exposed to risk
#     amount_at_risk: float = 0.0

#     # Initial estimated probability of successful recovery
#     probability: float = 0.0

#     # amount_at_risk × probability
#     expected_value: float = 0.0

#     # ---------------------------------------------------------
#     # Agent reasoning
#     # ---------------------------------------------------------

#     reason: str = ""

#     # Initial recommendation from detector.
#     # The AI Agent can override this.
#     recommended_action: str = ""

#     # ---------------------------------------------------------
#     # Priority
#     # ---------------------------------------------------------

#     priority: str = "LOW"

#     # ---------------------------------------------------------
#     # Recovery ground truth
#     # ---------------------------------------------------------

#     # Synthetic ground truth used by the simulator.
#     #
#     # IMPORTANT:
#     # This is NOT decided by the AI.
#     #
#     # AI:
#     #     recommends an action
#     #
#     # Ground truth:
#     #     determines whether recovery can actually succeed
#     #
#     recovery_eligible: bool = True

#     # Why the opportunity is or isn't recoverable.
#     recovery_reason: str = ""

#     # ---------------------------------------------------------
#     # Provenance
#     # ---------------------------------------------------------

#     # Which detector generated this opportunity.
#     # Useful later when we have multiple Recover detectors.
#     source_detector: str = ""


# # =============================================================
# # EXPECTED VALUE
# # =============================================================

# def calculate_expected_value(
#     amount: float,
#     probability: float
# ) -> float:

#     # Keep probability safely between 0 and 1.
#     probability = max(
#         0.0,
#         min(1.0, float(probability))
#     )

#     amount = max(
#         0.0,
#         float(amount)
#     )

#     return round(
#         amount * probability,
#         2
#     )


# # =============================================================
# # PRIORITY
# # =============================================================

# def calculate_priority(
#     expected_value: float
# ) -> str:

#     expected_value = float(
#         expected_value
#     )

#     if expected_value >= 50000:

#         return "HIGH"

#     if expected_value >= 10000:

#         return "MEDIUM"

#     return "LOW"



from dataclasses import dataclass
from typing import Optional


@dataclass
class Opportunity:

    opportunity_id: str

    # RECOVER / PREVENT / GROW
    category: str

    # Specific opportunity type
    opportunity_type: str

    customer_id: Optional[str] = None

    # Financial impact
    amount_at_risk: float = 0.0
    probability: float = 0.0
    expected_value: float = 0.0

    # Reasoning
    reason: str = ""
    recommended_action: str = ""

    # Priority
    priority: str = "LOW"

    # Ground truth
    recovery_eligible: bool = True
    recovery_reason: str = ""

    # Provenance
    source_detector: str = ""


def calculate_expected_value(
    amount: float,
    probability: float
) -> float:

    amount = max(
        0.0,
        float(amount)
    )

    probability = max(
        0.0,
        min(
            1.0,
            float(probability)
        )
    )

    return round(
        amount * probability,
        2
    )


def calculate_priority(
    expected_value: float
) -> str:

    expected_value = float(
        expected_value
    )

    if expected_value >= 50000:
        return "HIGH"

    if expected_value >= 10000:
        return "MEDIUM"

    return "LOW"