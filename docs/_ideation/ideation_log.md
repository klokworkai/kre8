# kre8 Framework -- Ideation & Architecture Log

**Generated on:** 2026-02-27 20:11 UTC

------------------------------------------------------------------------

## 1. Origin of the Idea

The initial spark for kre8 began as a personal productivity improvement
idea: - Use AWS Bedrock (Agent/LLM) to accept chat input. - Generate
Terraform infrastructure code. - Reduce repetitive infrastructure coding
effort.

This simple assistant concept evolved into a broader architectural
vision.

------------------------------------------------------------------------

## 2. Evolution of the Concept

### 2.1 From Tool to Layer

The idea matured from: - "AI that writes Terraform"

To:

-   A reasoning engine for platform creation
-   A system that understands intent, constraints, and tradeoffs
-   A higher-level abstraction over infrastructure tooling

This led to the introduction of the:

-   **AI Platform Engineering (AIPE)** discipline concept
-   **Thinking Platform Layer (TPL)** architectural model

------------------------------------------------------------------------

## 3. Core Definitions (Locked In)

### 3.1 AIPE -- AI Platform Engineering

AIPE represents the discipline of applying AI-assisted reasoning to
platform engineering workflows, including design, cost modeling, and
guardrail enforcement.

### 3.2 TPL -- Thinking Platform Layer

In our architecture, the Thinking Platform Layer is a reasoning layer
that: - Accepts user intent - Applies constraints (cost, region,
policies) - Produces a structured platform design plan

### 3.3 kre8

The product/framework implementing TPL.

Canonical definition:

> The kre8 framework is a Thinking Platform Layer for self-serve
> platform creation.

------------------------------------------------------------------------

## 4. Target Audience & Positioning

Primary target users: - Infrastructure teams - Platform engineering
teams - SRE teams

Value proposition: - Codifies platform judgment - Reduces cognitive
load - Standardizes cost-aware design decisions - Acts as a reasoning
layer across existing tools (Terraform, EKS, etc.) - Does not replace
tools; reasons across them

------------------------------------------------------------------------

## 5. Versioning Strategy

Semantic Versioning (SemVer) adopted:

MAJOR.MINOR.PATCH

-   Major: Breaking architectural changes
-   Minor: Backward-compatible feature additions
-   Patch: Bug fixes and minor improvements

Initial release track:

-   0.x.x versions represent evolving architecture
-   0.1.0 defined as first working Thinking Platform Layer slice

------------------------------------------------------------------------

## 6. kre8 0.1.0 Scope (Thinking-Only TPL)

kre8 0.1.0 will:

-   Accept structured or chat-based intent
-   Reason about platform design under cost constraints
-   Produce:
    -   A structured platform plan (JSON)
    -   Cost estimation
    -   Tradeoff explanations
    -   Optional Terraform code output (text only)

kre8 0.1.0 will NOT:

-   Provision infrastructure
-   Execute Terraform
-   Maintain state
-   Manage cloud resources

This establishes a reasoning-first architecture before execution is
introduced.

------------------------------------------------------------------------

## 7. Core Components for 0.1.0

### 7.1 kre8-think

Reasoning engine of the TPL. - Translates intent into platform design
plans. - Applies cost and constraint logic. - Produces structured
output.

### 7.2 kre8-agent

AI orchestration layer. - Interfaces with AWS Bedrock. - Manages prompt
templates and tool calls. - Ensures safe, structured reasoning flows.

### 7.3 kre8-bot

User interaction layer. - Chat-based UI. - Displays plan output. -
Enables human-in-the-loop validation.

------------------------------------------------------------------------

## 8. Long-Term Roadmap (High-Level)

Future expansions may include:

-   Plan validation engine
-   Policy enforcement layer
-   Terraform execution layer (kre8-kore)
-   State management
-   Multi-cloud support
-   Observability feedback loop
-   Backstage integration

These are intentionally deferred until the TPL reasoning core is stable.

------------------------------------------------------------------------

## 9. Architectural Philosophy

-   Build minimal working slices.
-   Expand through controlled iterations.
-   Separate reasoning from execution.
-   Codify platform judgment.
-   Treat TPL as the differentiating layer.
-   Avoid premature feature expansion.

------------------------------------------------------------------------

## 10. Additions from 2026-03-05

### 10.1 kre8 Laws

The platform rule system is now referred to as:

- **kre8_laws**

The law model is:

- **LADE**
  - **L** — Limit
  - **A** — Allow
  - **D** — Deny
  - **E** — Exception

Phrase retained for product language:

> **kre8 laws are always LADE**

### 10.2 I2D2

A named internal engine now exists inside `kre8_think`:

- **I2D2 — Intelligent Infrastructure Design Decision**

This is the internal reasoning engine responsible for making
infrastructure design decisions.

### 10.3 NLP Input Direction

An initial hybrid parsing direction was considered, but later dropped.

Current preferred direction:

```text
User NLP
↓
LLM-based intent extraction
↓
StructuredIntent
↓
I2D2
↓
DesignPlan
```

This avoids brittle heuristic parsing and keeps the product aligned with
true free-form intent capture.

### 10.4 Product Positioning Refinement

kre8 should not feel like a generic AI chat wrapper.

The desired product behavior is closer to:

```text
Intent
↓
Design reasoning
↓
Explanation
↓
Render
```

with minimal conversational back-and-forth.

### 10.5 Internal Data Contracts

Two core internal contracts are now established:

- **StructuredIntent**
- **DesignPlan**

These create a clean separation between:
- intent extraction
- reasoning
- rendering
- execution

------------------------------------------------------------------------


## 11. Additions from 2026-03-21

### 11.1 Structured Intent Checkpoint

The request flow now includes a mandatory system pause after Structured Intent is produced and validated.

Target behavior:

```text
User Input
↓
Structured Intent
↓
Validation
↓
Pause
↓
Go / Review
```

The pause is important because it creates a control point before Design Plan generation.  
However, SI review is **available but not mandatory** for all users.

### 11.2 Go / Review Interaction Model

The preferred UX model is:

- **Go** → proceed using the current interpreted intent
- **Review** → inspect and later modify the Structured Intent

This supports both:
- non-technical users who want a simple experience
- advanced users who want control over the intermediate contract

### 11.3 Realm Concept

A new core concept is introduced:

- **kre8_realm**

A realm is the scoped operating context under which user requests are interpreted and validated.

A realm is intended to provide:
- platform defaults
- environment assumptions
- shared infrastructure context
- bindings to applicable law sets

This arose from the insight that users naturally assume kre8 already knows the setup they operate within.

### 11.4 Laws and Realm Separation

The relationship between realms and laws is now clarified:

- **kre8_laws** should define reusable law sets and policy logic
- **kre8_realm** should bind applicable laws and hold scoped defaults/context
- laws should not be duplicated under every realm

This preserves reuse and avoids structural repetition.

### 11.5 ARC

The reusable solution memory/catalog component is now named:

- **ARC — Architecture Catalog**

ARC is intended to serve two purposes:
1. store and retain architecture outputs for future reuse
2. present a catalog of selectable or adaptable architecture options to users

This makes ARC both a memory layer and a user-facing selection layer.

### 11.6 Product Surfaces

Two primary UI surfaces are now taking shape:

- **Kiosk** — end-user request and delivery surface
- **Whiteboard** — administrative/configuration surface for realms and laws

Whiteboard will eventually support both UI-driven setup and batch/script-assisted updates.

### 11.7 Repo and Documentation Direction

The preferred near-term repo/documentation direction is:

- keep top-level component folders at repo root
- add new top-level folders for future components (`kre8_kiosk`, `kre8_whiteboard`, `kre8_realm`, `kre8_laws`, `kre8_arc`)
- use hybrid documentation:
  - central `docs/`
  - component-local READMEs

This supports easier future lift-and-shift into dedicated repositories.

------------------------------------------------------------------------

End of Ideation Log
