from typing import List

from app.workflows.recovery_workflow import (
    RecoveryWorkflow
)


class BatchRecoveryEngine:

    def __init__(self):

        self.workflow = RecoveryWorkflow()


    def run(
        self,
        opportunities: List
    ):

        results = []

        total_at_risk = 0.0

        total_expected = 0.0

        total_recovered = 0.0

        executed = 0

        blocked = 0

        failed = 0

        errors = 0


        for index, opportunity in enumerate(
            opportunities,
            start=1
        ):

            print(
                f"\nProcessing opportunity "
                f"{index}/{len(opportunities)}"
            )


            total_at_risk += float(
                opportunity.amount_at_risk
            )


            try:

                result = self.workflow.run(
                    opportunity
                )

                results.append(
                    result
                )


                total_expected += float(
                    result[
                        "agent_decision"
                    ].get(
                        "expected_recovery",
                        0
                    )
                )


                total_recovered += float(
                    result.get(
                        "recovered_amount",
                        0
                    )
                )


                status = result[
                    "action"
                ].get(
                    "status",
                    "FAILED"
                )


                if status == "SUCCESS":

                    executed += 1

                elif status == "BLOCKED":

                    blocked += 1

                else:

                    failed += 1


            except Exception as exc:

                errors += 1

                failed += 1

                print(
                    f"  ERROR: {exc}"
                )


        recovery_rate = (

            total_recovered
            /
            total_at_risk

            if total_at_risk > 0

            else 0
        )


        return {

            "summary": {

                "total_opportunities":
                    len(opportunities),

                "actions_executed":
                    executed,

                "actions_blocked":
                    blocked,

                "actions_failed":
                    failed,

                "processing_errors":
                    errors,

                "total_amount_at_risk":
                    round(
                        total_at_risk,
                        2
                    ),

                "total_expected_recovery":
                    round(
                        total_expected,
                        2
                    ),

                "total_recovered":
                    round(
                        total_recovered,
                        2
                    ),

                "recovery_rate":
                    round(
                        recovery_rate,
                        4
                    ),
            },

            "results":
                results,
        }