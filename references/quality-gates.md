# Quality gates: film first, prompt second

## Four-stage review (plus independent final acceptance)

**Gate A — brief + direction:** verified claims, actual assets, original thesis, audience fit, exclusion list.
**Gate B — storyboard + look:** every scene has purpose; focal hierarchy; camera intention; handoffs and accessibility.
**Gate C — motion previews:** image balance; text legibility; credible physics; timing; cut motivation; no flash/pop error.
**Gate D — final rendered deliverables:** verify encoded frames, audio rights/sync, formats, loop (when applicable), and source packaging. **Mandatory after render:** freeze media and invoke two isolated jurors via `references/independent-acceptance.md`, then use `scripts/review_gate.py aggregate` for evidence-gated acceptance. Earlier planning self-reviews are NOT post-render jury acceptance.

## Optional in-progress editorial rubric (1–5; NOT release acceptance)

- Narrative clarity (what changes and why)
- Art direction (recognizable visual identity; not generic)
- Typography/readability (phone-scale, multilingual)
- Visual hierarchy (one clear focus per shot)
- Motion intent/physics (causal, non-distracting)
- Continuity/camera language (spatial and semantic seams)
- Rhythm/sound sync (when audio exists)
- Product truth/source fidelity (no invented UI/data)
- Technical execution (no pop, clipping, font glitch, jitter)
- Format adaptation (safe cropping and resolution)

For preview-stage iteration only: critical truth, unsafe licensing or major clipping **blocks release** regardless of average. These informal 1–5 notes DO NOT count as final acceptance. For the final film, use two independent reviewers with the published 0–100 formula in `references/independent-acceptance.md`. Prefer fixing three highest-impact issues each pass.

## Mechanical checks

Run `python3 scripts/validate_storyboard.py storyboard.json`; separately perform checks that require renderer/media files, e.g. `ffprobe`, decoded-frame sheets, full-range frame differences, audio waveform and phone preview. This skill includes **actual video evidence preparation** (ffprobe + decoded frames) and deterministic jury scoring. It does not bundle an audio/MP4 rendering engine, and cannot independently hear music or summon agents when its host lacks agent tools. Don't claim these checks ran when they didn't.

## Anti-template questions

- Is the first image a generic floating logo/gradient?
- Is every cut a fade or every motion identical ease-out?
- Do any shots add no information?
- Is the product's real UI replaced by an imaginary style panel?
- Is any on-screen value claimed as real without verification?
- Has the most memorable movement been given enough quiet space?
- Does the film resemble source examples too closely instead of adapting their grammar?

## Review report

Document `observed evidence`, `severity`, `timecode/scene`, `revision`, `verified after fix`, and `unknown/unrun checks`. Include at least one reason for the creative decisions that remained unchanged.
