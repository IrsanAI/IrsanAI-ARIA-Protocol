# ARIA-RFC-010
## Resonance Circuit Breaker (RCB) — Draft v0.1

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define automatic chain-pausing behavior when repeated semantic risk events occur in a short window.

## Core Idea
Single guardrail failures may be tolerable. Repeated failures indicate systemic instability.
RCB triggers a temporary stop when risk-event density exceeds configured thresholds.

## Trigger Signals
- count of `review`/`block` guardrail outcomes,
- budget `warning`/`exhausted` transitions,
- failed canary cases.

## States
- `closed` (normal)
- `open` (traffic halted)
- `half_open` (limited recovery probes)

## Normative Direction
Implementations MUST:
1. Track rolling risk-event windows.
2. Open the circuit when threshold is exceeded.
3. Emit accountability event on state transitions.

Implementations SHOULD:
1. Use stricter thresholds for critical-safety tiers.
2. Allow controlled half-open probes after cooldown.
