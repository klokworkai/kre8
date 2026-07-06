# konform — Component Design
**Status:** NOT STARTED | **Folder:** `konform/`

---

## Role

konform is the policy gate executor. Stateless judge. It validates kit (kg1) and kanvas (kg2) against krule_registry policies referenced via kick_id. It never designs. It never writes to persistent stores. It only judges.

---

## skope vs krule_registry vs konform

- **skope** — named policy boundary. Defines which krules apply to a given team or environment. Behaviour is entirely determined by assigned krules.
- **krule_registry** — store of atomic policy rules (DEAL model). Governs how resources can be configured.
- **konform** — stateless gate executor. Validates kit and kanvas against policies referenced by kick_id. Returns verdict only.

---

## Gate Contract

**kg1 — Kit gate**
- Invoked by i2d2 post-kit, post-kick (pre-kraph)
- Inputs: `(kit, kick_id)`
- Output: `{pass: bool, violated_krule_ids: [...]}`

**kg2 — Kanvas gate**
- Invoked by i2d2 post-kanvas, pre-koder
- Inputs: `(kanvas, kick_id)`
- Output: `{pass: bool, violated_krule_ids: [...]}`

**On denial:** konform returns `violated_krule_ids` only. Human-readable messages live on krule_registry policies. kiosk renders messages by looking up violated IDs in krule_registry. Raw policy codes never surface to users directly.

**DAG and structural validation:** NOT konform's job. i2d2 owns DAG validation as a Pydantic model validator on kraph. See ADR-005.

**Kraken mode:** konform gates run normally regardless of kraken state. When `kraken: true`, i2d2 does not halt on violations — it collects them. konform's pure-judge contract is unchanged. (Kraken mechanics are TBD — no ADR yet.)

---

## DEAL Model (krule_registry policy system)

| Letter | Meaning | Description |
|--------|---------|-------------|
| **D** | Deny | Block a resource, service, or attribute outright |
| **A** | Allow | Explicitly permit a resource or pattern — always paired with a Limit |

Policy definitions live in `krule_registry/` as structured records.

---

## Relevant ADRs

ADR-003 · ADR-004 · ADR-005 · ADR-006

---

## TODO

- Full design session needed — after krule_registry design session
- skope schema design
- krule_registry schema design — DEAL implementation, storage format
- Cost estimation logic in kg2 — Cost is the recommended high-precedence
  krule on every skope, to catch unconstrained/expensive designs at kg2
  without blocking i2d2's design freedom at kg1. Open question: how does
  i2d2 signal to the user that a design passed kg1 but has a probable kg2
  violation, before kanvas assembly is complete?
