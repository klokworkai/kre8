# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

from pathlib import Path

import yaml

from konnekt.errors import KonnektError

_secret_cache: dict[str, str] = {}

_SECRETS_CONFIG_PATH = Path(__file__).parent.parent / "secrets.yaml"


def _read_config_file() -> dict:
    """Raw secrets.yaml read — no error wrapping. Raises FileNotFoundError as-is."""
    with open(_SECRETS_CONFIG_PATH) as f:
        return yaml.safe_load(f) or {}


def _load_kre8_config() -> dict:
    try:
        return _read_config_file()
    except FileNotFoundError:
        raise KonnektError(
            provider="secrets",
            model="",
            task="load_config",
            message=(
                f"secrets.yaml not found at {_SECRETS_CONFIG_PATH} — "
                "copy secrets.yaml.example and fill in your values"
            ),
            category="no_creds",
        )
    except Exception as e:
        raise KonnektError(
            provider="secrets",
            model="",
            task="load_config",
            message=f"Failed to parse secrets.yaml: {e}",
        )


def get_role_overrides() -> dict[str, tuple[int, int]]:
    """Load optional konnekt.role_overrides from secrets.yaml.

    role_overrides is opt-in — a missing secrets.yaml or a missing/empty
    role_overrides key both resolve to {} (fall through to ROLE_DEFAULTS),
    not an error. Only get_api_key/probe_all hard-fail on missing config.
    """
    try:
        config = _read_config_file()
    except FileNotFoundError:
        return {}
    overrides = (config.get("konnekt") or {}).get("role_overrides") or {}
    return {role: tuple(value) for role, value in overrides.items()}


def _get_provider_secret_map() -> dict[str, str]:
    config = _load_kre8_config()
    secrets = (config.get("konnekt") or {}).get("secrets") or {}
    if not secrets:
        raise KonnektError(
            provider="secrets",
            model="",
            task="load_config",
            message=(
                "secrets.yaml is missing konnekt.secrets — check secrets.yaml.example"
            ),
            category="no_creds",
        )
    return secrets


def _get_gcp_project_id() -> str:
    config = _load_kre8_config()
    project_id = (config.get("gcp") or {}).get("project_id")
    if not project_id:
        raise KonnektError(
            provider="secrets",
            model="",
            task="load_config",
            message=(
                "secrets.yaml is missing gcp.project_id — check secrets.yaml.example"
            ),
            category="no_creds",
        )
    return project_id


def get_secret(name: str) -> str:
    if name in _secret_cache:
        return _secret_cache[name]
    try:
        from google.cloud import secretmanager

        project_id = _get_gcp_project_id()
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
            provider="secrets",
            model="",
            task="get_secret",
            message=f"GCP Secret Manager fetch failed for '{name}': {e}",
            category="invalid_secret_store",
        )


def get_api_key(provider: str) -> str:
    secret_map = _get_provider_secret_map()
    secret_name = secret_map.get(provider)
    if not secret_name:
        raise KonnektError(
            provider=provider,
            model="",
            task="get_api_key",
            message=(
                f"No secret mapping for provider '{provider}' "
                "in secrets.yaml konnekt.secrets"
            ),
            category="no_creds",
        )
    return get_secret(secret_name)
