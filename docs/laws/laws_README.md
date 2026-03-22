# Laws

## Overview
Laws are the reusable policy and validation constructs used by kre8 to determine whether interpreted intent and resulting design artifacts are acceptable, warning-worthy, or blocked.

## Purpose
Laws ensure that kre8 does not generate design output without regard to platform guardrails, governance standards, and architectural constraints.

## What Laws Cover
Typical law domains include:
- security
- networking
- platform standards
- compliance
- cost guardrails
- naming and tagging rules

## Validation Role
Laws act on structured artifacts, especially Structured Intent, and are expected to produce outcomes such as:
- valid
- valid with warnings
- invalid

## Product Role
Laws influence:
- validation checkpoints in the user flow
- pause behavior before Design Plan generation
- realm-bound governance outcomes
- what Whiteboard administrators define and maintain

## Documentation Strategy
Keep concept-level law documentation here.
Keep component-specific implementation notes inside `kre8_laws/README.md`.
