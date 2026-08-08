"""
Thin wrapper around the Groq client for text generation.

This is the ONLY place that should hold a Groq client instance for chat
completions. speech_service.py reuses this same client for STT/TTS so we
never initialize the SDK twice.
"""
import json
import logging
from typing import Any

from groq import Groq

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_settings = get_settings()
_client: Groq | None = None


def get_groq_client() -> Groq:
    """Lazily create and reuse a single Groq client for the process."""
    global _client
    if _client is None:
        if not _settings.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your backend .env file."
            )
        _client = Groq(api_key=_settings.groq_api_key)
    return _client


class GroqServiceError(Exception):
    """Raised when the Groq API fails or returns something unusable."""


def chat_completion(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.6,
    max_tokens: int = 700,
    json_mode: bool = False,
) -> str:
    """Run a chat completion and return the raw text content."""
    client = get_groq_client()
    try:
        response = client.chat.completions.create(
            model=_settings.groq_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"} if json_mode else None,
        )
    except Exception as exc:  # network / auth / rate limit / etc.
        logger.exception("Groq chat completion failed")
        raise GroqServiceError(str(exc)) from exc

    content = response.choices[0].message.content
    if not content:
        raise GroqServiceError("Groq returned an empty response")
    return content


def chat_completion_json(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.4,
    max_tokens: int = 700,
) -> dict[str, Any]:
    """Run a chat completion and parse the result as JSON.

    Falls back to extracting the first {...} block if the model wraps the
    JSON in prose, so a minor formatting slip doesn't crash the interview.
    """
    raw = chat_completion(
        messages, temperature=temperature, max_tokens=max_tokens, json_mode=True
    )
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw[start : end + 1])
            except json.JSONDecodeError:
                pass
        logger.error("Could not parse JSON from Groq response: %s", raw)
        raise GroqServiceError("Groq returned malformed JSON")