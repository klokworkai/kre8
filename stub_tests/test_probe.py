# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

from unittest.mock import patch

import pytest

from konnekt import probe as probe_module
from konnekt.errors import KonnektError
from konnekt.models import MODEL_REGISTRY

_ALL_PROVIDERS = [family["provider"] for family in MODEL_REGISTRY.values()]


def _fake_get_api_key_factory(failing: dict[str, Exception]):
    def _fake_get_api_key(provider: str) -> str:
        if provider in failing:
            raise failing[provider]
        return f"fake-key-{provider}"

    return _fake_get_api_key


def _fake_probe_provider_factory(failing: set[str]):
    def _fake_probe_provider(provider: str, api_key: str, litellm_model: str) -> None:
        if provider in failing:
            raise Exception(f"{provider} rejected the key")

    return _fake_probe_provider


@pytest.fixture(autouse=True)
def _isolate_resolved_models(tmp_path, monkeypatch):
    monkeypatch.setattr(
        probe_module, "_RESOLVED_MODELS_PATH", tmp_path / "resolved_models.yaml"
    )


# --- single-category failures ---


def test_probe_all_no_creds_category():
    failing = {
        p: KonnektError(
            provider=p,
            model="",
            task="get_api_key",
            message="no mapping",
            category="no_creds",
        )
        for p in _ALL_PROVIDERS
    }
    fake_get_api_key = _fake_get_api_key_factory(failing)
    with (
        patch.object(probe_module, "get_api_key", side_effect=fake_get_api_key),
        patch.object(probe_module, "probe_provider"),
    ):
        with pytest.raises(KonnektError) as exc_info:
            probe_module.probe_all()

    assert exc_info.value.category == "no_creds"
    assert exc_info.value.category_breakdown == {p: "no_creds" for p in _ALL_PROVIDERS}


def test_probe_all_invalid_secret_store_category():
    failing = {
        p: KonnektError(
            provider=p,
            model="",
            task="get_secret",
            message="GCP SM unreachable",
            category="invalid_secret_store",
        )
        for p in _ALL_PROVIDERS
    }
    fake_get_api_key = _fake_get_api_key_factory(failing)
    with (
        patch.object(probe_module, "get_api_key", side_effect=fake_get_api_key),
        patch.object(probe_module, "probe_provider"),
    ):
        with pytest.raises(KonnektError) as exc_info:
            probe_module.probe_all()

    assert exc_info.value.category == "invalid_secret_store"
    assert exc_info.value.category_breakdown == {
        p: "invalid_secret_store" for p in _ALL_PROVIDERS
    }


def test_probe_all_invalid_api_keys_category():
    fake_get_api_key = _fake_get_api_key_factory({})
    fake_probe_provider = _fake_probe_provider_factory(set(_ALL_PROVIDERS))
    with (
        patch.object(probe_module, "get_api_key", side_effect=fake_get_api_key),
        patch.object(probe_module, "probe_provider", side_effect=fake_probe_provider),
    ):
        with pytest.raises(KonnektError) as exc_info:
            probe_module.probe_all()

    assert exc_info.value.category == "invalid_api_keys"
    assert exc_info.value.category_breakdown == {
        p: "invalid_api_keys" for p in _ALL_PROVIDERS
    }


# --- mixed-category failure ---


def test_probe_all_mixed_categories_no_summary_category():
    first_provider = _ALL_PROVIDERS[0]
    remaining = _ALL_PROVIDERS[1:]

    failing_secrets = {
        first_provider: KonnektError(
            provider=first_provider,
            model="",
            task="get_api_key",
            message="no mapping",
            category="no_creds",
        )
    }

    fake_get_api_key = _fake_get_api_key_factory(failing_secrets)
    fake_probe_provider = _fake_probe_provider_factory(set(remaining))
    with (
        patch.object(probe_module, "get_api_key", side_effect=fake_get_api_key),
        patch.object(probe_module, "probe_provider", side_effect=fake_probe_provider),
    ):
        with pytest.raises(KonnektError) as exc_info:
            probe_module.probe_all()

    err = exc_info.value
    assert err.category is None
    assert err.category_breakdown[first_provider] == "no_creds"
    assert all(err.category_breakdown[p] == "invalid_api_keys" for p in remaining)


# --- all-ok case does not raise ---


def test_probe_all_success_does_not_raise():
    fake_get_api_key = _fake_get_api_key_factory({})
    fake_probe_provider = _fake_probe_provider_factory(set())
    with (
        patch.object(probe_module, "get_api_key", side_effect=fake_get_api_key),
        patch.object(probe_module, "probe_provider", side_effect=fake_probe_provider),
    ):
        probe_module.probe_all()  # should not raise
