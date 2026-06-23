# konsole — Component Design
**Status:** NOT STARTED | **Folder:** `konsole/`

---

## Role

konsole is the admin UI. It is the management surface for skope, Klue registry, and user/team policy configuration. It is not in the inference or design pipeline — it operates entirely outside of i2d2's hot path.

konsole owns two internal LLM-powered methods: Klue NLP conversion and Klue assignment sanity check surfacing. Both are konsole-internal — the klue registry stores only validated structured Klues, and konform never sees raw NLP or unresolved conflicts.

---

## Responsibilities

- **Klue authoring** — two paths for admin Klue creation (see below)
- **Klue assignment** — assigns Klues to skopes; triggers sanity check before writing
- **Conflict surfacing** — surfaces Klue conflicts to admin at assignment time
- **skope management** — create, edit, deactivate skopes
- **User/team binding** — assign users or teams to a skope (design TBD)

---

## Klue Authoring

Admins have two paths to create a Klue:

**Path 1 — Structured upload**
Admin uploads a pre-filled Klue struct using the kre8-provided template. konsole validates the struct on import (required fields, valid DEAL value, known type). On validation pass, admin reviews and confirms — Klue is written to klue registry.

**Path 2 — NLP conversion**
Admin writes a natural language policy intent.
```
example: "us-east-1 only. instance sizes no greater than large. instance family t only."
```
konsole runs an internal LLM call to convert the NLP string into a structured Klue. Admin inspects the output, modifies any field values as needed, and confirms. On confirmation, the structured Klue is written to klue registry.

In both paths:
- Admin sees and can edit the structured Klue before it is persisted.
- The klue registry never stores raw NLP — only validated structured Klues.
- The LLM call is konsole-internal and has no dependency on konnekt or i2d2.

> ⚠️ **TODO (design):** Define the Klue struct template format for path 1. Define the NLP conversion prompt, output validation rules, and edit UX for path 2.

---

## Klue Assignment and Conflict Sanity Check

When an admin assigns a Klue to a skope, konsole triggers skope's conflict sanity check before writing:

```
konsole.assign(klue, skope)
  → skope.sanity_check(klue)
    → on conflict: konsole surfaces conflict detail to admin — hard block or warning (TBD)
    → on pass: klue_id appended to skope.klue_ids
```

Conflict detection is skope's responsibility. konsole is the surface that presents the result to the admin and enforces the block or warning. konform is not involved.

> ⚠️ **TODO (design):** Define conflict severity levels — hard block vs warning. Define the conflict detail UI in konsole (which Klues conflict, on what target, with what verdicts).

---

## Needs / Needed by

| | |
|---|---|
| **Needs** | klue registry, skope |
| **Needed by** | — (admin-facing only) |

---

## Relevant ADRs

> None assigned yet — pending design session.

---

## TODO

- Full design session — after klue registry and skope design sessions
- Klue struct template — define format for structured upload path
- NLP conversion — prompt design, output validation, edit UX
- Conflict surfacing UI — severity levels, detail display
- User/team to skope binding — auth layer integration (TBD)
- skope management UI — create, edit, deactivate
