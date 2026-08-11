"""
Central application settings, loaded once from environment variables.

Never expose GROQ_API_KEY to the frontend.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Groq
    groq_api_key: str = ""

    # LLM
    groq_model: str = "llama-3.3-70b-versatile"

    # Speech-to-Text
    groq_stt_model: str = "whisper-large-v3-turbo"

    # Text-to-Speech
    groq_tts_model: str = "canopylabs/orpheus-v1-english"
    groq_tts_voice: str = "hannah"

    # Frontend
    frontend_origin: str = "http://localhost:5173"

    # Database
    database_url: str = "postgresql://postgres:pravinwin4@127.0.0.1:5433/evalynx"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()