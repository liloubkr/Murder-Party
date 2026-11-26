import pytest
from pydantic import ValidationError

from alibi.config import GROQ_BASE_URL, Settings


def _settings(monkeypatch: pytest.MonkeyPatch, **env: str) -> Settings:
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return Settings(_env_file=None)


def test_defaults_without_env(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = _settings(monkeypatch)
    assert settings.llm_provider == "groq"
    assert settings.llm_temperature == 0.4
    assert settings.max_regenerations == 1
    assert settings.groq_api_key is None


def test_ollama_provider_selects_ollama_model_and_url(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = _settings(
        monkeypatch, LLM_PROVIDER="ollama", OLLAMA_MODEL="llama3.2:3b", GROQ_MODEL="other"
    )
    assert settings.llm_model == "llama3.2:3b"
    assert settings.llm_base_url == "http://localhost:11434/v1"


def test_groq_provider_uses_groq_url(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = _settings(monkeypatch, LLM_PROVIDER="groq", GROQ_MODEL="some-model")
    assert settings.llm_model == "some-model"
    assert settings.llm_base_url == GROQ_BASE_URL


def test_cache_flag_accepts_on_off(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _settings(monkeypatch, LLM_CACHE="off").llm_cache is False
    assert _settings(monkeypatch, LLM_CACHE="on").llm_cache is True


def test_secret_is_not_exposed_in_repr(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = _settings(monkeypatch, GROQ_API_KEY="sk-test-value")
    assert "sk-test-value" not in repr(settings)


@pytest.mark.parametrize("env", [{"LLM_PROVIDER": "openai"}, {"LLM_TEMPERATURE": "1.5"}])
def test_invalid_values_are_rejected(monkeypatch: pytest.MonkeyPatch, env: dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        _settings(monkeypatch, **env)
