# Whiteboard

## Overview
Whiteboard is the administrative and configuration surface for kre8.

It is intended for operators, architects, and platform owners who define and maintain the context and governance structures used elsewhere in the system.

## Primary Responsibilities
Whiteboard should support:
- creating and managing realms
- creating and managing laws
- binding law sets to realms
- previewing effective context and validation outcomes
- supporting future bulk import/export workflows

## Product Role
Whiteboard is the setup and governance counterpart to Kiosk.

- Kiosk is for request and delivery
- Whiteboard is for configuration and control

## Relationship to Other Components
- configures `kre8_realm`
- configures `kre8_laws`
- indirectly influences Think behavior
- shapes what users experience in Kiosk

## Documentation Strategy
Keep product-level Whiteboard workflows here.
Keep component-specific implementation notes inside `kre8_whiteboard/README.md`.
