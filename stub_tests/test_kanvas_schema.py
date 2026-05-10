import pytest
from i2d2.schemas import (
    DependsOnEntry,
    DesignConflicts,
    GateVerdict,
    Kanvas,
    Krux,
    KruxInput,
    KruxOutput,
    KruxResource,
)


# --- helpers ---


def _make_resource(**overrides) -> KruxResource:
    base = {
        "id": "main_vpc",
        "type": "nw:vpc",
        "layer": ["foundation"],
        "name": "Main VPC",
        "description": "Primary network boundary",
    }
    base.update(overrides)
    return KruxResource(**base)


def _make_minimal_krux(**overrides) -> Krux:
    base = {
        "name": "Test Krux",
        "description": "A minimal test krux",
        "resources": [_make_resource()],
    }
    base.update(overrides)
    return Krux(**base)


def _make_gate_verdict(pass_val: bool) -> GateVerdict:
    return GateVerdict(**{"pass": pass_val})


def _make_design_conflicts() -> DesignConflicts:
    return DesignConflicts(
        kg1=_make_gate_verdict(True),
        kg2=_make_gate_verdict(False),
    )


# --- GateVerdict ---


def test_gate_verdict_via_alias():
    gv = GateVerdict(**{"pass": True})
    assert gv.pass_ is True
    assert gv.violated_klaws_ids == []


def test_gate_verdict_via_python_name():
    gv = GateVerdict(pass_=False, violated_klaws_ids=["KLW-001"])
    assert gv.pass_ is False
    assert gv.violated_klaws_ids == ["KLW-001"]


def test_gate_verdict_serializes_as_pass():
    gv = GateVerdict(pass_=True)
    data = gv.model_dump(by_alias=True)
    assert "pass" in data
    assert data["pass"] is True


# --- KruxResource ---


def test_krux_resource_defaults():
    r = _make_resource()
    assert r.depends_on == []
    assert r.konfig == {}


def test_krux_resource_empty_layer_rejected():
    with pytest.raises(Exception):
        _make_resource(layer=[])


# --- Krux instantiation ---


def test_krux_auto_id():
    k1 = _make_minimal_krux()
    k2 = _make_minimal_krux()
    assert k1.id != k2.id


def test_krux_region_default_from_config():
    k = _make_minimal_krux()
    assert k.region == "us-east-1"


def test_krux_defaults():
    k = _make_minimal_krux()
    assert k.kraken is False
    assert k.inputs == []
    assert k.outputs == []


def test_krux_empty_resources_rejected():
    with pytest.raises(Exception):
        Krux(name="x", description="x", resources=[])


# --- Krux validators ---


def test_krux_duplicate_resource_id_rejected():
    r1 = _make_resource(id="vpc1")
    r2 = _make_resource(id="vpc1")
    with pytest.raises(Exception, match="duplicate resource ids"):
        Krux(name="x", description="x", resources=[r1, r2])


def test_krux_invalid_layer_rejected():
    with pytest.raises(Exception, match="invalid layer values"):
        Krux(name="x", description="x", resources=[_make_resource(layer=["edge"])])


def test_krux_invalid_type_format_rejected():
    with pytest.raises(Exception, match="must match"):
        Krux(name="x", description="x", resources=[_make_resource(type="ComputeLambda")])


def test_krux_unresolved_local_ref_rejected():
    dep = DependsOnEntry(role="nw:vpc", ref="nonexistent")
    r = _make_resource(id="app", type="compute:lambda_function", layer=["app"], depends_on=[dep])
    with pytest.raises(Exception, match="does not resolve"):
        Krux(name="x", description="x", resources=[r])


def test_krux_dep_on_non_foundation_rejected():
    app1 = _make_resource(id="app1", type="compute:lambda_function", layer=["app"])
    dep = DependsOnEntry(role="compute:lambda_function", ref="app1")
    app2 = _make_resource(id="app2", type="compute:lambda_function", layer=["app"], depends_on=[dep])
    with pytest.raises(Exception, match="not a foundation-layer resource"):
        Krux(name="x", description="x", resources=[app1, app2])


def test_krux_role_type_mismatch_rejected():
    vpc = _make_resource(id="main_vpc", type="nw:vpc", layer=["foundation"])
    dep = DependsOnEntry(role="sec:security_group", ref="main_vpc")
    app = _make_resource(id="app", type="compute:lambda_function", layer=["app"], depends_on=[dep])
    with pytest.raises(Exception, match="does not match"):
        Krux(name="x", description="x", resources=[vpc, app])


def test_krux_cycle_rejected():
    dep_a = DependsOnEntry(role="nw:vpc", ref="b")
    dep_b = DependsOnEntry(role="nw:vpc", ref="a")
    a = _make_resource(id="a", type="nw:vpc", layer=["foundation"], depends_on=[dep_a])
    b = _make_resource(id="b", type="nw:vpc", layer=["foundation"], depends_on=[dep_b])
    with pytest.raises(Exception, match="cycle"):
        Krux(name="x", description="x", resources=[a, b])


def test_krux_required_input_unreferenced_rejected():
    inp = KruxInput(name="target_vpc", role="nw:vpc", required=True)
    r = _make_resource()
    with pytest.raises(Exception, match="required input"):
        Krux(name="x", description="x", inputs=[inp], resources=[r])


def test_krux_optional_input_unreferenced_allowed():
    inp = KruxInput(name="target_vpc", role="nw:vpc", required=False)
    k = Krux(name="x", description="x", inputs=[inp], resources=[_make_resource()])
    assert len(k.inputs) == 1


def test_krux_input_ref_role_mismatch_rejected():
    inp = KruxInput(name="target_vpc", role="nw:vpc", required=True)
    dep = DependsOnEntry(role="sec:security_group", ref="$inputs.target_vpc")
    r = KruxResource(
        id="web_sg",
        type="sec:security_group",
        layer=["foundation"],
        name="Web SG",
        description="Web security group",
        depends_on=[dep],
    )
    with pytest.raises(Exception, match="does not match"):
        Krux(name="x", description="x", inputs=[inp], resources=[r])


def test_krux_with_valid_input_ref():
    inp = KruxInput(name="target_vpc", role="nw:vpc", required=True)
    dep = DependsOnEntry(role="nw:vpc", ref="$inputs.target_vpc")
    r = KruxResource(
        id="web_sg",
        type="sec:security_group",
        layer=["foundation"],
        name="Web SG",
        description="Web security group",
        depends_on=[dep],
    )
    k = Krux(name="x", description="x", inputs=[inp], resources=[r])
    assert k.inputs[0].name == "target_vpc"


# --- Kanvas ---


def test_kanvas_auto_id():
    krux = _make_minimal_krux()
    c1 = Kanvas(krux=krux, design_conflicts=_make_design_conflicts())
    c2 = Kanvas(krux=krux, design_conflicts=_make_design_conflicts())
    assert c1.id != c2.id


def test_kanvas_defaults():
    krux = _make_minimal_krux()
    c = Kanvas(krux=krux, design_conflicts=_make_design_conflicts())
    assert c.konfig == {}
    assert c.kraken is False


def test_kanvas_model_validate():
    krux = _make_minimal_krux()
    data = {
        "krux": krux.model_dump(),
        "design_conflicts": {
            "kg1": {"pass": True, "violated_klaws_ids": []},
            "kg2": {"pass": False, "violated_klaws_ids": ["KLW-001"]},
        },
    }
    c = Kanvas.model_validate(data)
    assert c.design_conflicts.kg1.pass_ is True
    assert c.design_conflicts.kg2.violated_klaws_ids == ["KLW-001"]
