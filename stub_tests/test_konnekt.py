from unittest.mock import MagicMock, patch

import pytest

from konnekt.config import KonnektConfig
from konnekt.errors import KonnektError
from konnekt.models import MODELS, resolve_model
from konnekt.secrets import _secret_cache, get_secret


# --- resolve_model ---

def test_resolve_model_valid():
    assert resolve_model("gpt-4o-mini") == "openai/gpt-4o-mini"
    assert resolve_model("claude-sonnet-4-6") == "anthropic/claude-sonnet-4-6"
    assert resolve_model("claude-opus-4-6") == "anthropic/claude-opus-4-6"
    assert resolve_model("deepseek-v4-flash") == "deepseek/deepseek-v4-flash"
    assert resolve_model("llama-3.3-70b-versatile") == "groq/llama-3.3-70b-versatile"


def test_resolve_model_unknown_raises():
    with pytest.raises(KonnektError) as exc_info:
        resolve_model("not-a-real-model")
    err = exc_info.value
    assert err.provider == "konnekt"
    assert err.model == "not-a-real-model"
    assert err.task == "resolve_model"


# --- KonnektConfig ---

def test_konnekt_config_defaults():
    config = KonnektConfig()
    assert config.temperature == 0.2
    assert config.max_tokens == 2000
    assert config.timeout == 30


def test_konnekt_config_override():
    config = KonnektConfig(temperature=0.8, max_tokens=1000, timeout=60)
    assert config.temperature == 0.8
    assert config.max_tokens == 1000
    assert config.timeout == 60


# --- KonnektError ---

def test_konnekt_error_str_format():
    err = KonnektError(
        provider="anthropic",
        model="claude-sonnet-4-6",
        task="think",
        message="timeout",
    )
    assert str(err) == "[konnekt] anthropic/claude-sonnet-4-6 (think): timeout"


def test_konnekt_error_fields():
    err = KonnektError(provider="openai", model="gpt-4o-mini", task="extract", message="rate limit")
    assert err.provider == "openai"
    assert err.model == "gpt-4o-mini"
    assert err.task == "extract"
    assert err.message == "rate limit"


# --- get_secret cache ---

def test_get_secret_cache_hit_skips_gcp():
    _secret_cache["TEST_CACHED_KEY"] = "cached-value"

    # GCP import should never be reached on a cache hit — patch the import to
    # confirm it's never called by having it raise if invoked
    with patch("konnekt.secrets.os.environ.get", side_effect=AssertionError("os.environ.get called — cache miss occurred")):
        result = get_secret("TEST_CACHED_KEY")

    assert result == "cached-value"

    del _secret_cache["TEST_CACHED_KEY"]


def test_get_secret_not_found_raises():
    key = "NONEXISTENT_KEY_XYZ"
    _secret_cache.pop(key, None)

    with patch("konnekt.secrets.os.environ.get", return_value=None):
        with patch.dict("os.environ", {}, clear=False):
            with pytest.raises(KonnektError) as exc_info:
                get_secret(key)

    err = exc_info.value
    assert err.provider == "secrets"
    assert key in err.message
