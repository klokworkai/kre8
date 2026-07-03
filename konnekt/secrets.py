# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

from pathlib import Path

import yaml

from konnekt.errors import KonnektError

_secret_cache: dict[str, str] = {}

_KRE8_CONFIG_PATH = Path(__file__).parent.parent / "kre8.yaml"


def _load_kre8_config() -> dict:
    try:
        with open(_KRE8_CONFIG_PATH) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        raise KonnektError(
            provider="secrets",
            model="",
            task="load_config",
            message=(
                f"kre8.yaml not found at {_KRE8_CONFIG_PATH} — "
                "copy kre8.yaml.example and fill in your values"
            ),
        )
    except Exception as e:
        raise KonnektError(
            provider="secrets",
            model="",
            task="load_config",
            message=f"Failed to parse kre8.yaml: {e}",
        )


def _get_provider_secret_map() -> dict[str, str]:
    config = _load_kre8_config()
    secrets = config.get("konnekt", {}).get("secrets", {})
    if not secrets:
        raise KonnektError(
            provider="secrets",
            model="",
            task="load_config",
            message="kre8.yaml is missing konnekt.secrets — check kre8.yaml.example",
        )
    return secrets


def _get_gcp_project_id() -> str:
    config = _load_kre8_config()
    project_id = config.get("gcp", {}).get("project_id")
    if not project_id:
        raise KonnektError(
            provider="secrets",
            model="",
            task="load_config",
            message="kre8.yaml is missing gcp.project_id — check kre8.yaml.example",
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
                "in kre8.yaml konnekt.secrets"
            ),
        )
    return get_secret(secret_name)
