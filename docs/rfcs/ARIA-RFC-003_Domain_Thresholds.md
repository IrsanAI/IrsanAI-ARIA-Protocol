# ARIA-RFC-003
## Domain Threshold Calibration (Draft)

```
Status:    DRAFT
Version:   0.1
Created:   2026-05-15
Depends:   ARIA-RFC-001, ARIA-RFC-002
```

## Abstract
This RFC draft defines how semantic drift thresholds should be calibrated by domain risk profile.

## Motivation
Different domains tolerate different semantic variance:
- Healthcare and finance require tight thresholds.
- Research or ideation workflows may allow broader tolerance.

## Draft Calibration Model
Each ARIA channel/context should map to a threshold profile:
- `strict`
- `balanced`
- `exploratory`

Suggested baseline cosine similarity floors:
- strict: `>= 0.95`
- balanced: `>= 0.90`
- exploratory: `>= 0.82`

## Normative Direction (to be formalized)
Implementations SHOULD:
1. Select a threshold profile before task execution.
2. Log profile selection in accountability metadata.
3. Escalate to semantic retransmit when below profile floor.

Implementations MUST NOT:
1. silently downgrade profile strictness in regulated workflows.

## Open Questions
- Per-atom vs global threshold weighting.
- Adaptive thresholds based on chain depth.
- Human override policy in emergency channels.
