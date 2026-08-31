from pathlib import Path
import sys

import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT / "backend")
)


# ============================================================
# IMPORTS
# ============================================================

from app.detectors.recover.payment_degradation import (
    detect_payment_degradation
)

from app.workflows.batch_recovery import (
    BatchRecoveryEngine
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
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "              BATCH AI REVENUE RECOVERY"
    )

    print("=" * 70)


    # ========================================================
    # 1. LOAD DATA
    # ========================================================

    print("\n[1] Loading dataset...")

    df = pd.read_csv(DATASET)

    print(
        f"✓ Loaded {len(df):,} transactions"
    )


    # ========================================================
    # 2. DETECT OPPORTUNITIES
    # ========================================================

    print(
        "\n[2] Detecting revenue opportunities..."
    )

    opportunities = (
        detect_payment_degradation(df)
    )

    print(
        f"✓ Found {len(opportunities)} opportunities"
    )


    if not opportunities:

        print(
            "\n❌ No revenue opportunities found."
        )

        return


    # ========================================================
    # 3. RUN BATCH RECOVERY
    # ========================================================

    print(
        "\n[3] Running batch recovery..."
    )

    engine = BatchRecoveryEngine()

    batch_result = engine.run(
        opportunities
    )


    # ========================================================
    # 4. SUMMARY
    # ========================================================

    summary = batch_result[
        "summary"
    ]

    results = batch_result[
        "results"
    ]


    print("\n")

    print("=" * 70)

    print(
        "                  RECOVERY SUMMARY"
    )

    print("=" * 70)


    print(
        f"\nOpportunities       : "
        f"{summary['total_opportunities']}"
    )

    print(
        f"Actions executed    : "
        f"{summary['actions_executed']}"
    )

    print(
        f"Actions blocked     : "
        f"{summary['actions_blocked']}"
    )

    print(
        f"Actions failed      : "
        f"{summary['actions_failed']}"
    )

    print(
        f"Processing errors   : "
        f"{summary.get('processing_errors', 0)}"
    )


    print("\nFinancial Impact")
    print("------------------------------")


    print(
        f"Revenue at risk     : "
        f"₹{summary['total_amount_at_risk']:,.2f}"
    )

    print(
        f"Expected recovery   : "
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


    # ========================================================
    # 5. DETAILED OPPORTUNITY RESULTS
    # ========================================================

    print("\n")

    print("=" * 70)

    print(
        "              OPPORTUNITY DETAILS"
    )

    print("=" * 70)


    for index, result in enumerate(
        results,
        start=1
    ):

        opportunity = result[
            "opportunity"
        ]

        agent = result[
            "agent_decision"
        ]

        policy = result[
            "policy"
        ]

        action = result[
            "action"
        ]


        print(
            f"\n[{index}] "
            f"{opportunity['opportunity_id']}"
        )

        print(
            "-" * 60
        )


        # ----------------------------------------------------
        # Opportunity
        # ----------------------------------------------------

        print(
            f"Type               : "
            f"{opportunity['opportunity_type']}"
        )

        print(
            f"Priority           : "
            f"{opportunity['priority']}"
        )

        print(
            f"Revenue at risk    : "
            f"₹{opportunity['amount_at_risk']:,.2f}"
        )

        print(
            f"Initial probability: "
            f"{opportunity['probability']:.0%}"
        )


        # ----------------------------------------------------
        # Detection reason
        # ----------------------------------------------------

        print(
            f"\nDetection reason:"
        )

        print(
            f"  {opportunity['reason']}"
        )


        # ----------------------------------------------------
        # Recovery ground truth
        # ----------------------------------------------------

        print(
            f"\nRecovery eligible  : "
            f"{opportunity['recovery_eligible']}"
        )

        print(
            f"Recovery reason    : "
            f"{opportunity['recovery_reason']}"
        )


        # ----------------------------------------------------
        # AI decision
        # ----------------------------------------------------

        print(
            "\nAI Agent Decision"
        )

        print(
            "------------------------------"
        )

        print(
            f"Diagnosis          : "
            f"{agent.get('diagnosis', 'N/A')}"
        )

        print(
            f"Confidence         : "
            f"{agent.get('confidence', 0):.0%}"
        )

        print(
            f"Recommended action : "
            f"{agent.get('recommended_action', 'N/A')}"
        )

        print(
            f"Expected recovery  : "
            f"₹{agent.get('expected_recovery', 0):,.2f}"
        )

        print(
            f"Reason             : "
            f"{agent.get('reason', 'N/A')}"
        )


        # ----------------------------------------------------
        # Policy
        # ----------------------------------------------------

        print(
            "\nPolicy"
        )

        print(
            "------------------------------"
        )

        print(
            f"Allowed            : "
            f"{policy.get('allowed', False)}"
        )

        print(
            f"Reason             : "
            f"{policy.get('reason', 'N/A')}"
        )


        # ----------------------------------------------------
        # Action
        # ----------------------------------------------------

        print(
            "\nAction Execution"
        )

        print(
            "------------------------------"
        )

        print(
            f"Action             : "
            f"{action.get('action', 'N/A')}"
        )

        print(
            f"Status             : "
            f"{action.get('status', 'N/A')}"
        )

        print(
            f"Success            : "
            f"{action.get('success', False)}"
        )

        print(
            f"Recovered          : "
            f"{action.get('recovered', False)}"
        )

        print(
            f"Message            : "
            f"{action.get('message', 'N/A')}"
        )


        # ----------------------------------------------------
        # Actual recovery
        # ----------------------------------------------------

        print(
            "\nRevenue Impact"
        )

        print(
            "------------------------------"
        )

        print(
            f"Actual recovered   : "
            f"₹{result.get('recovered_amount', 0):,.2f}"
        )


    # ========================================================
    # 6. FINAL JUDGE-FRIENDLY REPORT
    # ========================================================

    print("\n")

    print("=" * 70)

    print(
        "              FINAL RECOVERY IMPACT"
    )

    print("=" * 70)


    print(
        f"\n💰 Revenue at risk"
        f"       ₹{summary['total_amount_at_risk']:,.2f}"
    )

    print(
        f"🤖 AI expected recovery"
        f"  ₹{summary['total_expected_recovery']:,.2f}"
    )

    print(
        f"✅ Actual recovered"
        f"        ₹{summary['total_recovered']:,.2f}"
    )

    print(
        f"📈 Recovery rate"
        f"          {summary['recovery_rate']:.1%}"
    )

    print(
        f"🎯 Successful actions"
        f"      {summary['actions_executed']}"
    )

    print(
        f"❌ Failed actions"
        f"           {summary['actions_failed']}"
    )

    print(
        f"🛑 Policy blocked"
        f"          {summary['actions_blocked']}"
    )


    print("\n")

    print("=" * 70)

    print(
        "          ✓ BATCH RECOVERY COMPLETED"
    )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()