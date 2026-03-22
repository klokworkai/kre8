# Architecture

## Overview
This section describes the system-level architecture of kre8 as represented in the demo repository.

It focuses on:
- high-level component relationships
- request and response flow
- separation of concerns
- evolving product surfaces such as Kiosk and Whiteboard
- the role of realm context, laws, and ARC in the end-to-end flow

## Current System Shape
At a high level, kre8 is organized around the following concepts:

- `kre8_gate` for ingress
- `kre8_think` for intent understanding and design reasoning
- `kre8_agent` for LLM interaction
- `kre8_realm` for scoped context and defaults
- `kre8_laws` for validation and governance
- `kre8_arc` for architecture catalog, reuse, and lookup
- `kre8_kiosk` as the user-facing surface
- `kre8_whiteboard` as the administrative/configuration surface

## Canonical Flow
A generalized target flow is:

User → Realm → Input → Think → Structured Intent → Laws → Pause (Go / Review) → Design Plan → ARC

## Architectural Principles
- Separate thinking from execution
- Keep context, validation, and memory as distinct concerns
- Use structured intermediate artifacts
- Prefer reusable outputs over repeated generation where possible
- Design components so they can later be split into standalone repositories

## Purpose of this Section
Use this section to capture:
- the current architectural view
- major flow updates
- component boundary decisions
- changes to overall repository structure and product direction
