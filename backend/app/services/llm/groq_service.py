import json
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class GroqService:
    def __init__(self):
        self._builtin_api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

    def _get_client(self, api_key: str | None = None) -> Groq:
        """Return a Groq client using the provided key, or the built-in key."""
        key = api_key or self._builtin_api_key
        if not key:
            raise ValueError(
                "GROQ_API_KEY is not configured and no API key was provided."
            )
        return Groq(api_key=key)

    def evaluate_candidate(
        self,
        job_description: str,
        evidence: list[dict],
        api_key: str | None = None,
    ) -> dict:

        client = self._get_client(api_key)

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

        response = client.chat.completions.create(
            model=self.model,
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
            response_format={
                "type": "json_object"
            },
        )

        content = response.choices[0].message.content

        return json.loads(content)


groq_service = GroqService()