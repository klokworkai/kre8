# stub_tests — Test Instructions

Stub tests validate schemas, logic, and wired call chains. No real LLM calls, no network, no external services.

## Setup

```bash
cd kre8/
pip install -r requirements.txt
```

## Run all stub tests

```bash
pytest stub_tests/
```

## Run a single file

```bash
pytest stub_tests/test_konnekt.py -v
```

## What's covered

| File | Tests |
|------|-------|
| `test_kit_schema.py` | Kit schema models, IntentType enum, `extract_kit` stub path (konnekt=None) |
| `test_kanvas_schema.py` | GateVerdict, KraphResource, Kraph (instantiation + all 7 validators), Kanvas |
| `test_konnekt.py` | resolve_model role defaults + model_select overrides + error cases, KonnektConfig, KonnektError, secret cache |
| `test_konnekt_integration.py` | Full chain mock: resolve_model → get_api_key → GCP SM (mocked) → litellm.completion (mocked) |
| `test_pipeline.py` | — pending full pipeline stub |

## Adding tests

- One file per component — match the component name
- Stub tests only: schemas, logic, mock boundaries
- No real network calls — mock at GCP SM and litellm boundaries
- See `test_konnekt_integration.py` for the mock pattern
