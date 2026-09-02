from datetime import datetime


def create_audit_event(
    opportunity,
    agent_decision,
    policy_result,
    action_result,
    recovered_amount,
):

    return {

        "timestamp":
            datetime.utcnow().isoformat(),

        "opportunity_id":
            opportunity.opportunity_id,

        "category":
            opportunity.category,

        "opportunity_type":
            opportunity.opportunity_type,

        "source_detector":
            opportunity.source_detector,

        "amount_at_risk":
            opportunity.amount_at_risk,

        "agent_action":
            agent_decision.get(
                "recommended_action"
            ),

        "agent_confidence":
            agent_decision.get(
                "confidence"
            ),

        "policy_allowed":
            policy_result.get(
                "allowed"
            ),

        "executed_action":
            action_result.get(
                "action"
            ),

        "execution_status":
            action_result.get(
                "status"
            ),

        "recovered":
            action_result.get(
                "recovered",
                False
            ),

        "recovered_amount":
            recovered_amount,

        "recovery_eligible":
            opportunity.recovery_eligible,

        "recovery_reason":
            opportunity.recovery_reason,
    }