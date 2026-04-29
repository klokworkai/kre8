import os

from dotenv import load_dotenv

from konnekt.errors import KonnektError

load_dotenv()  # picks up GCP_PROJECT_ID only — no API keys in .env

_secret_cache: dict[str, str] = {}

PROVIDER_SECRET_MAP: dict[str, str] = {
    "openai":    "kre8-konnekt-dev-openai",
    "gemini":    "kre8-konnekt-dev-gemini",
    "anthropic": "kre8-konnekt-dev-anthropic",
    "deepseek":  "kre8-konnekt-dev-deepseek",
    "groq":      "kre8-konnekt-dev-groq",
}


def get_secret(name: str) -> str:
    if name in _secret_cache:
        return _secret_cache[name]
    try:
        from google.cloud import secretmanager
        project_id = os.environ["GCP_PROJECT_ID"]
        client = secretmanager.SecretManagerServiceClient()
        path = f"projects/{project_id}/secrets/{name}/versions/latest"
        response = client.access_secret_version(request={"name": path})
        value = response.payload.data.decode("utf-8").strip()
        _secret_cache[name] = value
        return value
    except KonnektError:
        raise
    except Exception as e:
        raise KonnektError(
            provider="secrets", model="", task="get_secret",
            message=f"GCP Secret Manager fetch failed for '{name}': {e}",
        )


def get_api_key(provider: str) -> str:
    secret_name = PROVIDER_SECRET_MAP.get(provider)
    if not secret_name:
        raise KonnektError(
            provider=provider, model="", task="get_api_key",
            message=f"No secret mapping for provider '{provider}'",
        )
    return get_secret(secret_name)
