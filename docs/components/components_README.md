# Components

## Overview
This section provides a product-level view of kre8 components and how they fit together.

It complements the `README.md` files inside each component folder by describing cross-component roles at the system level.

## Core Components
- `kre8_gate` — ingress layer
- `kre8_think` — thinking and reasoning layer
- `kre8_agent` — model interaction layer
- `kre8_cli` — command-line entry surface
- `kre8_kiosk` — end-user UI surface
- `kre8_whiteboard` — admin/configuration UI surface
- `kre8_realm` — scoped context and defaults
- `kre8_laws` — validation and governance
- `kre8_arc` — architecture catalog and reuse layer

## Component Boundaries
Each component should have:
- a clearly stated purpose
- explicit inputs and outputs
- minimal hidden coupling
- enough internal separation that future lift-and-shift into a dedicated repository is straightforward

## Relationship to Component-local READMEs
- Put component-specific operational and ownership details in the component folder itself
- Keep cross-cutting role descriptions and system relationships in this documentation area

## Purpose of this Section
Use this section to maintain the canonical component map of the product.
