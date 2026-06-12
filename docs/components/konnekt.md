# konnekt — Component Design
**Status:** DONE | **Folder:** `konnekt/`

---

## Role

konnekt is the LLM adapter layer. It is a dumb pipe — no domain knowledge, no pipeline awareness. Any kre8 component that needs an LLM call goes through konnekt.

---

## Interface

```python
complete(
    role: str,
    task: str,
    prompt: str,
    config: KonnektConfig,
    model_select: tuple[int, int] | None = None,
) -> str
```

| Param | Type | Description |
|-------|------|-------------|
| `role` | `str` | Role alias e.g. `"extractor"`, `"architect"`. Resolved to (family, tier) via `ROLE_DEFAULTS`. |
| `task` | `str` | Descriptive call context — logged only, no routing logic. |
| `prompt` | `str` | Raw string. Caller owns construction. |
| `config` | `KonnektConfig` | Pydantic model — temperature, max_tokens, timeout. |
| `model_select` | `tuple[int, int] \| None` | Optional override: `(family_idx, tier_idx)`. i2d2 uses `(3, 2)` for Opus toggle. |

Returns raw `str`. Raises `KonnektError` on failure. Caller owns all Pydantic validation.

---

## KonnektConfig

```python
class KonnektConfig(BaseModel):
    temperature: float = 0.2
    max_tokens: int = 2000
    timeout: int = 30
```

**Recommended max_tokens per role (set by caller):**

| Role | Recommended max_tokens |
|------|----------------------|
| extractor | 1000 |
| architect | 8000 |
| coder | 8000 |
| self-corrector | 1000 |

---

## Model Registry

Defined in `konnekt/models.py` — the **only** place in kre8 where model strings appear.

```python
MODEL_REGISTRY = {
    1: {"provider": "openai",    "variants": {1: "gpt-4o-mini",          2: "gpt-4o"}},
    2: {"provider": "gemini",    "variants": {1: "gemini-flash-latest",   2: "gemini-pro-latest"}},
    3: {"provider": "anthropic", "variants": {1: "claude-sonnet-4-6",     2: "claude-opus-4-6"}},
    4: {"provider": "deepseek",  "variants": {1: "deepseek-v4-flash",     2: "deepseek-v4-pro"}},
    5: {"provider": "groq",      "variants": {1: "llama-3.1-8b-instant",  2: "llama-3.3-70b-versatile"}},
}

ROLE_DEFAULTS = {
    "extractor":      (1, 1),   # gpt-4o-mini
    "architect":      (3, 1),   # claude-sonnet-4-6
    "coder":          (4, 1),   # deepseek-v4-flash
    "self-corrector": (5, 1),   # llama-3.1-8b-instant
}
```

---

## Secrets

GCP Secret Manager via ADC. Module-level `_secret_cache` — lazy loaded per provider, cached for process lifetime. `.env` contains `GCP_PROJECT_ID` only.

| Secret name | Provider |
|-------------|----------|
| `kre8-konnekt-dev-openai` | openai |
| `kre8-konnekt-dev-gemini` | gemini |
| `kre8-konnekt-dev-anthropic` | anthropic |
| `kre8-konnekt-dev-deepseek` | deepseek |
| `kre8-konnekt-dev-groq` | groq |

---

## Error Handling

```python
class KonnektError(Exception):
    def __init__(self, provider: str, model: str, task: str, message: str):
        ...
```

Raises on: unknown role, bad model_select index, GCP SM failure, provider API error, timeout. i2d2 catches and decides — retry, fallback, surface to user. konnekt never retries.

---

## DeepSeek Fallback

DeepSeek V4 thinking models may return chain-of-thought in `message.reasoning_content` when `message.content` is empty. konnekt falls back automatically:

```python
content = message.content
if not content:
    content = getattr(message, "reasoning_content", None) or ""
return content
```

---

## File Layout

```
konnekt/
  __init__.py     # exports: complete, KonnektConfig, KonnektError, MODEL_REGISTRY, ROLE_DEFAULTS
  konnekt.py      # complete() — main entry point
  models.py       # MODEL_REGISTRY + ROLE_DEFAULTS + resolve_model()
  secrets.py      # GCP SM fetch + _secret_cache; ADC-only
  config.py       # KonnektConfig
  errors.py       # KonnektError
  requirements.txt
```

---

## Test Coverage

- **Stub tests** (`stub_tests/test_konnekt.py`): 61 tests — all passing
- **Live tests** (`integration_tests/test_konnekt_live.py`): 14 tests — 12/14 passing (2 Gemini blocked by depleted prepay credits, not a code issue)

---

## Parked

- SecretsAdapter — cloud-agnostic vault abstraction (GCP SM / AWS SM / HashiCorp Vault / Azure KV). Post ship-ready.
- Gemini live tests — re-enable when credits restored.
