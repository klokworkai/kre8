"""
Kit is the first structured artifact in the kre8 pipeline.
It carries validated, as-is NLP signals extracted from raw user input.
All downstream components (konform Gate 1, skout, i2d2 Kanvas design) consume Kit.
No normalization occurs here — signal values are passed through verbatim.
"""

import uuid
from enum import Enum

from pydantic import BaseModel, Field


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
