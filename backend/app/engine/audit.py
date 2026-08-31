from datetime import datetime


def create_audit_event(
    opportunity,
    agent_decision,
    policy_result,
    action_result,
    recovered_amount
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

        "agent_diagnosis":
            agent_decision.get(
                "diagnosis"
            ),

        "agent_confidence":
            agent_decision.get(
                "confidence"
            ),

        "recommended_action":
            agent_decision.get(
                "recommended_action"
            ),

        "policy_allowed":
            policy_result.get(
                "allowed"
            ),

        "policy_reason":
            policy_result.get(
                "reason"
            ),

        "action":
            action_result.get(
                "action"
            ),

        "action_status":
            action_result.get(
                "status"
            ),

        "amount_at_risk":
            opportunity.amount_at_risk,

        "recovered_amount":
            recovered_amount
    }