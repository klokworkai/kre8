# Kiosk

## Overview
Kiosk is the end-user interaction surface for kre8.

It is intended to support both:
- users who want a simple request-and-receive experience
- advanced users who may want to inspect or modify the system’s interpreted intent before proceeding

## Canonical User Modes
A user may:
- ask for a completely new Design Plan in natural language
- browse ARC and choose an existing Design Plan
- choose an existing Design Plan and request changes in natural language

## Key UX Checkpoint
After Structured Intent is generated and validated, the system should pause and allow the user to choose:

- **Go** — continue with the current interpretation
- **Review** — inspect and potentially modify the interpreted intent

## Relationship to Other Components
- realm-aware behavior through `kre8_realm`
- validation display influenced by `kre8_laws`
- selection and reuse through `kre8_arc`
- plan generation orchestrated by `kre8_think`

## Documentation Strategy
Keep user-flow and product-level kiosk behavior here.
Keep component-specific implementation notes inside `kre8_kiosk/README.md`.
