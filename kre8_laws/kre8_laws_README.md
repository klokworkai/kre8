# kre8_laws

## Overview
`kre8_laws` is the validation and governance component of kre8.

It defines the reusable rules, policy sets, and validation logic that determine whether interpreted requests and resulting design intents are valid, allowed, warning-worthy, or blocked.

## Purpose
The laws component exists to ensure that kre8 does not generate infrastructure designs without regard to platform rules, security requirements, compliance expectations, or standard architectural boundaries.

## Core Responsibilities
- Validate Structured Intent
- Enforce reusable law sets
- Return validation status and issues
- Support required, warning, and advisory outcomes
- Work with realm bindings to determine applicable rule sets
- Support scoped exceptions where necessary

## What Laws Answer
A law set should answer:

- What is required?
- What is allowed?
- What is denied?
- What should produce a warning?

## Typical Law Domains
- Security
- Networking
- Platform standards
- Cost guardrails
- Compliance
- Naming and tagging conventions

## Validation Outcomes
Typical outcomes include:
- valid
- valid with warnings
- invalid

These outcomes are intended to influence the user checkpoint and downstream plan generation flow.

## Relationship to Other Components
- Validates outputs used by `kre8_think`
- Applies within the context of `kre8_realm`
- Can be managed through `kre8_whiteboard`
- Produces results that may be surfaced in `kre8_kiosk`

## Current Status
Planned component and documented concept.

Its role is central to the trustworthiness and determinism of the platform.

## Future Scope
- Reusable law profiles
- Severity-based validation responses
- Realm-specific law bindings
- Exception handling and waiver models
- Preview/testing workflows in Whiteboard
