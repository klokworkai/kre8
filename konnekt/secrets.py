import os

from dotenv import load_dotenv

from konnekt.errors import KonnektError

load_dotenv()

_secret_cache: dict[str, str] = {}

PROVIDER_SECRET_MAP: dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "groq": "GROQ_API_KEY",
}


def get_secret(name: str) -> str:
    if name in _secret_cache:
        return _secret_cache[name]

    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        try:
            from google.cloud import secretmanager

            project_id = os.environ["GCP_PROJECT_ID"]
            client = secretmanager.SecretManagerServiceClient()
            secret_path = f"projects/{project_id}/secrets/{name}/versions/latest"
            response = client.access_secret_version(request={"name": secret_path})
            value = response.payload.data.decode("utf-8").strip()
            _secret_cache[name] = value
            return value
        except Exception:
            pass

    value = os.environ.get(name)
    if value:
        _secret_cache[name] = value
        return value

    raise KonnektError(
        provider="secrets",
        model="",
        task="get_secret",
        message=f"Secret '{name}' not found in GCP Secret Manager or environment",
    )


def get_api_key(provider: str) -> str:
    secret_name = PROVIDER_SECRET_MAP.get(provider)
    if not secret_name:
        raise KonnektError(
            provider=provider,
            model="",
            task="get_api_key",
            message=f"No secret mapping for provider '{provider}'",
        )
    return get_secret(secret_name)
