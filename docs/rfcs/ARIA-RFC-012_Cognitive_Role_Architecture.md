# ARIA-RFC-012
## Cognitive Role Architecture (CRA) — Draft v0.1

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define a model-agnostic meta-cognitive layer that assigns **cognitive roles** (not fixed models) per mission.

## Why
Dispatcher-only routing answers “which model?”, but ARIA needs “which cognitive function?”.
CRA formalizes role-based orchestration for multi-agent semantic integrity.

## Canonical Roles
- `perception`
- `memory`
- `reasoning`
- `creativity`
- `code`
- `critique`
- `synthesis`

## Normative Direction
Implementations MUST:
1. Build a role map before high-complexity execution.
2. Assign `critique` when confidence is below high-confidence threshold.
3. Emit role-map accountability metadata in mission logs.

Implementations SHOULD:
1. Execute independent roles in parallel.
2. Use `synthesis` role to merge role outputs.
3. Persist role-map snapshots for replay/audit.
