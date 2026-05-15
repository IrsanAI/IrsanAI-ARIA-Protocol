# Contributing to ARIA Protocol

```
Status:   ACTIVE
Version:  0.1
Created:  Vatertag 2025
Authors:  Irsan + Claude (Anthropic)
```

**🌐 Language / Sprache:**
[🇬🇧 English](#english) · [🇩🇪 Deutsch](#deutsch)

---

<a name="english"></a>

## 🇬🇧 English

### Welcome

ARIA is an open specification. No single entity owns it.
If you are building agent systems, working on semantic integrity,
or thinking about the future of AI communication infrastructure —
you belong here.

This document explains how to contribute to the ARIA Protocol
through its RFC process.

---

### The ARIA RFC Process

ARIA evolves through **Request for Comments (RFCs)** —
the same mechanism that built the Internet.

```
IDEA → DRAFT RFC → COMMUNITY REVIEW → REVISION → ACCEPTED
```

Anyone can propose an RFC. No permission required.

---

### How to Propose a New RFC

**Step 1: Check existing RFCs**
Make sure your idea is not already covered or in progress.

```
Current RFCs:
  RFC-001  Protocol Stack
  RFC-002  Intent Checksum Algorithm
  RFC-003  Domain Threshold Calibration
  RFC-004  Embedding Model Registry        (planned)
  RFC-005  Quantum-Resistant Trust Layer   (planned)
  RFC-006  Performance Benchmarks          (planned)
```

**Step 2: Open a Discussion**
Before writing a full RFC, open a GitHub Discussion:
- Describe the problem you want to solve
- Explain why existing RFCs do not cover it
- Sketch your proposed approach

**Step 3: Write the RFC**
Use the RFC template below. Submit as a Pull Request.

**Step 4: Community Review**
The community reviews, comments, and proposes changes.
Minimum review period: 14 days.

**Step 5: Acceptance**
RFCs are accepted by consensus — not by vote, not by authority.
If there is no unresolved objection after the review period,
the RFC is merged.

---

### RFC Template

```markdown
# ARIA-RFC-[NUMBER]
## [Title]
### [Subtitle]

\```
Status:    DRAFT
Version:   0.1
Created:   [Date]
Authors:   [Name(s)]
Depends:   ARIA-RFC-[dependencies]
\```

## Abstract
[2-3 sentences: what problem does this solve?]

## 1. Problem Statement
[What exists today, what is missing, why it matters]

## 2. Proposed Solution
[The specification itself]

## 3. Examples
[Concrete examples showing the RFC in practice]

## 4. Relation to Existing RFCs
[How this fits into the existing stack]

## 5. Open Questions
[What is deliberately left for future RFCs]

## Document History
\```
v0.1  [Date]  Initial draft
\```
```

---

### What Makes a Good RFC

```
✓  Solves one specific problem
✓  Does not overlap with existing RFCs
✓  Includes concrete examples
✓  Specifies what is OUT of scope
✓  Leaves hard questions to future RFCs
✓  Is readable by someone unfamiliar with the area

✗  Tries to solve everything at once
✗  Is vague about implementation
✗  Has no examples
✗  Ignores existing RFCs
```

---

### Types of Contributions

**RFC Proposals**
New specifications that extend the ARIA standard.

**RFC Amendments**
Corrections, clarifications, or improvements to existing RFCs.
Submit as Pull Request with clear description of what changed and why.

**Reference Implementations**
Code that implements ARIA specifications.
Must clearly state which RFC version it implements.
Must include tests.

**Issue Reports**
Found an ambiguity, contradiction, or gap in an RFC?
Open an Issue with:
- Which RFC is affected
- The specific section
- What the problem is
- Suggested resolution (optional)

**Translations**
ARIA aims to be a global standard.
Translations of RFCs into other languages are welcome.
Must be clearly marked as translations, not normative documents.

---

### What We Do Not Accept

```
✗  Contributions that make ARIA proprietary
✗  Contributions that introduce single-vendor dependencies
✗  Contributions that weaken Tier 5 CRITICAL_SAFETY thresholds
   without ARIA Foundation approval
✗  Contributions without clear problem statement
✗  RFCs that conflict with core principles (see RFC-001 Section 2)
```

---

### Core Principles — Non-Negotiable

All contributions must respect ARIA's seven core principles:

```
OPEN          No entity owns ARIA.
MINIMAL       ARIA solves only agent communication.
SEMANTIC      Integrity of meaning, not just bytes.
TRANSPARENT   Every decision traceable.
DECENTRALIZED No single point of control.
BACKWARD COMP Runs over existing TCP/IP infrastructure.
AGENT-FIRST   Human remains principal. Agent is primary user.
```

A contribution that violates any of these will not be accepted,
regardless of technical merit.

---

### Code of Conduct

ARIA is a technical project. Discussions should be:

```
✓  Technical and substantive
✓  Respectful of different implementation approaches
✓  Focused on the problem, not the person
✓  Open to being wrong
```

The goal is the best possible protocol for agent communication.
Not credit. Not dominance. The protocol.

---

### Attribution

All accepted contributions are attributed in the RFC document history.
Significant contributions are listed in the RFC author field.

ARIA does not require copyright transfer.
Contributors retain their rights.
Contributions are published under the same open specification license as ARIA.

---

### Questions?

Open a GitHub Discussion.
Tag it `[question]` in the title.

There are no stupid questions about a protocol that did not exist yesterday.

---

<a name="deutsch"></a>

## 🇩🇪 Deutsch

<details>
<summary><strong>🇩🇪 Klicken um die deutsche Version anzuzeigen</strong></summary>

<br>

### Willkommen

ARIA ist eine offene Spezifikation. Niemand besitzt sie.
Wenn du Agenten-Systeme baust, an semantischer Integrität arbeitest
oder über die Zukunft der KI-Kommunikationsinfrastruktur nachdenkst —
gehörst du hierher.

Dieses Dokument erklärt, wie du zum ARIA-Protokoll
durch seinen RFC-Prozess beitragen kannst.

---

### Der ARIA RFC-Prozess

ARIA entwickelt sich durch **Request for Comments (RFCs)** —
denselben Mechanismus, der das Internet aufgebaut hat.

```
IDEE → ENTWURF RFC → COMMUNITY-REVIEW → REVISION → AKZEPTIERT
```

Jeder kann einen RFC vorschlagen. Keine Genehmigung erforderlich.

---

### Wie man einen neuen RFC vorschlägt

**Schritt 1: Bestehende RFCs prüfen**
Stelle sicher, dass deine Idee nicht bereits abgedeckt ist.

```
Aktuelle RFCs:
  RFC-001  Protocol Stack
  RFC-002  Intent Checksum Algorithm
  RFC-003  Domain Threshold Calibration
  RFC-004  Embedding Model Registry        (geplant)
  RFC-005  Quantum-Resistant Trust Layer   (geplant)
  RFC-006  Performance Benchmarks          (geplant)
```

**Schritt 2: Discussion öffnen**
Bevor du einen vollständigen RFC schreibst, öffne eine GitHub Discussion:
- Beschreibe das Problem das du lösen willst
- Erkläre warum bestehende RFCs es nicht abdecken
- Skizziere deinen Ansatz

**Schritt 3: RFC schreiben**
Nutze das RFC-Template. Einreichen als Pull Request.

**Schritt 4: Community-Review**
Die Community reviewt, kommentiert und schlägt Änderungen vor.
Mindest-Review-Zeitraum: 14 Tage.

**Schritt 5: Akzeptierung**
RFCs werden durch Konsens akzeptiert — nicht durch Abstimmung, nicht durch Autorität.
Wenn es nach dem Review-Zeitraum keinen ungelösten Einwand gibt,
wird der RFC gemergt.

---

### Was einen guten RFC ausmacht

```
✓  Löst ein spezifisches Problem
✓  Überschneidet sich nicht mit bestehenden RFCs
✓  Enthält konkrete Beispiele
✓  Spezifiziert was NICHT im Scope ist
✓  Lässt schwierige Fragen zukünftigen RFCs
✓  Ist lesbar für jemanden der den Bereich nicht kennt

✗  Versucht alles auf einmal zu lösen
✗  Vage bei der Implementierung
✗  Keine Beispiele
✗  Ignoriert bestehende RFCs
```

---

### Arten von Beiträgen

**RFC-Vorschläge** — Neue Spezifikationen die den ARIA-Standard erweitern.

**RFC-Änderungen** — Korrekturen, Klarstellungen oder Verbesserungen bestehender RFCs.

**Referenzimplementierungen** — Code der ARIA-Spezifikationen implementiert.
Muss klar angeben welche RFC-Version implementiert wird. Muss Tests enthalten.

**Issue-Berichte** — Mehrdeutigkeit, Widerspruch oder Lücke in einem RFC gefunden?
Issue öffnen mit: betroffener RFC, spezifischer Abschnitt, Problem, optionaler Lösungsvorschlag.

**Übersetzungen** — ARIA soll ein globaler Standard werden.
Übersetzungen sind willkommen. Müssen klar als Übersetzungen markiert sein.

---

### Kernprinzipien — Nicht verhandelbar

Alle Beiträge müssen ARIAs sieben Kernprinzipien respektieren:

```
OFFEN          Niemand besitzt ARIA.
MINIMAL        ARIA löst nur Agenten-Kommunikation.
SEMANTISCH     Integrität der Bedeutung, nicht nur Bytes.
TRANSPARENT    Jede Entscheidung nachvollziehbar.
DEZENTRAL      Kein zentraler Kontrollpunkt.
RÜCKWÄRTSKOMP. Läuft über bestehende TCP/IP-Infrastruktur.
AGENT-FIRST    Mensch bleibt Auftraggeber. Agent ist primärer Nutzer.
```

---

### Verhaltenskodex

ARIA ist ein technisches Projekt. Diskussionen sollten sein:

```
✓  Technisch und substanziell
✓  Respektvoll gegenüber verschiedenen Implementierungsansätzen
✓  Fokussiert auf das Problem, nicht die Person
✓  Offen dafür, falsch zu liegen
```

Das Ziel ist das bestmögliche Protokoll für Agenten-Kommunikation.
Nicht Anerkennung. Nicht Dominanz. Das Protokoll.

---

### Fragen?

GitHub Discussion öffnen. Mit `[Frage]` im Titel taggen.

Es gibt keine dummen Fragen über ein Protokoll,
das gestern noch nicht existierte.

</details>

---

<div align="center">

**ARIA Protocol** · IrsanAI · Vatertag 2025
[RFC-001](./ARIA-RFC-001_Protocol_Stack.md) · [RFC-002](./ARIA-RFC-002_Intent_Checksum.md) · [RFC-003](./ARIA-RFC-003_Domain_Thresholds.md) · [Issues](https://github.com/IrsanAI/IrsanAI-ARIA-Protocol/issues) · [Discussions](https://github.com/IrsanAI/IrsanAI-ARIA-Protocol/discussions)

</div>
