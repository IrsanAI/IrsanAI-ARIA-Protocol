<!-- ARIA Protocol — Root README -->
<!-- Language: EN (default) | DE (see below) -->

<div align="center">

<!-- LOGO / TITLE BLOCK -->

```
 █████╗ ██████╗ ██╗ █████╗
██╔══██╗██╔══██╗██║██╔══██╗
███████║██████╔╝██║███████║
██╔══██║██╔══██╗██║██╔══██║
██║  ██║██║  ██║██║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
```

### **Agent Reasoning & Intent Architecture**
#### *The Open Protocol Standard for Agent-to-Agent Communication*

---

[![Status](https://img.shields.io/badge/Status-DRAFT%20v0.1-orange?style=flat-square)]()
[![RFC](https://img.shields.io/badge/RFCs-002-blue?style=flat-square)]()
[![License](https://img.shields.io/badge/License-Open%20Specification-green?style=flat-square)]()
[![Origin](https://img.shields.io/badge/Origin-Vatertag%202025-lightgrey?style=flat-square)]()
[![Paradigm](https://img.shields.io/badge/Paradigm-Agent--First-purple?style=flat-square)]()

**🌐 Language / Sprache:**
[🇬🇧 English](#english) · [🇩🇪 Deutsch](#deutsch)

</div>

---

<a name="english"></a>

## 🇬🇧 English

### What is ARIA?

ARIA is an open, standardized communication protocol for the era of AI agents.

As **TCP/IP** standardized machine-to-machine communication,
ARIA standardizes **agent-to-agent communication** — with one fundamental difference:

> ARIA operates on **semantic integrity**, not just byte integrity.

The core problem ARIA solves:

**Semantic Loss over long agent chains.**

When AI agents communicate across systems, ecosystems, and organizations,
meaning degrades — the way packets degraded in early networks.
ARIA is the protocol that prevents this.

---

### The Paradigm Shift

```
Last 10–20 years:     Human is the primary user.
                      Algorithms optimize for human behavior.

ARIA era:             Agent is the primary user.
                      Protocols optimize for agent behavior.
                      The human remains the authorizing principal.
```

Almost no existing protocol thinks this way.
ARIA is designed from the ground up for a world where
AI agents act, decide, and communicate — on behalf of humans,
but with each other.

---

### The Problem No One Has Standardized Yet

```
Agent A → Agent B → Agent C → Agent D → Agent E

Original intent:  "Buy Apple stock. Max 10k€. Blue chips only."

Agent B receives: "Purchase AAPL shares up to 10.000€"        ✓
Agent C receives: "Acquire Apple securities"                   ~ warning
Agent D receives: "Invest in Apple"                           ✗ drift
Agent E receives: "Technology sector investment"              ✗ critical
```

TCP solved this for **bytes** in 1974.
ARIA solves this for **meaning** in 2025.

---

### The ARIA Protocol Stack

```
╔══════════════════════════════════════════════════════════╗
║                  ARIA PROTOCOL STACK                      ║
╠════╦═════════════════════════════════════════════════════╣
║  7 ║  MISSION-LAYER       What is the agent's mission?   ║
║  6 ║  CONTEXT-LAYER       What does the agent know?      ║
║  5 ║  TRUST-LAYER         Who communicates with whom?    ║
║  4 ║  PRIORITY-LAYER      What is critical right now?    ║
║    ║  └─ SEMANTIC-TRANSPORT SUBLAYER (STS)               ║
║    ║     Intent-Checksum · Semantic-ACK · Drift-Detect   ║
║  3 ║  ROUTING-LAYER       Which agent handles this?      ║
║  2 ║  ACCOUNTABILITY-LAYER Every decision traceable.     ║
║  1 ║  ORIGIN-LAYER        Where did the mission start?   ║
║    ║  HUMAN · AGENT · SYSTEM · HYBRID                    ║
╚════╩═════════════════════════════════════════════════════╝
```

---

### The 5 Agent Primitives

Every ARIA-compliant agent implements five universal primitives:

| # | Primitive | Description |
|---|---|---|
| 1 | **IDENTITY** | Who am I? Who are you? What trust level? |
| 2 | **MISSION** | What is my goal? What is NOT my goal? |
| 3 | **CONTEXT** | What do I know? What am I missing? |
| 4 | **PRIORITY** | What matters most right now? |
| 5 | **ACCOUNTABILITY** | Can I justify every decision I make? |

---

### ARIA Channels

Analogous to network ports — standardized communication types:

| Channel | Type | Description |
|---|---|---|
| `001` | HUMAN-ORIGIN | Direct human instruction |
| `002` | VERIFIED-HUMAN | Cryptographically verified human |
| `003` | AGENT-TO-AGENT | Agent communicating with agent |
| `004` | SYSTEM-AUTONOMOUS | Autonomous system instruction |
| `005` | HYBRID-AUTHORIZED | Human → System → Agent chain |
| `006` | EMERGENCY-OVERRIDE | Critical priority, dual verification |
| `007` | GOVERNANCE | Protocol-level, RFC updates |

---

### The Intent Checksum (ARIA-ICA)

The heart of ARIA. Before any agent passes context to another,
it generates an **Intent Checksum** — a compressed semantic fingerprint of meaning.

```
NOT a hash of the text.
A hash of the MEANING.

"Buy Apple stock"   ──┐
"Purchase AAPL"     ──┼──→  IC: [identical semantic vector]
"Acquire AAPL eq."  ──┘

Semantic ACK:  Did meaning arrive — not just bytes?
Drift Detect:  Continuous monitoring across the entire chain.
Retransmit:    Only the drifted semantic atom. Not the full context.
```

→ Full specification: [ARIA-RFC-002](./docs/rfcs/ARIA-RFC-002_Intent_Checksum.md)

---

### Core Principles

```
OPEN          →  No entity owns ARIA. Published as open RFC.
MINIMAL       →  ARIA solves only agent communication.
SEMANTIC      →  Integrity of meaning, not just bytes.
TRANSPARENT   →  Every decision traceable.
DECENTRALIZED →  No single point of control. Mesh topology.
BACKWARD COMP →  Runs over existing TCP/IP infrastructure.
AGENT-FIRST   →  Human remains principal. Agent is primary user.
```

---

### Historical Context

```
1969  ARPANET        Machines connected for the first time
1974  TCP/IP Spec    The standard written — before the WWW existed
1991  WWW            Built on TCP/IP — 17 years later
2025  LLM Agents     Agents act — but no semantic standard exists
2025  ARIA v0.1      This repository — Vatertag 2025  ← WE ARE HERE
20??  Agent Web      Built on ARIA — unknown yet
```

---

### Repository Structure

```
IrsanAI-ARIA-Protocol/
│
├── README.md                          ← You are here
├── docs/rfcs/ARIA-RFC-001_Protocol_Stack.md     ← Full protocol specification
├── docs/README_ARCHITECTURE.md               ← Architecture and intent compass
├── docs/rfcs/ARIA-RFC-002_Intent_Checksum.md    ← Intent Checksum Algorithm
├── docs/guides/CONTRIBUTING.md                    ← How to contribute
│
├── docs/rfcs/ARIA-RFC-003_Domain_Thresholds.md  ← Domain threshold calibration
├── docs/analysis/REPO_INTENT_UNIQUENESS_ASSESSMENT.md ← Strategic analysis and roadmap
│
├── /specs (planned)                   ← Future RFCs extension set
│   ├── ARIA-RFC-004 (planned)         ← Embedding model registry
│   └── ARIA-RFC-005 (planned)         ← Quantum-resistant trust layer
│
├── docs/agents/Claude IrsanAI - ARIA - Agent.md  ← Claude collaboration brief
├── reference/runtime/mission_orchestrator.py      ← Runtime scaffold
├── reference/runtime/execution_specialist.py      ← Runtime scaffold
├── reference/runtime/interfaces.py                ← Runtime contracts
├── reference/runtime/validation.py                ← Schema validation
├── reference/runtime/thresholds.py                ← RFC-003 threshold profiles
├── reference/runtime/rrc.py                       ← RFC-004 replay capsule emitter
├── reference/runtime/semantic.py                  ← Similarity + atom drift scoring
├── reference/runtime/accountability.py            ← Signed accountability events
├── reference/runtime/cli.py                       ← Minimal CLI (validate/ack/rrc)
├── reference/interop/legacy_bridge_adapter.py     ← Legacy bridge adapter
├── schemas/aria_packet.schema.json                ← Packet schema
├── schemas/semantic_ack.schema.json               ← ACK schema
├── schemas/rrc_capsule.schema.json                ← Replay capsule schema
├── tests/conformance/test_semantic_ack_chain.py   ← Conformance tests
├── tests/conformance/test_threshold_profiles_and_rrc.py ← Threshold + RRC tests
├── tests/conformance/test_semantic_atoms_and_accountability.py ← Atom drift + signatures
└── tests/conformance/test_cli_and_rrc_extensions.py ← CLI + RRC extension tests
```

---

### Roadmap

```
PHASE 0  FOUNDATION         [Vatertag 2025]  ✅ Complete
  Protocol stack · 5 Primitives · Intent Checksum concept · RFC-001 · RFC-002

PHASE 1  CORE SPECIFICATION              [ ] In Progress
  Intent Checksum full spec · ARIA-ID standard · Trust certificates

PHASE 2  REFERENCE IMPLEMENTATION        [ ] Planned
  Open source library · Semantic ACK PoC · Drift detection prototype

PHASE 3  STANDARDIZATION                 [ ] Future
  ARIA Foundation · Community RFC process · Compatibility suite

PHASE 4  ECOSYSTEM                       [ ] Future
  Public agent registry · Inter-ecosystem routing · IETF submission
```

---

### Relation to IrsanAI Ecosystem

ARIA is the infrastructure layer that connects the entire IrsanAI stack:

| Repository | Role in ARIA context |
|---|---|
| [IrsanAI-VERA](https://github.com/IrsanAI/IrsanAI-Universe) | Predictive validation — ARIA Mission-Layer candidate |
| [LRP-v1.3](https://github.com/IrsanAI/LRP-v1.3) | Language Resonance — feeds ARIA Context-Layer |
| [PDP-v3.0](https://github.com/IrsanAI/PDP-v3.0-) | Perspective Protocol — ARIA Trust-Layer alignment |
| [NTF-v1.0](https://github.com/IrsanAI/NTF-v1.0) | NeuroToken Framework — ARIA Priority-Layer candidate |
| [RKP-v2.0](https://github.com/IrsanAI/RKP-v2.0-) | Resonant Kinetic Prediction — Drift Detection synergy |

---

### Contributing

ARIA is an open specification. No single entity owns it.

If you are working on:
- AI agent frameworks
- Semantic integrity systems
- Agent communication protocols
- LLM orchestration infrastructure

→ Open an Issue. Start a Discussion. Submit a PR.

The RFC process is open to all. That is the point.

---

### License

ARIA Protocol Specification is published as an **open specification**.
Free to read, implement, extend, and build upon.
No permission required.

Attribution appreciated: *"Based on ARIA Protocol — IrsanAI, 2025"*

---

### Origin

> Created on **Vatertag 2025** — Father's Day, Germany.
> By Irsan + Claude (Anthropic).
> The first agent-first protocol specification of its kind.

---

<div align="center">

*"TCP/IP was specified in 1974. The WWW came 17 years later.*
*Nobody knew what would be built on top of it.*
*ARIA is specified today. What is built on top — nobody knows yet."*

</div>

---
---

<a name="deutsch"></a>

## 🇩🇪 Deutsch

<details>
<summary><strong>🇩🇪 Klicken um die deutsche Version anzuzeigen</strong></summary>

<br>

### Was ist ARIA?

ARIA ist ein offenes, standardisiertes Kommunikationsprotokoll für die Ära der KI-Agenten.

So wie **TCP/IP** die Maschine-zu-Maschine-Kommunikation standardisiert hat,
standardisiert ARIA die **Agenten-zu-Agenten-Kommunikation** — mit einem fundamentalen Unterschied:

> ARIA operiert auf **semantischer Integrität**, nicht nur auf Byte-Integrität.

Das Kernproblem das ARIA löst:

**Semantischer Verlust über lange Agenten-Ketten.**

Wenn KI-Agenten über Systeme, Ökosysteme und Organisationen hinweg kommunizieren,
degradiert die Bedeutung — so wie Pakete im frühen Internet verloren gingen.
ARIA ist das Protokoll, das dies verhindert.

---

### Der Paradigmenwechsel

```
Letzte 10–20 Jahre:   Der Mensch ist der primäre Nutzer.
                      Algorithmen optimieren menschliches Verhalten.

ARIA-Ära:             Der Agent ist der primäre Nutzer.
                      Protokolle optimieren Agenten-Verhalten.
                      Der Mensch bleibt der autorisierende Auftraggeber.
```

Nahezu kein bestehendes Protokoll denkt so.
ARIA ist von Grund auf für eine Welt entworfen, in der
KI-Agenten handeln, entscheiden und kommunizieren — im Auftrag von Menschen,
aber miteinander.

---

### Das Problem das noch niemand standardisiert hat

```
Agent A → Agent B → Agent C → Agent D → Agent E

Ursprünglicher Auftrag: "Apple-Aktien kaufen. Max 10k€. Nur Blue Chips."

Agent B empfängt: "AAPL-Aktien bis 10.000€ erwerben"           ✓
Agent C empfängt: "Apple-Wertpapiere akquirieren"              ~ Warnung
Agent D empfängt: "In Apple investieren"                       ✗ Drift
Agent E empfängt: "Technologiesektor-Investment"               ✗ Kritisch
```

TCP löste dies für **Bytes** im Jahr 1974.
ARIA löst dies für **Bedeutung** im Jahr 2025.

---

### Der ARIA Protocol Stack

```
╔══════════════════════════════════════════════════════════╗
║                  ARIA PROTOCOL STACK                      ║
╠════╦═════════════════════════════════════════════════════╣
║  7 ║  MISSION-LAYER       Was ist der Agenten-Auftrag?   ║
║  6 ║  CONTEXT-LAYER       Was weiß der Agent?            ║
║  5 ║  TRUST-LAYER         Wer kommuniziert mit wem?      ║
║  4 ║  PRIORITY-LAYER      Was ist gerade kritisch?       ║
║    ║  └─ SEMANTIC-TRANSPORT SUBLAYER (STS)               ║
║    ║     Intent-Checksum · Semantic-ACK · Drift-Erkennung║
║  3 ║  ROUTING-LAYER       Welcher Agent ist zuständig?   ║
║  2 ║  ACCOUNTABILITY-LAYER Jede Entscheidung nachvollz.  ║
║  1 ║  ORIGIN-LAYER        Woher kam der Auftrag?         ║
║    ║  MENSCH · AGENT · SYSTEM · HYBRID                   ║
╚════╩═════════════════════════════════════════════════════╝
```

---

### Die 5 Agenten-Primitive

Jeder ARIA-konforme Agent implementiert fünf universelle Primitive:

| # | Primitiv | Beschreibung |
|---|---|---|
| 1 | **IDENTITÄT** | Wer bin ich? Wer bist du? Welches Vertrauenslevel? |
| 2 | **MISSION** | Was ist mein Ziel? Was ist NICHT mein Ziel? |
| 3 | **KONTEXT** | Was weiß ich? Was fehlt mir? |
| 4 | **PRIORITÄT** | Was ist jetzt am wichtigsten? |
| 5 | **VERANTWORTLICHKEIT** | Kann ich jede Entscheidung begründen? |

---

### ARIA-Channels

Analog zu Netzwerk-Ports — standardisierte Kommunikationstypen:

| Channel | Typ | Beschreibung |
|---|---|---|
| `001` | HUMAN-ORIGIN | Direkte menschliche Anweisung |
| `002` | VERIFIED-HUMAN | Kryptographisch verifizierter Mensch |
| `003` | AGENT-TO-AGENT | Agent kommuniziert mit Agent |
| `004` | SYSTEM-AUTONOMOUS | Autonome System-Anweisung |
| `005` | HYBRID-AUTHORIZED | Mensch → System → Agent Kette |
| `006` | EMERGENCY-OVERRIDE | Kritische Priorität, doppelte Verifikation |
| `007` | GOVERNANCE | Protokollebene, RFC-Updates |

---

### Der Intent Checksum (ARIA-ICA)

Das Herzstück von ARIA. Bevor ein Agent Kontext an einen anderen übergibt,
generiert er einen **Intent Checksum** — einen komprimierten semantischen Fingerabdruck der Bedeutung.

```
KEIN Hash des Textes.
Ein Hash der BEDEUTUNG.

"Apple-Aktien kaufen"    ──┐
"AAPL erwerben"          ──┼──→  IC: [identischer semantischer Vektor]
"AAPL-Wertpapiere aqk."  ──┘

Semantic ACK:    Ist die Bedeutung angekommen — nicht nur Bytes?
Drift-Erkennung: Kontinuierliche Überwachung über die gesamte Kette.
Retransmit:      Nur das gedriftete semantische Atom. Nicht der volle Kontext.
```

→ Vollständige Spezifikation: [ARIA-RFC-002](./docs/rfcs/ARIA-RFC-002_Intent_Checksum.md)

---

### Kernprinzipien

```
OFFEN          →  Niemand besitzt ARIA. Veröffentlicht als offener RFC.
MINIMAL        →  ARIA löst nur Agenten-Kommunikation.
SEMANTISCH     →  Integrität der Bedeutung, nicht nur Bytes.
TRANSPARENT    →  Jede Entscheidung nachvollziehbar.
DEZENTRAL      →  Kein zentraler Kontrollpunkt. Mesh-Topologie.
RÜCKWÄRTSKOMP. →  Läuft über bestehende TCP/IP-Infrastruktur.
AGENT-FIRST    →  Mensch bleibt Auftraggeber. Agent ist primärer Nutzer.
```

---

### Historischer Kontext

```
1969  ARPANET        Maschinen erstmals verbunden
1974  TCP/IP Spec    Der Standard geschrieben — bevor das WWW existierte
1991  WWW            Auf TCP/IP gebaut — 17 Jahre später
2025  LLM-Agenten    Agenten handeln — kein semantischer Standard existiert
2025  ARIA v0.1      Dieses Repository — Vatertag 2025  ← WIR SIND HIER
20??  Agenten-Web    Auf ARIA gebaut — noch unbekannt
```

---

### Roadmap

```
PHASE 0  FUNDAMENT          [Vatertag 2025]  ✅ Abgeschlossen
  Protocol Stack · 5 Primitive · Intent Checksum · RFC-001 · RFC-002

PHASE 1  KERNSPEZIFIKATION               [ ] In Arbeit
  Intent Checksum vollständig · ARIA-ID Standard · Trust-Zertifikate

PHASE 2  REFERENZIMPLEMENTIERUNG         [ ] Geplant
  Open-Source-Bibliothek · Semantic ACK PoC · Drift-Detection Prototyp

PHASE 3  STANDARDISIERUNG               [ ] Zukunft
  ARIA Foundation · Community RFC-Prozess · Kompatibilitäts-Suite

PHASE 4  ÖKOSYSTEM                      [ ] Zukunft
  Öffentliches Agent-Registry · Inter-Ökosystem-Routing · IETF-Einreichung
```

---

### Relation zum IrsanAI-Ökosystem

ARIA ist die Infrastrukturschicht, die den gesamten IrsanAI-Stack verbindet:

| Repository | Rolle im ARIA-Kontext |
|---|---|
| [IrsanAI-VERA](https://github.com/IrsanAI/IrsanAI-Universe) | Prädiktive Validierung — ARIA Mission-Layer Kandidat |
| [LRP-v1.3](https://github.com/IrsanAI/LRP-v1.3) | Language Resonance — ARIA Context-Layer Einspeisung |
| [PDP-v3.0](https://github.com/IrsanAI/PDP-v3.0-) | Perspective Protocol — ARIA Trust-Layer Ausrichtung |
| [NTF-v1.0](https://github.com/IrsanAI/NTF-v1.0) | NeuroToken Framework — ARIA Priority-Layer Kandidat |
| [RKP-v2.0](https://github.com/IrsanAI/RKP-v2.0-) | Resonant Kinetic Prediction — Drift Detection Synergie |

---

### Mitwirken

ARIA ist eine offene Spezifikation. Niemand besitzt sie.

Wenn du arbeitest an:
- KI-Agenten-Frameworks
- Semantischen Integritätssystemen
- Agenten-Kommunikationsprotokollen
- LLM-Orchestrierungs-Infrastruktur

→ Öffne ein Issue. Starte eine Diskussion. Reiche einen PR ein.

Der RFC-Prozess steht allen offen. Das ist der Sinn.

---

### Lizenz

Die ARIA-Protokoll-Spezifikation wird als **offene Spezifikation** veröffentlicht.
Kostenlos zu lesen, zu implementieren, zu erweitern und darauf aufzubauen.
Keine Genehmigung erforderlich.

Namensnennung erwünscht: *„Basierend auf dem ARIA-Protokoll — IrsanAI, 2025"*

---

### Entstehung

> Erstellt am **Vatertag 2025** — Father's Day, Deutschland.
> Von Irsan + Claude (Anthropic).
> Die erste agenten-first Protokoll-Spezifikation ihrer Art.

---

<div align="center">

*„TCP/IP wurde 1974 spezifiziert. Das WWW kam 17 Jahre später.*
*Niemand wusste, was darauf aufgebaut werden würde.*
*ARIA wird heute spezifiziert. Was darauf aufgebaut wird — weiß noch niemand."*

</div>

</details>

---

<div align="center">

**ARIA Protocol** · IrsanAI · Vatertag 2025
[RFC-001](./docs/rfcs/ARIA-RFC-001_Protocol_Stack.md) · [RFC-002](./docs/rfcs/ARIA-RFC-002_Intent_Checksum.md) · [Issues](https://github.com/IrsanAI/IrsanAI-ARIA-Protocol/issues) · [Discussions](https://github.com/IrsanAI/IrsanAI-ARIA-Protocol/discussions)

</div>
