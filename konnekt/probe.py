# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

import logging
from datetime import UTC, datetime
from pathlib import Path

import litellm
import yaml

from konnekt.errors import KonnektError
from konnekt.models import MODEL_REGISTRY, ROLE_DEFAULTS
from konnekt.secrets import get_api_key

logger = logging.getLogger(__name__)

_RESOLVED_MODELS_PATH = Path(__file__).parent / "resolved_models.yaml"


def probe_provider(provider: str, api_key: str, litellm_model: str) -> None:
    """Make cheapest possible call to verify connectivity. Raises on failure."""
    litellm.completion(
        model=litellm_model,
        messages=[{"role": "user", "content": "ping"}],
        max_tokens=1,
        timeout=10,
        api_key=api_key,
    )


def probe_all() -> None:
    """Probe all MODEL_REGISTRY providers. Writes resolved_models.yaml.

    Hard-fails (raises KonnektError) if any provider is unreachable.
    """
    results: dict[str, dict] = {}
    failed: list[str] = []

    for family_idx, family in MODEL_REGISTRY.items():
        provider = family["provider"]
        try:
            litellm_model = f"{provider}/{family['variants'][1]}"
            logger.info("probe | provider=%s model=%s", provider, litellm_model)
            api_key = get_api_key(provider)
            probe_provider(provider, api_key, litellm_model)
            results[provider] = {"status": "ok", "model": litellm_model}
            logger.info("probe | %s ok", provider)
        except Exception as e:
            results[provider] = {
                "status": "failed",
                "model": locals().get("litellm_model", "<unresolved>"),
                "error": str(e),
            }
            failed.append(provider)
            logger.warning("probe | %s FAILED: %s", provider, e)

    manifest = {
        "probed_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "providers": results,
    }
    with open(_RESOLVED_MODELS_PATH, "w") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)

    if failed:
        affected_roles = [
            role
            for role, (fam_idx, _) in ROLE_DEFAULTS.items()
            if MODEL_REGISTRY[fam_idx]["provider"] in failed
        ]
        raise KonnektError(
            provider=", ".join(failed),
            model="",
            task="probe_all",
            message=(
                f"Providers unreachable: {failed}. "
                f"Affected roles: {affected_roles}. "
                "Reassign each affected role in kre8.yaml "
                "konnekt.role_overrides and re-run."
            ),
        )
