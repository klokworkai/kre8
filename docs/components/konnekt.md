# konnekt — Component Design
**Status:** INPROGRESS | **Folder:** `konnekt/`

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
    attachments: list[Attachment] | None = None,
) -> str
```

| Param | Type | Description |
|-------|------|-------------|
| `role` | `str` | Role alias e.g. `"extractor"`, `"architect"`. Resolved to (family, tier) via `ROLE_DEFAULTS`. |
| `task` | `str` | Descriptive call context — logged only, no routing logic. |
| `prompt` | `str` | Raw string. Caller owns construction. |
| `config` | `KonnektConfig` | Pydantic model — temperature, max_tokens, timeout. |
| `model_select` | `tuple[int, int] \| None` | Optional override: `(family_idx, tier_idx)`. i2d2 uses `(3, 2)` for Opus toggle. |
| `attachments` | `list[Attachment] \| None` | Optional list of file attachments — any type the caller needs to pass to the LLM (architecture diagrams, PDFs, requirement docs, images, etc.). Caller owns encoding (base64). Each `Attachment` carries `media_type: str` and `data: str` (base64-encoded content). |

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

## Model Registry and Probe

`MODEL_REGISTRY` in `models.py` is the static capability map — the **only** place in kre8 where model strings appear.

kiosk calls konnekt's init/probe on every launch — not an interim measure, kiosk always initializes konnekt before anything else runs. This replaces the earlier `kre8 init` / `kre8 probe` CLI framing: kli is not being built as a terminal UX (see `docs/components.md` — Parked), so kiosk is the sole caller of konnekt init/re-init. See ADR-008 and `docs/components/kiosk.md` for why kiosk reaches konnekt by direct import rather than through i2d2.

The probe validates connectivity to each configured provider and writes a verified model manifest to `konnekt/resolved_models.yaml`. The manifest is the runtime source of truth for which providers and models are available.

**Probe behaviour:**
- Fetches API keys from GCP SM per `secrets.yaml` config
- Makes a lightweight connectivity check per provider (cheapest possible call)
- Writes `konnekt/resolved_models.yaml` with verified providers, model strings, and probe timestamp
- Hard-fails kiosk's launch if any configured provider fails probe (current behaviour — see Auto-Fallback direction below for the planned change)
- If a provider is unreachable, all roles assigned to that provider cannot proceed. konnekt raises a clear "unable to proceed" error identifying the affected role(s). User must reassign each affected role to a validated working model in `secrets.yaml` and re-run init.
- Manual re-init: triggered from kiosk, always available, not gated behind any other app state. Use after key rotation, `secrets.yaml` edits, or a transient failure.
- Failure categorization: every raise site in `secrets.py`/`probe.py` carries a `category` on `KonnektError`, one of:
  - **no_creds** — no credentials defined for the provider in `secrets.yaml` (missing file, missing `konnekt.secrets`/`gcp.project_id`, no mapping for the provider)
  - **invalid_secret_store** — `secrets.yaml` has the project and secret name configured, but the GCP Secret Manager call for it fails (not-found, unreachable, or any other GCP-side failure)
  - **invalid_api_keys** — a key was retrieved successfully from GCP SM, but the model provider rejected it (`probe_provider()`'s `litellm.completion()` failure)

  `probe_all()` runs two separate try/except blocks per provider (one around `get_api_key()`, one around `probe_provider()`) so the category reflects which stage actually failed. Its final summary `KonnektError` sets `category` only when every failed provider shares the same one; when providers fail for different reasons, `category` is `None` and the new `category_breakdown: dict[provider, category]` field carries the full per-provider detail so kiosk can display each cause without guessing or string-parsing.

> `probe.py` implemented. `secrets.yaml` implemented (renamed from `kre8.yaml`). Startup hard-fail on unreachable provider is live — `probe_all()` raises `KonnektError` listing affected roles, category (or per-provider breakdown), and instructs reassignment in `secrets.yaml`. Failure categorization is implemented on the konnekt side; kiosk-side display wiring is still open (see `docs/components/kiosk.md`).

## Auto-Fallback (direction decided, mechanism deferred)

Direction: rather than hard-failing kiosk's launch on any single provider failure, konnekt should auto-fall back to a working key/model when a configured one errors out or is missing entirely, so kiosk can still launch as long as at least one provider is usable. This changes `probe_all()`'s current "any failure is fatal" contract.

Full mechanism (fallback ordering, which roles degrade to which fallback model, how the substitution is surfaced to the user) is deferred to its own design session — not part of the current build frame. This note exists so the direction isn't lost before that session happens.

```python
MODEL_REGISTRY = {
    1: {"provider": "openai",    "variants": {1: "gpt-4o-mini",          2: "gpt-4o"}},
    2: {"provider": "gemini",    "variants": {1: "gemini-flash-latest",   2: "gemini-pro-latest"}},
    3: {"provider": "anthropic", "variants": {1: "claude-sonnet-4-6",     2: "claude-opus-4-6"}},
    4: {"provider": "deepseek",  "variants": {1: "deepseek-v4-flash",     2: "deepseek-v4-pro"}},
    5: {"provider": "groq",      "variants": {1: "llama-3.1-8b-instant",  2: "llama-3.3-70b-versatile"}},
}
```

> Model strings above are as-coded at last review. Authoritative versions are resolved at probe time and written to `konnekt/resolved_models.yaml`.

---

## Role Defaults and User Overrides

kre8 ships with recommended role defaults. Users can override per-role in `secrets.yaml` — including assigning the same model to all roles.

```python
ROLE_DEFAULTS = {
    "extractor":      (1, 1),   # gpt-4o-mini — fast, cheap extraction
    "architect":      (3, 1),   # claude-sonnet-4-6 — design reasoning
    "coder":          (4, 1),   # deepseek-v4-flash — HCL synthesis
    "self-corrector": (5, 1),   # llama-3.1-8b-instant — lightweight correction
}
```

Role overrides in `secrets.yaml`:
```yaml
konnekt:
  role_overrides:
    architect: [3, 2]     # use claude-opus-4-6 instead
    coder: [3, 1]         # use claude-sonnet-4-6 for all coding roles
```

> ⚠️ **TODO (code):** `secrets.yaml` role override loading not yet implemented — `ROLE_DEFAULTS` still used exclusively.

---

## Secrets

GCP Secret Manager via ADC. Secret names and GCP project ID are provided by the user in `secrets.yaml` at repo root — never hardcoded in konnekt. `secrets.py` reads `secrets.yaml` to resolve the project ID and per-provider secret names, then fetches from GCP SM. Module-level `_secret_cache` — lazy loaded per provider, cached for process lifetime.

> `secrets.py` refactored — reads `gcp.project_id` and `konnekt.secrets` from `secrets.yaml`. Hardcoded map and `.env` dependency removed.
>
> **Note:** `secrets.yaml` currently supports GCP Secret Manager only. The `gcp` top-level key will expand to a vault-agnostic structure (AWS SM, HashiCorp Vault, Azure KV) when SecretsAdapter lands post-ship.

---

## Error Handling

```python
class KonnektError(Exception):
    def __init__(
        self,
        provider: str,
        model: str,
        task: str,
        message: str,
        category: Literal["no_creds", "invalid_secret_store", "invalid_api_keys"] | None = None,
        category_breakdown: dict[str, str] | None = None,
    ):
        ...
```

`category` and `category_breakdown` are optional/defaulted — most raise sites (unknown role, bad model_select index) don't set one. See Model Registry and Probe above for which raise sites in `secrets.py`/`probe.py` set which category.

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
  secrets.py      # GCP SM fetch + _secret_cache; reads secrets.yaml for project ID + secret names
  probe.py        # provider connectivity probe + resolved_models.yaml writer + failure categorization
  config.py       # KonnektConfig
  errors.py       # KonnektError
  requirements.txt
```

---

## Test Coverage

- **Stub tests** (`stub_tests/test_konnekt.py`, `stub_tests/test_probe.py`): 70 tests — all passing, including category coverage for all three categories plus the mixed-category `probe_all()` case
- **Live tests** (`integration_tests/test_konnekt_live.py`): 22 tests — skip without real GCP credentials configured (`-m integration` to run against live providers)

---

## TODO

- `secrets.yaml` role override loading — wire `konnekt.role_overrides` into `resolve_model()`
- Manual re-probe / key re-sync — triggered from a kiosk button calling `probe_all()` directly (see ADR-008); no CLI planned
- Gemini live tests — re-enable when credits restored
- `Attachment` type — define `media_type: str` + `data: str` (base64); wire into `complete()` signature and LLM call construction
- Tool/MCP-calling support — pass tool defs into `litellm.completion`, handle `tool_calls`, loop; needed for koder's Terraform MCP access
- SecretsAdapter — cloud-agnostic vault abstraction (GCP SM / AWS SM / HashiCorp Vault / Azure KV) — post ship-ready
