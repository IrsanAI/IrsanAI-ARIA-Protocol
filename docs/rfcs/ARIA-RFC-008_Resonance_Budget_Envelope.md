# ARIA-RFC-008
## Resonance Budget Envelope (RBE) — Draft v0.1

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define a cumulative semantic-risk budget for multi-hop chains.

## Core Idea
Even if single hops pass thresholds, cumulative drift can still become unsafe.
RBE introduces a mission-level budget that tracks aggregate drift and enforces stop/escalate behavior.

## Budget Model
- `budget_max`: maximum allowed cumulative drift delta.
- `budget_used`: running sum of per-hop drift deltas.
- `budget_remaining`: `budget_max - budget_used`.

## Decision Modes
- `within_budget`
- `warning`
- `exhausted`

## Normative Direction
Implementations MUST:
1. Track budget per mission chain.
2. Emit accountability events when entering `warning` or `exhausted`.
3. Stop or escalate handoff when budget is `exhausted`.

Implementations SHOULD:
1. Use lower budgets for critical-safety and healthcare tiers.
2. Include RBE snapshot in RRC capsules.
