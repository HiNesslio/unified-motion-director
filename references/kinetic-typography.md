# Kinetic Typography — semantic text that earns its screen time

Typography is a compositional system, not an effect menu. Choose type hierarchy from the brand, story and screen; **minimal-editorial is only an optional preset**.

## The semantic unit

- Chinese, Japanese and mixed text: group **meaningful phrases** rather than animating each character. Respect punctuation, compounds, numbers + units, proper nouns and UI labels.
- English: group by emphasis and grammatical phrase, not necessarily every word.
- Store intentional groups in the `typography_cues[].groups[]` sequence; automatic heuristics are only an aid and cannot prove semantic accuracy.
- Do not split a numeric value from its unit, a verb from a tightly linked object, or a proper name across different reveals unless the narrative specifically requires it.
- Keep actual Traditional Chinese copy in Unicode. Avoid machine translating user-approved words during implementation.

## Temporal grammar

Each `typography_cues[]` entry can include `enter_sec`, `settle_sec`, `exit_sec`, `groups`, `reveal_style`, `reading_hold_sec`, `font_px`, `layout_ref` and `beat_ref`. Times are absolute seconds within the film and must lie inside the owning scene. Text should not move while the viewer is expected to read it.

Suggest minimum **settled** holds, then verify at target mobile size:
- Short label: >= 0.9 seconds.
- Heading: >= 1.1 seconds + 0.18 seconds per additional semantic unit beyond 3.
- Technical / unfamiliar terms: > 1.5 seconds where needed.
- Final CTA: >= 2.0 seconds when it carries a meaningful action.
These are starting heuristics, not physiological guarantees; a juror must still read the actual render.

## Motion rules

- Masks must not clip glyph ascenders, punctuation or diacritics; test both scripts and fallback fonts.
- Prefer one reveal law per hierarchy level; primary type can arrive on a measured beat, secondary explanatory labels can enter off-beat to preserve reading rhythm.
- 55–100 ms stagger applies to *semantic groups* only where the sentence benefits. Never stagger every Chinese glyph mechanically.
- The transition out must not begin before the settled read hold has elapsed.
- Character width differs across fonts/scripts. Measure with the actual render at target aspect ratio; do not use character counts as geometric bounding boxes.

## Mobile evidence

Use `scripts/mobile_readability.py` on a **renderer-emitted** `layout.json` carrying actual boxes and font size, sampled across meaningful frames. Tool reports font/margin/duration *candidates*, not OCR or aesthetic scores. Missing manifest means **NOT_EVALUATED**, never passed.
