# ARIA-RFC-009
## Resonance Canary Suite (RCS) — Draft v0.1

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define a regression-safety mechanism that continuously checks semantic quality against known canary missions.

## Core Idea
Before/after runtime or model changes, run a fixed canary set and compare:
- similarity stability,
- drift deltas,
- guardrail and budget outcomes.

## Canary Outcomes
- `pass`: no significant semantic degradation.
- `watch`: slight degradation, review recommended.
- `fail`: unacceptable degradation, rollout blocked.

## Normative Direction
Implementations MUST:
1. Store baseline canary results with version IDs.
2. Compare new run against baseline before rollout.
3. Block production rollout on `fail`.

Implementations SHOULD:
1. Include canaries for each domain tier.
2. Emit RRC/ILG references for failing canaries.
