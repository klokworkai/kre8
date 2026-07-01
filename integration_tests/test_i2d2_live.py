"""
Live integration tests — full flow: i2d2 FastAPI → konnekt → GCP SM → LLM → Kit.

What this tests:
  - i2d2 /health endpoint
  - POST /process with real NLP input → real LLM extraction → valid Kit response
  - Kit schema fields populated correctly
  - Error response shape for invalid input

Requirements:
  - GCP_PROJECT_ID env var set
  - Valid ADC credentials: run `gcloud auth application-default login` once locally
  - Docker / AWS ECS / GKE: GOOGLE_APPLICATION_CREDENTIALS pointing to WIF
    credential config

Run:
  GCP_PROJECT_ID=kre8-dev pytest integration_tests/test_i2d2_live.py -m integration -v
"""

import pytest
from fastapi.testclient import TestClient

from i2d2.app import app
from konnekt.secrets import _secret_cache

pytestmark = pytest.mark.integration

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cache():
    _secret_cache.clear()
    yield
    _secret_cache.clear()


# --- health ---


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "component": "i2d2"}


# --- /process: Kit structure ---


def test_process_returns_valid_kit_fields():
    response = client.post("/process", json={"input": "provision a web app on AWS"})
    assert response.status_code == 200
    kit = response.json()
    assert "request_id" in kit
    assert "raw_input" in kit
    assert "intent" in kit
    assert kit["raw_input"] == "provision a web app on AWS"


def test_process_intent_is_provision():
    response = client.post("/process", json={"input": "deploy a new postgres database"})
    assert response.status_code == 200
    assert response.json()["intent"] == "PROVISION"


def test_process_intent_is_destroy():
    response = client.post(
        "/process", json={"input": "tear down the staging environment"}
    )
    assert response.status_code == 200
    assert response.json()["intent"] == "DESTROY"


def test_process_intent_is_query():
    response = client.post(
        "/process",
        json={"input": "what is the current state of the production cluster"},
    )
    assert response.status_code == 200
    assert response.json()["intent"] == "QUERY"


# --- /process: signal extraction ---


def test_process_extracts_explicit_infra():
    response = client.post(
        "/process", json={"input": "provision an EC2 instance with RDS"}
    )
    assert response.status_code == 200
    kit = response.json()
    infra_values = [s["value"] for s in kit.get("explicit_infra", [])]
    assert any("EC2" in v or "ec2" in v.lower() for v in infra_values), (
        f"Expected EC2 in explicit_infra, got: {infra_values}"
    )


def test_process_extracts_exclusion():
    response = client.post(
        "/process", json={"input": "deploy a web app on AWS, no kubernetes"}
    )
    assert response.status_code == 200
    kit = response.json()
    exclusion_targets = [s["target"] for s in kit.get("exclusions", [])]
    assert any("kubernetes" in t.lower() for t in exclusion_targets), (
        f"Expected kubernetes in exclusions, got: {exclusion_targets}"
    )


# --- error handling ---


def test_process_empty_input_returns_error():
    response = client.post("/process", json={"input": ""})
    # empty input should either return a Kit with minimal fields or a 422
    assert response.status_code in (200, 422)
