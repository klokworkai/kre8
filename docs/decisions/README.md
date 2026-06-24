# docs/decisions/

Architecture Decision Records for kre8.

ADRs capture non-obvious design decisions — ones where the reasoning needs to
outlast the conversation that made them. Not every design choice is an ADR.
Naming conventions, repo structure, and component renames live in architecture
docs, not here.

## What earns an ADR

A decision earns an ADR when a reasonable future contributor would look at the
system and ask "why is it built this way?" — and getting it wrong would cause
real damage. Each ADR here protects against a specific mistake.

## Note on numbering

This directory was reset in June 2026. Prior ADR numbers (ADR-007, ADR-008,
ADR-042) appear in git history but those files no longer exist. The decisions
they captured have either been superseded, folded into architecture docs, or
were not substantial enough to warrant preservation. The current set
(ADR-001 onwards) reflects the active architecture only.

Archived files are in `_archived/` for git history continuity.

## Index

| ADR | Title |
|-----|-------|
| ADR-001 | LLM is non-authoritative — structured JSON only, Pydantic-validated, never executes IaC |
| ADR-002 | Two konform gates: kg1 (kit) and kg2 (kanvas) |
| ADR-003 | konform is purely stateless — verdict only, never writes, never designs |
| ADR-004 | i2d2 is sole design authority and sole katalog writer |
| ADR-005 | DAG validation is owned by i2d2, not konform |
| ADR-006 | Kanvas is always stored — gate result travels with it |
| ADR-007 | Kit never normalizes — signal values extracted as-is |
