# kre8 — Component Registry
**Last Updated:** June 2026

---

## Component Table

| Component | Folder | Role | Needs | Needed by | Status |
|---|---|---|---|---|---|
| i2d2 | `i2d2/` | Orchestrator + reasoning engine. Owns Kit extraction, krux generation, DAG validation, all katalog writes. | konnekt, klue, konform, skout, skan, knit, koder | kiosk | INPROGRESS |
| konnekt | `konnekt/` | LLM adapter — all model calls go through here. Model strings live here only. | external LLMs, GCP SM | i2d2, koder | DONE |
| kiosk | `kiosk/` | Developer UI — NLP in, HCL out. | i2d2 | — | TODO |
| koder | `koder/` | HCL synthesizer. | konnekt, HashiCorp Terraform MCP | i2d2 | TODO |
| katalog | `katalog/` | Artifact store — kit, kick, krux, kanvas, HCL. Stub at MVP. | — | i2d2, koder, skout | TODO |
| konform | `konform/` | Stateless policy gate (OPA). Validates kit at kg1, kanvas at kg2. Never writes, never designs. | klaws | i2d2 | NOT STARTED |
| klaws | `klaws/` | Policy definitions (Rego/LADE) + klues store. | — | konform, klue, kwery | NOT STARTED |
| skope | `skope/` | Environment + workload context. Scopes what a user is allowed to design with. | — | i2d2, klue, kwery | NOT STARTED |
| klue | `klue/` | Infers kick (applicable klaws policy IDs) from kit + skope. Checks klues store before LLM inference. | klaws | i2d2 | NOT STARTED |
| knit | `knit/` | Assembles kanvas from krux — applies konfig values. Deterministic, no LLM. | kwery | i2d2 | NOT STARTED |
| kwery | `kwery/` | Resolves provider config values scoped by kick + skope. Internal lookup, no LLM. | skope, klaws | knit | NOT STARTED |
| skout | `skout/` | Semantic search + re-ranking over kpedia. Surfaces similar prior designs pre-krux. | kpedia | i2d2 | NOT STARTED |
| skan | `skan/` | Cloud infra scanner — reads live cloud state, feeds findings to i2d2. | cloud APIs (Steampipe) | i2d2 | PARKED |
| kpedia | `kpedia/` | RAG knowledge base — pillars, forums, provider docs, skan findings. pgvector. | — | skout | NOT STARTED |
| komb | `komb/` | Web scraper — feeds kpedia collections on a schedule. | — | kron | NOT STARTED |
| kron | `kron/` | Scheduler — triggers komb. | komb | — | NOT STARTED |
| kast | `kast/` | Slack/webhook notifier. | external webhooks | i2d2 | NOT STARTED |
| konsole | `konsole/` | Admin UI — manages skope, klaws config. | skope, klaws | — | NOT STARTED |
| gate | `gate/` | API ingress (parked — kiosk connects directly for now). | i2d2 | external clients | PARKED |
| kli | `kli/` | CLI tool (parked). | gate, i2d2 | — | PARKED |

---

## Artifacts

| Artifact | Produced by | Consumed by | Stored in |
|---|---|---|---|
| kit | i2d2 | i2d2, klue, konform | katalog |
| kick | klue | i2d2, konform | katalog |
| krux | i2d2 | knit, konform | katalog |
| kanvas | knit | koder, konform | katalog |
| skore | skout | i2d2 | kpedia + i2d2 working memory |
| skan findings | skan | i2d2 | TBD |
| HCL | koder | — | katalog |

> **klues** — the kick store inside klaws. Previously inferred kicks promoted for reuse. Not a pipeline artifact — owned by klaws, read by klue.

> **kick** — Kit Inferred Contextual Klaws. Live per-run artifact produced by klue. Contains the set of applicable klaws policy IDs for this kit + skope combination.

---

## Parked

| Item | Folder | Notes |
|---|---|---|
| gate | `gate/` | API ingress — kiosk connects directly for now |
| kli | `kli/` | CLI tool — not prioritized |
| kure | `koder/kure/` | Post-koder HCL lint + self-correct loop — parked until koder is built |
| skore | `skout/skore/` | skout re-ranked results artifact — park until skout is designed |
| skan | `skan/` | Cloud scanner — dedicated design session needed |
| klue learning loop | `klue/` | Successful LLM-fallback kicks promoted into klaws.klues — post-MVP |
| kraken mechanics | `i2d2/` | kraken_report, kill switches, drift handling — post-MVP |
| pause_for_review | `i2d2/` | Pipeline suspension + resume loop — post-MVP |
| kombine/konverge | — | Krux composition feature — post-MVP |
| SecretsAdapter | `konnekt/` | Cloud-agnostic vault abstraction — post ship-ready |

---

## Naming Conventions

- All component names start with **k** (exception: `gate`)
- Folder names use component name directly — no `kre8-` prefix inside mono-repo
- Python imports use folder name: `from konnekt.router import ...`
- The umlaut (klökwork) is **visual/brand only** — all code, CLI, domains use `klokwork`
