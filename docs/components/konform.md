# konform — Component Design
**Status:** NOT STARTED | **Folder:** `konform/`

---

## Role

konform is the policy gate executor. Stateless judge. It validates kit (kg1) and kanvas (kg2) against klaws policies referenced via kick_id. It never designs. It never writes to persistent stores. It only judges.

---

## skope vs klaws vs konform

- **skope** — high-level policy realm. Defines allowed/denied resources, regions, environments. Scopes what a user is permitted to design with.
- **klaws** — fine-grained policy rules (Rego, LADE model). Governs how allowed resources can be configured.
- **konform** — stateless gate executor. Validates kit and kanvas against policies referenced by kick_id. Returns verdict only.

---

## Gate Contract

**kg1 — Kit gate**
- Invoked by i2d2 post-kit, post-klue (pre-krux)
- Inputs: `(kit, kick_id)`
- Output: `{pass: bool, violated_klaws_ids: [...]}`

**kg2 — Kanvas gate**
- Invoked by i2d2 post-kanvas, pre-koder
- Inputs: `(kanvas, kick_id)`
- Output: `{pass: bool, violated_klaws_ids: [...]}`

**On denial:** konform returns `violated_klaws_ids` only. Human-readable messages live on klaws policies. kiosk renders messages by looking up violated_klaws_ids in klaws. Raw policy codes never surface to users directly.

**DAG and structural validation:** NOT konform's job. i2d2 owns DAG validation as a Pydantic model validator on krux. See ADR-024.

**Kraken mode:** konform gates run normally regardless of kraken state. When `kraken: true`, i2d2 does not halt on violations — it collects them. konform's pure-judge contract is unchanged. See ADR-038.

---

## LADE Model (klaws policy system)

| Letter | Meaning | Description |
|--------|---------|-------------|
| **L** | Limit | Constrain a resource |
| **A** | Allow | Explicitly permit a resource or pattern |
| **D** | Deny | Block a resource or pattern outright |
| **E** | Exception | Override an Allow/Deny for a specific context |

Policy definitions live in `klaws/policies/` as Rego files.

---

## MCP Candidate

konform is a full MCP candidate — consumer-owned policy bundles, product-specific context schemas. See ADR-011.

---

## Relevant ADRs

ADR-011 · ADR-020 · ADR-024 · ADR-034 · ADR-036 · ADR-038

---

## Parked

- Full design session needed — after klaws design session
- skope schema design
- klaws schema design — Rego policy structure, LADE implementation
- Cost estimation logic in kg2 (ADR-013)
