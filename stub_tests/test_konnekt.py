# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

from unittest.mock import patch

import pytest

from konnekt.config import KonnektConfig
from konnekt.errors import KonnektError
from konnekt.models import MODEL_REGISTRY, ROLE_DEFAULTS, resolve_model
from konnekt.secrets import _secret_cache, get_secret

# --- resolve_model: role defaults ---


def test_resolve_model_role_extractor():
    provider, model = resolve_model("extractor")
    assert provider == "openai"
    assert model == "openai/gpt-4o-mini"


def test_resolve_model_role_architect():
    provider, model = resolve_model("architect")
    assert provider == "anthropic"
    assert model == "anthropic/claude-sonnet-4-6"


def test_resolve_model_role_coder():
    provider, model = resolve_model("coder")
    assert provider == "deepseek"
    assert model == "deepseek/deepseek-v4-flash"


def test_resolve_model_role_self_corrector():
    provider, model = resolve_model("self-corrector")
    assert provider == "groq"
    assert model == "groq/llama-3.1-8b-instant"


# --- resolve_model: model_select overrides ---


def test_resolve_model_select_gemini_flash():
    provider, model = resolve_model("architect", model_select=(2, 1))
    assert provider == "gemini"
    assert model == "gemini/gemini-flash-latest"


def test_resolve_model_select_gemini_pro():
    provider, model = resolve_model("coder", model_select=(2, 2))
    assert provider == "gemini"
    assert model == "gemini/gemini-pro-latest"


def test_resolve_model_select_claude_opus():
    provider, model = resolve_model("extractor", model_select=(3, 2))
    assert provider == "anthropic"
    assert model == "anthropic/claude-opus-4-6"


def test_resolve_model_select_deepseek_pro():
    provider, model = resolve_model("coder", model_select=(4, 2))
    assert provider == "deepseek"
    assert model == "deepseek/deepseek-v4-pro"


def test_resolve_model_select_groq_versatile():
    provider, model = resolve_model("self-corrector", model_select=(5, 2))
    assert provider == "groq"
    assert model == "groq/llama-3.3-70b-versatile"


# --- resolve_model: error cases ---


def test_resolve_model_unknown_role_raises():
    with pytest.raises(KonnektError) as exc_info:
        resolve_model("unknown-role")
    assert "unknown-role" in exc_info.value.message


def test_resolve_model_invalid_family_raises():
    with pytest.raises(KonnektError) as exc_info:
        resolve_model("extractor", model_select=(99, 1))
    assert "99" in exc_info.value.message


def test_resolve_model_invalid_tier_raises():
    with pytest.raises(KonnektError) as exc_info:
        resolve_model("extractor", model_select=(1, 9))
    assert "9" in exc_info.value.message


# --- MODEL_REGISTRY and ROLE_DEFAULTS structure ---


def test_all_role_defaults_are_valid():
    for role, (family, tier) in ROLE_DEFAULTS.items():
        provider, model = resolve_model(role)
        assert "/" in model
        assert provider == MODEL_REGISTRY[family]["provider"]


def test_registry_covers_all_five_families():
    assert set(MODEL_REGISTRY.keys()) == {1, 2, 3, 4, 5}


# --- KonnektConfig ---


def test_konnekt_config_defaults():
    config = KonnektConfig()
    assert config.temperature == 0.2
    assert config.max_tokens == 2000
    assert config.timeout == 30


# --- KonnektError ---


def test_konnekt_error_str_format():
    err = KonnektError(
        provider="anthropic", model="claude-sonnet-4-6", task="think", message="timeout"
    )
    assert str(err) == "[konnekt] anthropic/claude-sonnet-4-6 (think): timeout"


# --- get_secret: cache hit ---


def test_get_secret_cache_hit_skips_gcp():
    _secret_cache["TEST_CACHED_KEY"] = "cached-value"

    with patch(
        "konnekt.secrets._load_kre8_config",
        side_effect=AssertionError("cache miss — _load_kre8_config called"),
    ):
        result = get_secret("TEST_CACHED_KEY")

    assert result == "cached-value"
    del _secret_cache["TEST_CACHED_KEY"]


def test_get_secret_not_found_raises():
    key = "NONEXISTENT_KEY_XYZ"
    _secret_cache.pop(key, None)

    with (
        patch("konnekt.secrets._get_gcp_project_id", return_value="fake-project"),
        patch("google.cloud.secretmanager", create=True) as mock_sm,
    ):
        client = mock_sm.SecretManagerServiceClient.return_value
        client.access_secret_version.side_effect = Exception(
            f"secret '{key}' not found"
        )
        with pytest.raises(KonnektError) as exc_info:
            get_secret(key)

    assert exc_info.value.provider == "secrets"
    assert key in exc_info.value.message
    assert exc_info.value.category == "invalid_secret_store"


# --- KonnektError categories: secrets.py raise sites ---


def test_load_kre8_config_missing_file_is_no_creds():
    from konnekt.secrets import _load_kre8_config

    with patch("konnekt.secrets._SECRETS_CONFIG_PATH", "/nonexistent/secrets.yaml"):
        with pytest.raises(KonnektError) as exc_info:
            _load_kre8_config()

    assert exc_info.value.category == "no_creds"


def test_get_provider_secret_map_empty_is_no_creds():
    from konnekt.secrets import _get_provider_secret_map

    fake_config = {"konnekt": {"secrets": {}}}
    with patch("konnekt.secrets._load_kre8_config", return_value=fake_config):
        with pytest.raises(KonnektError) as exc_info:
            _get_provider_secret_map()

    assert exc_info.value.category == "no_creds"


def test_get_gcp_project_id_missing_is_no_creds():
    from konnekt.secrets import _get_gcp_project_id

    with patch("konnekt.secrets._load_kre8_config", return_value={"gcp": {}}):
        with pytest.raises(KonnektError) as exc_info:
            _get_gcp_project_id()

    assert exc_info.value.category == "no_creds"


def test_get_api_key_missing_mapping_is_no_creds():
    from konnekt.secrets import get_api_key

    fake_map = {"openai": "some-secret"}
    with patch("konnekt.secrets._get_provider_secret_map", return_value=fake_map):
        with pytest.raises(KonnektError) as exc_info:
            get_api_key("anthropic")

    assert exc_info.value.category == "no_creds"
