"""
Thin wrapper around the Groq client for text generation.

This is the ONLY place that should hold a Groq client instance for chat
completions. speech_service.py reuses this same client for STT/TTS so we
never initialize the SDK twice.
"""
import json
import logging
from typing import Any

from groq import (
    Groq,
    APIStatusError,
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_settings = get_settings()
_client: Groq | None = None


class GroqServiceError(Exception):
    """Raised when the Groq API fails or returns something unusable."""
    def __init__(self, message: str, code: str = "AI_REQUEST_FAILED"):
        super().__init__(message)
        self.code = code


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
            "console.groq.com and paste it without formatting.",
            code="INVALID_API_KEY"
        )
    if not key:
        raise GroqServiceError("Please enter your Groq API key.", code="MISSING_API_KEY")
    return key


def get_groq_client(api_provider: str, api_key: str | None = None) -> Groq:
    """Lazily create and reuse a single Groq client, or create a new one if api_provider is user."""
    if api_provider == "user":
        if not api_key or not api_key.strip():
            raise GroqServiceError("Please enter your Groq API key.", code="MISSING_API_KEY")
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
    api_provider: str = "evalynx",
    api_key: str | None = None,
) -> str:
    """Run a chat completion and return the raw text content."""
    client = get_groq_client(api_provider, api_key)
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
    except AuthenticationError as exc:
        is_custom = api_provider == "user"
        msg = "Invalid Groq API key. Please check your key and try again." if is_custom else "Evalynx AI authentication failed. The configured API key may be invalid or expired."
        raise GroqServiceError(msg, code="INVALID_API_KEY") from exc
    except RateLimitError as exc:
        is_custom = api_provider == "user"
        msg = "Your Groq API key has reached its rate limit. Please try again later." if is_custom else "Evalynx AI limit has been reached. Please try again later or use your own Groq API key."
        raise GroqServiceError(msg, code="RATE_LIMITED") from exc
    except APITimeoutError as exc:
        raise GroqServiceError("Unable to reach the AI service due to a timeout. Please try again in a moment.", code="AI_TIMEOUT") from exc
    except APIConnectionError as exc:
        raise GroqServiceError("Unable to connect to the AI service. Please try again.", code="AI_SERVICE_UNAVAILABLE") from exc
    except APIStatusError as exc:
        is_custom = api_provider == "user"
        if exc.status_code == 403 or "quota" in str(exc).lower() or "limit" in str(exc).lower():
            msg = "Your Groq API key has reached its usage limit." if is_custom else "Evalynx AI limit has been reached. Please try again later or use your own Groq API key."
            raise GroqServiceError(msg, code="QUOTA_EXCEEDED") from exc
        raise GroqServiceError(f"AI service error: {exc.message}", code="AI_REQUEST_FAILED") from exc
    except Exception as exc:  # network / auth / rate limit / etc.
        logger.exception("Groq chat completion failed")
        raise GroqServiceError(str(exc), code="AI_REQUEST_FAILED") from exc

    content = response.choices[0].message.content
    if not content:
        raise GroqServiceError("Groq returned an empty response", code="AI_REQUEST_FAILED")
    return content


def chat_completion_json(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.4,
    max_tokens: int = 700,
    api_provider: str = "evalynx",
    api_key: str | None = None,
) -> dict[str, Any]:
    """Run a chat completion and parse the result as JSON.

    Falls back to extracting the first {...} block if the model wraps the
    JSON in prose, so a minor formatting slip doesn't crash the interview.
    """
    raw = chat_completion(
        messages, temperature=temperature, max_tokens=max_tokens, json_mode=True, api_provider=api_provider, api_key=api_key
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
        raise GroqServiceError("Groq returned malformed JSON", code="AI_REQUEST_FAILED")