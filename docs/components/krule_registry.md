# krule_registry — Component Design
**Status:** NOT STARTED | **Folder:** `krule_registry/`

---

## Role

krule_registry is the authoritative store of all krule policy objects. It is a pure data store — no behavior, no LLM dependency, no pipeline awareness. It is read by i2d2 during kick resolution and by konform during gate evaluation.

A **krule** (Kre8 Rule) is a single atomic policy rule. krules are independent of skope — they are created and managed without any skope dependency. A skope references krules by ID; a krule carries a back-reference to all skopes it is assigned to (for admin lookup).

---

## krule Schema (stub)

```
krule
  krule_id: UUID = auto-generated
  name: str                        # human-readable — e.g. "us-east-1 only"
  description: str                 # intent — what this rule enforces and why
  deal: "D" | "A"                  # DEAL verdict — Deny / Allow (Allow always requires a Limit)
  limit: dict | None = None        # required when deal = "A"; defines the bounds of the Allow
  type: str                        # policy category — e.g. "region", "service", "instance_size", "cost"
  target: str                      # what the rule applies to — e.g. "us-east-1", "lambda", "t.large"
  config: dict = {}                # type-specific parameters — opaque until full design session
  skope_ids: list[UUID] = []       # back-reference — which skopes this krule is assigned to
```

> **DEAL — two types only:**
> - `D` (Deny) — hard-blocks a resource, service, or attribute outright. No carve-outs at the krule level.
> - `A` (Allow) — explicitly permits a resource or pattern. An Allow is always paired with a `limit` — an Allow without a Limit is invalid and rejected at authoring time in konsole.
>
> `Exception` was considered and dropped — the use case is real (deny globally, carve out for one skope) but adds precedence complexity. Revisit post-OSS.
>
> Absent a krule, i2d2 designs freely using full LLM capability. krules constrain at gate time (konform), not at design time.

> **RESOLVED — NLP → Structured conversion via konsole (post-OSS design session for full implementation)**
>
> krules are always stored as structured objects. Admin authoring effort is reduced via konsole's
> NLP conversion path — admin writes natural language intent, konsole calls konnekt to produce a
> structured krule, admin inspects/modifies, then saves. krule_registry never sees raw NLP.
> konform evaluates structured krules via OPA/Rego unchanged.
>
> Two authoring paths supported in konsole:
> 1. **Structured upload** — admin uploads a pre-filled krule struct using the kre8-provided template.
> 2. **NLP conversion** — admin writes NLP intent → konsole calls konnekt → structured krule → admin inspects/modifies → save.
>
> Full konsole implementation details in `docs/components/konsole.md`.

---

## DEAL Model

| Letter | Meaning | Description |
|--------|---------|-------------|
| **D** | Deny | Block a resource, service, or attribute outright |
| **A** | Allow | Explicitly permit a resource or pattern — always paired with a Limit |

> **Limit** is not a standalone DEAL type — it is a required field on every Allow krule. It defines the bounds of what is permitted (e.g. instance family, size ceiling, region list).

---

## Relationship to skope

krules are fully independent. A krule can be assigned to zero or more skopes. skope holds a list of `krule_ids`. krule carries a `skope_ids` back-reference for admin lookups — e.g. "which skopes will be affected if I edit or delete this krule?" This is a deliberate many-to-many design: the same krule (e.g. "deny us-west-2") can be reused across multiple skopes without duplication.

During kick resolution, i2d2 queries: *"give me all krules assigned to this skope_id that are relevant to this Kit"* — that is the complete lookup contract.

---

## Conflicting krules

Two krules assigned to the same skope may conflict (e.g. `Allow: lambda` and `Deny: lambda`). Conflict detection is **skope's responsibility** — a sanity check runs at krule assignment time, before the krule is added to the skope. konform is not involved in conflict resolution; it receives a pre-validated skope and evaluates verdicts as presented.

> ⚠️ **TODO (design):** Define conflict detection rules — what constitutes a conflict, how it is surfaced to the admin (konsole), and whether conflicting assignments are hard-blocked or warned.

---

## Storage

> **Design decision:** krules are independent documents with a schemaless `config` field that varies by krule type. A document store (NoSQL) is the natural fit — no relational joins needed, no fixed schema fights. Each krule is a self-contained record; queries are by `krule_id` or `skope_id` — no joins, no foreign key traversal. A document DB (e.g. MongoDB, Firestore, or DynamoDB) maps cleanly to this access pattern. Storage format is deferred to the full design session; the object shape is always structured — raw NLP is never persisted.
>
> **Candidate ADR** — evaluate storage format decision during the krule_registry design session.

---

## Relevant ADRs

> None assigned yet — pending design session.

---

## TODO

- Full design session — krule type taxonomy, storage format, konsole integration
- krule type taxonomy — enumerate policy categories (region, service, instance_size, cost, etc.)
- Conflict detection rules — define what constitutes a conflict within a skope
- Storage format decision — document DB vs Rego files → candidate ADR
- krule struct template — provided to admins for structured upload path
- konsole integration — NLP conversion via konnekt, struct upload validation, conflict surfacing
