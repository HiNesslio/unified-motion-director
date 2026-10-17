# whaleyxbt Claude Motion — taste, review, sound and simulation routes

Sources: https://github.com/whaleyxbt/claude-motion (`AGENTS.md`, `.claude/skills/{motion-design,review-loop,sound-design,web-sims}/SKILL.md`, `sims/README.md`, `package.json`). MIT code; Remotion and media licenses separate. Use as an optional backend and cite its upstream source. Do not transplant its generated output/media into this skill.

## Route by production problem

- **Remotion/React video** when a scene is composed from UI components, typographic beats and reusable branded layouts. Use the actual upstream `src/`, `timeline.json`, Remotion composition registry and CLI commands after installing dependencies.
- **Web simulations** when a video is driven by hundreds of agents, particles, complex choreography, or a spatial object that needs a three.js fly-through. Use an offline-bundled HTML scene with pure `render(t)` and `sims/capture.mjs`. Pre-simulate physics once into arrays, interpolate on arbitrary seek; no frame-to-frame implicit state.
- **Sound-only integration** when a custom film needs original, procedural non-voice SFX but is otherwise built in another engine. Use upstream `sfx/` as optional executable code, not as a descriptive promise; `sfx/cues/<name>.py` reads the **same scene event times** as picture.

## Taste numbers: defaults, not laws

| Cue | Suggested start point | Verify |
|---|---|---|
| Arrive / entrance | cubic Bezier `(0.16,1,0.3,1)` | no slow, floaty arrival |
| Exit | `(0.6,0,0.9,0.35)`, often half an entrance duration | no lingering ghost at seams |
| State-to-state UI | `(0.65,0,0.35,1)` | form continuity and text sharpness |
| Word stagger | ~0.09 s | readable at phone width |
| UI item stagger | ~0.2–0.25 s | not one pop per beat unless intentional |
| General UI spring | damping 14 / stiffness 140 / mass 0.8 | no overshoot for serious data |
| Short phrase hold | ≥1 s after settling | actual audience reading test |
| End statement | ≥2 s when legibility requires | don't speed up to fit music |

Set fonts from the **real brand**; avoid cargo-culting the repo demo's Instrument Serif + coral. Make one focal point per frame, one purposeful accent, one hero moment. Default to muted-first comprehension. At 360px wide the key message must still read. These values are starting points from one published example, **not** Opus 5.5 universal constants.

## Shared timeline contract

Use named anchors (`s1.title`, `s1.exit`, `s2.start`) in a project-owned timeline JSON. No hardcoded audio/video time duplicated across components. Editor updates to named anchors should update the SFX cue sheet and every review sampling point. `scripts/production_router.py` exports a minimum adapter from this Skill's storyboard JSON to an engine-neutral `shared-timeline.json`; **manual mapping into Remotion and source scripts is required**.

## Review loop must happen before final jurors

1. Render a low-resolution playable draft.
2. Contact sheets at each timeline beat **after the change settles**, not just uniform 1 fps. Add 0.1–0.2-second transition strips around suspicious cuts.
3. Judge scene focal point, edge safety, clipping, moving text, readable holds, logo/source fidelity and frame-zero social thumbnail; never confuse self-critique with independent juror scoring.
4. Repair, re-render, and check **the repaired media**, then create master.
5. Waveform/audio pass: transient peaks should sit on planned cue markers; measure integrated LUFS and true peak of final encoded file. If audio can't be heard or checked, flag `not_evaluated` for holistic juror and hold as required.
6. Freeze checksum and dispatch both independent Codex jurors only after preflight. The production agent has no right to supply their subjective ratings.

## Procedural audio

- `sfx/synth.py`: sound generators (click, pop, whoosh, typing, impact, pad etc.).
- `sfx/mix.py` + `sfx/loudness.py`: event placement and loudness processing.
- `sfx/cues/<film>.py`: executable score that imports event anchors. Example uses -14 LUFS, true peak target ≤ -2 dBFS; not guaranteed when material is too transient.
- Audio aesthetic: hits accent meaning, not every motion; maintain single musical key for tonal sounds, pan to screen position when appropriate.
- Do not label generated SFX as licensed recorded sounds or vice versa.

## Web sim checklist

- Trigger if simulation, not simply because a 3D visual is requested. One object fly-through may also work with deterministic Three.js in Howseen engine.
- Bootstrap runtime, precompute any stateful motion at load, `render(t)` pure and arbitrarily seekable, `window.SIM.ready` for capture.
- Frame 0 must be usable as a social preview; chapter transitions follow named times. Prevent bloom from erasing detail and protect text labels from occlusion.
- Build/probe/capture with **commands from installed upstream `sims/README.md`**, not invented CLI arguments. Example commands (current inspected docs):
  - `node sims/build.mjs engine`
  - `node sims/capture.mjs engine --stills 0,4,8,12,16,20 --cols 3 --out out/sims/engine-review.png`
  - `node sims/capture.mjs engine --size 1080x1350 --out out/sims/engine.mp4`
- Test arbitrary seek order, on-screen temporal stability, audio timing, decode and final aspect ratio.

## Licensing / truth

Whaley repo is MIT, Remotion has separate licensing terms depending on use, and upstream included fonts/material or user-selected tracks require separate evaluation. Example simulations use fictional persons and domains; avoid pretending demo data is real. No upstream runtime code or outputs are bundled here.
