"""
Speech-to-text and text-to-speech, both backed by Groq.

Reuses the same Groq client from groq_service.py rather than creating a
second SDK instance.
"""
import logging

from app.core.config import get_settings
from app.services.llm.groq_client import GroqServiceError, get_groq_client

logger = logging.getLogger(__name__)
_settings = get_settings()


def transcribe_audio(audio_bytes: bytes, filename: str = "answer.webm", api_key: str | None = None) -> str:
    """Send recorded candidate audio to Groq Whisper and return the transcript."""
    client = get_groq_client(api_key)
    try:
        result = client.audio.transcriptions.create(
            file=(filename, audio_bytes),
            model=_settings.groq_stt_model,
            response_format="json",
        )
    except Exception as exc:
        logger.exception("Groq transcription failed")
        raise GroqServiceError(f"Transcription failed: {exc}") from exc

    text = getattr(result, "text", "").strip()
    if not text:
        raise GroqServiceError("Transcription returned no speech")
    return text


def synthesize_speech(text: str, api_key: str | None = None) -> bytes:
    """Convert interviewer question text into spoken audio via Groq TTS."""
    client = get_groq_client(api_key)
    try:
        response = client.audio.speech.create(
            model=_settings.groq_tts_model,
            voice=_settings.groq_tts_voice,
            input=text,
            response_format="wav",
        )
    except Exception as exc:
        logger.exception("Groq TTS failed")
        raise GroqServiceError(f"Speech synthesis failed: {exc}") from exc

    # The SDK returns a streamable response; read it fully into bytes.
    if hasattr(response, "read"):
        return response.read()
    return bytes(response)
