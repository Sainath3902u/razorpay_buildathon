import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .prompts import SYSTEM_PROMPT


# ---------------------------------------------------------
# Load THIS project's .env
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]

ENV_FILE = ROOT / ".env"

load_dotenv(
    ENV_FILE,
    override=True
)


class RevenueAgent:

    def __init__(self):

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:
            raise RuntimeError(
                f"OPENAI_API_KEY not found in {ENV_FILE}"
            )

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.6-luna"
        )


    def analyze(self, evidence):

        # -------------------------------------------------
        # Send ONLY structured evidence to the AI
        # -------------------------------------------------

        response = self.client.responses.create(

            model=self.model,

            instructions=SYSTEM_PROMPT,

            input=json.dumps(
                evidence,
                indent=2,
                default=str
            )
        )


        # -------------------------------------------------
        # Extract AI output
        # -------------------------------------------------

        output = response.output_text.strip()


        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        try:

            decision = json.loads(output)

        except json.JSONDecodeError as exc:

            raise RuntimeError(
                "OpenAI returned invalid JSON.\n\n"
                f"Model output:\n{output}"
            ) from exc


        # -------------------------------------------------
        # Validate required AI fields
        #
        # IMPORTANT:
        # expected_recovery is NOT an AI field.
        # We calculate it ourselves.
        # -------------------------------------------------

        required_fields = [
            "diagnosis",
            "confidence",
            "recommended_action",
            "reason"
        ]


        missing = [
            field
            for field in required_fields
            if field not in decision
        ]


        if missing:

            raise RuntimeError(
                "AI response is missing required fields: "
                f"{missing}\n\n"
                f"Response:\n{decision}"
            )


        # -------------------------------------------------
        # Validate confidence
        # -------------------------------------------------

        try:

            confidence = float(
                decision["confidence"]
            )

        except (TypeError, ValueError):

            raise ValueError(
                "AI confidence must be a number."
            )


        # -------------------------------------------------
        # Normalize percentage if model accidentally
        # returns something like 85 instead of 0.85
        # -------------------------------------------------

        if confidence > 1 and confidence <= 100:

            confidence = confidence / 100


        if not 0 <= confidence <= 1:

            raise ValueError(
                "AI confidence must be between 0 and 1."
            )


        decision["confidence"] = round(
            confidence,
            4
        )


        # -------------------------------------------------
        # Validate recommended action
        # -------------------------------------------------

        allowed_actions = {

            "WAIT_AND_RETRY",

            "RETRY_PAYMENT",

            "SEND_PAYMENT_LINK",

            "UPDATE_PAYMENT_METHOD",

            "SEND_REMINDER",

            "ESCALATE",

            "STOP"
        }


        action = str(
            decision["recommended_action"]
        ).strip().upper()


        if action not in allowed_actions:

            raise ValueError(
                "AI returned an invalid action: "
                f"{action}\n"
                f"Allowed actions: "
                f"{sorted(allowed_actions)}"
            )


        decision["recommended_action"] = action


        # -------------------------------------------------
        # Calculate expected recovery LOCALLY
        #
        # AI does NOT calculate money.
        # -------------------------------------------------

        amount_at_risk = float(
            evidence.get(
                "amount_at_risk",
                0
            )
        )


        decision["expected_recovery"] = round(
            amount_at_risk
            * decision["confidence"],
            2
        )


        # -------------------------------------------------
        # Add evidence reference for debugging/audit
        # -------------------------------------------------

        decision["amount_at_risk"] = round(
            amount_at_risk,
            2
        )


        return decision