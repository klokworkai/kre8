# kre8 — Component Registry
**Product:** kre8 by klökwork AI
**Last Updated:** April 2026

---

## Component Table

| Component | Folder | One-liner | Input | Output | Calls | Called by | Phase | Status |
|---|---|---|---|---|---|---|---|---|
| i2d2 | `i2d2/` | Reasoning engine and pipeline orchestrator | NLP string | kit, krux, kanvas → katalog | konnekt, klue, konform, skout, skan, knit, koder | kiosk | 1 | INPROGRESS |
| konnekt | `konnekt/` | LLM adapter — all model calls go through here | prompt + model role | structured JSON → caller | external LLMs | i2d2, koder | 1 | INPROGRESS |
| kiosk | `kiosk/` | Developer UI | user NLP input | HCL display → UI | i2d2 | — | 1 | TODO |
| koder | `koder/` | HCL synthesizer | kanvas | HCL → katalog | konnekt | i2d2 | 1 | TODO |
| katalog | `katalog/` | Artifact store | any artifact | stored artifact → persistent store | — | i2d2, koder, skout | 1 (stub) → 2.1 (real) | TODO |
| konform | `konform/` | Policy enforcement — OPA wrapper | artifact + kick_id | pass/fail + violated_kodex_ids → caller | kodex | i2d2 | 2.1 | TODO |
| kodex | `kodex/` | Policy definitions + klues store | admin-defined policies | Rego policies → kodex store; klues store → klue | — | konform, klue, kwery | 2.1 | TODO |
| kontext | `kontext/` | Environment and workload context | admin config | context object → caller | — | i2d2, klue, kwery | 2.1 | TODO |
| klue | `klue/` | Infers kick (Kit Inferred Contextual Kodex) from kit + kontext. Checks klues store before LLM inference. | kit + kontext | kick → katalog | kodex | i2d2 | 2.1 | TODO |
| knit | `knit/` | Kanvas assembler — applies konfig onto krux | krux | kanvas → katalog | kwery | i2d2 | 2.1 | TODO |
| kwery | `kwery/` | Provider value resolver — runtime konfig lookup | resource list | konfig values → knit | kontext, kodex | knit | 2.1 | TODO |
| skout | `skout/` | Semantic search + re-ranking over kpedia | kit_id + kick_id | skore → kpedia + i2d2 working memory | kpedia | i2d2 | 2.1 | TODO |
| kpedia | `kpedia/` | RAG knowledge base — pillars, forums, utd_docs, skan(TBD) | query | relevant docs/patterns → skout | — | skout | 2.1 | TODO |
| komb | `komb/` | Web scraper — feeds kpedia collections | URLs/sources | structured knowledge → kpedia | — | kron | 2.1 | TODO |
| skan | `skan/` | Cloud infra scanner | cloud credentials | skan findings → TBD | cloud APIs | i2d2 | 2.1 | INPROGRESS |
| kron | `kron/` | Scheduler | schedule config | triggered jobs → komb | komb | — | 2.2 | TODO |
| kast | `kast/` | Slack/webhook notifier | events | notifications → external webhooks | external webhooks | i2d2 | 3 | TODO |
| konsole | `konsole/` | Admin UI | admin input | config changes → kontext, kodex | kontext, kodex | — | 3 | TODO |
| gate | `gate/` | API ingress | HTTP requests | routed requests → i2d2 | i2d2 | external clients | 3 | PARKED |
| kli | `kli/` | CLI tool | CLI commands | CLI output → terminal | gate, i2d2 | — | 3 | PARKED |

---

## Artifacts

| Artifact | Produced by | Consumed by | Stored in |
|---|---|---|---|
| kit | i2d2 | i2d2, klue, konform | katalog |
| kick | klue | i2d2, konform | katalog |
| krux | i2d2 | knit, konform | katalog |
| kanvas | knit | koder, konform | katalog |
| skore | skout | i2d2 | kpedia + i2d2 working memory |
| skan findings | skan | i2d2 | TBD — possibly kpedia |
| HCL | koder | — | katalog |

> **klues** — the kick store inside kodex. A klue is a previously inferred kick (kit + kontext + resolved policy IDs) promoted into kodex for reuse. Not a pipeline artifact — owned by kodex, read by klue. See parked: klue learning loop.

> **kick** — Kit Inferred Contextual Kodex. The live per-run artifact produced by klue. Contains the set of applicable kodex policy IDs for this kit + kontext combination.

---

## Model Routing (via konnekt)

| Task | Role | Model |
|---|---|---|
| Intent extraction | Clerk | GPT-4o-mini |
| Design reasoning | Architect | Claude Sonnet (Opus for High/Critical — threshold TBD) |
| HCL synthesis | Coder | DeepSeek-V3 |
| Self-correction | Medic | Groq Llama 3.3 |

Model names in `konnekt/` only. Opus toggle logic in `i2d2/` only.

---

## kpedia Collections

| Collection | Content | Fed by |
|---|---|---|
| `pillars/` | Well-Architected frameworks, 3rd-party best practices | komb |
| `forums/` | Stack Overflow, GitHub issues, community wisdom | komb |
| `utd_docs/` | Up-to-date provider API docs (write-through cache) | koder via Context7 |
| `skan/` | Cloud scan findings | skan (TBD) |

---

## Parked

| Item | Folder | Notes |
|---|---|---|
| gate | `gate/` | API ingress — kiosk connects directly for now |
| kli | `kli/` | CLI tool — not prioritized |
| kure | `koder/kure/` | Post-koder HCL lint + self-correct loop — parked until koder is built |
| skore | `skout/skore/` | skout re-ranked results artifact — passed to i2d2 pre-Kanvas. Park until skout is designed. |
| kre8-kite | — | Lite/SaaS version of kre8 — future product, no design yet |
| No-LLM form mode | `kiosk/` | Future feature, post-ship |
| kloud_skan intelligence | `skan/` | Naming convention inference — dedicated session needed |
| koder naming conventions | `koder/` | Depends on skan intelligence |
| workload templates | `kiosk/` | Guided UX, continuous learning loop — post-ship |
| complexity scoring logic | `i2d2/` | Kit captures flags only — scoring + Opus trigger built later |
| kontext cost envelope | `kontext/` | Design when kontext is built |
| kontext compliance advisory | `kontext/` | User-facing — design when kiosk is built |
| pause_for_review loop | `i2d2/` | i2d2 clarification questions via kiosk — rename TBD. ADR-002. |
| exclusions/kontext overlap | `i2d2/` | Revisit post-MVP when kontext is designed |
| kronicle | `kodex/` | Audit history registry under kodex — named, post-MVP |
| kombine / konverge | — | Krux composition feature (was kraux). Name undecided, post-MVP |
| $$$ mode / relaxed budget mode | `kiosk/` | May be UI framing on kraken. Mechanics TBD, post-MVP |
| klue learning loop | `klue/` | Successful LLM-fallback kicks promoted into kodex.klues store — post-MVP |
| kraken mechanics | `i2d2/` | kraken_report, kill switches, drift handling — post-MVP |
| composite / named sub-layers | `i2d2/` | app:app1 style — deferred post-MVP |
| SecretsAdapter | `konnekt/` | Cloud-agnostic vault abstraction — post ship-ready |

---

## Phase 3 — Enterprise Platform
*README placeholders only until Phase 3 begins.*

| Component | Folder | Role |
|---|---|---|
| kache | `kache/` | Session state, Kanvas history, job state |
| kue | `kue/` | Async job queue — decouple pipeline stages |
| keys | `keys/` | Auth/identity — SSO, API key management |
| keen | `keen/` | Platform observability — metrics, traces, logs |
| konf | `konf/` | Config management across components |
| kloud-skan | `kloud_skan/` | Discover and import existing cloud infra |
| klone | `klone/` | Clone/copy an existing Kanvas |
| klean | `klean/` | Teardown/destroy IaC safely |
| kre8-kite | — | Lite/SaaS version of kre8 |

---

## Naming Conventions

- All component names start with **k** (exception: `gate`)
- Folder names use component name directly — no `kre8-` prefix inside mono-repo
- When split into individual repos: `klokworkai/kre8-<component>` e.g. `klokworkai/kre8-konnekt`
- Python imports use folder name: `from konnekt.router import ...`
- The umlaut (klökwork) is **visual/brand only** — all code, CLI, domains use `klokwork`
