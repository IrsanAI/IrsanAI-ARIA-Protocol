# CONTRIBUTING to ARIA Protocol

Thank you for helping improve the ARIA specification.

## Scope
This repository currently contains draft protocol RFC documents.
Contributions should prioritize:
1. Clarity of normative language (MUST / SHOULD / MAY)
2. Interoperability and testability
3. Backward-compatible evolution of wire semantics

## Contribution Types
- RFC wording improvements
- New RFC drafts in the ARIA series
- Consistency fixes across README and RFC docs
- Reference implementation proposals (clearly marked as non-normative)

## RFC Authoring Rules
- Use concise section numbering.
- Explicitly separate:
  - Normative requirements
  - Informative examples
- When introducing new fields, define:
  - datatype
  - allowed range
  - failure behavior

## Pull Request Checklist
- [ ] Changes are internally consistent across related docs.
- [ ] Terminology is aligned with RFC-001 and RFC-002.
- [ ] New claims are justified with rationale.
- [ ] Breaking semantic changes are flagged clearly.

## Governance (Current Draft Stage)
Until formal foundation governance is established, maintainers review by:
- conceptual coherence,
- interoperability impact,
- implementation feasibility.

## Code of Collaboration
- Be constructive and precise.
- Critique text, not people.
- Prefer concrete alternatives when suggesting changes.
