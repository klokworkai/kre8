# kre8_kiosk

## Overview
`kre8_kiosk` is the end-user interaction surface for kre8.

It is the primary UI through which users submit natural-language infrastructure requests, browse existing architecture options from ARC, review interpreted intent when needed, and receive final Design Plans.

## Purpose
The kiosk exists to make kre8 usable by both technical and non-technical users.

It should support:
- requesting a brand-new Design Plan in natural language
- selecting an existing Design Plan from ARC
- selecting an existing Design Plan and asking for changes in natural language
- pausing after Structured Intent generation so the user can choose **Go** or **Review**

## Core Responsibilities
- Authenticate or identify the user
- Resolve or display the user’s active realm
- Accept natural-language input
- Surface ARC browsing and selection
- Present system understanding / Structured Intent checkpoint
- Allow **Go** or **Review**
- Present the final Design Plan back to the user

## Primary Inputs
- User identity or session context
- Active realm
- Natural-language request
- Optional selected ARC entry
- Optional user change request against an existing Design Plan

## Primary Outputs
- Request payload to the kre8 thinking flow
- Optional user-confirmed review action
- Final Design Plan display
- User-triggered reuse or modification request

## Key UX Concepts
- Simple by default for non-technical users
- Optional deeper review for advanced users
- Realm-aware behavior
- Clear separation between:
  - request entry
  - Structured Intent checkpoint
  - final Design Plan delivery

## Relationship to Other Components
- Works with `kre8_realm` to determine applicable context
- Calls the thinking flow driven by `kre8_think`
- Surfaces validation outcomes from `kre8_laws`
- Browses and selects from `kre8_arc`

## Current Status
Planned component.

The initial implementation is expected to be a minimal UI for the demo repository and can later evolve into a fuller standalone user-facing application.

## Future Scope
- Realm switching where allowed
- ARC recommendations based on interpreted intent
- Structured Intent review and editing for advanced users
- Saved request history
- Guided workflows for common infrastructure requests
