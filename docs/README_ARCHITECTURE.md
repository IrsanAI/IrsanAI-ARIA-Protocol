# ARIA Repository Architecture Map

This document is the navigation compass for contributors and implementers.
It aligns repository structure with ARIA's core intent: **semantic integrity for agent-to-agent communication**.

## 1) Intent Compass
ARIA's directional north star is:
- preserve mission meaning across agent chains,
- detect semantic drift early,
- make decisions auditable and interoperable.

If a change does not improve one of these three, it should be reconsidered.

## 2) Directory Overview

- `docs/rfcs/`
  - Normative and draft specifications (protocol + runtime + extensions).
- `docs/guides/`
  - Contributor and process guidance.
- `docs/analysis/`
  - Strategic assessments and ecosystem positioning.
- `docs/agents/`
  - Collaboration briefs for agent-system development.
- `reference/runtime/`
  - Minimal ARIA runtime scaffolds and interfaces.
- `reference/interop/`
  - Legacy bridge/adaptation logic.
- `schemas/`
  - Machine-readable contracts (packet/ack/replay capsule).
- `tests/conformance/`
  - Conformance-oriented tests for protocol behavior.

## 3) Build Order for Maturation
1. **Contracts first** (`schemas/`, runtime interfaces)
2. **Reference behavior second** (`reference/runtime/`)
3. **Interop compatibility third** (`reference/interop/`)
4. **Conformance evidence always** (`tests/conformance/`)

## 4) Resonance Checklist (pre-merge)
Before merging, verify:
- Does this reduce semantic drift risk?
- Does this improve traceability/accountability?
- Does this increase interop without diluting ARIA semantics?
- Is it testable with conformance assertions?

## 5) Near-term Priorities
- Implement deterministic ICA API boundary.
- Introduce threshold-aware semantic ACK using RFC-003 profiles.
- Emit replay-ready events compatible with RFC-004 RRC.
