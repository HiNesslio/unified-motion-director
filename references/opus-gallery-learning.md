# Opus 5.5 public gallery study — evidence-calibrated directing

Date reviewed: 2026-10-17. Research source: public descriptions, prompts, public landing pages, and selected static poster frames at [Prompt Motion](https://prompt-motion.com/) and [Skillry Opus 5.5](https://skillry.dev/ai-videos/opus-5-5). In this review, **embedded source/remake animations were NOT played or decoded frame-by-frame**. Do not call these case notes a video review. The skills below are *reproducible production inferences* from published creator instructions, not access to Opus 5.5's hidden thought processes.

## Evidence ladder (mandatory in research-based claims)

- `PUBLISHED_PROMPT`: creator-supplied text specifies desired choreography. Proof of intended direction, **not proof achieved visual quality**.
- `STATIC_FRAME`: actual gallery poster/image. Supports only composition/typography/colour of that frame; cannot establish speed, seamless transitions, beat alignment or smoothness.
- `SITE_METADATA`: runtime category, stack, counts or original/remake availability. Does not prove frame fidelity.
- `DECODED_VIDEO`: local video inspected at defined timestamps via ffmpeg. Required for visual claims about movement, cuts, legibility and pace.
- `SOUND_VERIFIED`: audio waveform or playback analyzed. Required for real beat/sync/sound design claims.
- `ORIGINAL_REMAKE_COMPARE`: matched local clips inspected by corresponding normalized timestamps and differences explicitly documented. Do not conflate original and recreation.

When direct video access is unavailable, report that limitation and label conclusions **prompt-derived hypotheses**. Invite users to provide downloadable original/remake MP4s for actual film analysis. A screenshot/poster cannot establish motion.

## Director's synthesis: 8 decision mechanisms

1. **Single visual thesis:** A line, dot, photo, icon or camera world is the organizing idea. Ask what transforms rather than which effects can be added. Product films can use editorial cuts if conceptually motivated; never mandate seamless morphing across unrelated work.
2. **Transition seam is a first-class object:** For each scene change record outgoing/incoming geometry, position, velocity, scale, shape, depth and semantic continuity. Use object-to-object morph, occlusion, screen-filling wipe, motivated match-cut or deliberately contrasting cut; generic crossfade is the fallback, not the default.
3. **One convincing actor:** For UI, cursor direct manipulation should cause believable consequences; drag value follows pointer while held, release applies spring only after release. UI controls must remain brand/product-accurate.
4. **Camera as an editorial sentence:** One dominant camera intention per move; smooth push/pull/pan with purposeful pace. Camera's scale changes propagate consistently to scene, cursor and overlays. For 3D, use physically grounded material and light decisions, not endless orbit.
5. **Controlled physicality:** Closed-form springs and inertia, sparing overshoot. Use shape-specific mechanics (leading/trailing edges when an indicator stretches); different elements should not use the same generic spring by default.
6. **Beat-informed, never beat-enslaved:** Align major reveals and key physical impacts with measured audio beats. Preserve legibility and allow rests. Distinguish manually sketched tempo from waveform-verified cue sheets.
7. **Purposeful subtraction:** Common generic AI tells are decorative particles, gratuitous glow, frame-corner micro-labels, unmotivated HUDs, indiscriminate crossfades, rubbery bounce, invented UI and too much copy. They are anti-patterns unless the concept justifies them.
8. **Frame discipline:** Build deterministic seekable time; inspect keyframes, beat frames, text handoffs, transitions and first/last frame of loops. Detect pops/speed discontinuity on real decoded video; do not treat prompt promises as accomplished QA.

## Technique recipes derived from recurring PUBLIC descriptions

- **Continuous UI morph:** Shared-container identity → geometric interpolation → masked content replacement with non-overlapping exits/entries → cursor-mediated state changes → closure into initial frame for loops. Reference [@twoclipping](https://prompt-motion.com/twoclipping-5cba86).
- **Editorial product reveal:** product truth and authentic assets → one message per beat/shot → hero feature proof → palette-consistent handoff → high-information shot followed by selective quiet → brand resolution. Reference [@jhylee95](https://prompt-motion.com/jhylee95-e1152f) and [@LexnLin](https://prompt-motion.com/lexnlin-6161a6).
- **Slow single-world camera:** One spatial world, no hard cuts if continuous camera is concept; camera pushes/pans 1.5–3 seconds in the specific reference, not a global constant; preserve spatial continuity and cursor scale. Reference [@jake11moran](https://skillry.dev/ai-videos/opus-5-5/jake11moran-414633).
- **Physical 3D hero:** Design final signature shot FIRST → compose prior shots as path to it → one named camera movement per shot → key/fill/rim + environment map + realistic roughness → inspect shadow artifacts, camera clipping, jitter, aliased edges. Reference [Prompt Motion 3D template](https://prompt-motion.com/templates/realtime).
- **Kinetic type as edit:** Change hierarchy/meaning, not simply animate glyphs; preserve reading duration and intentional cadence. Reference [showreel template](https://prompt-motion.com/templates/showreel) and [@LexnLin editorial ad](https://prompt-motion.com/lexnlin-038035).
- **Look/feel with restraint:** Use title hierarchy and negative space, not generic panel templates; track intended emotion per beat, including calm. Gallery commentary explicitly warns against mistaking visual density for authorship: [AI-looking tells](https://prompt-motion.com/blog/make-ai-motion-graphics-look-less-ai).

## Original vs remake — evaluation protocol

Skillry advertises an original and a remake made from the shared prompt. The **replication gap** is evidence that the prompt alone is not the film. When local source media becomes available:

1. Record creator/URL, duration, aspect, frame rate, codec, audio status; preserve origin/rights.
2. Extract both clips to comparable contact sheets via `scripts/video_reference_sheet.py ORIGINAL.mp4 --out <dir>` and for the remake. Sample boundaries at 0, 25, 50, 75, end and around visible cut/impact candidates. Align by *narrative beats*, not raw frame numbers when timings differ.
3. Create a two-column comparison: typography fidelity, shot framing, spatial continuity, start/end poses, shape identity, curve/overshoot, camera intent, actual sound hit, use of original assets and loop seam.
4. Record **observations**, **evidence timestamps**, **underlying cause hypothesis** and **skill rule to change**. Failures in visual quality should revise direction/review gate, not just add longer prompt text.
5. Do not write "watched" unless decoded video was actually viewed; do not claim beat accuracy without audio check.

## Director loop integrated into the master Skill

`RESEARCH (public reference + evidence) → THESIS (one visual idea) → LOOK (hierarchy & omissions) → STORYBOARD (timecoded, frame-described, seam ledger) → ANIMATIC (tempo & camera blocking) → REALIZE (appropriate backend) → BLIND REVIEW (actual frames) → ON-BRIEF REVIEW (claims/assets) → FIX & RE-RENDER`.

### Minimum approval gate before render

Show: one-sentence thesis, 4-8 timecoded shots, a 4–6 frame contact sheet/rough stills, exact audio provenance or silence, and the two most risky transitions. If only still descriptions exist, call them **planned frames**, not rendered keyframes.

## References and rights

- [Prompt Motion gallery](https://prompt-motion.com/) and [original prompt study (October 10)](https://prompt-motion.com/blog/ai-motion-graphics-prompts)
- [Skillry Opus 5.5 gallery](https://skillry.dev/ai-videos/opus-5-5)
- [Source-specific casebook](opus-casebook.md)

Metadata counts change over time. Original images, clips, prompts and branded UI belong to their respective parties. This research file is new guidance, not a republished corpus.
