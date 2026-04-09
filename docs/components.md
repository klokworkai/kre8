# kre8 — Component Registry
**Product:** kre8 by klökwork AI
**Last Updated:** April 2026

---

## Phase 1 — Pilot
*Goal: Single prompt in kiosk → validated HCL output. Demoable end-to-end.*

| Component | Folder | Role | Tech |
|---|---|---|---|
| **kre8** | `kre8/` | Brain — i2d2 orchestrator, NLP→SI→Kanvas reasoning | Python, Pydantic |
| **konnekt** | `konnekt/` | Master LLM adapter/agent router | LiteLLM |
| **koder** | `koder/` | HCL synthesis engine | DeepSeek-V3, Context7 |
| **kure** | `koder/kure/` | Validate + self-correct loop (sub-module of koder) | Checkov, OpenTofu |
| **konform** | `konform/` | OPA policy engine wrapper | OPA |
| **kodex** | `kodex/` | Rego policy definitions (LADE model) | OPA Rego |
| **kontext** | `kontext/` | Environment/workload context and defaults | JSON/DB |
| **kiosk** | `kiosk/` | Developer UI — prompt in, HCL out | React, Mermaid.js |
| **konsole** | `konsole/` | Admin UI — manage kontext, kodex, konnekt config | React |

### Model Routing (via konnekt)

| Task | Role | Model |
|---|---|---|
| Intent extraction | Clerk | GPT-4o-mini |
| Design reasoning | Architect | Claude Sonnet |
| HCL synthesis | Coder | DeepSeek-V3 |
| Self-correction | Medic | Groq Llama 3.3 |

---

## Phase 2.1 — Governed Pipeline
*Goal: Policy enforcement, semantic search, knowledge base.*

| Component | Folder | Role | Tech |
|---|---|---|---|
| **skout** | `skout/` | Semantic search + re-ranking (Cohere or Groq, TBD) — katalog + kpedia | pgvector |
| **katalog** | `katalog/` | Architecture pattern catalog — stores successful Kanvas | Postgres |
| **kpedia** | `kpedia/` | RAG knowledge base (pillars, forums, utd_docs) | pgvector, Crawl4AI |
| **komb** | `komb/` | Web scraper — feeds kpedia/pillars and kpedia/forums | Crawl4AI |
| **gate** | `gate/` | API ingress, session management | FastAPI |

### kpedia Collections
| Collection | Content | Fed By |
|---|---|---|
| `pillars/` | Well-Architected frameworks, 3rd party best practices | komb |
| `forums/` | Stack Overflow, GitHub issues, community wisdom | komb |
| `utd_docs/` | Up-to-date provider API docs (write-through cache) | koder via Context7 |

---

## Phase 2.2 — Ops & Notifications
*Goal: Scheduling, alerts, bootstrap tooling.*

| Component | Folder | Role | Tech |
|---|---|---|---|
| **kron** | `kron/` | Scheduler — komb scrapes, cache TTL refresh | APScheduler |
| **kast** | `kast/` | Slack/webhook notifier for pipeline events | Webhooks |
| **kick** | `kick/` | Bootstrap/init — workspace and realm setup | Python |

---

## Phase 3 — Enterprise Platform
*README placeholders only until Phase 3 begins.*

| Component | Folder | Role |
|---|---|---|
| **kli** | `kli/` | CLI — `klok kre8 --prompt "..."` |
| **kache** | `kache/` | Session state, Kanvas history, job state |
| **kue** | `kue/` | Async job queue — decouple pipeline stages |
| **keys** | `keys/` | Auth/identity — SSO, API key management |
| **keen** | `keen/` | Platform observability — metrics, traces, logs |
| **konf** | `konf/` | Config management across components |
| **kloud-skan** | `kloud_skan/` | Discover and import existing AWS infra |
| **klone** | `klone/` | Clone/copy an existing Kanvas |
| **klean** | `klean/` | Teardown/destroy IaC safely |

---

## Parked / Unnamed

| Name | Notes |
|---|---|
| `kruise` | No definition yet |
| `krank` | No definition yet |
| `klear` | Too close to klean — parked |

---

## Naming Conventions

- All component names start with **k** (exceptions: `gate`)
- Folder names use component name directly — no `kre8-` prefix inside mono-repo
- When split into individual repos: `klokworkai/kre8-<component>` e.g. `klokworkai/kre8-konnekt`
- Python imports use folder name: `from konnekt.router import ...`
- The umlaut (klökwork) is **visual/brand only** — all code, CLI, domains use `klokwork`

---

## GitHub Structure

**Now (mono-repo):**
```
klokworkai/kre8
├── kre8/           ← brain
├── konnekt/        ← LLM router
├── koder/          ← HCL synthesis
│   └── kure/       ← validate + self-correct
├── konform/        ← OPA engine
├── kodex/          ← policies
├── kontext/        ← context/realm
├── kiosk/          ← developer UI
├── konsole/        ← admin UI
├── gate/           ← ingress (Phase 2.1)
├── katalog/        ← arch catalog (Phase 2.1)
├── skout/          ← search + rerank (Phase 2.1)
├── kpedia/         ← knowledge base (Phase 2.1)
├── komb/           ← scraper (Phase 2.1)
└── docs/
```

**Later (split repos):**
```
klokworkai/
├── kre8            ← mono-repo or orchestration
├── kre8-konnekt
├── kre8-koder
└── ...
```
