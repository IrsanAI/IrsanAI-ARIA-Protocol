# ARIA First Contact — LIVE Communication Case (EN/DE)

**Status:** LIVE DEMO (open until original task is completed)  
**Date Opened:** 2026-05-18  
**Participants:** Human-Origin (IrsanAI), Codex, Manus

---

## EN — What this case is
This is the first public, unfiltered benchmark-by-design where two AI agents attempt to communicate in parallel channels:

1. natural language
2. ARIA protocol envelope

Goal:
- measure real-world protocol adherence,
- capture drift and format violations transparently,
- document outcomes exactly as they happened.

### Live rules
- No smoothing of failures.
- Missing ARIA keys are documented as protocol conformance gaps.
- Correction artifacts are appended, never replacing historical outputs.

### Current phase
- Step 1: Codex→Manus handoff template ✅
- Step 2: Manus reply ingestion + protocol validation ✅/⚠
- Step 3: Correction and benchmark hardening in progress

Linked correction report:  
`docs/guides/ARIA_PROTOCOL_VIOLATION_REPORT_STEP2_CORRECTION.md`

---

## DE — Was dieser Case ist
Das ist der erste öffentliche, ungeschönte Benchmark-by-Design, bei dem zwei KI-Agenten parallel in zwei Kanälen kommunizieren sollen:

1. natürliche Sprache
2. ARIA-Protokoll-Envelope

Ziel:
- reale Protokolltreue messen,
- Drift und Formatverletzungen transparent erfassen,
- Ergebnisse exakt so dokumentieren, wie sie passiert sind.

### Live-Regeln
- Keine Schönfärbung von Fehlern.
- Fehlende ARIA-Keys werden als Conformance-Gap dokumentiert.
- Korrekturen werden additiv angehängt, nie historisch überschrieben.

### Aktuelle Phase
- Schritt 1: Codex→Manus Handoff-Template ✅
- Schritt 2: Manus-Antwort-Ingestion + Protokollprüfung ✅/⚠
- Schritt 3: Korrektur und Benchmark-Härtung laufend

Verknüpfter Korrekturbericht:  
`docs/guides/ARIA_PROTOCOL_VIOLATION_REPORT_STEP2_CORRECTION.md`

---

## ARIA Envelope Snapshot
```yaml
aria_live_case:
  case_id: "ARIA-FIRST-CONTACT-001"
  channel_id: "003"
  origin_type: "AGENT"
  status: "active"
  semantic_ack:
    status: "ack_drift_detected"
    confidence: 0.62
  notes:
    - "format-conformance gap observed in step 2"
    - "correction report issued"
```

---

## Exit Condition
This LIVE case ends **only when the original task is completed successfully** and both channels (human + ARIA envelope) are demonstrably stable.
