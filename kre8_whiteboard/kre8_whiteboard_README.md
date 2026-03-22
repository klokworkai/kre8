# kre8_whiteboard

## Overview
`kre8_whiteboard` is the administrative and configuration surface for kre8.

It is intended for platform owners, architects, and administrators who define and manage realms, laws, and other system-level controls that shape the behavior of the kiosk and the underlying thinking flow.

## Purpose
The whiteboard exists to provide a clear operator-facing surface for setting up and governing kre8.

It should support:
- creating and maintaining realms
- creating and maintaining law sets
- binding laws to realms
- managing exceptions and overrides
- previewing effective context and validation behavior

## Core Responsibilities
- Manage realm definitions
- Manage law definitions and law sets
- Manage realm-to-law bindings
- Surface effective configuration views
- Support validation previews
- Support future import/export and batch-assisted setup workflows

## Primary Inputs
- Realm definitions
- Law definitions
- Binding rules
- Exceptions or override records
- Administrative changes from platform owners

## Primary Outputs
- Saved realm configurations
- Saved law configurations
- Updated bindings
- Previewable effective realm + law combinations

## Key UX Concepts
- Clear operator/admin experience
- Separation of realm context from law enforcement
- Preview before applying
- Support for future scripted/batch setup in parallel with UI-based administration

## Relationship to Other Components
- Configures `kre8_realm`
- Configures `kre8_laws`
- Supports downstream behavior in `kre8_kiosk`
- Indirectly influences how `kre8_think` interprets user requests

## Current Status
Planned component.

In the demo repository, it starts as a documented concept and can later become its own UI surface or service-backed administrative application.

## Future Scope
- Realm creation wizard
- Law set editor
- Effective policy preview
- Sample Structured Intent validation against selected realm
- Bulk import/export support
- Role-based administration
