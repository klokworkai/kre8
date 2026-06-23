# ADR-006: Kanvas is always stored — gate result travels with it

**Status:** Active
**Date:** 2026-06-20

## Context

The intuitive approach: store kanvas only after it passes kg2. A failed kanvas
is a rejected design — why keep it?

Two reasons that intuition breaks down:

First, kg1 and kg2 apply the same krule_registry rules. A kit that passes kg1
and produces a full kanvas will almost always pass kg2. The rare kg2 failure
occurs when vague intent in the kit resolves to explicit konfig values that
breach a boundary (a cost limit, a region restriction, a specific instance type
cap) that was not visible at the kit level. The kanvas itself is a valid design —
it just exceeded a boundary that the current skope enforces.

Second, a kanvas that fails kg2 under one skope may be a valid, ready-to-use
design under a different skope. katalog is a reusable design artifact store.
Discarding a failed kanvas discards a potentially complete infrastructure design
that another user, team, or skope configuration could use directly — or that
the original user could reuse after requesting a skope exception.

## Decision

Kanvas is always written to katalog immediately after assembly, before kg2 runs.
The kg2 gate verdict is appended to the kanvas record in katalog after the gate
completes — pass or fail.

A kanvas in katalog is always a complete design artifact. Its gate verdict is
metadata about policy compliance under the skope it was evaluated against, not
a judgment on the quality of the design.

Users browsing katalog can find a kg2-failed kanvas, inspect the violated policy
IDs, adjust konfig values or request a skope exception, and reuse the design
without starting from scratch.

## Consequences

- katalog stores designs, not just approved designs
- Gate failures are inspectable and actionable rather than silently discarded
- i2d2 writes kanvas to katalog before calling konform for kg2 (ADR-004 still
  holds — i2d2 is the writer)
- kiosk must surface gate verdict status clearly when browsing katalog — a
  kg2-failed kanvas should be visually distinct but browsable
- Policy compliance is always relative to a skope — the same kanvas can be
  compliant under one skope and non-compliant under another
