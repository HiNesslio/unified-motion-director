# Howseen deterministic HTML film backend — distilled implementation contract

Source: https://github.com/howseen-ai/claude-motion-design (`skill/motion-design/SKILL.md`, `examples/howseen-launch/render.py`). License: MIT for repository code. This file is a **selective operational synthesis**, not a copied upstream skill. Follow upstream source when actually executing. Upstream may change.

## When to choose

Choose for tightly art-directed, audio-synced, code-only launch films; elaborate shape transformations; precise camera paths; subframe motion blur; or reference analysis with licensed source video. Choose only when Playwright Chromium, FFmpeg and Python packages can be installed/audited. Avoid this backend for complex interactive state or real-time playback requirements unless you implement a separate live-preview driver.

## Contract before writing code

1. `BRIEF.md` specifies one visual thesis, named visual reference, literal copy and source-backed claims, scene duration, safe areas, and rights status.
2. `storyboard.json` is the authored director plan. Generate a **shared named time map** (see `scripts/production_router.py`); replace placeholder beats only after measuring the *actual* licensed song. Never describe illustrative beat times as measured.
3. Make four key stills before final implementation; check hero frame, one transition, UI fidelity, end card at phone size.
4. Build a film page with `window.ready` only after fonts, images, and assets settle. `window.seek(t)` computes all on-screen state from time. Use closed-form motion laws, per-shot registry, explicit layers, seeded random values, and a camera transformation whose zoom interpolates in log space; do not mutate hidden state on sequential calls.
5. Every transition must preserve a reason for the cut or a shared object with a plausible physical handoff. A source-object colour flood must reach the farthest corner before replacing the scene; prevent texture/pop artifacts at the seam.
6. Optional: use `seek(frameIndex)` for frame-locked briefs, but clearly specify the clock and map frames ↔ seconds. Do not mix `seek(t)` seconds and `seek(F)` frames implicitly.

## Render gate: cheap to expensive

- `probe`: multiple decisive timestamps and transition edges; verify characters/icons/colour grade and text before a draft.
- `draft`: 540p/half scale and 1 screenshot per output frame for rhythm. Review contact sheets and a playable proxy **before** master render.
- `master`: 60fps where specified; 180° shutter can be approximated by 4–8 equally spaced **within-shot** subframe samples. Avoid averaging across a hard cut. Upstream's `tmix` is an implementation example, not universal drop-in code for arbitrary shot boundaries. Probe subframe placement at exact cuts.
- `encode`: verify BT.709 range, `yuv420p`, expected frame count, dimensions and audio muxed duration. Prefer measured `ffprobe`/`ffmpeg` rather than assumptions.
- `pops`: consecutive-frame luma difference spikes (>3× neighbours in one upstream example) are **candidates for review**, not necessarily bugs; intentional cuts and flash accents can produce spikes. Inspect strips around each candidate.
- `loop`: compare both position and velocity at loop seam, not only first/last image pixels.
- `freeze`: use `scripts/motion_preflight.py` against **final encoded MP4**, then `review_gate.py prepare`, then two actual jurors.

## Sound + truth

- Measure the actual song's low-band/full-band energy to locate a real drop. A BPM tracker alone can be off by a bar or two. Specify exact hero frame and move song start accordingly.
- Place SFX to align its *audible peak*, not the beginning of its file. For a soft Apple-like piece, a few restrained accents often work better than one SFX per motion.
- When producing loudness-normalized deliverables, measure the **final mux**. -14 LUFS is an example loudness target for social films, not a requirement across all platforms.
- Brand UI can be rebuilt as animation, but keep exact product claims truthful and distinguish illustrative data. When recreating a reference film, require rights to reproduce it; absent rights, extract principles and create different original shots.

## Evidence and limitations

README, upstream skill and `examples/howseen-launch/render.py` were inspected. Source descriptions claim deterministic and beat-synced output; no upstream video was independently played or rendered as part of this integration. No external assets or upstream code are bundled.
