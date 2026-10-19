# Music-to-Picture Choreography — meaningful motion meets sound

**Origin:** original UMD adaptation of production principles studied in [huashu-motion](https://github.com/alchaincyf/huashu-motion) (MIT), not a copy of its composer, score format, samples, audio renderer, `OM.sfx` or CLI. No third-party audio assets are bundled.

## Choose the collaboration mode

- **Licensed-track-first:** analyze the actual approved audio with `scripts/analyze_music.py`. Treat proposed BPM, onsets and energy peaks as candidates until checked by listening. Arrange the storyboard so major reveals fit *musical phrases*, not a metronome.
- **Picture-first score:** write the film's narrative landmarks and target frame times, then brief a composer or a licensed sound engine to create original music around these anchors. This skill does not itself synthesize a soundtrack.
- **Silent or sound-optional:** keep a self-sufficient visual narrative and intentional rests. Never auto-add music against a no-audio brief.

Choose 3–5 main landmarks where appropriate: `hook`, `turn`, `rest`, `hero-reveal`, `resolve`. Secondary data and text need not land on every beat. Separate **picture event** (when the animated effect visibly lands), **sound event** (transient or phrase boundary), and **intentional offset** (anticipation / reaction) in seconds.

## Make sound and action causally related

- An impact or tap is an audible consequence of an actual visual contact, not a decorative sound on every cut.
- A camera acceleration may create anticipation; the impact belongs to the settling or reveal frame, not necessarily the start of the camera movement.
- A hard musical stop can support an essential reading hold. Preserve quiet as an intentional design option.
- Reuse a coherent sonic family across shots. Do not stack unrelated presets on every motion event.
- A soundtrack should never dictate false product actions or claims. Keep the Product Truth Gate upstream.

## Precise storyboard handshake

Store optional `audio.motion_sync_cues` alongside the existing scene `events`:

```json
"motion_sync_cues": [{
  "id": "hero-hit",
  "scene_id": "S02",
  "event_action": "result_land",
  "picture_time_sec": 4.5,
  "audio_anchor_sec": 4.5,
  "intentional_offset_sec": 0,
  "priority": "hero",
  "alignment": "hit",
  "source_status": "illustrative",
  "sfx_ref": "optional-impact-asset"
}]
```

- `scene_id`/`event_action` must identify an existing scene event, and `picture_time_sec` must agree with that event (within half a frame).
- `alignment` is one of `hit`, `anticipate`, `follow`, `free`; `intentional_offset_sec` explains a planned nonzero offset. Positive offset means picture follows audio.
- `source_status: illustrative` or `candidate_unverified` **never** confirms beat synchronization; `measured` requires an actual soundtrack, identified analysis or listening evidence and producer attestation. Even then, the final rendered audiovisual result must be independently checked.
- `priority: hero|primary|secondary` informs attention and tolerance; do not quantize every secondary element.
- The canonical `shared-timeline.json` passes these cues to Remotion or HTML seek(t). No duplicated engine-local cue clocks.

## QA

1. Validate storyboard and generate `scripts/motion_spine.py storyboard.json --out motion-spine.json`; warnings are **planning issues**, not measured defects.
2. Draft render and inspect at normal speed **with audio**; compare important motion landings with **actual** waveform and perceived onsets. Sync needs listening, not just waveform peaks.
3. Re-render sound/visual output after timing changes, then freeze a new SHA-256 for the two independent jurors. Without audible evidence, sound remains `NOT_EVALUATED`.
4. Preserve artist and instrument/track licences; samples labelled free or royalty-free are not automatically sublicensable.

Never impose a specific BPM, number of hits, drop location or genre. The emotional arc decides how busy the soundtrack should be.
