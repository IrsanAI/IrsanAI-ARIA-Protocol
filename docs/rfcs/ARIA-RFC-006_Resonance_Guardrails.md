# ARIA-RFC-006
## Resonance Guardrails Gateway (RGG) — Draft v0.1

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define a pre-handoff guardrail gateway that evaluates semantic risk before forwarding across agent hops.

## Core Idea
Before hop handoff, RGG computes a policy decision from:
- current semantic similarity,
- domain tier,
- threshold profile,
- cumulative drift trend.

## Decision Modes
- `allow` → handoff continues
- `review` → human/validator checkpoint required
- `block` → handoff denied; retransmit/escalation required

## Normative Direction
Implementations MUST:
1. Emit an accountability event for every guardrail decision.
2. Attach guardrail decision metadata to RRC capsules.
3. Block forwarding on `block` decisions.

Implementations SHOULD:
1. Use stricter policy defaults for critical-safety and healthcare tiers.
2. Track moving-average drift to detect compounding semantic degradation.
