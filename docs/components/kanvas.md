# kanvas — Artifact Design
**Status:** LOCKED | **Produced by:** i2d2 | **Consumed by:** koder, konform | **Stored in:** katalog

---

## Role

Kanvas is the full infrastructure manifest — the complete, policy-validated, konfig-resolved artifact that koder synthesizes into HCL. It wraps a kraph (with konfig resolved and assembled directly by i2d2) and carries the design_conflicts verdict from both konform gates.

Kanvas is stored in katalog pre-kg2 gate. koder receives kanvas only after kg2 passes.

---

## Schema

```
GateVerdict
  pass: bool
  violated_krule_ids: list[str] = []

DesignConflicts
  kg1: GateVerdict
  kg2: GateVerdict

Kanvas
  id: UUID                    # auto-generated
  kraph: Kraph                # fully populated — konfig resolved by i2d2
  konfig: dict = {}           # opaque — typed when kanvas assembly is designed
  design_conflicts: DesignConflicts
  kraken: bool = False        # propagated from kraph — traceability only; kraken=true blocks koder invocation
```

---

## Notes on konfig

`konfig` is the resolved configuration block assembled by i2d2 during kanvas assembly. As of now, `konfig` is an empty dict. The shape will be defined during the kanvas assembly design session.

---

## Lifecycle

```
i2d2 assembles kanvas from kraph
  → katalog.write(kanvas)           # pre-kg2
  → konform(kanvas, kick_id)        # kg2 gate
    → kanvas.design_conflicts.kg2 updated in katalog
  → if kg2.pass:
      → koder(kanvas) → HCL
  → if kraken (regardless of kg2):
      → koder NOT invoked — kanvas is terminal output
      → manual re-submit with kraken: false required to proceed to HCL
```

---

## kraken Behaviour

When `kraken: true`:
- kg1 and kg2 gates run normally — violations recorded in `design_conflicts`
- i2d2 does NOT halt on gate failures
- koder is NOT invoked in kraken mode — kanvas is the terminal output. Skipping koder avoids an expensive LLM call on what may be an experimental or review-only run.
- A manual approval step is required before koder can be invoked post-kraken review.
- `kraken` propagates kit → kick → kraph → kanvas for full traceability

> ⚠️ **TODO (design):** Define the manual approval mechanism for kraken → koder invocation (kiosk approval flow, CLI flag, or explicit re-submit with kraken: false).

---

## Design Decisions

- Kanvas stored pre-kg2 — i2d2 writes to katalog before gate runs
- konform is purely stateless — never writes to katalog
- i2d2 is the only writer to katalog
- `konfig` is opaque at the moment (`dict = {}`) — typed during kanvas assembly design
- `design_conflicts` carries both gate verdicts — kg1 populated at kit gate, kg2 at kanvas gate
- `violated_krule_ids` — references krule_registry policy IDs

## Relevant ADRs

ADR-002 · ADR-003 · ADR-004 · ADR-006 · ADR-007
