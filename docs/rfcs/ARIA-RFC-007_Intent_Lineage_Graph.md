# ARIA-RFC-007
## Intent Lineage Graph (ILG) — Draft v0.1

Status: DRAFT  
Version: 0.1  
Date: 2026-05-16

## Purpose
Define a graph-native structure to track semantic lineage across branching agent chains.

## Core Idea
RRC provides a replay capsule for a chain. ILG extends this to *branching topologies*:
- multiple downstream agent branches,
- merge points,
- per-edge drift/guardrail metadata.

## Node/Edge Model
- Node = mission state at a hop.
- Edge = semantic transition from one node to next.

Each edge SHOULD include:
- similarity score,
- drift delta,
- guardrail mode,
- threshold profile.

## Normative Direction
Implementations MUST:
1. Assign stable IDs to nodes and edges.
2. Preserve parent-child lineage for every branch.
3. Emit ILG export in incidents with `review`/`block` guardrail decisions.

Implementations SHOULD:
1. Support graph compression for long chains.
2. Attach accountability signatures at merge nodes.
