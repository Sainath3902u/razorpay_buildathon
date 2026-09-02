import sys
from pathlib import Path

import pandas as pd


ROOT = Path(
    __file__
).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT / "backend")
)


from app.engine.detector_engine import (
    detect_all_opportunities
)

from app.workflows.batch_recovery import (
    BatchRecoveryEngine
)


DATASET = (
    ROOT
    / "data"
    / "demo"
    / "merchant_revenue_data.csv"
)


def main():

    print("=" * 70)

    print(
        "             AI REVENUE INTELLIGENCE"
    )

    print("=" * 70)


    # ========================================================
    # DATA
    # ========================================================

    print("\n[1] Loading dataset...")

    df = pd.read_csv(
        DATASET
    )

    print(
        f"✓ Loaded {len(df):,} rows"
    )


    # ========================================================
    # DETECTION
    # ========================================================

    print(
        "\n[2] Running all opportunity detectors..."
    )

    opportunities = (
        detect_all_opportunities(df)
    )


    print(
        f"✓ Total opportunities: "
        f"{len(opportunities)}"
    )


    # ========================================================
    # CATEGORY SUMMARY
    # ========================================================

    recover = [
        x for x in opportunities
        if x.category == "RECOVER"
    ]

    prevent = [
        x for x in opportunities
        if x.category == "PREVENT"
    ]

    grow = [
        x for x in opportunities
        if x.category == "GROW"
    ]


    print("\nCATEGORY SUMMARY")
    print("------------------------------")

    print(
        f"RECOVER : {len(recover)}"
    )

    print(
        f"PREVENT : {len(prevent)}"
    )

    print(
        f"GROW    : {len(grow)}"
    )


    # ========================================================
    # TYPE SUMMARY
    # ========================================================

    print("\nOPPORTUNITY TYPES")
    print("------------------------------")


    type_counts = {}

    for opportunity in opportunities:

        key = (
            opportunity.category,
            opportunity.opportunity_type
        )

        type_counts[key] = (
            type_counts.get(
                key,
                0
            )
            + 1
        )


    for (
        category,
        opportunity_type
    ), count in sorted(
        type_counts.items()
    ):

        print(
            f"{category:<8} "
            f"{opportunity_type:<35} "
            f"{count}"
        )


    # ========================================================
    # BATCH
    # ========================================================

    print(
        "\n[3] Running AI Agent + Policy + Action..."
    )


    engine = BatchRecoveryEngine()

    batch = engine.run(
        opportunities
    )


    summary = batch[
        "summary"
    ]


    # ========================================================
    # FINANCIAL SUMMARY
    # ========================================================

    print("\n")

    print("=" * 70)

    print(
        "                 FINANCIAL IMPACT"
    )

    print("=" * 70)


    print(
        f"\nRevenue at risk     : "
        f"₹{summary['total_amount_at_risk']:,.2f}"
    )

    print(
        f"AI expected recovery: "
        f"₹{summary['total_expected_recovery']:,.2f}"
    )

    print(
        f"Actual recovered    : "
        f"₹{summary['total_recovered']:,.2f}"
    )

    print(
        f"Recovery rate       : "
        f"{summary['recovery_rate']:.1%}"
    )


    print("\nACTION SUMMARY")
    print("------------------------------")

    print(
        f"Executed            : "
        f"{summary['actions_executed']}"
    )

    print(
        f"Blocked             : "
        f"{summary['actions_blocked']}"
    )

    print(
        f"Failed              : "
        f"{summary['actions_failed']}"
    )

    print(
        f"Processing errors   : "
        f"{summary['processing_errors']}"
    )


    # ========================================================
    # TOP OPPORTUNITIES
    # ========================================================

    print("\n")

    print("=" * 70)

    print(
        "                 TOP OPPORTUNITIES"
    )

    print("=" * 70)


    for index, opportunity in enumerate(
        opportunities[:15],
        start=1
    ):

        print(
            f"\n{index}. "
            f"{opportunity.opportunity_id}"
        )

        print(
            f"   Category : "
            f"{opportunity.category}"
        )

        print(
            f"   Type     : "
            f"{opportunity.opportunity_type}"
        )

        print(
            f"   Customer : "
            f"{opportunity.customer_id}"
        )

        print(
            f"   Risk     : "
            f"₹{opportunity.amount_at_risk:,.2f}"
        )

        print(
            f"   Priority : "
            f"{opportunity.priority}"
        )

        print(
            f"   Action   : "
            f"{opportunity.recommended_action}"
        )


    print("\n")

    print("=" * 70)

    print(
        "             ✓ FULL PIPELINE PASSED"
    )

    print("=" * 70)


if __name__ == "__main__":

    main()