# krux — Artifact Design
**Status:** LOCKED | **Produced by:** i2d2 | **Consumed by:** knit, konform | **Stored in:** katalog

---

## Role

Krux is the infrastructure design graph — the structured, validated representation of what needs to be built. Produced by i2d2 after Kit extraction and policy inference (kick), and before Kanvas assembly. Krux captures resources, their types, their layers, and their dependencies. It is the primary input to knit.

---

## Schema

```
DependsOnEntry
  role: str          # "<namespace>:<resource_type>" — e.g., "nw:vpc"
  ref: str           # local resource id OR "$inputs.<name>"

KruxInput
  name: str
  role: str          # "<namespace>:<resource_type>"
  required: bool

KruxOutput
  name: str
  ref: str           # local resource id

KruxResource
  id: str            # unique within krux
  type: str          # "<namespace>:<resource_type>"
  layer: list[str]   # non-empty — values in {foundation, app, data}
  name: str          # LLM-generated
  description: str   # LLM-generated
  depends_on: list[DependsOnEntry] = []
  konfig: dict = {}  # populated by knit — opaque at krux level

Krux
  id: UUID           # auto-generated
  name: str          # LLM-generated
  description: str   # LLM-generated
  region: str        # default "us-east-1" — skope-inherited post-MVP
  kraken: bool = False
  inputs: list[KruxInput] = []
  outputs: list[KruxOutput] = []
  resources: list[KruxResource]
```

---

## Layer Registry

| Layer | Namespaces |
|-------|------------|
| `foundation` | `nw`, `sec`, `iam`, `storage`, `db` — closed set (ADR-028) |
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
9. Inputs marked `required: true` must be supplied at krux instantiation

Retry loop: i2d2 retries LLM krux generation max 2 times on validation failure. Beyond that → `design_conflicts[]`.

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

ADR-022 · ADR-023 · ADR-024 · ADR-027 · ADR-028 · ADR-029 · ADR-030 · ADR-031 · ADR-032 · ADR-033 · ADR-038
