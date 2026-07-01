import os

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: requires GCP_PROJECT_ID + valid ADC credentials + real LLM access",
    )


@pytest.fixture(autouse=True)
def require_gcp(request):
    if request.node.get_closest_marker("integration"):
        if not os.environ.get("GCP_PROJECT_ID"):
            pytest.skip("GCP_PROJECT_ID not set — skipping integration test")
