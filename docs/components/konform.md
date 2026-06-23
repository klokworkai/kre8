# konform — Component Design
**Status:** NOT STARTED | **Folder:** `konform/`

---

## Role

konform is the policy gate executor. Stateless judge. It validates kit (kg1) and kanvas (kg2) against klue registry policies referenced via kick_id. It never designs. It never writes to persistent stores. It only judges.

---

## skope vs klue registry vs konform

- **skope** — high-level policy realm. Defines allowed/denied resources, regions, environments. Scopes what a user is permitted to design with.
- **klue registry** — fine-grained policy rules (Rego, DEAL model). Governs how allowed resources can be configured.
- **konform** — stateless gate executor. Validates kit and kanvas against policies referenced by kick_id. Returns verdict only.

---

## Gate Contract

**kg1 — Kit gate**
- Invoked by i2d2 post-kit, post-kick (pre-kraph)
- Inputs: `(kit, kick_id)`
- Output: `{pass: bool, violated_klue_ids: [...]}`

**kg2 — Kanvas gate**
- Invoked by i2d2 post-kanvas, pre-koder
- Inputs: `(kanvas, kick_id)`
- Output: `{pass: bool, violated_klue_ids: [...]}`

**On denial:** konform returns `violated_klue_ids` only. Human-readable messages live on klue registry policies. kiosk renders messages by looking up violated IDs in klue registry. Raw policy codes never surface to users directly.

**DAG and structural validation:** NOT konform's job. i2d2 owns DAG validation as a Pydantic model validator on kraph. See ADR-024.

**Kraken mode:** konform gates run normally regardless of kraken state. When `kraken: true`, i2d2 does not halt on violations — it collects them. konform's pure-judge contract is unchanged. See ADR-038.

---

## DEAL Model (klue registry policy system)

| Letter | Meaning | Description |
|--------|---------|-------------|
| **D** | Deny | Block a resource or pattern outright |
| **E** | Exception | Override an Allow/Deny for a specific context |
| **A** | Allow | Explicitly permit a resource or pattern |
| **L** | Limit | Constrain a resource |

Policy definitions live in `klue_registry/policies/` as Rego files.

---

## Relevant ADRs

ADR-003 · ADR-004 · ADR-005 · ADR-006

---

## TODO

- Full design session needed — after klue registry design session
- skope schema design
- klue registry schema design — Rego policy structure, DEAL implementation
- Cost estimation logic in kg2
