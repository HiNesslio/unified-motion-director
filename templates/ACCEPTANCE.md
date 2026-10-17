# Acceptance report — Independent dual-juror review

- Candidate video: `...`
- SHA-256: `...`
- Technical evidence: `ffprobe`, timecoded decoded PNGs
- Reviewer independence: two separate agents; no access to one another's scores
- Verdict: `HOLD_EVIDENCE` / `PASS` / `REVISE` / `REWORK` / `BLOCKED` / `NEEDS_ADJUDICATION`

| Independent review | Score | Weight | Observed evidence |
|---|---:|---:|---|
| Visual aesthetic | /100 | 55% | contact sheet + ≥6 decoded frames |
| Holistic film | /100 | 45% | contact sheet + ≥6 decoded frames |
| **Composite** | **/100** | **100%** | calculated by `review_gate.py` |

## Release blockers

## Strongest three revisions

## Unknowns and confidence

## Next step

No pre-filled scores: generated acceptance scores must come from genuinely separate reviewer JSON files, each matching exactly the frozen media SHA.
