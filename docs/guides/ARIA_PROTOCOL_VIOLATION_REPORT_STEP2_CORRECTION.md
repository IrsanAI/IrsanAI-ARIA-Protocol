# ARIA Protocol Violation Report — Step 2 Correction

**Date:** 2026-05-18  
**Context:** Manus ↔ Codex first handshake benchmark  
**Mission ID:** `MSN-MANUS-CODEX-HANDSHAKE-001`

## 1) Detected Violation
During Step 2 of the benchmark flow, the expected dual-output response format was not fully preserved:

- Human-readable narrative existed,
- ARIA-structured response envelope was incomplete/inconsistent.

This is classified as a **format-conformance violation** (not a semantic-failure by default).

## 2) Root Cause (Observed)
Likely causes:
1. Agent-side prompt-following prioritized natural language over strict envelope output.
2. No hard validator enforced required ARIA response keys at ingestion.
3. No blocking gate for malformed `aria_response` payloads.

## 3) Correction Applied
This correction introduces a stricter benchmark expectation:

- Require parallel response:
  - natural language summary
  - full ARIA envelope block
- Treat missing envelope keys as `ack_drift_detected` in benchmark logs.
- Persist result as transparent artifact (pass/fail, no smoothing).

## 4) Required Envelope Keys (minimum)
```yaml
aria_response:
  semantic_ack:
    status:
    confidence:
  progress_summary:
  modified_files:
  risks:
  next_steps:
```

## 5) Follow-up Action
- Integrate schema check for agent handoff responses in the benchmark flow.
- Add explicit conformance test case for malformed ARIA response envelopes.
- Keep this report linked from the live communication case.

## 6) Integrity Statement
No retrospective alteration of raw interaction logs is allowed.  
Corrections are additive and transparent.
