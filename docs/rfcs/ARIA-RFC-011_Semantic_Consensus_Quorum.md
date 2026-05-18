# ARIA-RFC-011
## Semantic Consensus Quorum (SCQ) — Draft v0.1

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define a quorum mechanism for high-stakes actions where multiple agents must semantically agree before execution.

## Core Idea
Single-agent ACK can be insufficient for critical actions. SCQ requires a minimum quorum of agreeing semantic ACKs.

## Inputs
- set of agent votes (`ack_confirmed` / `ack_drift_detected`),
- per-vote similarity,
- required quorum ratio.

## Outcomes
- `quorum_confirmed`
- `quorum_degraded`
- `quorum_rejected`

## Normative Direction
Implementations MUST:
1. Declare quorum ratio before critical execution.
2. Reject execution when quorum is not met.
3. Emit accountability event with vote breakdown.

Implementations SHOULD:
1. Use higher quorum ratios in critical-safety and healthcare tiers.
2. Include SCQ outcome in RRC and ILG exports.
