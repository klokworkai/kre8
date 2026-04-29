from konnekt.errors import KonnektError

# family index → provider name + tier variants
MODEL_REGISTRY: dict[int, dict] = {
    1: {
        "provider": "openai",
        "variants": {
            1: "gpt-4o-mini",
            2: "gpt-4o",
        },
    },
    2: {
        "provider": "gemini",
        "variants": {
            1: "gemini-1.5-flash",
            2: "gemini-1.5-pro",
        },
    },
    3: {
        "provider": "anthropic",
        "variants": {
            1: "claude-sonnet-4-6",
            2: "claude-opus-4-6",
        },
    },
    4: {
        "provider": "deepseek",
        "variants": {
            1: "deepseek-v4-flash",
            2: "deepseek-v4-pro",
        },
    },
    5: {
        "provider": "groq",
        "variants": {
            1: "llama-3.1-8b-instant",
            2: "llama-3.3-70b-versatile",
        },
    },
}

# role → (family, tier) default
ROLE_DEFAULTS: dict[str, tuple[int, int]] = {
    "extractor":      (1, 1),
    "architect":      (3, 1),
    "coder":          (4, 1),
    "self-corrector": (5, 1),
}


def resolve_model(role: str, model_select: tuple[int, int] | None = None) -> tuple[str, str]:
    """Return (provider, litellm_model_string) for a role, with optional override."""
    if model_select is not None:
        family_idx, tier_idx = model_select
        source = f"model_select={model_select}"
    else:
        if role not in ROLE_DEFAULTS:
            raise KonnektError(
                provider="konnekt", model=role, task="resolve_model",
                message=f"Unknown role '{role}' — not in ROLE_DEFAULTS",
            )
        family_idx, tier_idx = ROLE_DEFAULTS[role]
        source = f"role={role}"

    if family_idx not in MODEL_REGISTRY:
        raise KonnektError(
            provider="konnekt", model=source, task="resolve_model",
            message=f"Unknown family index {family_idx} — not in MODEL_REGISTRY",
        )

    family = MODEL_REGISTRY[family_idx]

    if tier_idx not in family["variants"]:
        raise KonnektError(
            provider="konnekt", model=source, task="resolve_model",
            message=f"Unknown tier {tier_idx} for family {family_idx} ({family['provider']})",
        )

    provider = family["provider"]
    model_string = family["variants"][tier_idx]
    return provider, f"{provider}/{model_string}"
