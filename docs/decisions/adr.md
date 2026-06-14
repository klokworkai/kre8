# adr.md — Architecture Decision Index
> Individual ADR files live in `docs/decisions/`. This index provides a quick reference.
> For full rationale, open the individual file.

| ADR | Title | Status |
|-----|-------|--------|
| ADR-001 | skope and klaws are separate components | Active |
| ADR-002 | Kit pause_for_review flag | Parked |
| ADR-003 | Mono-repo with extractable boundaries | Active |
| ADR-004 | LLM output always structured JSON, always Pydantic-validated | Active |
| ADR-005 | koder owns HashiCorp Terraform MCP integration | Active |
| ADR-006 | Naming conventions | Active |
| ADR-007 | (Superseded by ADR-008) | Superseded |
| ADR-008 | i2d2 reinstated as named engine | Active |
| ADR-009 | skout owns semantic search and re-ranking | Draft |
| ADR-010 | MCP extractability as first-class design constraint | Active |
| ADR-011 | konform is a full MCP candidate | Draft |
| ADR-012 | kre8 is a Thinking Infrastructure Engine (TIE) | Active |
| ADR-013 | Cost enforcement is Gate 2 only | Active |
| ADR-014 | inferred_implicit retired — inferred: bool field on every signal | Active |
| ADR-015 | skope→klaws one-to-many mapping | Draft |
| ADR-016 | i2d2 pre-assembly before LLM design call | Draft |
| ADR-017 | Kanvas layered structure: krux + konfig | Active |
| ADR-018 | knit is deterministic — no LLM | Active |
| ADR-019 | kick artifact: kit_id + applicable klaws policy IDs | Active |
| ADR-020 | Two konform gates: kg1 (kit) and kg2 (kanvas) | Active |
| ADR-021 | klue: LLM-powered inference service for klaws policy resolution | Active |
| ADR-022 | Krux shape: flat list with layer tags | Active |
| ADR-023 | plane_refs retired — depends_on adopted | Active |
| ADR-024 | DAG validation as Pydantic model validator — i2d2 owns, not konform | Active |
| ADR-025 | kwery: kick-scoped config value resolver | Active |
| ADR-026 | Kraken mode: pipeline flag + violation collection | Draft |
| ADR-027 | Layer model replaces "plane" terminology | Active |
| ADR-028 | Foundation namespace set is closed at 5: nw, sec, iam, storage, db | Active |
| ADR-029 | Edge layer dropped | Active |
| ADR-030 | Multi-tag layer model on resources | Active |
| ADR-031 | Single depends_on field — membership/dependency distinction collapsed | Active |
| ADR-032 | depends_on targets only foundation-tagged resources | Active |
| ADR-033 | Reusable krux via inputs/outputs | Active |
| ADR-034 | design_conflicts contract is minimal: {pass, violated_klaws_ids} | Active |
| ADR-035 | Kanvas stored pre-kg2 gate | Active |
| ADR-036 | konform is purely stateless — no reads or writes to persistent stores | Active |
| ADR-037 | Step-8 retrofit path when skout findings are sufficient | Active |
| ADR-038 | kraken is toggle-only for MVP | Active |
| ADR-039 | Composite/named sub-layers deferred post-MVP | Active |
| ADR-040 | Environment handled by skope — not a schema field | Active |
| ADR-041 | kraux renamed to kombine/konverge, feature deferred post-MVP | Active |
| ADR-042 | kontext renamed to skope | Active |
