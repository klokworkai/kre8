# ADR-042: `kontext` renamed to `skope`

**Status:** Active
**Date:** 2026-06-11

## Context

The component formerly named `kontext` defines environment + workload scope (what a user is allowed to design with — resources, regions, environments). "Kontext" overlapped semantically with "intent context" and the LLM-facing notion of context windows, creating ambiguity in design docs and conversations with i2d2/klue.

## Decision

Rename `kontext` → `skope` across the codebase and all design docs (34 occurrences). `skope` better reflects its role as a scope/boundary definition consumed by i2d2, klue, and kwery.

## Consequences

- No functional change — naming only.
- All references in `docs/`, schemas, and component glossary updated.
- Future ADRs and code use `skope` exclusively; `kontext` is retired terminology.
