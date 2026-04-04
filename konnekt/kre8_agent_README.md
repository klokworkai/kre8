# kre8_agent

## Overview
`kre8_agent` is the AI interaction and orchestration adapter for kre8.

It is responsible for brokering structured interactions between the kre8 thinking layer and external LLM providers or model-serving backends. In the current demo repository, it is implemented as a stubbed adapter used to validate overall system flow before live LLM integration is introduced.

## Purpose
The agent exists to keep model-facing logic separated from core reasoning logic.

This allows the platform to:
- isolate prompt and response handling
- enforce structured JSON outputs
- swap model backends later with less disruption
- keep the core thinking layer focused on intent and design orchestration

## Core Responsibilities
- Receive requests from `kre8_think`
- Interact with an LLM or model backend
- Return structured outputs expected by the thinking flow
- Enforce or normalize schema-conformant responses
- Encapsulate prompt orchestration and model-specific logic

## Current Role in the Demo
At present, the agent is used as a stub to support:
- Structured Intent extraction
- placeholder design reasoning responses
- end-to-end architecture validation without live Bedrock integration

## Inputs
Typical inputs include:
- natural-language intent
- prompt context
- schema expectations
- future realm- and law-informed context

## Outputs
Typical outputs include:
- Structured Intent-compatible responses
- intermediate reasoning outputs
- design-plan-oriented structured responses

## Relationship to Other Components
- Called by `kre8_think`
- Indirectly serves flows initiated through `kre8_gate`
- May later be used by `kre8_kiosk` and `kre8_whiteboard` through orchestrated service paths rather than direct coupling

## Current Status
Implemented as a stubbed adapter in the demo repository.

## Future Scope
- AWS Bedrock integration
- provider abstraction layer
- prompt templates and prompt versioning
- structured response validation and retry handling
- model selection by task type
