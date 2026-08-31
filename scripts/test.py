from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT / "backend")
)


from app.detectors.recover.payment_degradation import (
    detect_payment_degradation
)


DATASET = (
    ROOT
    / "data"
    / "demo"
    / "merchant_revenue_data.csv"
)


def main():

    print("=" * 60)
    print("       PAYMENT DEGRADATION DETECTOR")
    print("=" * 60)

    # --------------------------------------------------
    # Load dataset
    # --------------------------------------------------

    if not DATASET.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n{DATASET}"
        )

    df = pd.read_csv(DATASET)

    print(
        f"\nLoaded {len(df):,} rows"
    )

    # --------------------------------------------------
    # Run detector
    # --------------------------------------------------

    opportunities = (
        detect_payment_degradation(df)
    )

    print(
        f"\nOpportunities found: "
        f"{len(opportunities)}"
    )

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------

    for opportunity in opportunities:

        print("\n" + "-" * 50)

        print(
            f"Opportunity ID : "
            f"{opportunity.opportunity_id}"
        )

        print(
            f"Category       : "
            f"{opportunity.category}"
        )

        print(
            f"Type           : "
            f"{opportunity.opportunity_type}"
        )

        print(
            f"Amount at risk : "
            f"₹{opportunity.amount_at_risk:,.2f}"
        )

        print(
            f"Probability    : "
            f"{opportunity.probability:.0%}"
        )

        print(
            f"Expected value : "
            f"₹{opportunity.expected_value:,.2f}"
        )

        print(
            f"Priority       : "
            f"{opportunity.priority}"
        )

        print(
            f"Reason         : "
            f"{opportunity.reason}"
        )

        print(
            f"Action         : "
            f"{opportunity.recommended_action}"
        )

    print("\n" + "=" * 60)
    print("Detector test completed")
    print("=" * 60)


if __name__ == "__main__":
    main()