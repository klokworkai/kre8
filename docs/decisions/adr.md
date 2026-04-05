# kre8 — Architecture Decision Records
**Last Updated:** April 2026

This file captures committed architectural decisions for kre8.
Format: Context → Options Considered → Decision → Rationale.

---

## ADR-001 — Separate Context from Policy

**Context:** Defaults, environment assumptions, and governance rules were initially considered as one concern.

**Options:**
- Single component handles context + policy
- Split into two distinct components

**Decision:** Split into `kontext` (context/defaults) and `kodex` (policy/governance).

**Rationale:** Kontext defines *what the environment is*. Kodex defines *what is allowed*. These change at different rates, owned by different personas (platform team vs security team), and must be independently auditable.

---

## ADR-002 — SI Pause (Go / Review)

**Context:** Some users want to inspect and edit the StructuredIntent before design proceeds. Others want fully automatic flow.

**Options:**
- Always pause for review
- Never pause, fully automatic
- Optional pause controlled by user/realm config

**Decision:** SI exposes a `pause_for_review` flag. Kiosk surfaces the SI for editing if true. Kontext config sets the default per environment.

**Rationale:** Balances simplicity for casual users with control for advanced users. SI becomes a first-class auditable artifact rather than an internal implementation detail.

---

## ADR-003 — Mono-repo with Extractable Boundaries

**Context:** Need to balance fast MVP iteration with a future microservices architecture.

**Options:**
- Full microservices from day one
- Coupled monolith
- Mono-repo with clean component boundaries

**Decision:** Single repo (`klokworkai/kre8`) with each component in its own folder, self-contained (own `requirements.txt`, `Dockerfile`, `tests/`). No cross-component direct imports.

**Rationale:** Faster iteration now. Clean extraction into individual repos later with minimal friction. Flat-root structure enforced — no nested monorepo wrappers.

---

## ADR-004 — LLM is Non-Authoritative

**Context:** LLMs are probabilistic and can hallucinate. Giving LLMs direct execution authority over infrastructure is unsafe.

**Options:**
- LLM generates and executes IaC directly
- LLM generates structured JSON only, validated before any downstream use

**Decision:** LLM output is always structured JSON, always Pydantic-validated, never passed raw to any downstream component. LLM never triggers execution.

**Rationale:** Deterministic validation gates (konform/OPA) sit between every LLM call and the next pipeline stage. This makes the system auditable, safe, and testable independently of LLM behavior.

---

## ADR-005 — koder owns Context7 integration

**Context:** Context7 provides up-to-date provider API docs needed for accurate HCL synthesis. Question was whether this belongs in kpedia or koder.

**Decision:** koder calls Context7 directly at synthesis time and writes responses into `kpedia/utd_docs` as a write-through cache. Cache-first on subsequent calls.

**Rationale:** koder is the consumer of this data — it knows what module docs it needs at the point of synthesis. kpedia owns the storage. komb owns scraping for pillars/forums. Clean separation of who fetches what.

---

## ADR-006 — Company and Product Naming

**Decision:**
- Company: klökwork Inc, operating as klökwork AI
- Product: kre8 by klökwork AI
- The umlaut (ö) is visual/brand only — all code, CLI, domains, GitHub use `klokwork`
- GitHub org: `klokworkai`
- All component names start with `k` where possible
- Mono-repo: `klokworkai/kre8`

**Rationale:** "klok" means smart/wise in Swedish. "Klokwork" = clockwork precision + smart/wise. The k-naming convention creates brand cohesion across components while remaining typeable and functional.

---

## ADR-007 — kre8 is the Engine (SUPERSEDED by ADR-008)

~~**Decision:** Drop the I2D2 label entirely. The `kre8` component *is* the engine.~~

**Status: Superseded by ADR-008.** This decision was reversed. See ADR-008 for current state and rationale.

---

## ADR-008 — i2d2 Reinstated as Named Engine Inside kre8

**Context:** ADR-007 dropped the i2d2 label, treating `kre8` as both the component name and the engine name. After further review, this conflated two distinct concepts: the TPL framework (kre8) and its internal reasoning engine (i2d2).

**Options:**
- Keep ADR-007: `kre8` component = engine, no separate i2d2 label
- Reinstate i2d2 as the named reasoning engine inside the `kre8` component

**Decision:** i2d2 (Intelligent Infrastructure Design Decision) is reinstated as the named reasoning engine that powers the `kre8` component. `i2d2.py` is the orchestration entry point inside `kre8/`.

**The distinction:**
- **kre8** is the TPL framework product — the umbrella platform and the `kre8/` component within it
- **i2d2** is the reasoning engine *inside* the `kre8` component — the mechanism that transforms StructuredIntent into a validated Kanvas
- kre8 (framework) is powered by kre8 (component), which is powered by i2d2 (engine)

**Rationale:**
- Conceptual clarity: the reasoning engine deserves its own identity separate from the component and framework names
- Branding: i2d2 as a named engine strengthens the product narrative — "kre8 is a Thinking Platform Layer, powered by the i2d2 engine"
- Naming collision: without i2d2, the word "kre8" carries three meanings simultaneously (framework, component, engine). Named separation eliminates this ambiguity.
- The README clearly states: "At its core is i2d2 — the reasoning engine that transforms raw intent into structured, policy-validated infrastructure design decisions"

**Rule going forward:** Any change to a decision already captured in an ADR must supersede or amend that ADR in the same commit as the CLAUDE.md update. ADRs and CLAUDE.md must never be out of sync.
