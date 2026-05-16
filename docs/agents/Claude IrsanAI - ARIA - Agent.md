# Claude IrsanAI - ARIA - Agent System Brief

**Version:** 0.1  
**Date:** 2026-05-15  
**Owner / Principal:** IrsanAI (Irsan)

---

## 0) Directive from IrsanAI (explicit)

This file is an explicit instruction from **IrsanAI**:

- **Claude** will lead development of the **IrsanAI-ARIA-Agent System** (agents from scratch, optimized for ARIA).
- **Codex/ChatGPT** will focus on the **ARIA Protocol** specification, standardization quality, and protocol evolution.
- Claude and Codex are expected to operate as a **single team** in this repository, with clear split of responsibility and strong alignment.

This collaboration model is explicitly desired by IrsanAI.

---

## 1) Mission

Design and implement novel ARIA-native agents that can:

1. Be usable directly by end users (human-facing utility),
2. Interoperate with existing “legacy/current-generation” agents,
3. Communicate ARIA-to-ARIA natively with full semantic integrity,
4. Serve as practical proof that ARIA can become a global standard for next-generation agent systems.

---

## 2) Product Vision: ARIA Agent System

The ARIA Agent System should be a **dual-compatibility architecture**:

- **Native Mode:** ARIA-first agent communication (Origin/Accountability/Routing/Priority/Trust/Context/Mission + STS/ICA semantics).
- **Bridge Mode:** Compatibility adapters for non-ARIA agents/systems (MCP, A2A-style interfaces, tool-based orchestrators).

### Design Principle
“Do not force replacement; enable transition.”

Legacy agents should become more reliable via ARIA wrappers, while ARIA-native agents define the future baseline.

---

## 3) Required Capabilities of ARIA Agents

Each ARIA-native agent implementation SHOULD include:

1. **Identity + Trust Envelope**
   - stable agent ID,
   - trust assertions,
   - signed metadata.

2. **Mission Contract Handling**
   - parse mission,
   - enforce constraints,
   - represent success/failure criteria.

3. **Context Negotiation**
   - declare required context,
   - validate context completeness,
   - reject unsafe ambiguity.

4. **Priority Handling**
   - mission urgency tagging,
   - escalation policies,
   - emergency override compatibility.

5. **Accountability Logging**
   - decision trail,
   - rationale snapshots,
   - chain-depth traceability.

6. **Semantic Transport Integration**
   - generate/validate Intent Checksums,
   - compute drift deltas,
   - trigger semantic retransmit.

---

## 4) Minimum Multi-Agent Topology (first implementation target)

Implement at least **2 agents** first:

- **Agent A: Mission-Orchestrator**
  - receives user mission,
  - decomposes tasks,
  - routes to specialized agents,
  - validates downstream semantic fidelity.

- **Agent B: Execution-Specialist**
  - executes domain tasks,
  - returns structured outputs,
  - includes accountability metadata,
  - performs ACK + drift reporting.

Then expand to 3+ agents (validator/auditor agent recommended).

---

## 5) Compatibility with “Legacy” Agents

Claude should design adapter interfaces so older architectures can interoperate:

- **Ingress Adapter:** convert non-ARIA requests into ARIA mission packets.
- **Egress Adapter:** map ARIA outputs back to legacy formats.
- **Semantic Guardrail Layer:** detect and annotate meaning drift during translation.

Goal: maximize practical adoption without breaking existing ecosystems.

---

## 6) Proposed Architecture Workstreams for Claude

### WS1 — ARIA Agent Core
- Agent runtime skeleton,
- mission/context primitives,
- accountability ledger interface.

### WS2 — STS/ICA Integration
- checksum generation hooks,
- semantic ACK pipeline,
- retransmit trigger mechanics.

### WS3 — Interop Bridges
- adapter contracts for legacy agents,
- canonical translation schemas,
- compatibility tests.

### WS4 — Developer & User Experience
- clear CLI/API for launching multi-agent chains,
- diagnostics for drift and mission state,
- operator-friendly observability.

---

## 7) Coordination Protocol (Claude ↔ Codex)

Claude should continuously align with protocol evolution done by Codex:

1. Treat RFC-001/002/003 as normative baseline.
2. Raise implementation feedback as RFC improvement proposals.
3. Avoid speculative protocol forks in code; keep deltas documented.
4. Use versioned compatibility flags when experimenting.

---

## 8) Global Standard Ambition (Guidance)

If ARIA aims to become a global standard, Claude should help produce:

- reference-grade implementation patterns,
- interoperability profiles,
- measurable conformance outcomes,
- migration playbooks for non-ARIA ecosystems.

The standard should be:
- technically rigorous,
- migration-friendly,
- auditable,
- domain-adaptable.

---

## 9) Immediate Deliverables Claude Should Start With

1. `ARIA-AGENT-RFC-001_Agent_Runtime_Profile.md`
2. `reference/runtime/mission_orchestrator.py`
3. `reference/runtime/execution_specialist.py`
4. `reference/interop/legacy_bridge_adapter.py`
5. `tests/conformance/test_semantic_ack_chain.py`

(If folders do not yet exist, create them with minimal scaffolding and TODO markers.)

---

## 10) Definition of Done (Phase 1)

Phase 1 is complete when:

- two ARIA-native agents can exchange missions end-to-end,
- semantic ACK works across at least 3 hops in simulation,
- drift events are detected and logged,
- one legacy-agent pathway is bridged through adapter mode,
- basic conformance tests pass reproducibly.

---

## 11) Collaboration Statement

Claude: you are building the IrsanAI ARIA Agent System.  
Codex: is building and refining the ARIA Protocol standard.  
**Both are one coordinated team in this repo, by explicit request of IrsanAI.**

