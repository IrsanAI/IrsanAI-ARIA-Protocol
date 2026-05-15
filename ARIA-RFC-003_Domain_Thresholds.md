# ARIA-RFC-003
## Domain Threshold Calibration
### Semantic Drift Tolerance by Domain

```
Status:    DRAFT
Version:   0.1
Created:   Vatertag 2025
Authors:   Irsan + Claude (Anthropic)
Depends:   ARIA-RFC-001, ARIA-RFC-002
```

---

## Abstract

ARIA-RFC-002 defines four ACK status levels with default drift thresholds:

```
PERFECT        DELTA < 0.05
CONFIRMED      DELTA < 0.15
DRIFT_WARNING  DELTA < 0.30
DRIFT_CRITICAL DELTA ≥ 0.30
```

These defaults are appropriate for general-purpose agent communication.
However, different domains carry fundamentally different risk profiles.

A 0.25 drift in a creative writing agent chain is negligible.
A 0.25 drift in a surgical robot command chain is catastrophic.

ARIA-RFC-003 specifies **domain-aware threshold calibration** —
the mechanism by which ARIA-compliant systems adapt semantic drift
tolerance to the criticality of the domain they operate in.

---

## 1. The Core Problem

### 1.1 One Threshold Does Not Fit All

```
DOMAIN: Creative Content Generation
  Agent A: "Write a poem about autumn"
  Agent E: "Compose verse about fall season"
  DELTA: 0.22  →  Acceptable. Same intent, different phrasing.
  With default thresholds: DRIFT_WARNING  ← too strict

DOMAIN: Financial Transaction Execution
  Agent A: "Buy 1000 AAPL at market price"
  Agent E: "Acquire Apple equity position"
  DELTA: 0.22  →  Dangerous. Order type, size, timing lost.
  With default thresholds: DRIFT_WARNING  ← too lenient

DOMAIN: Medical Device Control
  Agent A: "Administer 5mg morphine IV"
  Agent E: "Provide pain management"
  DELTA: 0.22  →  Life-threatening. Dosage, route, drug lost.
  With default thresholds: DRIFT_WARNING  ← catastrophically lenient
```

### 1.2 The Risk Spectrum

```
LOW RISK ────────────────────────────────────── HIGH RISK
   │                                                │
Creative   Research   Business   Legal   Financial  Medical
Content    Analysis   Operations Advice  Execution  Control
   │                                                │
Lenient                                         Strict
thresholds                               thresholds
```

---

## 2. Domain Classification System

ARIA-RFC-003 defines **six domain tiers**, each with calibrated thresholds.

### Tier 0 — CREATIVE
*Content generation, brainstorming, artistic tasks*

```
PERFECT        DELTA < 0.15    (3× default)
CONFIRMED      DELTA < 0.30    (2× default)
DRIFT_WARNING  DELTA < 0.50    (1.7× default)
DRIFT_CRITICAL DELTA ≥ 0.50

Rationale: Semantic variation is often desirable in creative domains.
           Strict thresholds would incorrectly penalize creative reinterpretation.

Examples:  Content writing agents, design assistants, brainstorming systems
```

---

### Tier 1 — RESEARCH
*Information gathering, analysis, summarization*

```
PERFECT        DELTA < 0.08
CONFIRMED      DELTA < 0.20
DRIFT_WARNING  DELTA < 0.35
DRIFT_CRITICAL DELTA ≥ 0.35

Rationale: Research integrity matters but some reformulation is expected.
           Key facts must survive; phrasing may adapt.

Examples:  Literature review agents, competitive intelligence, data analysis
```

---

### Tier 2 — GENERAL (Default)
*Standard business operations, general assistance*

```
PERFECT        DELTA < 0.05
CONFIRMED      DELTA < 0.15
DRIFT_WARNING  DELTA < 0.30
DRIFT_CRITICAL DELTA ≥ 0.30

Rationale: Balanced defaults. Used when no domain is specified.

Examples:  General-purpose agents, task management, scheduling
```

---

### Tier 3 — BUSINESS_CRITICAL
*Customer commitments, contractual actions, operational decisions*

```
PERFECT        DELTA < 0.03
CONFIRMED      DELTA < 0.08
DRIFT_WARNING  DELTA < 0.15
DRIFT_CRITICAL DELTA ≥ 0.15

Rationale: Business decisions carry legal and financial consequences.
           High precision required. Ambiguity is costly.

Examples:  Contract execution agents, procurement, customer-facing commitments
```

---

### Tier 4 — FINANCIAL
*Trading, transactions, asset management*

```
PERFECT        DELTA < 0.02
CONFIRMED      DELTA < 0.05
DRIFT_WARNING  DELTA < 0.10
DRIFT_CRITICAL DELTA ≥ 0.10

Rationale: Financial instructions require near-exact semantic transmission.
           Even small drift can cause wrong instrument, size, or timing.
           Regulatory liability compounds the risk.

Examples:  Trading agents, payment execution, portfolio management

Special:   CONSTRAINT atom weight increased to 35% (from 25%)
           in financial domain IC calculation.
           Order size and price limits are non-negotiable constraints.
```

---

### Tier 5 — CRITICAL_SAFETY
*Medical, infrastructure, emergency, defense*

```
PERFECT        DELTA < 0.01
CONFIRMED      DELTA < 0.03
DRIFT_WARNING  DELTA < 0.05
DRIFT_CRITICAL DELTA ≥ 0.05

Rationale: Human life or critical infrastructure may depend on
           exact semantic transmission. No tolerance for ambiguity.
           Any drift above 0.05 triggers immediate halt and human review.

Examples:  Medical device control, emergency response, power grid management

Special:   HUMAN-IN-THE-LOOP mandatory for all DRIFT_WARNING events.
           Automatic ABORT on DRIFT_CRITICAL. No retry without human authorization.
           ACCOUNTABILITY-LAYER entries are legally immutable.
```

---

## 3. Domain Detection

### 3.1 Explicit Declaration

The preferred method. The ORIGIN agent declares the domain tier
in the ARIA-IC header:

```
ARIA-IC Header Extension (RFC-003):
┌─────────────────────────────────────┐
│ DOMAIN_TIER: {0|1|2|3|4|5}        │
│ DOMAIN_LABEL: string (optional)    │
│ THRESHOLD_OVERRIDE: bool           │
│ CUSTOM_THRESHOLDS: object (opt.)   │
└─────────────────────────────────────┘
```

### 3.2 Automatic Domain Inference

When no domain is declared, ARIA performs automatic inference
using keyword and semantic pattern matching on the MISSION atom:

```
INFERENCE ENGINE:

Financial signals:
  Keywords: trade, order, buy, sell, price, portfolio, asset, fund
  Entities: stock tickers, currency codes, exchange names
  → Assign: Tier 4 FINANCIAL

Medical signals:
  Keywords: dose, administer, patient, diagnosis, medication, surgery
  Entities: drug names, medical procedure codes, ICD codes
  → Assign: Tier 5 CRITICAL_SAFETY

Legal signals:
  Keywords: contract, liability, clause, regulation, compliance
  → Assign: Tier 3 BUSINESS_CRITICAL

Creative signals:
  Keywords: write, generate, create, imagine, design, compose
  No transactional entities present
  → Assign: Tier 0 CREATIVE

Default (no clear signal):
  → Assign: Tier 2 GENERAL
```

### 3.3 Inference Confidence

```
If inference confidence < 0.80:
  → Default to next stricter tier
  → Log inference uncertainty in ACCOUNTABILITY-LAYER
  → Notify origin agent (async)

Rationale: When in doubt, be stricter.
           False positives (over-strict) cause retransmits.
           False negatives (under-strict) can cause harm.
```

---

## 4. Threshold Override Mechanism

### 4.1 When Overrides Are Permitted

Domain operators may customize thresholds within permitted ranges:

```
TIER 0 CREATIVE:         any value ≥ Tier 2 defaults
TIER 1 RESEARCH:         any value ≥ Tier 2 defaults
TIER 2 GENERAL:          locked (reference defaults)
TIER 3 BUSINESS_CRITICAL: may only be stricter than defaults
TIER 4 FINANCIAL:         may only be stricter than defaults
TIER 5 CRITICAL_SAFETY:   locked (cannot be relaxed)
                           ARIA Foundation approval required for any change
```

### 4.2 Override Logging

All threshold overrides are mandatory entries in the ACCOUNTABILITY-LAYER:

```
ACCOUNTABILITY LOG — THRESHOLD OVERRIDE:
  timestamp:         [ISO 8601]
  agent_id:          [ARIA-ID]
  domain_tier:       [tier number]
  default_thresholds: [values]
  applied_thresholds: [values]
  override_reason:   [string]
  authorized_by:     [ARIA-ID or HUMAN-ORIGIN channel]
```

---

## 5. Domain Atom Weight Adjustments

RFC-002 defines default atom weights for IC generation.
RFC-003 permits domain-specific weight adjustments:

```
                CORE  CONSTRAINTS  CONTEXT  SUCCESS  FAILURE
TIER 0 Creative  0.50    0.10       0.20     0.12     0.08
TIER 1 Research  0.40    0.20       0.25     0.10     0.05
TIER 2 General   0.40    0.25       0.15     0.12     0.08  (default)
TIER 3 Business  0.35    0.30       0.15     0.12     0.08
TIER 4 Financial 0.30    0.35       0.15     0.10     0.10
TIER 5 Safety    0.25    0.35       0.15     0.10     0.15
```

Rationale for Safety tier:
- FAILURE atom weight increased: knowing when to abort is critical
- CONSTRAINT atom weight increased: hard limits must survive transmission
- CORE atom weight reduced: specific instructions matter more than abstract goal

---

## 6. Multi-Domain Agent Chains

### 6.1 The Strictest Domain Wins

When an agent chain spans multiple domains:

```
Agent A (General) → Agent B (Financial) → Agent C (General)
  Tier 2              Tier 4               Tier 2

Applied threshold for ENTIRE chain: Tier 4 FINANCIAL

Rationale: The chain is only as safe as its most critical link.
           Relaxing thresholds at chain exit does not undo
           the risk introduced at the critical segment.
```

### 6.2 Domain Transition Logging

Every domain boundary crossing is logged:

```
ACCOUNTABILITY LOG — DOMAIN TRANSITION:
  timestamp:       [ISO 8601]
  from_agent:      [ARIA-ID]
  to_agent:        [ARIA-ID]
  from_tier:       [tier number]
  to_tier:         [tier number]
  applied_tier:    [effective tier for chain]
  chain_ic:        [IC_origin reference]
```

---

## 7. Reference Threshold Table

```
┌──────────────────────┬─────────┬───────────┬─────────────┬──────────────┐
│ Domain Tier          │ PERFECT │ CONFIRMED │ DRIFT_WARN  │ DRIFT_CRIT   │
├──────────────────────┼─────────┼───────────┼─────────────┼──────────────┤
│ 0 CREATIVE           │ < 0.15  │ < 0.30    │ < 0.50      │ ≥ 0.50       │
│ 1 RESEARCH           │ < 0.08  │ < 0.20    │ < 0.35      │ ≥ 0.35       │
│ 2 GENERAL (default)  │ < 0.05  │ < 0.15    │ < 0.30      │ ≥ 0.30       │
│ 3 BUSINESS_CRITICAL  │ < 0.03  │ < 0.08    │ < 0.15      │ ≥ 0.15       │
│ 4 FINANCIAL          │ < 0.02  │ < 0.05    │ < 0.10      │ ≥ 0.10       │
│ 5 CRITICAL_SAFETY    │ < 0.01  │ < 0.03    │ < 0.05      │ ≥ 0.05       │
└──────────────────────┴─────────┴───────────┴─────────────┴──────────────┘
```

---

## 8. Open Questions

```
[ ] Tier 5 approval process for threshold modifications — governance details
[ ] Hybrid domain classification (e.g. legal-financial overlap)
[ ] Dynamic tier escalation mid-chain (agent discovers higher risk mid-execution)
[ ] Industry-specific sub-tiers (healthcare vs. pharma vs. surgical)
[ ] Regulatory mapping (EU AI Act, FDA, SEC compliance integration)
```

---

## Document History

```
v0.1  Vatertag 2025  Initial specification
                     Authors: Irsan + Claude (Anthropic)
                     Status: DRAFT
                     Depends: ARIA-RFC-001, ARIA-RFC-002
```

---

*ARIA-RFC-003 — Domain Threshold Calibration*
*© 2025 Irsan — Published as open specification*
*"The stakes determine the tolerance."*
