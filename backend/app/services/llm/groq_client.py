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


class GroqServiceError(Exception):
    """Raised when the Groq API fails or returns something unusable."""


def sanitize_api_key(key: str) -> str:
    """
    Strip whitespace and validate that the key is pure ASCII.

    Pasting from some OS/browser clipboard converts hyphens to em-dashes
    (U+2014) or adds other non-ASCII characters, which causes httpx to raise
    a UnicodeEncodeError when it tries to set the Authorization header.
    We catch this early and give the user a clear, actionable error message.
    """
    key = key.strip()
    try:
        key.encode("ascii")
    except UnicodeEncodeError:
        bad = {ch for ch in key if ord(ch) > 127}
        bad_repr = ", ".join(f"U+{ord(c):04X} ({c!r})" for c in sorted(bad))
        raise GroqServiceError(
            f"Your Groq API key contains non-ASCII characters: {bad_repr}. "
            "This usually happens when autocorrect replaces hyphens with "
            "em-dashes. Please copy the key again directly from "
            "console.groq.com and paste it without formatting."
        )
    if not key:
        raise GroqServiceError("Groq API key is empty.")
    return key


def get_groq_client(api_key: str | None = None) -> Groq:
    """Lazily create and reuse a single Groq client, or create a new one if api_key is provided."""
    if api_key:
        clean_key = sanitize_api_key(api_key)
        return Groq(api_key=clean_key)

    global _client
    if _client is None:
        if not _settings.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your backend .env file."
            )
        _client = Groq(api_key=_settings.groq_api_key)
    return _client


def chat_completion(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.6,
    max_tokens: int = 700,
    json_mode: bool = False,
    api_key: str | None = None,
) -> str:
    """Run a chat completion and return the raw text content."""
    client = get_groq_client(api_key)
    try:
        response = client.chat.completions.create(
            model=_settings.groq_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"} if json_mode else None,
        )
    except GroqServiceError:
        raise  # re-raise sanitize errors without wrapping
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
    api_key: str | None = None,
) -> dict[str, Any]:
    """Run a chat completion and parse the result as JSON.

    Falls back to extracting the first {...} block if the model wraps the
    JSON in prose, so a minor formatting slip doesn't crash the interview.
    """
    raw = chat_completion(
        messages, temperature=temperature, max_tokens=max_tokens, json_mode=True, api_key=api_key
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