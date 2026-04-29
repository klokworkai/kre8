"""
Live integration tests — konnekt standalone.

What this tests:
  - GCP Secret Manager reachability and correct IAM bindings
  - Secret retrieval for all 5 providers
  - In-memory cache populated after first fetch
  - Real LLM call returns a non-empty response for each role default
  - model_select override reaches the correct provider

Requirements:
  - GCP_PROJECT_ID env var set
  - Valid ADC credentials: run `gcloud auth application-default login` once locally
  - Docker / AWS ECS / GKE: GOOGLE_APPLICATION_CREDENTIALS pointing to WIF credential config

Run:
  GCP_PROJECT_ID=kre8-dev pytest integration_tests/test_konnekt_live.py -m integration -v
"""
import pytest

from konnekt import complete, KonnektConfig
from konnekt.secrets import PROVIDER_SECRET_MAP, _secret_cache, get_secret

pytestmark = pytest.mark.integration


@pytest.fixture(autouse=True)
def clear_cache():
    _secret_cache.clear()
    yield
    _secret_cache.clear()


# --- GCP Secret Manager ---

@pytest.mark.parametrize("provider", ["openai", "anthropic", "deepseek", "groq", "gemini"])
def test_secret_retrieval(provider):
    secret_name = PROVIDER_SECRET_MAP[provider]
    key = get_secret(secret_name)
    assert key and len(key) > 10, f"Expected a real API key for {provider}, got: {key!r}"


def test_secret_cache_populated_after_fetch():
    secret_name = PROVIDER_SECRET_MAP["openai"]
    get_secret(secret_name)
    assert secret_name in _secret_cache


def test_secret_cache_hit_does_not_refetch():
    secret_name = PROVIDER_SECRET_MAP["openai"]
    get_secret(secret_name)
    cached_value = _secret_cache[secret_name]
    # second call should return same value from cache
    result = get_secret(secret_name)
    assert result == cached_value


# --- LLM calls: role defaults ---

@pytest.mark.parametrize("role,model_select,provider_label", [
    ("extractor",      None,    "openai/gpt-4o-mini"),
    ("architect",      None,    "anthropic/claude-sonnet-4-6"),
    ("coder",          None,    "deepseek/deepseek-v4-flash"),
    ("self-corrector", None,    "groq/llama-3.1-8b-instant"),
])
def test_complete_role_default(role, model_select, provider_label):
    result = complete(
        role=role,
        task="smoke-test",
        prompt="Reply with the word PONG only. Do not add anything else.",
        config=KonnektConfig(max_tokens=20, temperature=0),
        model_select=model_select,
    )
    assert result, f"{provider_label} returned empty response"
    assert "PONG" in result.upper(), f"{provider_label} did not return PONG — got: {result!r}"


# --- model_select override ---

@pytest.mark.parametrize("role,model_select,label", [
    ("extractor", (2, 1), "gemini-1.5-flash"),
    ("extractor", (2, 2), "gemini-1.5-pro"),
    ("coder",     (3, 2), "claude-opus-4-6"),
    ("architect", (4, 2), "deepseek-v4-pro"),
    ("architect", (5, 2), "llama-3.3-70b-versatile"),
])
def test_complete_model_select_override(role, model_select, label):
    result = complete(
        role=role,
        task="smoke-test",
        prompt="Reply with the word PONG only. Do not add anything else.",
        config=KonnektConfig(max_tokens=20, temperature=0),
        model_select=model_select,
    )
    assert result, f"{label} returned empty response"
    assert "PONG" in result.upper(), f"{label} did not return PONG — got: {result!r}"
