# Source-assisted Motion Production (Hype-yolo integration)

**Purpose:** fill the gap between an attractive storyboard and technically convincing animated objects. The director (this skill) still owns narrative, art direction, timing, product accuracy and acceptance. Hype-yolo owns optional source discovery, example import, source-based drawing/animation and renderer. This integration is **instructions + handoff bridge**, not embedded code, footage or preinstalled upstream renderer.

## Evidence and scope (reviewed 2026-10-17)

- Repo: https://github.com/Hype-yolo/claude-motion-skill ; release README: v0.4.0-beta.1; MIT for original tools, with independent licenses for imported models, assets and third-party code.
- Advertised 47 open-source cases (36 previews, 11 gaps); 5 making systems / 10 development demos; 14 scene entries (including 3 experimental); 30 object/model entries; 20 sourced extensions. These counts **overlap**, and are *not* 116 isolated proven styles.
- Relevant extension examples: anatomy/mechanisms, procedural animals, hand-drawn paper; earlier material/drawing approaches include signal infographics, glass product, watercolor transport, vehicle dynamics, rain city, voxel and geometric architecture. Do not promise all run on the target machine.
- Published installer requirements: Node.js 22+, npm, FFmpeg and ffprobe, Playwright Chromium; upstream said release tests on macOS only. It does not ship every dependency and not every case was rendered individually.

## Route by missing production capability — NOT adjectives

| Problem in the storyboard | Preferred operation | Why |
|---|---|---|
| Detailed subject silhouette, true paper fibers, ink printing, stylized glass | Find a source case, examine actual draw/material modules | Merely describing the look in a prompt does not preserve the mechanism |
| Story naturally matches a complete world e.g. HD-2D miniature / papercut | Find a making system (`--engines` then `create-engine`) | Start from a working multi-layer environment rather than assembling incompatible examples |
| Layout or event structure already fits | `--scenes` then `create-scene` | Adapt the events, not only the labels |
| Only one specialized effect missing | `--extensions` then `create-extension` | Reuse the exact material/action component in a coherent style |
| Credible full animal, vehicle, product model needed | `--models` then `create-model` | Inspect topology, legal use, rig/actions; a static GLB is not an animated character |
| Motion typography, UI transitions, abstract geometry | Existing GSAP/Remotion/Motion Director route | Do not invoke an illustrated case just to insert unrelated texture |

## Source-first agent procedure

1. **Director authored truth.** Freeze the brief, look, storyboard, timing and original asset policy (unless new findings require explicit revision). Include evidence status.
2. **Decompose shots by requirements.** For each shot list recognizable silhouette, materials, rig, real action, occlusion/contact, camera, transitions and needed assets. Identify *one primary visual system across the film*.
3. **Discover actual mechanisms.** With reviewed upstream installed, run `route.mjs --query` against subject+action+material, not just a genre keyword. Inspect up to five matches and scene/engine/extension/model candidates. Query rank is not taste or technical proof.
4. **Show working representative mechanism.** Read source modules and licenses; inspect authentic preview; stage *one* representative shot with the required effect active. Test whether a supposedly reused module really contributes to pixels, not merely imported. If a 3D animal lacks walking contact, add actual foot/body movement or choose a different source.
5. **Adapt the story.** Preserve the licensed relevant shaders, brush/printing operations, figure construction or IK mechanics. Rewrite **subject, relationships, actions, camera, timed events, text and transitions** for the new film. No unchanged demos with swapped titles. Keep contour, scale, palette, lighting, movement grammar coherent when merging objects.
6. **Deterministic rendering.** Use upstream's `scene.js` or page contract; all drawing must depend on absolute t, not prior frames or remote assets. Run its own keyframe export, then 24fps MP4 example command only after dependencies are installed. No audio unless genuinely rendered.
7. **Independent review.** Compare source expression, legibility, shapes, motion, occlusion/contact, coherence, timing and actual decoded output. Frame extraction alone does not prove smooth movement, sound sync or pleasing aesthetic. Revise.
8. **Provenance.** Produce `ADAPTATION.md`: source/project/commit, licenses, copied modules and whether used in render, new work, absent assets, actual QA and limits.

## Native upstream commands (examples, never automatically executed)

```bash
# Run from a reviewed local upstream installation; <skill> is its skills/claude-motion directory.
node <skill>/scripts/route.mjs --query "stylized transit, vehicle motion, paper grain, route progression" --limit 5
node <skill>/scripts/route.mjs --engines
node <skill>/scripts/route.mjs --scenes
node <skill>/scripts/route.mjs --extensions
node <skill>/scripts/route.mjs --models
node <skill>/scripts/prepare-case.mjs --case <id> --out <new-film-folder>
node <skill>/scripts/create-extension.mjs --extension <id> --out <new-film-folder>
node <skill>/scripts/render.mjs --root <new-film-folder> --out <new-film-folder>/film.mp4 --fps 24
```

`prepare-case` requires a verified catalogue ID; `create-*` commands may accept different required flags. Consult upstream SKILL and scripts, not guesses. Upstream reports canvas scene exports `width,height,duration,render(ctx,t)`; page mode has `READY,DUR,render(t),CAPTURE` and optional `audioWav()`. Its own render report verifies image/video technical properties; our reviewer verifies visual quality and content.

## Risk & truth guardrails

- Upstream original tools are MIT, **but** imported GLB, models, fonts, libraries and remotion runtime have their own licenses. Review before redistribution, especially public ads. This ZIP carries none of those assets.
- Read/install upstream from a pinned reviewed commit before execution. `source_manager --install` performs only a shallow clone of current heads, NOT verified or pinned production setup. Do not silently execute remote code or assume benchmark numbers constitute third-party validation.
- A prompt-only derived video is not a source-backed adaptation; the adapter must name and materially execute copied drawing/material/action modules.
- Technical success != pleasing visuals. Upstream itself reports negative feedback for some extensions; do not claim a guaranteed Opus aesthetic or access to hidden model thought.
- If rendering tools/assets are missing, ship a correct source selection plan + handoff, **not** a claimed finished MP4.

## Handoff / traceability

Run `python3 scripts/hype_motion_bridge.py --status`. To review commands without executing upstream, use `--plan --storyboard examples/parkgo/storyboard.json`. To generate traceable production planning JSON, use `--handoff --storyboard examples/parkgo/storyboard.json --output /tmp/parkgo-handoff.json`. Fill in candidate IDs **after** actual routing; never fabricate match results. Use `templates/ADAPTATION.md` at final delivery.
