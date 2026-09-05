# import sys
# from pathlib import Path

# import pandas as pd


# ROOT = Path(
#     __file__
# ).resolve().parents[1]

# sys.path.insert(
#     0,
#     str(ROOT / "backend")
# )


# from app.engine.detector_engine import (
#     detect_all_opportunities
# )

# from app.workflows.batch_recovery import (
#     BatchRecoveryEngine
# )


# DATASET = (
#     ROOT
#     / "data"
#     / "demo"
#     / "merchant_revenue_data.csv"
# )


# def main():

#     print("=" * 70)

#     print(
#         "             AI REVENUE INTELLIGENCE"
#     )

#     print("=" * 70)


#     # ========================================================
#     # DATA
#     # ========================================================

#     print("\n[1] Loading dataset...")

#     df = pd.read_csv(
#         DATASET
#     )

#     print(
#         f"✓ Loaded {len(df):,} rows"
#     )


#     # ========================================================
#     # DETECTION
#     # ========================================================

#     print(
#         "\n[2] Running all opportunity detectors..."
#     )

#     opportunities = (
#         detect_all_opportunities(df)
#     )


#     print(
#         f"✓ Total opportunities: "
#         f"{len(opportunities)}"
#     )


#     # ========================================================
#     # CATEGORY SUMMARY
#     # ========================================================

#     recover = [
#         x for x in opportunities
#         if x.category == "RECOVER"
#     ]

#     prevent = [
#         x for x in opportunities
#         if x.category == "PREVENT"
#     ]

#     grow = [
#         x for x in opportunities
#         if x.category == "GROW"
#     ]


#     print("\nCATEGORY SUMMARY")
#     print("------------------------------")

#     print(
#         f"RECOVER : {len(recover)}"
#     )

#     print(
#         f"PREVENT : {len(prevent)}"
#     )

#     print(
#         f"GROW    : {len(grow)}"
#     )


#     # ========================================================
#     # TYPE SUMMARY
#     # ========================================================

#     print("\nOPPORTUNITY TYPES")
#     print("------------------------------")


#     type_counts = {}

#     for opportunity in opportunities:

#         key = (
#             opportunity.category,
#             opportunity.opportunity_type
#         )

#         type_counts[key] = (
#             type_counts.get(
#                 key,
#                 0
#             )
#             + 1
#         )


#     for (
#         category,
#         opportunity_type
#     ), count in sorted(
#         type_counts.items()
#     ):

#         print(
#             f"{category:<8} "
#             f"{opportunity_type:<35} "
#             f"{count}"
#         )


#     # ========================================================
#     # BATCH
#     # ========================================================

#     print(
#         "\n[3] Running AI Agent + Policy + Action..."
#     )


#     engine = BatchRecoveryEngine()

#     batch = engine.run(
#         opportunities
#     )


#     summary = batch[
#         "summary"
#     ]


#     # ========================================================
#     # FINANCIAL SUMMARY
#     # ========================================================

#     print("\n")

#     print("=" * 70)

#     print(
#         "                 FINANCIAL IMPACT"
#     )

#     print("=" * 70)


#     print(
#         f"\nRevenue at risk     : "
#         f"₹{summary['total_amount_at_risk']:,.2f}"
#     )

#     print(
#         f"AI expected recovery: "
#         f"₹{summary['total_expected_recovery']:,.2f}"
#     )

#     print(
#         f"Actual recovered    : "
#         f"₹{summary['total_recovered']:,.2f}"
#     )

#     print(
#         f"Recovery rate       : "
#         f"{summary['recovery_rate']:.1%}"
#     )


#     print("\nACTION SUMMARY")
#     print("------------------------------")

#     print(
#         f"Executed            : "
#         f"{summary['actions_executed']}"
#     )

#     print(
#         f"Blocked             : "
#         f"{summary['actions_blocked']}"
#     )

#     print(
#         f"Failed              : "
#         f"{summary['actions_failed']}"
#     )

#     print(
#         f"Processing errors   : "
#         f"{summary['processing_errors']}"
#     )


#     # ========================================================
#     # TOP OPPORTUNITIES
#     # ========================================================

#     print("\n")

#     print("=" * 70)

#     print(
#         "                 TOP OPPORTUNITIES"
#     )

#     print("=" * 70)


#     for index, opportunity in enumerate(
#         opportunities[:15],
#         start=1
#     ):

#         print(
#             f"\n{index}. "
#             f"{opportunity.opportunity_id}"
#         )

#         print(
#             f"   Category : "
#             f"{opportunity.category}"
#         )

#         print(
#             f"   Type     : "
#             f"{opportunity.opportunity_type}"
#         )

#         print(
#             f"   Customer : "
#             f"{opportunity.customer_id}"
#         )

#         print(
#             f"   Risk     : "
#             f"₹{opportunity.amount_at_risk:,.2f}"
#         )

#         print(
#             f"   Priority : "
#             f"{opportunity.priority}"
#         )

#         print(
#             f"   Action   : "
#             f"{opportunity.recommended_action}"
#         )


#     print("\n")

#     print("=" * 70)

#     print(
#         "             ✓ FULL PIPELINE PASSED"
#     )

#     print("=" * 70)


# if __name__ == "__main__":

#     main()




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

    # IMPORTANT:
    # All opportunities are detected ONCE.
    opportunities = (
        detect_all_opportunities(df)
    )

    print(
        f"✓ Total opportunities: "
        f"{len(opportunities)}"
    )


    # ========================================================
    # CATEGORY SPLIT
    # ========================================================

    # These are NOT separate detection runs.
    # We are only organizing the already detected
    # opportunities by category.

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


    # ========================================================
    # CATEGORY SUMMARY
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                    OPPORTUNITY SUMMARY")
    print("=" * 70)

    print(
        f"\nTOTAL OPPORTUNITIES : {len(opportunities)}"
    )

    print(
        f"RECOVER             : {len(recover)}"
    )

    print(
        f"PREVENT             : {len(prevent)}"
    )

    print(
        f"GROW                : {len(grow)}"
    )


    # ========================================================
    # OPPORTUNITY TYPE SUMMARY
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                 OPPORTUNITY TYPES")
    print("=" * 70)

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
    # RECOVER / PREVENT / GROW DETAILS
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                     RECOVER")
    print("=" * 70)

    if not recover:

        print("\nNo RECOVER opportunities found.")

    else:

        for index, opportunity in enumerate(
            recover,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{opportunity.opportunity_id}"
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
    print("                     PREVENT")
    print("=" * 70)

    if not prevent:

        print("\nNo PREVENT opportunities found.")

    else:

        for index, opportunity in enumerate(
            prevent,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{opportunity.opportunity_id}"
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
    print("                       GROW")
    print("=" * 70)

    if not grow:

        print("\nNo GROW opportunities found.")

    else:

        for index, opportunity in enumerate(
            grow,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{opportunity.opportunity_id}"
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
                f"   Opportunity Value : "
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


    # ========================================================
    # RECOVERY BATCH
    # ========================================================

    print("\n")
    print("=" * 70)
    print("             RECOVER EXECUTION PIPELINE")
    print("=" * 70)

    print(
        f"\nSending ONLY RECOVER opportunities "
        f"to AI Agent + Policy + Action..."
    )

    print(
        f"RECOVER opportunities: {len(recover)}"
    )


    engine = BatchRecoveryEngine()

    # IMPORTANT:
    # Only RECOVER opportunities are executed.
    batch = engine.run(
        recover
    )


    summary = batch[
        "summary"
    ]


    # ========================================================
    # RECOVER FINANCIAL IMPACT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                 RECOVER FINANCIAL IMPACT")
    print("=" * 70)


    print(
        f"\nRevenue at risk       : "
        f"₹{summary['total_amount_at_risk']:,.2f}"
    )

    print(
        f"AI expected recovery  : "
        f"₹{summary['total_expected_recovery']:,.2f}"
    )

    print(
        f"Actual recovered      : "
        f"₹{summary['total_recovered']:,.2f}"
    )

    print(
        f"Recovery rate         : "
        f"{summary['recovery_rate']:.1%}"
    )


    # ========================================================
    # RECOVER ACTION SUMMARY
    # ========================================================

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
    # TOP RECOVER OPPORTUNITIES
    # ========================================================

    print("\n")
    print("=" * 70)
    print("              TOP RECOVER OPPORTUNITIES")
    print("=" * 70)


    for index, opportunity in enumerate(
        recover[:15],
        start=1
    ):

        print(
            f"\n{index}. "
            f"{opportunity.opportunity_id}"
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


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                 PIPELINE SUMMARY")
    print("=" * 70)

    print(
        f"\nTotal detected : {len(opportunities)}"
    )

    print(
        f"RECOVER        : {len(recover)}"
    )

    print(
        f"PREVENT        : {len(prevent)}"
    )

    print(
        f"GROW           : {len(grow)}"
    )

    print(
        f"\nRECOVERED      : "
        f"₹{summary['total_recovered']:,.2f}"
    )

    print(
        f"RECOVERY RATE  : "
        f"{summary['recovery_rate']:.1%}"
    )


    print("\n")
    print("=" * 70)

    print(
        "             ✓ FULL PIPELINE PASSED"
    )

    print("=" * 70)


if __name__ == "__main__":

    main()