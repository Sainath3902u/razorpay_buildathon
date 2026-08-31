from dataclasses import asdict

from app.agents.revenue_agent import RevenueAgent
from app.engine.policy import check_policy
from app.engine.action import execute_action
from app.engine.recovery import calculate_recovery
from app.engine.audit import create_audit_event


class RecoveryWorkflow:

    def __init__(self):

        self.agent = RevenueAgent()


    def run(
        self,
        opportunity
    ):

        # =====================================================
        # STEP 1 — Convert Opportunity to Evidence
        # =====================================================

        evidence = {

            "type":
                opportunity.opportunity_type,

            "opportunity_id":
                opportunity.opportunity_id,

            "customer_id":
                opportunity.customer_id,

            # ---------------------------------------------
            # Financial evidence
            # ---------------------------------------------

            "amount_at_risk":
                opportunity.amount_at_risk,

            "probability":
                opportunity.probability,

            "expected_value":
                opportunity.expected_value,

            # ---------------------------------------------
            # Detection evidence
            # ---------------------------------------------

            "reason":
                opportunity.reason,

            "initial_recommended_action":
                opportunity.recommended_action,

            "priority":
                opportunity.priority,

            # ---------------------------------------------
            # Ground truth
            #
            # This is NOT used by the AI to decide whether
            # recovery actually happened.
            #
            # It is passed through the workflow so the
            # execution engine can use it later.
            # ---------------------------------------------

            "recovery_eligible":
                opportunity.recovery_eligible,

            "recovery_reason":
                opportunity.recovery_reason,

            # ---------------------------------------------
            # Provenance
            # ---------------------------------------------

            "source_detector":
                opportunity.source_detector,
        }


        # =====================================================
        # STEP 2 — AI AGENT
        # =====================================================

        agent_decision = self.agent.analyze(
            evidence
        )


        # =====================================================
        # STEP 3 — Extract AI action
        # =====================================================

        action = agent_decision.get(
            "recommended_action",
            "ESCALATE"
        )


        # =====================================================
        # STEP 4 — POLICY CHECK
        # =====================================================

        policy_result = check_policy(

            action=action,

            retry_count=0,

            payment_method_valid=True,

            customer_contact_allowed=True
        )


        # =====================================================
        # STEP 5 — POLICY REJECTION
        # =====================================================

        if not policy_result["allowed"]:

            action_result = {

                "action": action,

                "status": "BLOCKED",

                "success": False,

                "recovered": False,

                "message":
                    "Action blocked by policy."
            }

            recovered_amount = 0.0


        # =====================================================
        # STEP 6 — EXECUTE APPROVED ACTION
        # =====================================================

        else:

            action_result = execute_action(

                action=action,

                probability=agent_decision.get(
                    "confidence",
                    opportunity.probability
                ),

                recovery_eligible=(
                    opportunity.recovery_eligible
                )
            )


            # ---------------------------------------------
            # Calculate ACTUAL recovery
            #
            # This does NOT use AI confidence.
            # ---------------------------------------------

            recovered_amount = calculate_recovery(

                opportunity.amount_at_risk,

                action_result
            )


        # =====================================================
        # STEP 7 — AUDIT
        # =====================================================

        audit_event = create_audit_event(

            opportunity=opportunity,

            agent_decision=agent_decision,

            policy_result=policy_result,

            action_result=action_result,

            recovered_amount=recovered_amount
        )


        # =====================================================
        # STEP 8 — COMPLETE RESULT
        # =====================================================

        return {

            "opportunity":
                asdict(opportunity),

            "evidence":
                evidence,

            "agent_decision":
                agent_decision,

            "policy":
                policy_result,

            "action":
                action_result,

            "recovered_amount":
                recovered_amount,

            "audit":
                audit_event
        }