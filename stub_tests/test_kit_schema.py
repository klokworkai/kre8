from i2d2.schemas import (
    ExclusionSignal,
    IntentType,
    Kit,
    KitSignal,
    NfrSignal,
    SizeSignal,
    TemporalSignal,
)
from i2d2.extract_kit import extract_kit


# --- signal models ---

def test_kit_signal_defaults():
    s = KitSignal(value="ec2", source_span=None)
    assert s.value == "ec2"
    assert s.source_span is None
    assert s.inferred is False


def test_size_signal():
    s = SizeSignal(metric="rps", value="10000", source_span="10k RPS")
    assert s.metric == "rps"
    assert s.inferred is False


def test_nfr_signal():
    s = NfrSignal(metric="latency", value="fast", source_span="fast")
    assert s.value == "fast"


def test_temporal_signal():
    s = TemporalSignal(pattern_type="burst", value="morning spike", source_span=None)
    assert s.pattern_type == "burst"


def test_exclusion_signal():
    s = ExclusionSignal(target="kubernetes", reason=None, source_span=None)
    assert s.target == "kubernetes"
    assert s.reason is None


# --- IntentType enum ---

def test_intent_type_values():
    assert IntentType.PROVISION == "PROVISION"
    assert IntentType.MODIFY == "MODIFY"
    assert IntentType.DESTROY == "DESTROY"
    assert IntentType.QUERY == "QUERY"


# --- Kit model ---

def test_kit_auto_request_id():
    k1 = Kit(raw_input="deploy an api", intent=IntentType.PROVISION)
    k2 = Kit(raw_input="deploy an api", intent=IntentType.PROVISION)
    assert k1.request_id != k2.request_id


def test_kit_default_empty_lists():
    k = Kit(raw_input="deploy an api", intent=IntentType.PROVISION)
    assert k.explicit_infra == []
    assert k.exclusions == []
    assert k.complexity_flags == []


def test_kit_model_validate():
    data = {
        "raw_input": "deploy a web app on EC2",
        "intent": "PROVISION",
        "app_type": [{"value": "web app", "source_span": "web app", "inferred": False}],
        "explicit_infra": [{"value": "EC2", "source_span": "EC2", "inferred": False}],
    }
    k = Kit.model_validate(data)
    assert k.intent == "PROVISION"
    assert k.app_type[0].value == "web app"
    assert k.explicit_infra[0].value == "EC2"


def test_kit_missing_required_fields():
    import pytest
    with pytest.raises(Exception):
        Kit.model_validate({"raw_input": "oops"})  # missing intent


# --- extract_kit stub ---

def test_extract_kit_stub_no_konnekt():
    k = extract_kit("deploy a postgres database", konnekt=None)
    assert k.raw_input == "deploy a postgres database"
    assert k.intent == "PROVISION"
    assert k.app_type[0].value == "stub"
    assert k.request_id is not None
