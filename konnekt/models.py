from konnekt.errors import KonnektError

MODELS: dict[str, str] = {
    "extractor": "gpt-4o-mini",
    "architect": "claude-sonnet-4-6",
    "coder": "deepseek-v4-flash",
    "self-corrector": "llama-3.3-70b-versatile",
}

PROVIDER_PREFIXES: dict[str, str] = {
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "claude-sonnet-4-6": "anthropic/claude-sonnet-4-6",
    "claude-opus-4-6": "anthropic/claude-opus-4-6",
    "deepseek-v4-flash": "deepseek/deepseek-v4-flash",
    "llama-3.3-70b-versatile": "groq/llama-3.3-70b-versatile",
}


def resolve_model(model: str) -> str:
    if model not in PROVIDER_PREFIXES:
        raise KonnektError(
            provider="konnekt",
            model=model,
            task="resolve_model",
            message=f"Unknown model '{model}' — not in PROVIDER_PREFIXES",
        )
    return PROVIDER_PREFIXES[model]
