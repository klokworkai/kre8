# Documentation

## Overview
This `docs` directory contains product-level, architecture-level, and working-reference documentation for the demo repository.

The documentation model is intentionally hybrid:

- **central docs** describe the system as a whole
- **component-local READMEs** describe individual component responsibilities and boundaries
- **working logs** capture ongoing state, work history, and ideation

This structure supports both day-to-day iteration inside the demo repository and easier lift-and-shift of components into separate repositories later.

## Documentation Areas

### Architecture
System-level design, flows, boundaries, and structural decisions.

### Components
Cross-component reference documentation that explains how the major parts of kre8 fit together.

### Realms
Definitions and structure for realm context, defaults, and bindings.

### Laws
Definitions and structure for validation, governance, and constraint modeling.

### ARC
Documentation for the Architecture Catalog, including reuse and selection workflows.

### Kiosk
End-user interaction model and request flow.

### Whiteboard
Administrative/configuration surface for realms, laws, and related governance setup.

### Schemas
Shared schema-oriented documentation and model definitions.

### State
Current snapshot of project status and active direction.

### Work Log
Chronological record of work performed.

### Ideation
Idea capture, exploratory thinking, and possible future directions.

### Decisions
Architecture decisions and major structural choices captured over time.

## Documentation Principles
- Keep product/system docs centralized here
- Keep component-specific operational docs inside each component folder where appropriate
- Prefer a single `README.md` per docs area until a section becomes large enough to justify splitting
