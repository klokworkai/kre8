# ADR-008: kiosk depends on konnekt directly for init/re-init — i2d2 is not a universal proxy

**Status:** Active
**Date:** 2026-07-04

## Context

kiosk must guarantee konnekt is initialized (probed against all configured
providers) every time it launches, with a hard stop and a clear, categorized
error if init fails — not an interim measure, not something users opt into.
kiosk must also expose a manual re-init, usable at any time, for use after key
rotation or `secrets.yaml` edits.

konnekt has no HTTP surface of its own. It is a plain Python library —
`probe.probe_all()`, `konnekt.complete()` — imported directly by whatever
needs it. Today that is i2d2 and koder. The component table lists kiosk's only
documented dependency as i2d2, which raised a real question: does kiosk reach
konnekt by adding a thin passthrough endpoint on i2d2 (`POST /probe`), or by
importing konnekt directly, the same way i2d2 and koder already do?

kli (the CLI tool) is not being built as a terminal UX. The `kre8 init` /
`kre8 probe` commands referenced in earlier konnekt design notes have no home
unless something else calls konnekt's init/probe directly.

## Decision

kiosk imports konnekt directly, in-process, for `init()` and `re-init()` only.
All design-flow calls — Kit extraction today, kick/kraph/kanvas/koder once
built — continue to go through i2d2 over HTTP.

kiosk therefore has two structurally different edges:
- **kiosk → konnekt** — in-process import, init/re-init only
- **kiosk → i2d2** — HTTP, design/dummy-run flow only

## Rationale

- konnekt init/probe is a lifecycle concern, not a design decision. Routing it
  through i2d2 would make i2d2 a pass-through gateway for functionality it has
  no reasoning role in — scope creep against i2d2's defined role as sole design
  authority (ADR-004).
- Precedent already exists: konsole depends on skope and krule_registry
  directly, not through i2d2, for its own admin-plane concerns. Extending the
  same pattern to kiosk↔konnekt keeps one consistent rule — reasoning-plane
  calls go through i2d2, infra/lifecycle-plane calls go direct — instead of
  special-casing kiosk.
- konnekt has no service boundary to cross. Both i2d2 and koder already import
  it directly; kiosk becomes a third direct importer, not a new kind of
  dependency on the system.

## Consequences

- The two-edge shape is not visible in the pipeline diagram (`NLP → Kit →
  kick → ...`) and must stay explicit in `docs/components/kiosk.md` and
  `docs/architecture.md`'s build-state diagram, or it will look like a
  layering violation to a future contributor.
- Any future component needing konnekt lifecycle guarantees (e.g. a future
  headless API-mode client, if kli resurfaces in that form) should follow the
  same direct-import pattern rather than proxying through i2d2.
- If konnekt is ever split out into its own service — not currently planned —
  this decision needs revisiting, since the direct-import assumption breaks.
- Secrets themselves remain entirely inside konnekt's existing `secrets.yaml` +
  GCP Secret Manager flow. kiosk does not read, write, or proxy secrets in any
  form — it only triggers init/re-init and displays the categorized result.
