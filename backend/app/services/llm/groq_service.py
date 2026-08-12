import json
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


from app.services.llm.groq_client import chat_completion_json

class GroqService:

    def evaluate_candidate(
        self,
        job_description: str,
        evidence: list[dict],
        api_provider: str = "evalynx",
        api_key: str | None = None,
    ) -> dict:

        evidence_text = "\n\n".join(
            [
                (
                    f"[Section: {item['section']}]\n"
                    f"{item['text']}"
                )
                for item in evidence
            ]
        )

        system_prompt = """
You are a resume screening assistant.

Evaluate a candidate against the provided job description.

Use ONLY the evidence provided from the candidate's resume.
Do not invent skills, experience, education, or achievements.

Return the evaluation as valid JSON.

The JSON must contain:

- overall_score: integer from 0 to 100
- skills_score: integer from 0 to 100
- experience_score: integer from 0 to 100
- education_score: integer from 0 to 100
- strengths: list of strings
- gaps: list of strings
- recommendation: one of:
  "Strong Match",
  "Good Match",
  "Potential Match",
  "Weak Match"

Return ONLY JSON.
Do not include markdown, explanations, or code fences.

Be conservative when evidence is missing.
"""

        user_prompt = f"""
JOB DESCRIPTION:

{job_description}

CANDIDATE RESUME EVIDENCE:

{evidence_text}
"""

        return chat_completion_json(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.1,
            api_provider=api_provider,
            api_key=api_key,
        )


groq_service = GroqService()