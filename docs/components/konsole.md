# konsole — Component Design
**Status:** NOT STARTED | **Folder:** `konsole/`

---

## Role

konsole is the admin UI. It is the management surface for skope, krule_registry, and user/team policy configuration. It is not in the inference or design pipeline — it operates entirely outside of i2d2's hot path.

konsole owns two internal LLM-powered methods: krule NLP conversion and krule assignment sanity check surfacing. Both route through konnekt — all LLM calls in kre8 go through konnekt. The krule_registry stores only validated structured krules, and konform never sees raw NLP or unresolved conflicts.

---

## Responsibilities

- **krule authoring** — two paths for admin krule creation (see below)
- **krule assignment** — assigns krules to skopes; triggers sanity check before writing
- **Conflict surfacing** — surfaces krule conflicts to admin at assignment time
- **skope management** — create, edit, deactivate skopes
- **User/team binding** — assign users or teams to a skope (design TBD)

---

## krule Authoring

Admins have two paths to create a krule:

**Path 1 — Structured upload**
Admin uploads a pre-filled krule struct using the kre8-provided template. konsole validates the struct on import (required fields, valid DEAL value, known type). On validation pass, admin reviews and confirms — krule is written to krule_registry.

**Path 2 — NLP conversion**
Admin writes a natural language policy intent.
```
example: "us-east-1 only. instance sizes no greater than large. instance family t only."
```
konsole calls konnekt to convert the NLP string into a structured krule. Admin inspects the output, modifies any field values as needed, and confirms. On confirmation, the structured krule is written to krule_registry.

In both paths:
- Admin sees and can edit the structured krule before it is persisted.
- krule_registry never stores raw NLP — only validated structured krules.
- The konnekt call is initiated by konsole; all LLM calls in kre8 go through konnekt.

> ⚠️ **TODO (design):** Define the krule struct template format for path 1. Define the NLP conversion prompt, output validation rules, and edit UX for path 2.

---

## krule Assignment and Conflict Sanity Check

When an admin assigns a krule to a skope, konsole triggers skope's conflict sanity check before writing:

```
konsole.assign(krule, skope)
  → skope.sanity_check(krule)
    → on conflict: konsole surfaces conflict detail to admin — hard block or warning (TBD)
    → on pass: krule_id appended to skope.krule_ids
```

Conflict detection is skope's responsibility. konsole is the surface that presents the result to the admin and enforces the block or warning. konform is not involved.

> ⚠️ **TODO (design):** Define conflict severity levels — hard block vs warning. Define the conflict detail UI in konsole (which krules conflict, on what target, with what verdicts).

---

## Needs / Needed by

| | |
|---|---|
| **Needs** | krule_registry, skope |
| **Needed by** | — (admin-facing only) |

---

## Relevant ADRs

> None assigned yet — pending design session.

---

## TODO

- Full design session — after krule_registry and skope design sessions
- krule struct template — define format for structured upload path
- NLP conversion — prompt design, output validation, edit UX
- Conflict surfacing UI — severity levels, detail display
- User/team to skope binding — auth layer integration (TBD)
- skope management UI — create, edit, deactivate
