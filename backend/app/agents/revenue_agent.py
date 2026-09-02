import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

from app.agents.prompts import SYSTEM_PROMPT

ROOT = Path(__file__).resolve().parents[3]

load_dotenv(
    ROOT / ".env",
    override=True
)


class RevenueAgent:

    def __init__(self):

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:

            raise RuntimeError(
                "OPENAI_API_KEY not found."
            )

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.6"
        )


    def analyze(
        self,
        evidence
    ):

        response = (
            self.client.responses.create(

                model=self.model,

                instructions=SYSTEM_PROMPT,

                input=json.dumps(
                    evidence,
                    indent=2,
                    default=str
                )
            )
        )


        output = (
            response.output_text
            .strip()
        )


        try:

            decision = json.loads(
                output
            )

        except json.JSONDecodeError as exc:

            raise RuntimeError(
                "OpenAI returned invalid JSON.\n"
                f"Output:\n{output}"
            ) from exc


        required = [
            "diagnosis",
            "confidence",
            "recommended_action",
            "reason",
            "expected_recovery",
        ]


        missing = [
            x for x in required
            if x not in decision
        ]


        if missing:

            raise RuntimeError(
                f"Missing AI fields: {missing}"
            )


        decision["confidence"] = float(
            decision["confidence"]
        )


        decision["confidence"] = max(
            0.0,
            min(
                1.0,
                decision["confidence"]
            )
        )


        decision["expected_recovery"] = float(
            decision["expected_recovery"]
        )


        return decision