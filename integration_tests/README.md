# integration_tests — Test Instructions

Live integration tests. Hit real GCP Secret Manager and real LLM APIs.
Tests auto-skip if `GCP_PROJECT_ID` is not set.

---

## Setup

**1 — Authenticate to GCP (once per machine)**

```bash
gcloud auth application-default login
```

Credentials are cached at `~/.config/gcloud/` — not a key file, expires and refreshes automatically.

**2 — Set project env var**

```bash
export GCP_PROJECT_ID=kre8-dev
```

Or prefix each command inline (see examples below).

---

## Run

**konnekt standalone — secrets + LLM calls:**

```bash
GCP_PROJECT_ID=kre8-dev python3 -m pytest integration_tests/test_konnekt_live.py -m integration -v
```

**Full flow — i2d2 → konnekt → LLM → Kit:**

```bash
GCP_PROJECT_ID=kre8-dev python3 -m pytest integration_tests/test_i2d2_live.py -m integration -v
```

**Both together:**

```bash
GCP_PROJECT_ID=kre8-dev python3 -m pytest integration_tests/ -m integration -v
```

---

## See which model is being called

Logging is built into `konnekt.complete()`. Enable it with `--log-cli-level`:

```bash
GCP_PROJECT_ID=kre8-dev python3 -m pytest integration_tests/test_konnekt_live.py -m integration -v --log-cli-level=INFO
```

Each call prints:
```
konnekt.konnekt | konnekt | role=architect task=think model=anthropic/claude-sonnet-4-6 select=None
```

To see it outside tests:

```bash
GCP_PROJECT_ID=kre8-dev python3 -c "
import logging
logging.basicConfig(level=logging.INFO, format='%(name)s | %(message)s')
from konnekt import complete, KonnektConfig
result = complete('architect', 'think', 'Reply PONG only.', KonnektConfig(max_tokens=20))
print('Response:', result)
"
```

---

## Switch models — model_select

Every `complete()` call uses the role's default model. Pass `model_select=(family, tier)` to override.

### Model registry

| Index | Provider | Tier 1 (fast) | Tier 2 (strong) |
|-------|----------|---------------|-----------------|
| `(1, _)` | openai | `gpt-4o-mini` | `gpt-4o` |
| `(2, _)` | gemini | `gemini-flash-latest` → gemini-3.1-flash-preview | `gemini-pro-latest` → gemini-3.1-pro-preview |
| `(3, _)` | anthropic | `claude-sonnet-4-6` | `claude-opus-4-6` |
| `(4, _)` | deepseek | `deepseek-v4-flash` | `deepseek-v4-pro` |
| `(5, _)` | groq | `llama-3.1-8b-instant` | `llama-3.3-70b-versatile` |

### Role defaults

| Role | Default |
|------|---------|
| `extractor` | `(1, 1)` — openai/gpt-4o-mini |
| `architect` | `(3, 1)` — anthropic/claude-sonnet-4-6 |
| `coder` | `(4, 1)` — deepseek/deepseek-v4-flash |
| `self-corrector` | `(5, 1)` — groq/llama-3.1-8b-instant |

### Override examples

```python
from konnekt import complete, KonnektConfig

config = KonnektConfig(max_tokens=100)

# use role default
complete("architect", "think", prompt, config)                       # → claude-sonnet-4-6

# switch to opus
complete("architect", "think", prompt, config, model_select=(3, 2))  # → claude-opus-4-6

# run architect task on gemini flash
complete("architect", "think", prompt, config, model_select=(2, 1))  # → gemini-flash-latest

# run any role on gpt-4o
complete("extractor", "extract", prompt, config, model_select=(1, 2)) # → gpt-4o
```

model_select overrides the model only — the role still sets the task label in logs.

### From the command line

```bash
GCP_PROJECT_ID=kre8-dev python3 -c "
import logging
logging.basicConfig(level=logging.INFO, format='%(name)s | %(message)s')
from konnekt import complete, KonnektConfig
result = complete('architect', 'think', 'Reply PONG only.', KonnektConfig(max_tokens=20), model_select=(3, 2))
print(result)
"
```

---

## What's covered

| File | Tests |
|------|-------|
| `test_konnekt_live.py` | Secret retrieval for all 5 providers, cache behaviour, LLM smoke test for all 4 role defaults, model_select overrides for all 5 families |
| `test_i2d2_live.py` | /health, POST /process → Kit structure, intent type detection (PROVISION / DESTROY / QUERY), signal extraction, error handling |

---

## Known limitations

| Provider | Status | Notes |
|----------|--------|-------|
| Gemini | Requires prepay credits | 429 if Google AI Studio account balance is depleted |
| DeepSeek V4 | ✅ | reasoning_content fallback handled in konnekt |
