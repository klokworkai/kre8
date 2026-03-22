# Realms

## Overview
A realm is the scoped operating context under which user requests are interpreted and validated.

Realms exist because users often assume the platform already knows their defaults, baseline environment choices, shared resources, and applicable rules.

## Purpose
Realms provide the missing context needed to reduce ambiguity during intent interpretation and validation.

A realm should help answer:
- What exists here?
- What is standard here?
- Which defaults should be assumed?
- Which law sets apply here?

## Typical Realm Contents
- realm identity and description
- business unit, team, or application scope
- cloud or platform defaults
- environment list such as dev, qa, prod
- default regions
- shared infrastructure references
- bindings to law sets
- optional scoped exceptions

## Product Role
Realms influence:
- how `kre8_think` interprets requests
- how `kre8_laws` validates requests
- which ARC entries may be relevant
- what the user sees or assumes in Kiosk
- what administrators configure in Whiteboard

## Documentation Strategy
Keep concept-level realm documentation here.
Keep component-specific implementation notes inside `kre8_realm/README.md`.
