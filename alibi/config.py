"""Application settings loaded from environment variables and an optional `.env` file."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Provider = Literal["groq", "ollama"]

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


class Settings(BaseSettings):
    """Typed runtime configuration.

    Missing secrets are allowed at load time so that tests and CI run without them;
    the LLM client checks for the key when it is actually built.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_provider: Provider = "groq"
    groq_api_key: SecretStr | None = None
    groq_model: str = ""
    ollama_model: str = ""
    ollama_base_url: str = "http://localhost:11434/v1"
    llm_temperature: float = Field(default=0.4, ge=0.0, le=1.0)
    llm_timeout_seconds: float = Field(default=30.0, gt=0)
    max_regenerations: int = Field(default=1, ge=0)
    llm_cache: bool = True
    llm_cache_dir: Path = Path(".cache/llm")
    db_path: Path = Path(".data/alibi.db")
    intent_model_path: Path = Path("models/intent.joblib")

    @property
    def llm_model(self) -> str:
        """Return the model identifier of the active provider."""
        return self.groq_model if self.llm_provider == "groq" else self.ollama_model

    @property
    def llm_base_url(self) -> str:
        """Return the OpenAI-compatible base URL of the active provider."""
        return GROQ_BASE_URL if self.llm_provider == "groq" else self.ollama_base_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings instance (loaded once)."""
    return Settings()
