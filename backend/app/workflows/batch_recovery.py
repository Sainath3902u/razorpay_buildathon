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

        total_expected_recovery = 0.0

        total_recovered = 0.0

        actions_executed = 0

        actions_blocked = 0

        actions_failed = 0

        processing_errors = 0


        # =====================================================
        # PROCESS EVERY OPPORTUNITY
        # =====================================================

        for index, opportunity in enumerate(
            opportunities,
            start=1
        ):

            print(
                f"\nProcessing opportunity "
                f"{index}/{len(opportunities)}"
            )


            # ---------------------------------------------
            # Count revenue at risk regardless of outcome
            # ---------------------------------------------

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


                # -----------------------------------------
                # Expected recovery
                # -----------------------------------------

                total_expected_recovery += float(
                    result[
                        "agent_decision"
                    ].get(
                        "expected_recovery",
                        0
                    )
                )


                # -----------------------------------------
                # Actual recovery
                # -----------------------------------------

                total_recovered += float(
                    result.get(
                        "recovered_amount",
                        0
                    )
                )


                # -----------------------------------------
                # Action status
                # -----------------------------------------

                action_status = result[
                    "action"
                ].get(
                    "status",
                    "FAILED"
                )


                if action_status == "BLOCKED":

                    actions_blocked += 1


                elif action_status == "SUCCESS":

                    actions_executed += 1


                elif action_status == "FAILED":

                    actions_failed += 1


                else:

                    actions_failed += 1


            except Exception as exc:

                processing_errors += 1

                actions_failed += 1


                print(
                    f"  ❌ Processing error: {exc}"
                )


        # =====================================================
        # RECOVERY RATE
        # =====================================================

        if total_at_risk > 0:

            recovery_rate = (
                total_recovered
                /
                total_at_risk
            )

        else:

            recovery_rate = 0.0


        # =====================================================
        # RETURN
        # =====================================================

        return {

            "summary": {

                "total_opportunities":
                    len(opportunities),

                "actions_executed":
                    actions_executed,

                "actions_blocked":
                    actions_blocked,

                "actions_failed":
                    actions_failed,

                "processing_errors":
                    processing_errors,

                "total_amount_at_risk":
                    round(
                        total_at_risk,
                        2
                    ),

                "total_expected_recovery":
                    round(
                        total_expected_recovery,
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
                    )
            },

            "results":
                results
        }