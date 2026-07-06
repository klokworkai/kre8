# kiosk — Component Design
**Status:** INPROGRESS (scaffold in place, no wiring yet) | **Folder:** `kiosk/`

---

## Role

kiosk is the developer-facing entry point to kre8 — NLP in, HCL out, once the
full pipeline exists. Until i2d2's downstream stages (kick, kraph, kanvas,
koder) are built, kiosk runs a dummy flow that exercises exactly as much of
the pipeline as is real, and says so plainly for the rest — no illusion of
completeness ahead of the actual code.

kiosk is also the sole caller of konnekt's init/probe lifecycle. This is not
an interim measure — kiosk always initializes konnekt on launch, for the
lifetime of the project, independent of how much of the design pipeline
exists at any given time.

---

## Current State

Scaffold implemented: `server.py` (FastAPI app, `/` serves `static/index.html`,
`/health`, `/static` mount, `POST /shutdown` — responds first, then schedules
a graceful `SIGTERM` via `asyncio.get_running_loop().call_later()`, must be
`async def` since a sync route runs in a worker thread with no event loop),
`__main__.py` (`python -m kiosk`, no console-script entry point yet — see
`pyproject.toml` packaging gap in `CLAUDE.md`), and `static/index.html` +
`style.css` + `app.js`. The page has the intent textarea, an output box, and
Design / Konnekt / Close buttons. Only Close is wired — it POSTs `/shutdown`
and disables the page. Design and Konnekt are present in the DOM but have no
click handlers; konnekt init-on-launch, manual re-init, and the i2d2
dummy-run flow described below are all still unwired.

## Responsibilities (v0 — this build)

- **konnekt init on launch** — kiosk calls konnekt's init/probe every time it
  starts, before anything else runs. Hard stop on failure — no degraded mode,
  no partial launch.
- **Categorized init failure** — failures are surfaced as one of three
  categories, not a raw exception string (now implemented on the konnekt
  side as `KonnektError.category`; kiosk-side display wiring is still open):
  - `no_creds` (no credentials defined for the provider in `secrets.yaml`)
  - `invalid_secret_store` (`secrets.yaml` has project + secret name configured, but the GCP Secret Manager call fails)
  - `invalid_api_keys` (key retrieved fine, but the model provider rejected it)
  - if `probe_all()` fails for more than one provider and the categories
    differ, `KonnektError.category` is `None` and
    `KonnektError.category_breakdown: dict[provider, category]` carries the
    per-provider detail — kiosk should display this breakdown rather than
    guessing from a single top-level category
- **Manual re-init** — always available, not gated behind any other app
  state. Used after key rotation, `secrets.yaml` edits, or a transient failure.
- **Dummy run** — accepts NL input, `POST`s to i2d2 `/process`, displays the
  returned Kit. Displays a static notice that kick/kraph/kanvas/koder are not
  yet implemented. One request, one response — no polling, no retry loop.

---

## Explicitly out of scope (v0)

- **Secrets editing, in any form.** konnekt's `secrets.yaml` + GCP Secret Manager
  flow is untouched and out of kiosk's reach entirely — edited outside kiosk,
  by whoever runs it. konsole is the only planned future home for secrets
  provider management (see `docs/components/konsole.md`).
- katalog browsing — needs katalog to exist.
- skan live-scan diagram rendering — needs skan to exist.
- Any pipeline stage beyond Kit extraction.

---

## Dependencies

| | |
|---|---|
| **Needs** | i2d2 (HTTP — design/dummy-run flow) · konnekt (direct import — init/re-init only) — see ADR-008 |
| **Needed by** | — |

kiosk has two structurally different edges to the rest of the system. This is
deliberate, not an oversight — see ADR-008 for why konnekt is not reached
through i2d2.

---

## Interface (planned)

- `GET /` — serves the UI shell (static HTML/JS)
- Backend calls `konnekt.probe.probe_all()` directly on process start, and
  again on manual re-init
- Backend proxies design-flow requests to i2d2 over HTTP — `POST
  <i2d2_host>/process`

UX shape: a minimal local web UI — FastAPI backend serving static HTML/JS,
modeled on kollab's `server.py` + `static/` pattern (single FastAPI app,
`StaticFiles` mount, plain JS frontend, no build step). No CLI, no terminal
UI — kli is not being built as a terminal UX (see `docs/components.md` —
Parked).

---

## Relevant ADRs

- ADR-008 — kiosk depends on konnekt directly for init/re-init; i2d2 is not a
  universal proxy

---

## TODO

**Design:**
- Define exactly how `category` / `category_breakdown` render in the UI
  (banner copy per category, how a multi-provider breakdown is laid out).
- Define the dummy-run UI: Kit display format, static
  "not yet implemented" notice copy.

**Code:**
- Wire init-on-launch calling `konnekt.probe.probe_all()`, hard stop on
  failure, surfacing `category`/`category_breakdown`
- Wire manual re-init endpoint/control (Design/Konnekt buttons currently
  inert)
- Wire dummy-run: form → `POST i2d2/process` → render Kit → static notice
- Console-script entry point (`kre8` → `kiosk.__main__:main`) blocked on the
  `pyproject.toml` packaging gap — see `CLAUDE.md` Pending Action Items
