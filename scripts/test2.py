from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT / "backend")
)


from app.agents.revenue_agent import RevenueAgent


def main():

    print("=" * 60)
    print("           OPENAI REVENUE AGENT TEST")
    print("=" * 60)

    evidence = {

        "type": "PAYMENT_DEGRADATION",

        "opportunity_id":
            "TEST-OPENAI-001",

        "bank":
            "SBI",

        "payment_method":
            "UPI",

        "hour":
            19,

        "observed_failure_rate":
            0.243,

        "baseline_failure_rate":
            0.032,

        "dominant_failure_reason":
            "network_error",

        "affected_transactions":
            1243,

        "amount_at_risk":
            153613.13,

        "expected_value":
            135197.09
    }


    print("\nSending evidence to OpenAI...")

    agent = RevenueAgent()

    decision = agent.analyze(
        evidence
    )


    print("\nAI DECISION")
    print("-" * 40)

    print(
        "Diagnosis:",
        decision["diagnosis"]
    )

    print(
        "Confidence:",
        f"{decision['confidence']:.0%}"
    )

    print(
        "Action:",
        decision["recommended_action"]
    )

    print(
        "Reason:",
        decision["reason"]
    )

    print(
        "Expected recovery:",
        f"₹{decision['expected_recovery']:,.2f}"
    )


    print("\n✓ OPENAI AGENT TEST PASSED")


if __name__ == "__main__":
    main()