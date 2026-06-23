# skope — Component Design
**Status:** NOT STARTED | **Folder:** `skope/`

---

## Role

skope is a named policy boundary. It defines the context within which a user or team is permitted to design infrastructure. skope has no policy rules of its own — its behaviour is entirely determined by the Klues assigned to it.

skope is intentionally thin by design. All policy expressiveness lives in Klue. skope is the identity and boundary; Klue is the substance.

---

## Schema (stub)

```
skope
  skope_id: UUID = auto-generated
  name: str                  # e.g. "platform-team-prod", "data-eng-staging"
  description: str | None
  klue_ids: list[UUID] = []  # assigned Klues — order has no meaning
```

> skope has no rules, regions, or resource lists of its own. A region restriction is a Klue. A
> service allowlist is a Klue. A cost ceiling is a Klue. skope is the named container that groups
> the applicable Klues for a given team or environment.

---

## Relationship to Klue

- A Klue is an independent atomic policy unit — created without any skope dependency.
- skope holds a flat list of `klue_ids`. Many-to-many: the same Klue can be assigned to multiple skopes.
- i2d2 reads a skope's `klue_ids` during kick resolution to determine which policies apply to a given Kit.

---

## Klue Assignment and Conflict Sanity Check

When a Klue is assigned to a skope, skope runs a sanity check before accepting the assignment. If the incoming Klue conflicts with an already-assigned Klue (e.g. `Allow: lambda` already present, `Deny: lambda` being added), the assignment is rejected or flagged — not silently accepted.

Conflict detection is **skope's responsibility**. konform is not involved — it receives a pre-validated skope and evaluates verdicts as presented.

> ⚠️ **TODO (design):** Define conflict detection rules — what constitutes a conflict, severity levels (hard block vs warning), and how conflicts are surfaced in konsole.

---

## Lifecycle

```
# Klue authoring (konsole-internal)
admin authors Klue via konsole (NLP conversion or structured upload)
  → konsole produces structured Klue → admin inspects/modifies → confirms
  → Klue written to klue registry

# Klue assignment to skope (konsole-internal)
konsole assigns Klue to skope
  → skope.sanity_check(klue) — conflict detection against existing klue_ids
    → on conflict: reject + surface to admin in konsole
    → on pass: klue_id appended to skope.klue_ids

# kick resolution (i2d2-internal, hot path)
i2d2 reads skope.klue_ids
  → infers applicable Klues for this Kit via LLM call
  → produces kick (kit_id + klue_ids)
```

---

## Relevant ADRs

> None assigned yet — pending design session.

---

## TODO

- Full design session — depends on Klue format decision (NLP vs structured vs combo); see `klue_registry.md`
- Conflict detection implementation — rules, severity, konsole surfacing
- skope assignment to users/teams — how a user is bound to a skope (auth layer, TBD)
- Multi-skope — can a user operate under multiple skopes simultaneously? Deferred.
