# ARIA-RFC-005
## Interop Compatibility Profiles (Draft v0.1)

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define compatibility profiles for integrating non-ARIA agent stacks without losing ARIA semantic guarantees.

## Profiles
- `native`: end-to-end ARIA envelopes and ACK semantics.
- `bridge-safe`: non-ARIA transport with ARIA semantic guardrails.
- `bridge-legacy`: legacy transport with best-effort semantic annotation.

## Normative Direction
Implementations MUST:
1. Declare compatibility profile per session.
2. Preserve `mission_core`, `constraints`, and `intent_checksum` across adapters.
3. Emit accountability events for each profile boundary crossing.

Implementations SHOULD:
1. Emit RRC capsules for bridge-safe and bridge-legacy sessions.
2. Flag confidence reduction on lossy field mappings.
