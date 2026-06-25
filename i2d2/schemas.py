# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

"""All kre8 pipeline schemas — Kit, Kraph, Kanvas."""

import re
import uuid
from enum import Enum
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator


def _load_default_region() -> str:
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)["default_region"]


_DEFAULT_REGION = _load_default_region()

_VALID_LAYERS = {"foundation", "app", "data"}
_TYPE_RE = re.compile(r"^[a-z]+:[a-z_]+$")


# ── Kit ──────────────────────────────────────────────────────────────────────


class KitSignal(BaseModel):
    value: str
    source_span: str | None
    inferred: bool = False


class SizeSignal(BaseModel):
    metric: str
    value: str
    source_span: str | None
    inferred: bool = False


class NfrSignal(BaseModel):
    metric: str
    value: str
    source_span: str | None
    inferred: bool = False


class TemporalSignal(BaseModel):
    pattern_type: str
    value: str
    source_span: str | None
    inferred: bool = False


class ExclusionSignal(BaseModel):
    target: str
    reason: str | None
    source_span: str | None
    inferred: bool = False


class IntentType(str, Enum):
    PROVISION = "PROVISION"
    MODIFY = "MODIFY"
    DESTROY = "DESTROY"
    QUERY = "QUERY"


class Kit(BaseModel):
    model_config = {"use_enum_values": True}

    request_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    raw_input: str
    intent: IntentType
    kraken: bool = False
    explicit_infra: list[KitSignal] = Field(default_factory=list)
    app_type: list[KitSignal] = Field(default_factory=list)
    qualifiers: list[KitSignal] = Field(default_factory=list)
    size_and_scale: list[SizeSignal] = Field(default_factory=list)
    nfr_targets: list[NfrSignal] = Field(default_factory=list)
    temporal_pattern: list[TemporalSignal] = Field(default_factory=list)
    lifecycle: list[KitSignal] = Field(default_factory=list)
    data_characteristics: list[KitSignal] = Field(default_factory=list)
    access_pattern: list[KitSignal] = Field(default_factory=list)
    security_posture: list[KitSignal] = Field(default_factory=list)
    cost_posture: list[KitSignal] = Field(default_factory=list)
    explicit_constraint: list[KitSignal] = Field(default_factory=list)
    exclusions: list[ExclusionSignal] = Field(default_factory=list)
    complexity_flags: list[str] = Field(default_factory=list)


# ── Kraph ─────────────────────────────────────────────────────────────────────


class DependsOnEntry(BaseModel):
    role: str
    ref: str


class KraphInput(BaseModel):
    name: str
    role: str
    required: bool


class KraphOutput(BaseModel):
    name: str
    ref: str


class KraphResource(BaseModel):
    id: str
    type: str
    layer: list[str] = Field(min_length=1)
    name: str
    description: str
    depends_on: list[DependsOnEntry] = Field(default_factory=list)
    konfig: dict = Field(default_factory=dict)


class Kraph(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: str
    region: str = _DEFAULT_REGION
    kraken: bool = False
    inputs: list[KraphInput] = Field(default_factory=list)
    outputs: list[KraphOutput] = Field(default_factory=list)
    resources: list[KraphResource] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_kraph(self) -> "Kraph":
        resource_ids = {r.id for r in self.resources}
        input_names = {i.name for i in self.inputs}
        input_by_name = {i.name: i for i in self.inputs}
        resource_by_id = {r.id: r for r in self.resources}

        # 1. no duplicate resource ids
        if len(resource_ids) != len(self.resources):
            seen, dupes = set(), []
            for r in self.resources:
                if r.id in seen:
                    dupes.append(r.id)
                else:
                    seen.add(r.id)
            raise ValueError(f"duplicate resource ids: {dupes}")

        for r in self.resources:
            # 2. layer values in valid set
            bad_layers = [lyr for lyr in r.layer if lyr not in _VALID_LAYERS]
            if bad_layers:
                raise ValueError(f"resource '{r.id}' has invalid layer values: {bad_layers}")

            # 3. type matches <namespace>:<resource_type>
            if not _TYPE_RE.match(r.type):
                raise ValueError(
                    f"resource '{r.id}' type '{r.type}' must match <namespace>:<resource_type>"
                )

            for dep in r.depends_on:
                if dep.ref.startswith("$inputs."):
                    input_name = dep.ref[len("$inputs."):]
                    # 4. $inputs ref resolves to a declared input
                    if input_name not in input_names:
                        raise ValueError(
                            f"resource '{r.id}' dep ref '{dep.ref}' does not resolve to a declared input"
                        )
                    # 6. role consistency for $inputs refs
                    if input_by_name[input_name].role != dep.role:
                        raise ValueError(
                            f"resource '{r.id}' dep role '{dep.role}' does not match "
                            f"input '{input_name}' role '{input_by_name[input_name].role}'"
                        )
                else:
                    # 4. local ref resolves to a resource id
                    if dep.ref not in resource_ids:
                        raise ValueError(
                            f"resource '{r.id}' dep ref '{dep.ref}' does not resolve to a local resource id"
                        )
                    target = resource_by_id[dep.ref]
                    # 5. local dep target must include foundation layer
                    if "foundation" not in target.layer:
                        raise ValueError(
                            f"resource '{r.id}' depends on '{dep.ref}' which is not a foundation-layer resource"
                        )
                    # 6. role consistency for local refs
                    if target.type != dep.role:
                        raise ValueError(
                            f"resource '{r.id}' dep role '{dep.role}' does not match "
                            f"resource '{dep.ref}' type '{target.type}'"
                        )

        # 9. required inputs must be referenced by at least one resource
        all_input_refs = {
            dep.ref[len("$inputs."):]
            for r in self.resources
            for dep in r.depends_on
            if dep.ref.startswith("$inputs.")
        }
        for inp in self.inputs:
            if inp.required and inp.name not in all_input_refs:
                raise ValueError(
                    f"required input '{inp.name}' is not referenced by any resource"
                )

        # 7. DAG is acyclic
        ts = TopologicalSorter()
        for r in self.resources:
            ts.add(r.id)
            for dep in r.depends_on:
                if not dep.ref.startswith("$inputs."):
                    ts.add(r.id, dep.ref)
        try:
            ts.prepare()
        except CycleError as e:
            raise ValueError(f"cycle detected in depends_on graph: {e.args}")

        return self


# ── Kanvas ───────────────────────────────────────────────────────────────────


class GateVerdict(BaseModel):
    model_config = {"populate_by_name": True}

    pass_: bool = Field(..., alias="pass")
    violated_klaws_ids: list[str] = Field(default_factory=list)


class DesignConflicts(BaseModel):
    kg1: GateVerdict
    kg2: GateVerdict


class Kanvas(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    kraph: Kraph
    konfig: dict = Field(default_factory=dict)
    design_conflicts: DesignConflicts
    kraken: bool = False
