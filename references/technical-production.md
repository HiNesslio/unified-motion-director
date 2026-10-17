# Technical producer: engine choice and reproducible delivery

## Decision router

- **Static storyboard only** → JSON + HTML board, no render dependency.
- **SVG small visual / loop / icon** → native SVG, CSS keyframes or GSAP as appropriate; provide reduced-motion fallback.
- **Complex interactive web UI** → HTML/SVG + GSAP/Canvas; keep user event state separate from off-line seek-based rendering.
- **React/JS video with precise outputs** → Remotion, subject to installed package/version/license.
- **High-end code-directed music-synced film** → upstream Claude Motion Director + HyperFrames when explicitly installed and compatible.
- **Heavy procedural 3D** → Three.js/WebGL or 3D software workflow as available.
- **Deterministic editorial HTML film with controlled motion blur** → howseen-ai `claude-motion-design`: seek(t), Chromium capture, verified beat/drop and selective in-shot shutter integration.
- **React/UI and timeline-synchronized original procedural SFX** → whaleyxbt `claude-motion`: Remotion, named timeline anchors, Python sound cue sheet.
- **Many agents or simulated physics with 3D camera** → whaleyxbt `sims/` frame-stepped web capture; separate from Remotion route.
- **Text-to-video models** → prompts for cinematic plates only when allowed; composite exact text and actual UI in post where possible.

## Canonical file contract

`BRIEF.md`, `LOOK.md`, `storyboard.json`/shotlist, `assets-ledger.md`, `cues.json` (if audio), engine-native source directory, `REVIEW.md`, `out/` with exports.

Source storyboard is authoritative; map its scene ids to engine scene ids. If an upstream tool prefers its own config, write a transform/adaptor rather than claim it natively consumes this JSON. No adaptor is bundled yet to translate storyboard into HyperFrames scene code automatically.

## Render QA

- Lock dimensions, FPS, duration, font loading and stable asset versions.
- Seek selected frames in randomized order and compare repeated renders for determinism.
- Render 3–5 frames around every seam and check semantic continuity and visual pops.
- Check last frame against first only if looping.
- Decode frames from *final encoded file* and inspect, rather than trusting preview/HTML alone.
- Validate requested aspect-ratio variants individually for safe areas and cropped text.
- Record versions, commands, input checksum when reproducibility matters.

## External build backends

The optional `external/claude-motion-director` includes its own engine and render scripts. Follow its official documentation; do not transplant our stage names into its commands. Upstream may specify particular Node, FFmpeg, Python and HyperFrames versions, and installed requirements may change. `source_manager.py` clones source only; it does not install or execute code.


## Hype-yolo source-assisted renderer (optional)

When a shot needs a character rig, particular material synthesis, real vehicle/animal action, sculpted object, print composite or illustrative world, read `source-assisted-production.md` and route to Hype-yolo's source cases **after audit**. This is not the same as generating code from adjectives. Keep the film-level art direction and soundtrack storyboard here; use the upstream seek-deterministic Canvas/WebGL/Playwright/FFmpeg stack for the relevant build. Require a real representative-shot test before attempting the full cut.

## v1.5 bridge utilities

After validating storyboard, use `scripts/production_router.py` to export shared named timing and an **advisory** backend choice. This is a production-plan bridge, not generated working source code. Keep the engine-native implementation as source-of-truth for pixels only; never keep divergent time and SFX anchors.

After final encode, run `scripts/motion_preflight.py` to confirm decoded media properties and inspect suspect flash/pop transitions before the independent visual/holistic jury. Machine-generated pop candidates can be intentional scene cuts, so do not automatically reject for a single spike.
