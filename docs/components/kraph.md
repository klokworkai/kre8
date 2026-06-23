# kraph — Artifact Design
**Status:** LOCKED | **Produced by:** i2d2 | **Consumed by:** i2d2, konform | **Stored in:** katalog

---

## Role

Kraph is the infrastructure design graph — the structured, validated representation of what needs to be built. Produced by i2d2 after Kit extraction and kick resolution, and before Kanvas assembly. Kraph captures resources, their types, their layers, and their dependencies. It is the primary input to i2d2's kanvas assembly step. Kraph carries a `references` trail recording what skout/skan surfaced during design — design transparency.

Kraph is a two-part artifact: `resources` (the typed DAG) and `dsl` (Mermaid DSL). Both are generated atomically by i2d2 at construction time. The DSL is a deterministic serialization of the graph — no LLM call required. kiosk renders it on demand from katalog.

---

## Schema

```
DependsOnEntry
  role: str          # "<namespace>:<resource_type>" — e.g., "nw:vpc"
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
  layer: list[str]   # non-empty — values in {foundation, app, data}
  name: str          # LLM-generated
  description: str   # LLM-generated
  depends_on: list[DependsOnEntry] = []
  konfig: dict = {}  # populated during kanvas assembly — opaque at kraph level

TrailEntry
  source: "skout" | "skan"   # which subsystem surfaced this
  ref: str                    # match ID (skout) or finding ID (skan)
  summary: str | None         # human-readable — what was surfaced

Kraph
  id: UUID           # auto-generated
  name: str          # LLM-generated
  description: str   # LLM-generated
  region: str        # default "us-east-1" — skope-inherited post-MVP
  kraken: bool = False
  inputs: list[KraphInput] = []
  outputs: list[KraphOutput] = []
  resources: list[KraphResource]   # min_length=1
  references: list[TrailEntry] = []   # design transparency trail — populated by i2d2 pre-kraph
  dsl: str = ""      # Mermaid DSL — generated deterministically by i2d2 at construction time
```

---

## DSL Generation

`dsl` is a pure function of the graph — i2d2 walks `resources` and `depends_on` edges and emits Mermaid DSL string. No LLM call. Generated in the same operation as the Kraph struct and written to katalog together. If the retry loop produces a revised Kraph, both fields are overwritten atomically.

kiosk fetches `dsl` from katalog and passes it directly to mermaid.js. kiosk has no knowledge of Kraph's internal structure.

---

## Layer Registry

| Layer | Namespaces |
|-------|------------|
| `foundation` | `nw`, `sec`, `iam`, `storage`, `db` — closed set |
| `app` | `compute`, and others — open set |
| `data` | no fixed namespace — contextual |

---

## Validation Rules (Pydantic model validators — owned by i2d2)

1. Every resource has `id`, `type`, `layer` (non-empty list)
2. Every `layer` entry must be in `{foundation, app, data}`
3. Every `type` must match `<namespace>:<resource_type>` format
4. Every `depends_on[].ref` must resolve to a local resource id OR `$inputs.<n>` declared in `inputs`
5. Every local `depends_on[].ref` must point at a resource whose `layer` includes `foundation`
6. The `(role, ref)` pair must be type-consistent — referenced resource's `type` must match `role`
7. The `depends_on` graph must be acyclic (DAG validation)
8. No two resources share an `id`
9. Inputs marked `required: true` must be supplied at kraph instantiation

Retry loop: i2d2 retries LLM kraph generation max 2 times on validation failure. Beyond that → `design_conflicts[]`.

---

## Examples

### Minimal resource
```yaml
- id: main_vpc
  type: nw:vpc
  layer: [foundation]
  name: "Main VPC"
  description: "Primary network boundary"
```

### Multi-tagged resource
```yaml
- id: app_postgres
  type: db:rds_postgres
  layer: [foundation, data]
  name: "Application Database"
  description: "Primary relational store"
  depends_on:
    - {role: nw:vpc, ref: main_vpc}
```

### App-layer resource with multiple foundation deps
```yaml
- id: api_lambda
  type: compute:lambda_function
  layer: [app]
  name: "API Handler"
  description: "Core request handler"
  depends_on:
    - {role: nw:vpc, ref: main_vpc}
    - {role: sec:security_group, ref: web_sg}
    - {role: iam:role, ref: app_role}
    - {role: db:rds_postgres, ref: app_postgres}
```

---

## Relevant ADRs

ADR-005 · ADR-006 · ADR-007
