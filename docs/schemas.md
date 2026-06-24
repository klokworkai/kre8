# schemas.md — kre8 Schema Reference

---

## Kit Schema
**File:** `i2d2/schemas.py` | **Status:** Implemented ✅

### Signal Types

```
KitSignal
  value: str
  source_span: str | None
  inferred: bool = False

SizeSignal
  metric: str          # "rps", "storage", "concurrent_users", etc.
  value: str           # as-is, no normalization
  source_span: str | None
  inferred: bool = False

NfrSignal
  metric: str          # "latency", "availability", "throughput", etc.
  value: str           # as-is — "fast", "99.99%", "100ms"
  source_span: str | None
  inferred: bool = False

TemporalSignal
  pattern_type: str    # "peak_window", "schedule", "burst"
  value: str
  source_span: str | None
  inferred: bool = False

ExclusionSignal
  target: str          # "kubernetes", "lambda", etc.
  reason: str | None   # only if stated or clearly implied
  source_span: str | None
  inferred: bool = False

IntentType (enum)
  PROVISION | MODIFY
```

> ⚠️ **CODE SYNC PENDING:** `schemas.py` still contains `DESTROY` and `QUERY` in the `IntentType` enum.
> Trim to `PROVISION | MODIFY` once all docs are settled. Tracked in CLAUDE.md action items.

```

Kit
  kit_id: UUID = auto-generated
  raw_input: str
  intent: IntentType
  kraken: bool = False
  explicit_infra: list[KitSignal]        = []
  app_type: list[KitSignal]              = []
  qualifiers: list[KitSignal]            = []
  size_and_scale: list[SizeSignal]       = []
  nfr_targets: list[NfrSignal]           = []
  temporal_pattern: list[TemporalSignal] = []
  lifecycle: list[KitSignal]             = []
  data_characteristics: list[KitSignal]  = []
  access_pattern: list[KitSignal]        = []
  security_posture: list[KitSignal]      = []
  cost_posture: list[KitSignal]          = []
  explicit_constraint: list[KitSignal]   = []
  exclusions: list[ExclusionSignal]      = []
  complexity_flags: list[str]            = []
```

### Kit Extraction Categories

| # | Category | Signal type | Notes |
|---|---|---|---|
| 1 | `explicit_infra` | `KitSignal` | Verbatim infra terms |
| 2 | `app_type` | `KitSignal` | Noun phrases only — multi-label |
| 3 | `qualifiers` | `KitSignal` | Modifiers only — multi-label |
| 4 | `size_and_scale` | `SizeSignal` | Users, RPS, storage, payload, counts |
| 5 | `nfr_targets` | `NfrSignal` | Perf, latency, availability — as-is |
| 6 | `temporal_pattern` | `TemporalSignal` | Schedule, peak windows, burst |
| 7 | `lifecycle` | `KitSignal` | Ephemeral, long-running, scheduled |
| 8 | `data_characteristics` | `KitSignal` | Data type, shape, sensitivity |
| 9 | `access_pattern` | `KitSignal` | Sync/async, batch/streaming, connection shape |
| 10 | `security_posture` | `KitSignal` | Non-regulatory security signals |
| 11 | `cost_posture` | `KitSignal` | Qualitative cost intent |
| 12 | `explicit_constraint` | `KitSignal` | Hard stated requirements |
| 13 | `exclusions` | `ExclusionSignal` | Negative preferences |
| 14 | `complexity_flags` | `list[str]` | High-complexity terms — scored downstream |

**Parked:** `environment_stage` · `compliance_signals` · `ownership_signals` · `integration_signals`

---

## Kraph Schema
**File:** `i2d2/schemas.py` | **Status:** Implemented ✅
**Design file:** `docs/components/kraph.md`

```
DependsOnEntry
  role: str          # "<namespace>:<resource_type>"
  ref: str           # local resource id OR "$inputs.<name>"

KraphInput
  name: str
  role: str          # "<namespace>:<resource_type>"
  required: bool

KraphOutput
  name: str
  ref: str           # local resource id

KraphResource
  id: str            # unique within kraph
  type: str          # "<namespace>:<resource_type>"
  layer: list[str]   # non-empty — {foundation, app, data}
  name: str          # LLM-generated
  description: str   # LLM-generated
  depends_on: list[DependsOnEntry] = []
  konfig: dict = {}  # populated during kanvas assembly

TrailEntry
  source: "skout" | "skan"   # which subsystem surfaced this
  ref: str                    # match ID (skout) or finding ID (skan)
  summary: str | None         # human-readable — what was surfaced

Kraph
  id: UUID = auto-generated
  name: str          # LLM-generated
  description: str   # LLM-generated
  region: str        # loaded from i2d2/config.yaml
  kraken: bool = False
  inputs: list[KraphInput] = []
  outputs: list[KraphOutput] = []
  resources: list[KraphResource]   # min_length=1
  references: list[TrailEntry] = []   # design transparency trail — populated by i2d2 pre-kraph
  dsl: str = ""      # Mermaid DSL — generated deterministically by i2d2 at construction time
```

> **Note for implementors:** `GateVerdict` uses `pass_` as the Python field name with `alias="pass"` to avoid collision with the Python keyword. Serialize/deserialize with `by_alias=True`.

---

## kick Schema
**File:** `i2d2/schemas.py` | **Status:** Not implemented ⬜
**Design file:** `docs/components/i2d2.md`

```
kick
  kick_id: UUID = auto-generated
  kit_id: UUID               # references Kit this kick was resolved from
  krule_ids: list[str]       # resolved krule_registry policy IDs applicable to this run
```

> kick is intentionally minimal — it is a resolved binding of a Kit to applicable policy IDs. No config, no signals, no design content.

---

## Kanvas Schema
**File:** `i2d2/schemas.py` | **Status:** Implemented ✅
**Design file:** `docs/components/kanvas.md`

```
GateVerdict
  pass_: bool  (serialized as "pass" — alias field, see note above)
  violated_krule_ids: list[str] = []

DesignConflicts
  kg1: GateVerdict
  kg2: GateVerdict

Kanvas
  id: UUID = auto-generated
  kraph: Kraph
  konfig: dict = {}           # opaque — typed during kanvas assembly design
  design_conflicts: DesignConflicts
  kraken: bool = False        # propagated from kraph
```

---

## skope Schema
**Status:** Not started ⬜

> Design session pending.

---

## krule Schema
**Status:** Not started ⬜

> Design session pending. krule (Kre8 Rule) is the atomic policy object — DEAL model (Deny / Allow+Limit). krule_registry is the store.
