# stub_tests — Test Instructions

Stub tests validate schemas and stub behaviour only. No LLM calls, no network, no external services.

## Setup

```bash
pip install -r requirements.txt
```

## Run all stub tests

From the `kre8/` root:

```bash
pytest stub_tests/
```

## Run a single file

```bash
pytest stub_tests/test_kit_schema.py -v
```

## What's covered

| File | Tests |
|------|-------|
| `test_kit_schema.py` | Kit schema models, IntentType enum, `extract_kit` stub path (konnekt=None) |
| `test_konnekt.py` | — pending konnekt implementation |
| `test_kanvas_schema.py` | — pending Kanvas schema implementation |
| `test_pipeline.py` | — pending full pipeline stub |

## Adding tests

- One file per component schema — match the component name
- Stub tests only: instantiate models, validate field defaults, test `konnekt=None` paths
- No mocking of LLM calls — test the stub return path directly
