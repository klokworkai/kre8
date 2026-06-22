# kanvas — Artifact Design
**Status:** LOCKED (MVP) | **Produced by:** i2d2 | **Consumed by:** koder, konform | **Stored in:** katalog

---

## Role

Kanvas is the full infrastructure manifest — the complete, policy-validated, konfig-resolved artifact that koder synthesizes into HCL. It wraps a krux (with konfig resolved and assembled directly by i2d2) and carries the design_conflicts verdict from both konform gates.

Kanvas is stored in katalog pre-kg2 gate. koder receives kanvas only after kg2 passes (or kraken is true).

---

## Schema

```
GateVerdict
  pass: bool
  violated_klue_registry_ids: list[str] = []

DesignConflicts
  kg1: GateVerdict
  kg2: GateVerdict

Kanvas
  id: UUID                    # auto-generated
  krux: Krux                  # fully populated — konfig resolved by knit
  konfig: dict = {}           # knit output — opaque at MVP, typed when knit is designed
  design_conflicts: DesignConflicts
  kraken: bool = False        # propagated from krux — traceability
```

---

## Notes on konfig

`konfig` is the resolved configuration block assembled by i2d2 during kanvas assembly. At MVP, `konfig` is an empty dict. The shape will be defined during the kanvas assembly design session.

---

## Lifecycle

```
i2d2 assembles kanvas from krux
  → katalog.write(kanvas)           # pre-kg2
  → konform(kanvas, kick_id)        # kg2 gate
    → kanvas.design_conflicts.kg2 updated
  → if kg2.pass OR kraken:
      → koder(kanvas) → HCL
```

---

## kraken Behaviour

When `kraken: true`:
- kg1 and kg2 gates run normally — violations recorded in `design_conflicts`
- i2d2 does NOT halt on gate failures
- koder runs regardless of gate results
- `kraken` propagates kit → kick → krux → kanvas for full traceability

---

## Design Decisions

- Kanvas stored pre-kg2 — i2d2 writes to katalog before gate runs
- konform is purely stateless — never writes to katalog
- i2d2 is the only writer to katalog
- `konfig` is opaque at MVP (`dict = {}`) — typed during kanvas assembly design
- `design_conflicts` carries both gate verdicts — kg1 populated at kit gate, kg2 at kanvas gate
- `violated_klue_registry_ids` — references klue registry policy IDs, not klaws

## Relevant ADRs

ADR-002 · ADR-003 · ADR-004 · ADR-006 · ADR-007
