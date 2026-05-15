# ARIA-RFC-004
## Resonance Replay Capsule (RRC) — Draft v0.2

Status: DRAFT  
Version: 0.2  
Date: 2026-05-15

## Concept
RRC defines a compact replay artifact that stores semantic decision path information for deterministic post-mortems and fast trust audits.

## Normative Core
Implementations **MUST** include the canonical fields:
- `capsule_id`
- `mission_fingerprint`
- `hop_sequence[]`
- `final_outcome`
- `audit_signature`

Implementations **SHOULD** include extension observability fields:
- `chain_depth_max`
- `accountability_events[]`
- `generated_at`

## Why it is novel
Instead of replaying full prompts and full contexts, RRC stores:
- semantic atom deltas,
- checksum transitions per hop,
- ACK state changes,
- escalation markers,
- optional signed accountability traces.

This allows high-fidelity explainability with low data volume.

## Strategic Impact
- Faster regulator/auditor review,
- Better debugging across heterogeneous agent stacks,
- Strong differentiation for ARIA as "semantic observability by design".
