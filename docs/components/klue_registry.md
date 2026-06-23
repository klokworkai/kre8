# klue_registry — Component Design
**Status:** NOT STARTED | **Folder:** `klue_registry/`

---

## Role

The Klue Registry is the authoritative store of all Klue policy objects. It is a pure data store — no behavior, no LLM dependency, no pipeline awareness. It is read by i2d2 during kick resolution and by konform during gate evaluation.

A **Klue** (Kre8 Law UniversE) is a single atomic policy rule. Klues are independent of skope — they are created and managed without any skope dependency. A skope references Klues by ID; a Klue has no back-reference to any skope.

---

## Klue Schema (stub)

```
Klue
  klue_id: UUID = auto-generated
  name: str                  # human-readable — e.g. "us-east-1 only"
  description: str           # intent — what this rule enforces and why
  deal: "D" | "E" | "A" | "L"   # DEAL verdict — Deny / Exception / Allow / Limit
  type: str                  # policy category — e.g. "region", "service", "instance_size", "cost"
  target: str                # what the rule applies to — e.g. "us-east-1", "lambda", "t.large"
  config: dict = {}          # type-specific parameters — opaque until full design session
```

> **RESOLVED — NLP → Structured conversion via konsole (post-OSS design session for full implementation)**
>
> Klues are always stored as structured objects. Admin authoring effort is reduced via konsole's
> NLP conversion path — admin writes natural language intent, konsole runs an internal LLM call
> to produce a structured Klue, admin inspects/modifies, then saves. The klue registry never
> sees raw NLP. konform evaluates structured Klues via OPA/Rego unchanged.
>
> Two authoring paths supported in konsole:
> 1. **Structured upload** — admin uploads a pre-filled Klue struct using the kre8-provided template.
> 2. **NLP conversion** — admin writes NLP intent → konsole LLM call → structured Klue → admin inspects/modifies → save.
>
> Full konsole implementation details in `docs/components/konsole.md`.

---

## DEAL Model

| Letter | Meaning | Description |
|--------|---------|-------------|
| **D** | Deny | Block a resource or pattern outright |
| **E** | Exception | Override an Allow/Deny for a specific context |
| **A** | Allow | Explicitly permit a resource or pattern |
| **L** | Limit | Constrain a resource |

---

## Relationship to skope

Klues are fully independent. A Klue can be assigned to zero or more skopes. skope holds a list of `klue_ids` — the Klue itself has no back-reference. This is a deliberate many-to-many design: the same Klue (e.g. "deny us-west-2") can be reused across multiple skopes without duplication.

During kick resolution, i2d2 queries: *"give me all Klues assigned to this skope_id that are relevant to this Kit"* — that is the complete lookup contract.

---

## Conflicting Klues

Two Klues assigned to the same skope may conflict (e.g. `Allow: lambda` and `Deny: lambda`). Conflict detection is **skope's responsibility** — a sanity check runs at Klue assignment time, before the Klue is added to the skope. konform is not involved in conflict resolution; it receives a pre-validated skope and evaluates verdicts as presented.

> ⚠️ **TODO (design):** Define conflict detection rules — what constitutes a conflict, how it is surfaced to the admin (konsole), and whether conflicting assignments are hard-blocked or warned.

---

## Storage

Klue definitions are stored as structured records in `klue_registry/`. Storage format (Rego files vs DB records) is deferred to the full design session, but the object shape is always structured — raw NLP is never persisted.

---

## Relevant ADRs

> None assigned yet — pending design session.

---

## TODO

- Full design session — Klue type taxonomy, storage format, konsole integration
- Klue type taxonomy — enumerate policy categories (region, service, instance_size, cost, etc.)
- Conflict detection rules — define what constitutes a conflict within a skope
- Storage format — Rego files vs structured records
- Klue struct template — provided to admins for structured upload path
- konsole integration — NLP conversion prompt + validation, struct upload validation, conflict surfacing
