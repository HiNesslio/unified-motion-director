# Cinematic Continuity — one evolving film, not independent animated cards

**Origin:** editorial lessons studied from [OneTake](https://github.com/feitangyuan/onetake), independently expressed for UMD. The upstream code and templates are **PolyForm Noncommercial 1.0.0** and are not bundled or relicensed. These are film-directing principles, not a port of `lib/motion.js`, `probe.py`, camera code or prescribed thresholds.

## Direct the connective tissue

Write the explanation and focal subject of the whole film before scene-by-scene effects. Every section boundary makes one of four choices:

1. **Carry:** a stable, recognizable subject persists and changes job across the seam. The viewer's attention follows an object, hand, shape or label. The same entity should remain traceable, not just match in colour.
2. **Anchor:** one object remains fixed while the world or camera reveals a new context. This can be more comprehensible than an elaborate morph.
3. **Motivated cut:** a clean editorial break advances meaning, point of view or time. State why a cut is better than continuity. Hard cuts are not defects.
4. **Rhythmic montage hit:** rapid, intentionally disconnected images gain a shared musical, geometric or thematic spine. Reserve it for planned accelerations, not as a substitute for a story.

A quiet end card can legitimately resolve with no carrier. Never force a fake shared element to satisfy a metric. A continuous one-take may have no conventional scene boundaries; judge tracking and comprehension at intermediate times instead.

## Camera as an attentive operator

- **Anticipate:** frame where the subject *will land*, not merely where it is now. Use intended screen-space destination and a controlled arrival.
- **Follow:** allow a small, deliberate lag when the story calls for observation rather than a snap. No perpetual floating camera on readability holds.
- **Settle:** stop the camera as information becomes legible. A real hold should be still unless slow motion carries meaning.
- **Preserve focus:** preflight the entering and exiting anchor at every large zoom, cut and change of direction. Check full-frame crops at each supported aspect ratio.
- **Scale carefully:** for deep zooms, express the focal target in normalized screen coordinates and compute the camera path in the chosen renderer. Never copy another project's camera implementation to achieve it.

Describe the `continuity_plan` on the **outgoing** scene, while the receiving scene records what it inherits. For example (generic subject only):

```json
"continuity_plan": {
  "mode": "carry",
  "carrier_id": "selection-ring",
  "handoff_target": "next-scene.detail-heading",
  "camera_behavior": "anticipate-then-settle",
  "reason": "A selected value becomes the next scene's focal heading"
}
```

For an intentional cut use `mode: motivated_cut`, leave out `carrier_id`, and explain the semantic cut in `reason`.

## Tests and limitations

- **Storyboard check:** list seam strategy, stable carrier identity, receiving visual anchor, camera behaviour, and exceptions. `scripts/motion_spine.py` audits whether this intent is documented; it cannot prove pixels really carry across cuts.
- **Draft check:** render at low resolution first; inspect `t−2 frames`, `t−1 frame`, `t`, `t+1 frame`, `t+2 frames` for seams, lost objects, subject jumps, text occlusion and overactive camera.
- **Motion check:** review video at normal speed. Compare perceptual centre of attention over the boundary. Note movement variation and deliberate moments of stillness, but do not force a fixed stillness ratio or uniform carry score.
- **Final gate:** independent jurors inspect the actual frozen MP4, not source metadata. No continuity statistics or planning manifest can replace them.

Reference-derived numeric heuristics (shot variation, carry fractions, velocity) are **observations**, not universal acceptance thresholds. A restrained explainer, dance-like montage and documentary cut will have different valid rhythms.

**Licensing boundary:** Do **not** copy the upstream Noncommercial implementation into this MIT repository; use only original contracts and renderer-neutral planning concepts.
