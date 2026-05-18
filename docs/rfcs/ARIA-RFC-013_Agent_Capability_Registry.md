# ARIA-RFC-013
## Agent Capability Registry (ACR) — Draft v0.1

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define a registry contract so ARIA agents can advertise capabilities, trust posture, supported roles, and protocol compatibility.

## Core Idea
Runtime routing should use machine-readable agent capability cards instead of hardcoded assumptions.

## Normative Direction
Implementations MUST:
1. Expose capability cards with stable `agent_id`.
2. Include supported cognitive roles and domain capabilities.
3. Include protocol compatibility metadata (`aria_version`, supported RFC extensions).

Implementations SHOULD:
1. Include performance hints (latency class, context window).
2. Include trust posture and governance metadata.
