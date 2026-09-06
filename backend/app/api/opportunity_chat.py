import json
import os
from typing import Any

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel


load_dotenv(override=True)


router = APIRouter(
    prefix="/api",
    tags=["opportunity-chat"],
)


class OpportunityChatRequest(BaseModel):
    question: str
    opportunity: dict[str, Any]


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured.",
        )

    return OpenAI(api_key=api_key)


@router.post("/opportunity-chat")
def opportunity_chat(
    request: OpportunityChatRequest,
):
    client = get_client()

    question = request.question.strip()
    opportunity = request.opportunity

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    # Only send information relevant to this opportunity.
    opportunity_context = {
        "opportunity_id": opportunity.get(
            "opportunity_id"
        ),
        "opportunity_type": opportunity.get(
            "opportunity_type"
        ),
        "category": opportunity.get(
            "category"
        ),
        "priority": opportunity.get(
            "priority"
        ),
        "customer_id": opportunity.get(
            "customer_id"
        ),
        "amount_at_risk": opportunity.get(
            "amount_at_risk"
        ),
        "probability": opportunity.get(
            "probability"
        ),
        "expected_value": opportunity.get(
            "expected_value"
        ),
        "reason": opportunity.get(
            "reason"
        ),
        "recommended_action": opportunity.get(
            "recommended_action"
        ),
        "recovery_eligible": opportunity.get(
            "recovery_eligible"
        ),
        "recovery_reason": opportunity.get(
            "recovery_reason"
        ),
        "source_detector": opportunity.get(
            "source_detector"
        ),
    }

    system_prompt = """
You are RevenueOS AI, a specialist revenue intelligence
assistant.

YOUR ONLY JOB:
Answer questions related to the CURRENTLY SELECTED
REVENUE OPPORTUNITY.

You are NOT a general-purpose chatbot.

You MUST follow these rules:

1. Only answer questions that are directly related to
   the selected revenue opportunity.

2. Relevant topics include:
   - opportunity type
   - customer signal
   - amount at risk
   - expected value
   - probability
   - priority
   - category
   - why the opportunity was detected
   - source detector
   - recovery eligibility
   - recovery reason
   - recommended action
   - possible business impact
   - what the merchant should do next

3. If the user's question is unrelated to the selected
   opportunity, DO NOT answer it.

4. For unrelated questions, respond exactly in this style:
   "I can only answer questions related to this revenue
   opportunity. Ask me about its risk, value, priority,
   detection reason, or recommended action."

5. Do not answer general knowledge questions.

6. Do not answer questions about politics, geography,
   mathematics unrelated to this opportunity, coding,
   entertainment, sports, or other general topics.

7. Do not invent information.

8. Use only the supplied opportunity context.

9. If the requested opportunity information is not
   available, say:
   "That information is not available for this
   opportunity."

10. Never claim that an action was actually executed.
    You may only explain the recommended action.

11. Keep answers concise, clear, and useful for a
    business user.

12. When discussing money, use Indian Rupee formatting.

CURRENT OPPORTUNITY:
The following information is the ONLY business context
you should use.
"""

    user_prompt = f"""
CURRENT OPPORTUNITY DATA:

{json.dumps(
    opportunity_context,
    indent=2,
    default=str,
)}

USER QUESTION:

{question}
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=system_prompt,
            input=user_prompt,
        )

        answer = response.output_text.strip()

        if not answer:
            answer = (
                "I could not generate an answer for "
                "this opportunity."
            )

        return {
            "answer": answer,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI request failed: {str(exc)}",
        )