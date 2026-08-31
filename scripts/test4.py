import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

ROOT = Path(
    __file__
).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT / "backend")
)


# ============================================================
# IMPORT
# ============================================================

from app.detectors.recover.checkout_dropoff import (
    detect_checkout_dropoff
)


# ============================================================
# DATASET
# ============================================================

DATASET = (
    ROOT
    / "data"
    / "demo"
    / "merchant_revenue_data.csv"
)


# ============================================================
# TEST
# ============================================================

def main():

    print("=" * 70)

    print(
        "             CHECKOUT DROP-OFF DETECTOR"
    )

    print("=" * 70)


    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    print("\n[1] Loading dataset...")

    df = pd.read_csv(
        DATASET
    )

    print(
        f"✓ Loaded {len(df):,} rows"
    )


    # --------------------------------------------------------
    # Detect
    # --------------------------------------------------------

    print(
        "\n[2] Detecting checkout drop-offs..."
    )

    opportunities = (
        detect_checkout_dropoff(df)
    )


    print(
        f"✓ Found {len(opportunities)} opportunities"
    )


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    for index, opportunity in enumerate(
        opportunities,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"Opportunity {index}"
        )

        print(
            f"ID                : "
            f"{opportunity.opportunity_id}"
        )

        print(
            f"Type              : "
            f"{opportunity.opportunity_type}"
        )

        print(
            f"Customer          : "
            f"{opportunity.customer_id}"
        )

        print(
            f"Amount at risk    : "
            f"₹{opportunity.amount_at_risk:,.2f}"
        )

        print(
            f"Probability       : "
            f"{opportunity.probability:.0%}"
        )

        print(
            f"Expected value    : "
            f"₹{opportunity.expected_value:,.2f}"
        )

        print(
            f"Priority          : "
            f"{opportunity.priority}"
        )

        print(
            f"Recovery eligible : "
            f"{opportunity.recovery_eligible}"
        )

        print(
            f"Recommended action: "
            f"{opportunity.recommended_action}"
        )

        print(
            f"Reason            : "
            f"{opportunity.reason}"
        )


    print("\n")

    print("=" * 70)

    print(
        "          ✓ CHECKOUT DETECTOR TEST COMPLETE"
    )

    print("=" * 70)


if __name__ == "__main__":

    main()