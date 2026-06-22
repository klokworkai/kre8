# kre8 — Component Registry
**Last Updated:** June 2026

---

## Component Table

| Component | Folder | Role | Needs | Needed by | Status |
|---|---|---|---|---|---|
| i2d2 | `i2d2/` | Orchestrator + reasoning engine. Owns Kit extraction, kick resolution, krux generation, DAG validation, kanvas assembly, config resolution, all katalog writes. | konnekt, klue registry, konform, skout, skan, koder | kiosk | INPROGRESS |
| konnekt | `konnekt/` | LLM adapter — all model calls go through here. Model strings live here only. | external LLMs, GCP SM | i2d2, koder | DONE |
| kiosk | `kiosk/` | Developer UI — NLP in, HCL out. | i2d2 | — | TODO |
| koder | `koder/` | HCL synthesizer. | konnekt, HashiCorp Terraform MCP | i2d2 | TODO |
| katalog | `katalog/` | Artifact store — kit, kick, krux, kanvas, HCL. Stub at MVP. | — | i2d2, koder, skout | TODO |
| konform | `konform/` | Stateless policy gate (OPA). Validates kit+kick at kg1, kanvas at kg2. Never writes, never designs. | klue registry | i2d2 | NOT STARTED |
| klue registry | `klue_registry/` | Policy definitions only — pure data store, no behavior. Source of truth for what is allowed/denied/limited. | — | i2d2, konform | NOT STARTED |
| skope | `skope/` | Environment + workload context. Scopes what a user is allowed to design with. | — | i2d2 | NOT STARTED |
| skout | `skout/` | Semantic search + re-ranking over kpedia. Surfaces similar prior designs pre-krux. | kpedia | i2d2 | NOT STARTED |
| skan | `skan/` | Cloud infra scanner — reads live cloud state. Dual call path: direct from kiosk (mermaid.js diagrams) and from i2d2 (design context for MODIFY). | cloud APIs (Steampipe) | i2d2, kiosk | NOT STARTED |
| kpedia | `kpedia/` | RAG knowledge base — pillars, forums, provider docs, skan findings. pgvector. Owns its own scheduled scraping/ingestion internally. | — | skout | NOT STARTED |
| kast | `kast/` | Slack/webhook notifier. | external webhooks | i2d2 | NOT STARTED |
| konsole | `konsole/` | Admin UI — manages skope, klue registry config. | skope, klue registry | — | NOT STARTED |

---

## Artifacts

| Artifact | Produced by | Consumed by | Stored in |
|---|---|---|---|
| kit | i2d2 | i2d2, konform | katalog |
| kick | i2d2 | i2d2, konform | katalog |
| krux | i2d2 | i2d2, konform | katalog |
| kanvas | i2d2 | koder, konform | katalog |
| skan findings | skan | i2d2 | TBD |
| HCL | koder | — | katalog |

> **kick** — kit_id + resolved klue registry policy IDs for this run. Produced by i2d2 directly (reads klue registry as data, infers via its own LLM call). i2d2 checks katalog for an existing matching kick before re-resolving.

---

## Deferred (TODO — not current build frame)

| Item | Folder | Notes |
|---|---|---|
| kure | `koder/kure/` | Post-koder HCL lint + self-correct loop — build after koder is done |
| kraken mechanics | `i2d2/` | kraken_report, kill switches, drift handling — post-MVP |
| pause_for_review | `i2d2/` | Pipeline suspension + resume loop — post-MVP |
| SecretsAdapter | `konnekt/` | Cloud-agnostic vault abstraction — post ship-ready |

---

## Parked (undecided — may or may not be implemented)

| Item | Folder | Notes |
|---|---|---|
| gate | `gate/` | API ingress — kiosk connects directly for now; unclear if a separate ingress layer is needed |
| kli | `kli/` | CLI tool — raw API calls sufficient for now; value unclear vs kiosk |

---

## Naming Conventions

- All component names start with **k** (exception: `gate`)
- Folder names use component name directly — no `kre8-` prefix inside mono-repo
- Python imports use folder name: `from konnekt.router import ...`
- The umlaut (klökwork) is **visual/brand only** — all code, CLI, domains use `klokwork`
