# skope — Component Design
**Status:** NOT STARTED | **Folder:** `skope/`

---

## Role

skope is a named policy boundary. It defines the context within which a user or team is permitted to design infrastructure. skope has no policy rules of its own — its behaviour is entirely determined by the krules assigned to it.

skope is intentionally thin by design. All policy expressiveness lives in krule. skope is the identity and boundary; krule is the substance.

---

## Schema (stub)

```
skope
  skope_id: UUID = auto-generated
  name: str                  # e.g. "platform-team-prod", "data-eng-staging"
  description: str | None
  krule_ids: list[UUID] = []  # assigned krules — order has no meaning
```

> skope has no rules, regions, or resource lists of its own. A region restriction is a krule. A
> service allowlist is a krule. A cost ceiling is a krule. skope is the named container that groups
> the applicable krules for a given team or environment.

---

## Relationship to krule

- A krule is an independent atomic policy unit — created without any skope dependency.
- skope holds a flat list of `krule_ids`. Many-to-many: the same krule can be assigned to multiple skopes.
- i2d2 reads a skope's `krule_ids` during kick resolution to determine which policies apply to a given Kit.

---

## krule Assignment and Conflict Sanity Check

When a krule is assigned to a skope, skope runs a sanity check before accepting the assignment. If the incoming krule conflicts with an already-assigned krule (e.g. `Allow: lambda` already present, `Deny: lambda` being added), the assignment is rejected or flagged — not silently accepted.

Conflict detection is **skope's responsibility**. konform is not involved — it receives a pre-validated skope and evaluates verdicts as presented.

> ⚠️ **TODO (design):** Define conflict detection rules — what constitutes a conflict, severity levels (hard block vs warning), and how conflicts are surfaced in konsole.

---

## Lifecycle

```
# krule authoring (konsole-internal)
admin authors krule via konsole (NLP conversion or structured upload)
  → konsole calls konnekt → structured krule → admin inspects/modifies → confirms
  → krule written to krule_registry

# krule assignment to skope (konsole-internal)
konsole assigns krule to skope
  → skope.sanity_check(krule) — conflict detection against existing krule_ids
    → on conflict: reject + surface to admin in konsole
    → on pass: krule_id appended to skope.krule_ids

# kick resolution (i2d2-internal, hot path)
i2d2 reads skope.krule_ids
  → infers applicable krules for this Kit via LLM call
  → produces kick (kit_id + krule_ids)
```

---

## Relevant ADRs

> None assigned yet — pending design session.

---

## TODO

- Full design session — depends on krule format decision; see `krule_registry.md`
- Conflict detection implementation — rules, severity, konsole surfacing
- skope assignment to users/teams — how a user is bound to a skope (auth layer, TBD)
- Multi-skope / stackable skopes — deferred. Stackable skopes introduce precedence rules, merge semantics, and conflict resolution across layers (equivalent to IAM role stacking). Revisit when a concrete use case cannot be solved with krule composition within a single skope.
