# kre8_think

## Overview
`kre8_think` is the core reasoning engine of kre8 and currently represents the main implementation of the Thinking Platform Layer (TPL).

It is responsible for transforming user infrastructure intent into structured intermediate artifacts and, ultimately, Design Plans governed by system context and rules.

## Purpose
The thinking layer exists to separate infrastructure reasoning from infrastructure execution.

Instead of provisioning resources directly, it focuses on:
- understanding intent
- structuring that intent
- reasoning about design choices
- validating constraints
- producing deterministic design artifacts

## Core Responsibilities
- Orchestrate intent extraction
- Produce Structured Intent (SI)
- Invoke design reasoning workflows such as I2D2
- Work with realm context and law validation
- Produce or prepare Design Plan outputs
- Coordinate with the agent layer for AI-backed reasoning

## Key Internal Concepts
- **Structured Intent (SI)**: the intermediate, structured representation of user intent
- **Design Plan (DP)**: the architecture-oriented output delivered back to the user
- **I2D2**: the internal design reasoning engine used to generate infrastructure design decisions

## Inputs
Typical inputs include:
- natural-language infrastructure intent
- selected or default realm context
- optional baseline Design Plan from ARC
- optional user-requested delta against an existing Design Plan

## Outputs
Typical outputs include:
- Structured Intent
- validation-ready intermediate artifacts
- Design Plan outputs
- future recommendations or refinement candidates

## Relationship to Other Components
- Receives requests through `kre8_gate`
- Uses `kre8_agent` for LLM interaction
- Will work with `kre8_realm` for context
- Will work with `kre8_laws` for validation
- Will work with `kre8_arc` for reuse and retrieval
- Will support user-facing flows through `kre8_kiosk`

## Current Status
This is the most active implementation area in the demo repository and currently contains the intent extraction and I2D2 orchestration skeleton.

## Future Scope
- fuller SI handling
- realm-aware context enrichment
- laws-aware validation checkpoints
- ARC-backed retrieval and reuse
- separation into clearer internal modules or eventual standalone service boundaries
