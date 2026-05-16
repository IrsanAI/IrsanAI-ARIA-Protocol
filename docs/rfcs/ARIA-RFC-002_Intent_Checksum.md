# ARIA-RFC-002
## Intent Checksum Algorithm (ARIA-ICA)
### Semantic Integrity for Agent-to-Agent Communication

```
Status:    DRAFT
Version:   0.1
Created:   Vatertag 2025
Authors:   Irsan + Claude (Anthropic)
Depends:   ARIA-RFC-001 (ARIA Protocol v0.1)
```

---

## Abstract

ARIA-RFC-002 specifies the **Intent Checksum Algorithm (ARIA-ICA)** — the core mechanism by which ARIA guarantees semantic integrity across agent-to-agent communication chains.

Where TCP guarantees byte integrity via numerical checksums, ARIA-ICA guarantees **meaning integrity** via semantic vector checksums. A receiving agent can verify not just that bytes arrived — but that **meaning arrived unchanged.**

---

## 1. Problem Statement

### 1.1 Semantic Loss in Agent Chains

```
Agent A → Agent B → Agent C → Agent D → Agent E
[Original Intent: "Buy Apple stock, max 10k€, Blue Chips only"]

Agent B receives:  "Purchase AAPL shares up to 10.000€"       ✓
Agent C receives:  "Acquire Apple securities"                  ~ warning
Agent D receives:  "Invest in Apple"                          ✗ drift
Agent E receives:  "Technology sector investment"             ✗ critical
```

No existing protocol detects or corrects this degradation.

### 1.2 Why Byte Checksums Fail Here

```
"Buy Apple stock"     → SHA256: a3f9b2...
"Purchase AAPL"       → SHA256: 7c4e1d...   ← Different hash
                                                Same meaning
                                                SHA256 useless
```

A semantic checksum must produce **similar outputs for similar meanings** — the opposite of cryptographic hash design.

### 1.3 The Core Requirement

```
ARIA-ICA MUST:
→ Produce identical or near-identical checksums for semantically
  equivalent inputs regardless of surface form
→ Produce detectably different checksums for semantically
  different inputs regardless of lexical similarity
→ Enable precise localization of which semantic component drifted
→ Enable minimal retransmission of only the drifted component
→ Be computationally feasible for real-time agent communication
→ Be model-agnostic (no single LLM dependency)
```

---

## 2. Semantic Decomposition

Before checksumming, every agent mission is decomposed into **5 Semantic Atoms** — the irreducible units of agent intent.

### 2.1 The 5 Semantic Atoms

```
┌─────────────────────────────────────────────────────────────┐
│                    SEMANTIC ATOMS                            │
├──────────────────┬──────────────────────────────────────────┤
│                  │                                          │
│  ATOM 1          │  CORE INTENT                            │
│  Weight: 40%     │  The fundamental goal in one sentence.  │
│                  │  Non-negotiable. Cannot be empty.        │
│                  │  Example: "Execute equity purchase"      │
│                  │                                          │
├──────────────────┼──────────────────────────────────────────┤
│                  │                                          │
│  ATOM 2          │  CONSTRAINTS                            │
│  Weight: 25%     │  What must NOT be done.                 │
│                  │  The negative space of the mission.     │
│                  │  Example: "Max 10k€. Blue chips only."  │
│                  │                                          │
├──────────────────┼──────────────────────────────────────────┤
│                  │                                          │
│  ATOM 3          │  CONTEXT DEPENDENCIES                   │
│  Weight: 15%     │  What knowledge the next agent needs.  │
│                  │  Prerequisites for correct execution.   │
│                  │  Example: "Portfolio state, risk class" │
│                  │                                          │
├──────────────────┼──────────────────────────────────────────┤
│                  │                                          │
│  ATOM 4          │  SUCCESS CONDITION                      │
│  Weight: 12%     │  Binary completion criterion.           │
│                  │  How agent knows: mission accomplished. │
│                  │  Example: "Order executed + confirmed"  │
│                  │                                          │
├──────────────────┼──────────────────────────────────────────┤
│                  │                                          │
│  ATOM 5          │  FAILURE CONDITION                      │
│  Weight: 8%      │  When to abort. Safety net.            │
│                  │  Protects against runaway execution.    │
│                  │  Example: "Price drops >5% mid-order"  │
│                  │                                          │
└──────────────────┴──────────────────────────────────────────┘
```

### 2.2 Decomposition Process

The decomposition engine uses a three-pass extraction:

```
PASS 1: Explicit extraction
        → Identify atoms explicitly stated in mission text

PASS 2: Implicit inference
        → Infer atoms not stated but clearly implied
        → Example: "Buy Apple" implies SUCCESS = "purchase confirmed"

PASS 3: Default injection
        → For any atom still empty: inject domain-appropriate defaults
        → Empty FAILURE_CONDITION → inject: "on any unrecoverable error, halt"
        → Prevents null atoms from corrupting the checksum
```

---

## 3. Vector Embedding

Each atom is transformed into a semantic vector using an **ensemble of three embedding models.**

### 3.1 Why Ensemble

Single-model embedding creates a dependency vulnerability:

```
SINGLE MODEL RISK:
→ Model update changes embedding space → all ICs invalidated
→ Model bias skews specific domains
→ Single point of manipulation

ENSEMBLE SOLUTION:
→ Three independent models vote
→ Majority semantic direction preserved
→ Resistant to single-model drift or manipulation
```

### 3.2 Ensemble Architecture

```
                    ATOM TEXT INPUT
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ MODEL A  │   │ MODEL B  │   │ MODEL C  │
    │ General  │   │ Domain   │   │Constraint│
    │ Semantic │   │ Specific │   │Specialized│
    └──────────┘   └──────────┘   └──────────┘
          │               │               │
    V_a [1536]      V_b [1536]      V_c [1536]
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                  ENSEMBLE COMBINER
                  V_final = normalize(
                    0.4 × V_a +
                    0.35 × V_b +
                    0.25 × V_c
                  )
                          │
                    V_atom [1536]
```

### 3.3 Model Selection Criteria

ARIA-ICA does not mandate specific models. ARIA-compliant implementations MUST use models that satisfy:

```
REQUIREMENT 1: Open or auditable weights
REQUIREMENT 2: Stable embedding space (versioned)
REQUIREMENT 3: Multilingual capability (minimum: EN, DE, ZH, AR, ES)
REQUIREMENT 4: Reproducible outputs for identical inputs
REQUIREMENT 5: Published benchmark on semantic similarity tasks
```

*Specific model recommendations: see ARIA-RFC-004 (pending)*

---

## 4. Intent Checksum Generation

### 4.1 The IC Formula

```
IC_vector = normalize(
  Σ (weight_i × V_atom_i)  for i in {1..5}
)

Where:
  weight_1 = 0.40  (CORE_INTENT)
  weight_2 = 0.25  (CONSTRAINTS)
  weight_3 = 0.15  (CONTEXT_DEPENDENCIES)
  weight_4 = 0.12  (SUCCESS_CONDITION)
  weight_5 = 0.08  (FAILURE_CONDITION)
  Σ weights = 1.00
```

### 4.2 IC Packet Format

```
┌─────────────────────────────────────────────────────────────┐
│                    ARIA-IC PACKET FORMAT                     │
├────────────────────┬────────────────────────────────────────┤
│   HEADER (64 bit)  │                                        │
│                    │  SEMANTIC PAYLOAD (256 dimensions)     │
│  [4]  Version      │                                        │
│  [4]  Channel ID   │  IC_vector: float32 × 256             │
│  [8]  Origin Type  │                                        │
│  [32] Timestamp    │  + per-atom sub-vectors (for          │
│  [8]  Chain Depth  │    drift localization):               │
│  [8]  Reserved     │                                        │
│                    │  V_atom_1: float32 × 256              │
│                    │  V_atom_2: float32 × 256              │
│                    │  V_atom_3: float32 × 256              │
│                    │  V_atom_4: float32 × 256              │
│                    │  V_atom_5: float32 × 256              │
└────────────────────┴────────────────────────────────────────┘

Total IC size: ~5.1 KB
Negligible overhead compared to typical agent context sizes.
```

### 4.3 IC Immutability Rules

```
RULE 1: IC_origin is generated ONCE at mission origin.
        It NEVER changes, regardless of chain length.

RULE 2: IC_origin travels with every transmission
        in the ARIA packet header — untouched.

RULE 3: Chain Depth increments at each hop.
        IC_vector does NOT change with depth.

RULE 4: Only the ORIGIN agent may issue a new IC.
        Intermediate agents may NOT modify IC_origin.
```

---

## 5. Semantic ACK Protocol

### 5.1 ACK Generation

Upon receiving a transmission, the receiving agent:

```
STEP 1: Extract IC_origin from packet header
STEP 2: Extract context payload
STEP 3: Independently generate IC_received from context
        (full decomposition + embedding — no shortcuts)
STEP 4: Compute DELTA
STEP 5: Issue ACK_STATUS
STEP 6: Log to ACCOUNTABILITY-LAYER
```

### 5.2 Delta Computation

```
DELTA = 1 - cosine_similarity(IC_origin.vector, IC_received.vector)

cosine_similarity(A, B) = (A · B) / (|A| × |B|)

DELTA range: [0.0, 2.0]
  0.0 = identical meaning
  1.0 = orthogonal (unrelated)
  2.0 = opposite meaning
```

### 5.3 ACK Status Thresholds

```
┌────────────────────────────────────────────────────────────┐
│                   ACK STATUS DECISION TREE                  │
├──────────────────┬─────────────────────────────────────────┤
│ DELTA < 0.05     │ SEMANTIC_ACK: PERFECT                   │
│                  │ → Proceed immediately                   │
│                  │ → No action required                    │
├──────────────────┼─────────────────────────────────────────┤
│ 0.05 ≤ DELTA     │ SEMANTIC_ACK: CONFIRMED                 │
│       < 0.15     │ → Proceed                               │
│                  │ → Log delta for chain monitoring        │
├──────────────────┼─────────────────────────────────────────┤
│ 0.15 ≤ DELTA     │ SEMANTIC_ACK: DRIFT_WARNING             │
│       < 0.30     │ → Proceed with caution flag             │
│                  │ → Alert origin agent (async)            │
│                  │ → Increase monitoring frequency         │
├──────────────────┼─────────────────────────────────────────┤
│ DELTA ≥ 0.30     │ SEMANTIC_ACK: DRIFT_CRITICAL            │
│                  │ → HALT execution                        │
│                  │ → Localize drifted atom                 │
│                  │ → Request SEMANTIC_RETRANSMIT           │
│                  │ → Alert origin agent (sync/blocking)    │
└──────────────────┴─────────────────────────────────────────┘

Note: Threshold values are ARIA v0.1 defaults.
Domain-specific implementations may adjust via ARIA-RFC process.
Financial/medical domains recommended: stricter thresholds.
```

---

## 6. Chain Integrity Monitoring

### 6.1 The DNA Principle

```
IC_origin travels through the entire chain
like DNA through every cell of an organism.

Every cell carries the complete blueprint.
Every agent carries the complete original intent.

Agent A → Agent B → Agent C → Agent D → Agent E
  IC₀  →   IC₀  →   IC₀  →   IC₀  →   IC₀
(depth=0) (depth=1) (depth=2) (depth=3) (depth=4)
```

### 6.2 Chain Drift Accumulation Detection

```
At each hop, every agent computes:

CHAIN_DRIFT = cosine_distance(IC_origin, IC_current_local)

This detects CUMULATIVE drift —
the total semantic distance traveled from origin.

Individual hop ACKs catch local drift.
Chain Drift catches slow, gradual semantic erosion
that no individual hop would flag.
```

### 6.3 Origin Alert Protocol

```
CHAIN_DRIFT > 0.30:

→ Alert sent to ORIGIN AGENT (not current agent)
→ Alert sent to ACCOUNTABILITY-LAYER
→ Chain paused pending origin decision

Origin agent receives:
  - Chain depth at which critical drift occurred
  - Which atom drifted most
  - Full drift trajectory (delta at each hop)
  - Recommended: RETRANSMIT or ABORT or OVERRIDE

KEY PRINCIPLE:
The source decides. Not the last agent in the chain.
This preserves mission integrity and human authorization.
```

---

## 7. Semantic Retransmit

### 7.1 The Git-Diff Principle

```
NAIVE RETRANSMIT (inefficient):
→ Resend entire context (potentially millions of tokens)
→ Full re-embedding computation
→ High latency, high cost

ARIA SEMANTIC RETRANSMIT (efficient):
→ Identify which specific atom drifted
→ Resend only that atom's semantic core
→ Minimal transmission, surgical precision

Analogy: git diff vs git clone
```

### 7.2 Atom Drift Localization

```
DRIFT_LOCALIZER:

For each atom i in {1..5}:
  atom_delta_i = cosine_distance(
    IC_origin.V_atom_i,
    IC_received.V_atom_i
  )

drifted_atom = argmax(atom_delta_i)

→ Highest delta = most drifted atom
→ This atom alone is retransmitted as PATCH
```

### 7.3 Retransmit Packet Format

```
ARIA-RETRANSMIT PACKET:
┌────────────────────────────────────┐
│ IC_origin (unchanged reference)   │
│ PATCH_ATOM_ID: {1|2|3|4|5}       │
│ PATCH_CONTENT: [atom text]        │
│ PATCH_VECTOR: [atom embedding]    │
│ RETRANSMIT_COUNT: [n]             │
│ RETRANSMIT_REASON: [drift_delta]  │
└────────────────────────────────────┘

Max retransmit attempts: 3 (default)
After 3 failures → ABORT + ORIGIN_ALERT + ACCOUNTABILITY_LOG
```

---

## 8. Full Algorithm — Reference Implementation

```python
# ARIA Intent Checksum Algorithm — Reference Implementation
# ARIA-RFC-002 v0.1
# Status: DRAFT

import numpy as np
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class ACKStatus(Enum):
    PERFECT = "PERFECT"
    CONFIRMED = "CONFIRMED"
    DRIFT_WARNING = "DRIFT_WARNING"
    DRIFT_CRITICAL = "DRIFT_CRITICAL"

class OriginType(Enum):
    HUMAN = "HUMAN"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"
    HYBRID = "HYBRID"

@dataclass
class SemanticAtoms:
    core_intent: str
    constraints: str
    context_dependencies: str
    success_condition: str
    failure_condition: str

@dataclass
class ARIAHeader:
    version: str = "ARIA-ICA-1.0"
    channel: int = 3
    origin_type: OriginType = OriginType.HUMAN
    timestamp: float = 0.0
    chain_depth: int = 0

@dataclass
class IntentChecksum:
    header: ARIAHeader
    ic_vector: np.ndarray        # 256-dim combined
    atom_vectors: dict           # per-atom 256-dim vectors

@dataclass
class ACKResult:
    status: ACKStatus
    delta: float
    drifted_atom: Optional[int] = None
    atom_deltas: Optional[dict] = None

class ARIA_ICA:
    
    ATOM_WEIGHTS = {
        'core_intent': 0.40,
        'constraints': 0.25,
        'context_dependencies': 0.15,
        'success_condition': 0.12,
        'failure_condition': 0.08
    }
    
    ACK_THRESHOLDS = {
        'PERFECT': 0.05,
        'CONFIRMED': 0.15,
        'DRIFT_WARNING': 0.30,
    }

    def decompose(self, mission_text: str) -> SemanticAtoms:
        """
        Extract 5 semantic atoms from mission text.
        Three-pass: explicit → implicit → defaults
        Implementation: domain-specific NLP pipeline
        """
        # Reference implementation: placeholder
        # Production: fine-tuned decomposition model
        raise NotImplementedError("Implement domain-specific decomposer")

    def ensemble_embed(self, text: str) -> np.ndarray:
        """
        Generate ensemble embedding from 3 models.
        Returns normalized 256-dim vector.
        """
        # Model A: General semantic (weight 0.40)
        # Model B: Domain specific (weight 0.35)  
        # Model C: Constraint specialized (weight 0.25)
        # Returns: weighted normalized combination
        raise NotImplementedError("Implement ensemble embedder")

    def generate(self,
                 mission_text: str,
                 header: ARIAHeader) -> IntentChecksum:
        
        # Step 1: Decompose into atoms
        atoms = self.decompose(mission_text)
        atom_dict = vars(atoms)
        
        # Step 2: Embed each atom
        atom_vectors = {}
        for atom_name, atom_text in atom_dict.items():
            atom_vectors[atom_name] = self.ensemble_embed(atom_text)
        
        # Step 3: Weighted combination
        ic_vector = np.zeros(256)
        for atom_name, weight in self.ATOM_WEIGHTS.items():
            ic_vector += weight * atom_vectors[atom_name]
        
        # Normalize to unit vector
        ic_vector = ic_vector / np.linalg.norm(ic_vector)
        
        return IntentChecksum(
            header=header,
            ic_vector=ic_vector,
            atom_vectors=atom_vectors
        )

    def verify(self,
               received_context: str,
               ic_origin: IntentChecksum) -> ACKResult:
        
        # Generate IC independently from received context
        ic_received = self.generate(
            received_context,
            ic_origin.header
        )
        
        # Compute overall delta
        delta = self._cosine_distance(
            ic_origin.ic_vector,
            ic_received.ic_vector
        )
        
        # Compute per-atom deltas
        atom_deltas = {}
        for atom_name in self.ATOM_WEIGHTS:
            atom_deltas[atom_name] = self._cosine_distance(
                ic_origin.atom_vectors[atom_name],
                ic_received.atom_vectors[atom_name]
            )
        
        # Determine ACK status
        if delta < self.ACK_THRESHOLDS['PERFECT']:
            return ACKResult(ACKStatus.PERFECT, delta, atom_deltas=atom_deltas)
        
        elif delta < self.ACK_THRESHOLDS['CONFIRMED']:
            return ACKResult(ACKStatus.CONFIRMED, delta, atom_deltas=atom_deltas)
        
        elif delta < self.ACK_THRESHOLDS['DRIFT_WARNING']:
            return ACKResult(ACKStatus.DRIFT_WARNING, delta, atom_deltas=atom_deltas)
        
        else:
            # Localize drifted atom
            drifted = max(atom_deltas, key=atom_deltas.get)
            return ACKResult(
                ACKStatus.DRIFT_CRITICAL,
                delta,
                drifted_atom=drifted,
                atom_deltas=atom_deltas
            )

    def retransmit_patch(self,
                         ic_origin: IntentChecksum,
                         drifted_atom: str) -> dict:
        return {
            'ic_origin_ref': ic_origin.header,
            'patch_atom': drifted_atom,
            'patch_vector': ic_origin.atom_vectors[drifted_atom],
            'retransmit_reason': f'DRIFT_CRITICAL on atom: {drifted_atom}'
        }

    def _cosine_distance(self,
                         v1: np.ndarray,
                         v2: np.ndarray) -> float:
        similarity = np.dot(v1, v2) / (
            np.linalg.norm(v1) * np.linalg.norm(v2)
        )
        return float(1 - similarity)
```

---

## 9. Comparison to Existing Approaches

```
┌──────────────────┬────────────────┬──────────────────────────┐
│ Approach         │ What it solves │ What ARIA-ICA adds       │
├──────────────────┼────────────────┼──────────────────────────┤
│ SHA256/MD5       │ Byte integrity │ Semantic integrity       │
│ Embeddings       │ Similarity     │ Standardized IC format   │
│ RAG              │ Context recall │ Proactive drift detect   │
│ Summarization    │ Compression    │ Atomic retransmission    │
│ LangChain memory │ State persist  │ Cross-agent verification │
│ Google A2A       │ Orchestration  │ Semantic ACK protocol    │
│ Anthropic MCP    │ Tool context   │ Chain integrity monitor  │
└──────────────────┴────────────────┴──────────────────────────┘
```

---

## 10. Open Questions & Future RFCs

```
RFC-003 (planned): Threshold calibration per domain
                   (Finance, Medical, Legal — stricter)

RFC-004 (planned): Approved embedding model registry
                   (Which models qualify as ARIA-compliant)

RFC-005 (planned): Quantum-resistant IC signatures
                   (Post-quantum Trust-Layer integration)

RFC-006 (planned): ARIA-ICA performance benchmarks
                   (Latency, cost, accuracy targets)

OPEN:   Optimal vector dimensionality (256 vs 512 vs 1536)
OPEN:   Cross-language IC stability (same intent, different language)
OPEN:   Adversarial robustness (intentional IC manipulation)
```

---

## Appendix A: Quick Reference

```
GENERATE IC:    decompose → embed (ensemble) → weight → normalize
VERIFY:         generate IC from received → cosine_distance → ACK
DELTA RANGES:   PERFECT <0.05 | CONFIRMED <0.15 | WARNING <0.30 | CRITICAL ≥0.30
RETRANSMIT:     localize drifted atom → patch only that atom
CHAIN MONITOR:  every agent holds IC_origin → computes cumulative drift
SOURCE RULE:    only origin agent decides on abort/retransmit/override
```

---

## Document History

```
v0.1  Vatertag 2025  Initial specification
                     Authors: Irsan + Claude (Anthropic)
                     Status: DRAFT
                     Depends: ARIA-RFC-001
```

---

*ARIA-RFC-002 — Intent Checksum Algorithm*
*© 2025 Irsan — Published as open specification*
*"Meaning must arrive as intact as bytes."*
