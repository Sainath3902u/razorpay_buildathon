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

from app.workflows.recovery_workflow import (
    RecoveryWorkflow
)


DATASET = (
    ROOT
    / "data"
    / "demo"
    / "merchant_revenue_data.csv"
)


def main():

    print("=" * 70)
    print("          AI REVENUE RECOVERY WORKFLOW")
    print("=" * 70)


    # ========================================================
    # LOAD DATA
    # ========================================================

    print("\n[1] Loading dataset...")

    df = pd.read_csv(DATASET)

    print(
        f"✓ Loaded {len(df):,} transactions"
    )


    # ========================================================
    # DETECT
    # ========================================================

    print("\n[2] Detecting revenue opportunities...")

    opportunities = (
        detect_payment_degradation(df)
    )

    print(
        f"✓ Found {len(opportunities)} opportunities"
    )


    if not opportunities:

        print(
            "\n⚠ No opportunities found."
        )

        print(
            "Check your injected degradation patterns."
        )

        return


    # ========================================================
    # SELECT FIRST OPPORTUNITY
    # ========================================================

    opportunity = opportunities[0]

    print("\nSelected opportunity:")

    print(
        f"  ID: "
        f"{opportunity.opportunity_id}"
    )

    print(
        f"  Type: "
        f"{opportunity.opportunity_type}"
    )

    print(
        f"  Amount at risk: "
        f"₹{opportunity.amount_at_risk:,.2f}"
    )

    print(
        f"  Probability: "
        f"{opportunity.probability:.0%}"
    )


    # ========================================================
    # RUN AGENTIC WORKFLOW
    # ========================================================

    print(
        "\n[3] Starting AI Revenue Agent..."
    )

    workflow = RecoveryWorkflow()

    result = workflow.run(
        opportunity
    )


    # ========================================================
    # AGENT DECISION
    # ========================================================

    print("\n[4] Agent decision")

    agent = result["agent_decision"]

    print(
        f"  Diagnosis: "
        f"{agent['diagnosis']}"
    )

    print(
        f"  Confidence: "
        f"{agent['confidence']:.0%}"
    )

    print(
        f"  Action: "
        f"{agent['recommended_action']}"
    )

    print(
        f"  Reason: "
        f"{agent['reason']}"
    )


    # ========================================================
    # POLICY
    # ========================================================

    print("\n[5] Policy check")

    policy = result["policy"]

    print(
        f"  Allowed: "
        f"{policy['allowed']}"
    )

    print(
        f"  Reason: "
        f"{policy['reason']}"
    )


    # ========================================================
    # ACTION
    # ========================================================

    print("\n[6] Action execution")

    action = result["action"]

    print(
        f"  Action: "
        f"{action['action']}"
    )

    print(
        f"  Status: "
        f"{action['status']}"
    )


    # ========================================================
    # RECOVERY
    # ========================================================

    print("\n[7] Revenue impact")

    recovered = result[
        "recovered_amount"
    ]

    print(
        f"  💰 Recovered: "
        f"₹{recovered:,.2f}"
    )


    # ========================================================
    # AUDIT
    # ========================================================

    print("\n[8] Audit trail")

    audit = result["audit"]

    print(
        f"  Opportunity: "
        f"{audit['opportunity_id']}"
    )

    print(
        f"  Decision: "
        f"{audit['recommended_action']}"
    )

    print(
        f"  Policy: "
        f"{audit['policy_allowed']}"
    )

    print(
        f"  Action: "
        f"{audit['action']}"
    )

    print(
        f"  Result: "
        f"{audit['action_status']}"
    )

    print(
        f"  Recovered: "
        f"₹{audit['recovered_amount']:,.2f}"
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print("\n" + "=" * 70)

    print(
        "       ✓ COMPLETE RECOVERY WORKFLOW PASSED"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()