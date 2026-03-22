# Decisions Log

This document records committed architectural and product decisions for kre8.

---

## Decision: Introduce Hybrid Documentation Model

### Context
The project required both system-level documentation and component-level documentation, while also preserving working logs such as state, work log, and ideation.

### Decision
Adopt a hybrid documentation structure:
- Central `docs/` for system, domain, and product-level concepts
- Component-level README files inside each component folder
- Separate folders for logs (state, work_log, ideation)

### Rationale
- Supports lift-and-shift of components later
- Keeps system understanding centralized
- Avoids duplication and fragmentation

### Impact
- New docs folder structure created
- Component README files introduced
- Logs separated from specs

---

## Decision: Introduce New Core Components

### Context
The system evolved beyond initial components (`gate`, `think`, `agent`, `cli`) to include context, governance, UI, and reuse layers.

### Decision
Introduce the following components:
- kre8_kiosk (user interface)
- kre8_whiteboard (admin interface)
- kre8_realm (context layer)
- kre8_laws (validation/governance)
- kre8_arc (architecture catalog)

### Rationale
- Clear separation of concerns
- Supports product evolution
- Enables future independent services

### Impact
- New top-level folders created
- Documentation aligned to components

---

## Decision: Use ARC (Architecture Catalog)

### Context
Needed a name for the catalog component that stores and serves reusable design plans.

### Options Considered
- Catalog
- Blueprints / Prints
- PAC / PARC
- ARC

### Decision
Use ARC (Architecture Catalog)

### Rationale
- Clean and pronounceable
- Strong alignment with architecture domain
- Supports both storage and selection use cases

### Impact
- Naming standardized across docs and components

---

## Decision: Introduce Realm Concept

### Context
Users assume platform defaults (cloud, networking, etc.) which are not explicitly provided in natural language input.

### Decision
Introduce `kre8_realm` as a context layer:
- Provides defaults
- Represents environment and platform assumptions
- Binds applicable law sets

### Rationale
- Reduces ambiguity in intent interpretation
- Improves design accuracy
- Separates context from validation

### Impact
- Realm concept added to system flow
- Whiteboard needed for configuration

---

## Decision: Separate Laws from Context

### Context
There was a question of whether defaults, policies, and validation should live in the same component.

### Decision
Keep laws separate from realm:
- Realm = context and defaults
- Laws = validation and governance

### Rationale
- Avoids duplication
- Enables reuse of law sets
- Keeps responsibilities clean

### Impact
- kre8_laws defined as global rule system
- Realms bind to laws rather than redefining them

---

## Decision: Introduce Structured Intent Pause (Go / Review)

### Context
Users may not always understand infrastructure details, but advanced users may want control.

### Decision
Introduce a pause after Structured Intent generation:
- Go (auto proceed)
- Review (inspect/edit SI)

### Rationale
- Balances simplicity and control
- Avoids forcing all users into technical workflows

### Impact
- Kiosk flow updated
- SI becomes a first-class intermediate artifact

---

## Decision: Keep Single Repo with Component Boundaries

### Context
Needed to balance ease of development with future multi-repo architecture.

### Decision
Keep a single demo repo but:
- create top-level component folders
- design clear boundaries
- avoid deep coupling

### Rationale
- Faster iteration now
- Easier lift-and-shift later

### Impact
- No `components/` root introduced
- Components remain at repo root

---

## Decision: Use Whiteboard for Admin UI

### Context
Needed a name for the configuration/admin interface.

### Decision
Use "Whiteboard"

### Rationale
- Represents design and setup surface
- Distinct from user-facing kiosk

### Impact
- Terminology standardized
- Docs aligned

---

## Decision: Keep Ideation and Decisions Separate

### Context
Overlap observed between ideation log and decisions.

### Decision
Keep them separate:
- Ideation = exploration
- Decisions = committed outcomes

### Rationale
- Prevents confusion between ideas and final choices
- Keeps decisions authoritative

### Impact
- Decisions document structured in ADR style
