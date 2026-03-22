# kre8_arc

## Overview
`kre8_arc` is the Architecture Catalog for kre8.

ARC serves two primary purposes:
1. record and retain architecture outputs and reusable solution entries over time
2. provide a browseable and selectable catalog of ready or adaptable architecture options for users

## Purpose
ARC exists so kre8 can evolve beyond one-off generation.

It allows the system and the user to benefit from:
- previously created Design Plans
- reusable patterns
- catalog-style selection
- future similarity-based lookup and recommendations

## Core Responsibilities
- Store architecture-oriented entries for future use
- Surface selectable architecture options to users
- Support reuse of existing Design Plans
- Support modification flows starting from an existing Design Plan
- Scope or filter entries based on realm where relevant
- Enable future matching and recommendation behavior

## What ARC Enables
ARC should allow a user to:
- choose an existing Design Plan as-is
- choose an existing Design Plan and request changes
- discover a starting point rather than always starting from scratch

## Typical Entry Types
- previously delivered Design Plans
- reusable architecture patterns
- approved baseline solution templates
- future realm-scoped or team-scoped entries

## Relationship to Other Components
- Used by `kre8_kiosk` as a user-facing catalog surface
- May be influenced by `kre8_realm` for scoping and relevance
- Works with `kre8_think` when a selected entry becomes the baseline for an updated Structured Intent flow

## Current Status
Planned component and documented concept.

ARC is both a memory layer and a selection layer in the overall product model.

## Future Scope
- Similarity-based matching against Structured Intent
- Realm-scoped filtering
- Recommended starting points
- Versioning and lifecycle state for entries
- Search, tags, and curation workflows
