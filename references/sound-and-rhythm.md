# Sound and visual rhythm

## Policies

- No supplied audio means no claims about measured BPM, drops or waveform peaks.
- If the user specifies no voiceover, keep on-screen story understandable through visuals/text and track only.
- Use licensed / original audio with provenance. Do not rip commercial songs merely because they are available online.
- A beat grid is **optional** for poetic voice / speech / restrained films; do not quantize every event.

## Cue sheet

Every cue has: `time_sec`, `event`, `asset`, `asset_license`, `sync_point` (transient peak / bar / phrase), `function`, `verified`.

For user-supplied BGM: analyze length, tempo/phrases/drop using available sound tools; set visual payoff near a meaningful musical event, preserving room for anticipation and recovery.

For SFX: align perceived attack/peak rather than file start if tooling supports peak analysis; normalize mix to user/platform standards and listen to the actual render. A −14 LUFS mix is a **published case-study convention**, not a mandatory spec for every platform.

## Silent feed test

Watch without audio. First 1–2 seconds must present a compelling visual subject or tension, main benefit remains intelligible, brand or next action is clear if requested.

## Audio QA

Check length, clipping, silence, license ledger, cue/frame sync and any LUFS requirement. The cue checker must never report pass for a waveform it did not analyze.
