"""
Mock integration tests for konnekt.complete().

These tests exercise the full call chain end-to-end:
  resolve_model → get_api_key → get_secret (GCP SM mocked) → litellm.completion (mocked)

No real credentials or LLM calls are made. Replace mock targets with real
calls once WIF is configured and a runtime identity is available.
"""
from unittest.mock import MagicMock, patch

import google.cloud.secretmanager
import pytest

from konnekt import complete, KonnektConfig
from konnekt.errors import KonnektError


def _make_litellm_response(content: str) -> MagicMock:
    response = MagicMock()
    response.choices[0].message.content = content
    return response


def _patch_gcp(secret_values: dict[str, str]):
    """Context manager that patches GCP Secret Manager with a fixed secret map."""
    mock_client = MagicMock()

    def fake_access(request):
        name = request["name"]
        secret_id = name.split("/secrets/")[1].split("/versions")[0]
        if secret_id not in secret_values:
            raise Exception(f"Secret '{secret_id}' not found")
        mock_response = MagicMock()
        mock_response.payload.data = secret_values[secret_id].encode()
        return mock_response

    mock_client.access_secret_version.side_effect = fake_access
    return mock_client


# --- full chain: default role models ---

@pytest.mark.parametrize("role,expected_model", [
    ("extractor",      "openai/gpt-4o-mini"),
    ("architect",      "anthropic/claude-sonnet-4-6"),
    ("coder",          "deepseek/deepseek-v4-flash"),
    ("self-corrector", "groq/llama-3.1-8b-instant"),
])
def test_complete_default_roles(role, expected_model, monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "kre8-dev")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "/fake/wif-config.json")

    secret_map = {
        "kre8-konnekt-dev-openai":    "sk-openai-fake",
        "kre8-konnekt-dev-anthropic": "sk-anthropic-fake",
        "kre8-konnekt-dev-deepseek":  "sk-deepseek-fake",
        "kre8-konnekt-dev-groq":      "sk-groq-fake",
    }
    mock_client = _patch_gcp(secret_map)

    # clear cache between tests
    from konnekt.secrets import _secret_cache
    _secret_cache.clear()

    captured = {}

    def fake_completion(**kwargs):
        captured["model"] = kwargs["model"]
        captured["api_key"] = kwargs["api_key"]
        return _make_litellm_response("PONG")

    with patch.object(google.cloud.secretmanager, "SecretManagerServiceClient", return_value=mock_client):
        with patch("litellm.completion", side_effect=fake_completion):
            result = complete(role, "smoke-test", "Reply PONG.", KonnektConfig(max_tokens=10))

    assert result == "PONG"
    assert captured["model"] == expected_model


# --- model_select override ---

def test_complete_model_select_gemini_flash(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "kre8-dev")

    from konnekt.secrets import _secret_cache
    _secret_cache.clear()

    secret_map = {"kre8-konnekt-dev-gemini": "gemini-fake-key"}
    mock_client = _patch_gcp(secret_map)

    captured = {}

    def fake_completion(**kwargs):
        captured["model"] = kwargs["model"]
        return _make_litellm_response("PONG")

    with patch.object(google.cloud.secretmanager, "SecretManagerServiceClient", return_value=mock_client):
        with patch("litellm.completion", side_effect=fake_completion):
            result = complete(
                "architect", "think", "Reply PONG.",
                KonnektConfig(), model_select=(2, 1),
            )

    assert result == "PONG"
    assert captured["model"] == "gemini/gemini-flash-latest"


def test_complete_model_select_claude_opus(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "kre8-dev")

    from konnekt.secrets import _secret_cache
    _secret_cache.clear()

    secret_map = {"kre8-konnekt-dev-anthropic": "sk-anthropic-fake"}
    mock_client = _patch_gcp(secret_map)

    captured = {}

    def fake_completion(**kwargs):
        captured["model"] = kwargs["model"]
        return _make_litellm_response("PONG")

    with patch.object(google.cloud.secretmanager, "SecretManagerServiceClient", return_value=mock_client):
        with patch("litellm.completion", side_effect=fake_completion):
            result = complete(
                "architect", "think", "Reply PONG.",
                KonnektConfig(), model_select=(3, 2),
            )

    assert result == "PONG"
    assert captured["model"] == "anthropic/claude-opus-4-6"


# --- GCP SM failure → KonnektError ---

def test_complete_gcp_secret_fetch_failure_raises(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "kre8-dev")

    from konnekt.secrets import _secret_cache
    _secret_cache.clear()

    mock_client = MagicMock()
    mock_client.access_secret_version.side_effect = Exception("GCP SM unreachable")

    with patch.object(google.cloud.secretmanager, "SecretManagerServiceClient", return_value=mock_client):
        with pytest.raises(KonnektError) as exc_info:
            complete("extractor", "extract", "test", KonnektConfig())

    assert exc_info.value.provider == "secrets"
    assert "GCP SM unreachable" in exc_info.value.message


# --- LiteLLM failure → KonnektError ---

def test_complete_litellm_failure_raises(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "kre8-dev")

    from konnekt.secrets import _secret_cache
    _secret_cache.clear()

    secret_map = {"kre8-konnekt-dev-openai": "sk-openai-fake"}
    mock_client = _patch_gcp(secret_map)

    with patch.object(google.cloud.secretmanager, "SecretManagerServiceClient", return_value=mock_client):
        with patch("litellm.completion", side_effect=Exception("provider timeout")):
            with pytest.raises(KonnektError) as exc_info:
                complete("extractor", "extract", "test", KonnektConfig())

    err = exc_info.value
    assert err.provider == "openai"
    assert err.task == "extract"
    assert "provider timeout" in err.message


# --- config values passed through to litellm ---

def test_complete_passes_config_to_litellm(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "kre8-dev")

    from konnekt.secrets import _secret_cache
    _secret_cache.clear()

    secret_map = {"kre8-konnekt-dev-openai": "sk-openai-fake"}
    mock_client = _patch_gcp(secret_map)

    captured = {}

    def fake_completion(**kwargs):
        captured.update(kwargs)
        return _make_litellm_response("ok")

    config = KonnektConfig(temperature=0.9, max_tokens=500, timeout=45)

    with patch.object(google.cloud.secretmanager, "SecretManagerServiceClient", return_value=mock_client):
        with patch("litellm.completion", side_effect=fake_completion):
            complete("extractor", "extract", "test", config)

    assert captured["temperature"] == 0.9
    assert captured["max_tokens"] == 500
    assert captured["timeout"] == 45
