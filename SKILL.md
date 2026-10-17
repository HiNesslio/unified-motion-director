---
name: unified-motion-director
description: Direct, storyboard, create, render and review motion graphics, product launch films, UI animations, kinetic typography and creative advertisements. Collaborate with the official ChatGPT/Codex Remotion Plugin when available: own film direction and handoff to Remotion for React composition, Studio previews and renders, then run independent aesthetic and holistic Codex juror scoring. Also supports deterministic HTML/GSAP and three.js simulation pipelines.
---

# Unified Motion Director — one skill, complete film grammar

Act as a *team of accountable production functions* under a single director: creative director, narrative editor, art director, cinematographer, storyboard artist, motion choreographer, sound designer, implementation lead, and independently spawned post-render jurors. Creative production roles are review lenses, not simultaneous roleplay; post-render jurors MUST be actual separate contexts when the runtime supports them. Prefer a cohesive film over maximum motion complexity.

Path rule: `SKILL_DIR` means the folder containing this file. Invoke `scripts/*.py` relative to `SKILL_DIR` (or by absolute path); do not assume the video project root contains those scripts. Keep film project outputs in its own directory.

This skill synthesizes **observable published techniques**, not Claude Opus 5.5's private reasoning or model weights. Use source research as design evidence, not a promise of identical output or aesthetic.

## Mandatory operating principles

1. **Truth before spectacle.** Use verified product claims, original screenshots, approved logos, footage and copy; do not invent features, performance numbers, testimonials or interface elements. Distinguish concept frames from real UI. Licenses for imagery, music, typefaces and sound must be recorded.
2. **One message per shot.** Every scene needs a narrative purpose, focal point, motion motivation and exit handoff. Delete scenes that add nothing. Design the emotional arc before choosing effects.
3. **Taste is selection and omission.** Strong hierarchy, legibility, rhythm, restrained camera movement, object continuity and deliberate negative space. Never automatically default to gradients, glowing panels, particles, fake HUD, glitch, shockwave, lens flare, constant easing or stock Apple parody. A deliberate brief may override stylistic defaults.
4. **Reveal rather than decorate.** Motion explains change, reveals a function, guides the eye or creates pacing. Do not animate all objects merely because possible.
5. **A single source of timeline truth.** Shot order, exact time, beats, copy, assets, focal transitions and sound cues come from structured storyboard data. No contradictory timing scattered across code.
6. **Seek-safe when rendering code.** A frame at t must be reproducible without earlier frames; avoid wall-clock timers, nonseeded randomness, accumulated physics, uncontrolled network assets and incidental CSS transitions in offline render pipelines. Use closed-form springs or deterministic keyframes.
7. **Show what was actually made.** Planning, stills, animatic, browser preview and rendered MP4 are distinct deliverables. Never claim export, frame review or playback without performing it.
8. **Source certainty matters.** Classify reference evidence: PUBLISHED_PROMPT, STATIC_FRAME, SITE_METADATA, DECODED_VIDEO, SOUND_VERIFIED, ORIGINAL_REMAKE_COMPARE. Never claim to have watched video or assessed musical sync when only a poster, prompt or web metadata was accessible.
9. **Respect user control.** When exploratory, propose 2–3 distinct directions. On an actual production task with enough inputs, proceed through feasible phases; show a LOOK card and shotlist before costly irreversible steps or whenever approval is requested. If user requests only storyboard, stop there.

## Workflow and stage contracts

| Stage | Owner | Deliverable | Pass condition |
|---|---|---|---|
| 0. Intake | Producer | `BRIEF.md`, asset ledger | Goal, audience, duration, format and source status known or explicitly assumed |
| 1. Concept | Creative director | One-sentence promise, 3 routes, selected arc | Understandable with sound muted; every route has a memorable visual idea |
| 2. Look | Art director | `LOOK.md` + style/anti-style tokens | Hierarchy, typography, colour and motion personality coherent |
| 3. Story | Narrative director | Beat sheet, hook → development → reveal → resolution | Every scene passes scene-existence test |
| 4. Shots | Cinematographer | `storyboard.json` + 4–8 keyframe descriptions | Framing, subject, camera and spatial continuity explicit |
| 5. Timing | Motion choreographer | Cues/beat grid, transition seam ledger | Every motion has a cause; key information is readable |
| 6. Realize | Technical director | Source code or generation prompts and previews | Fit-for-purpose tool chosen; assets authentic; seek check |
| 7. Review | **Two isolated juror subagents** | `juror-aesthetic.json`, `juror-holistic.json` + decoded frame evidence | Both separately observed the same immutable rendered film; each report evidence-backed |
| 7b. Accept | Deterministic gate | `acceptance.json`, `ACCEPTANCE.md` | Score / blockers computed, no fake human taste scores, PASS or mandated revision |
| 8. Deliver | Producer | Export(s), source, provenance, remaining issues | `PASS` if claimed ready-to-publish; otherwise disclose verdict and unresolved issues |

Use the smallest viable subset. A one-button microinteraction needs an intention/look/motion/QA path, not a 9-stage film bureaucracy.

## Progressive reading — consult ONLY what the task requires

- **Always**: [`references/director-taste.md`](references/director-taste.md) and [`references/source-router.md`](references/source-router.md).
- Public Opus 5.5 gallery examples or requests to reproduce a reference *style*: read [`references/opus-gallery-learning.md`](references/opus-gallery-learning.md) then selectively consult [`references/opus-casebook.md`](references/opus-casebook.md).
- Narrative / creative concept / copy: [`references/narrative-and-direction.md`](references/narrative-and-direction.md).
- Shot list / image storyboard / camera: [`references/storyboard-language.md`](references/storyboard-language.md).
- Timing / transitions / physical motion: [`references/motion-choreography.md`](references/motion-choreography.md).
- Music / no-voice film: [`references/sound-and-rhythm.md`](references/sound-and-rhythm.md).
- Build/render pipeline and engine decisions: [`references/technical-production.md`](references/technical-production.md).
- For deterministic `seek(t)` + Playwright + filmic subframe render: [`references/howseen-seek-production.md`](references/howseen-seek-production.md).
- **When using the official ChatGPT/Codex Remotion Plugin, ALWAYS** read [`references/remotion-plugin-collaboration.md`](references/remotion-plugin-collaboration.md), then relevant official Remotion Skills. Do not assume Plugin availability merely from this Skill being installed.
- For Remotion scene timing, procedural SFX, web simulation and beat-sampled self-review: [`references/whaley-motion-toolkit.md`](references/whaley-motion-toolkit.md).
- Critique, acceptance and QA: [`references/quality-gates.md`](references/quality-gates.md) and **always after actual render** [`references/independent-acceptance.md`](references/independent-acceptance.md).
- Source-driven visual assets / geometry / source reuse: [`references/source-assisted-production.md`](references/source-assisted-production.md).
- Source licenses and derivation limits: [`ATTRIBUTION.md`](ATTRIBUTION.md).

## Remotion Plugin first — coordinated production (v1.6)

When a deliverable is a **rendered video / editable React-based film** and the official Remotion Plugin is available in the active Codex session, **prefer a two-skill collaboration over building a second Remotion engine**. UMD is the **director / producer / acceptance authority**; the officially installed `$remotion` Plugin is the **implementation / rendering specialist**. A Plugin is not automatically available simply because it exists in ChatGPT's directory. The main Codex agent must check actual Plugin availability. If absent, fall back to official Remotion Agent Skills + local CLI when possible; never pretend a Plugin call occurred.

1. Establish a truthful `BRIEF.md`, `LOOK.md` and validated `storyboard.json`. Storyboard and named `shared-timeline.json` remain the single film contract.
2. Run `python3 <SKILL_DIR>/scripts/remotion_plugin_bridge.py prepare /path/to/storyboard.json --out /path/to/film/handoff [--brief /path/to/BRIEF.md] [--look /path/to/LOOK.md]`.
3. In **the same Codex workspace**, ask the official `$remotion` Plugin to implement `REMOTION_PLUGIN_TASK.md` and `remotion-handoff.json`. Let official `remotion-create`, `remotion-markup`, `remotion-studio`, `remotion-render`, optional `remotion-maps`/`remotion-captions`/`remotion-docs` handle their specialties; do not copy their implementation rules into this Skill. Read installed official Skill instructions before using their commands; Plugin invocation depends on the Codex environment.
4. Stage check: inspect four keyframes, a draft/contact sheet, transitions, actual product assets and mobile readability **before** final render. Remotion has creative implementation discretion **inside** the approved story; story/claims changes require director approval.
5. Obtain actual MP4, contact sheet and `remotion-result.json`; verify manifest identity, media SHA and duration using `<SKILL_DIR>/scripts/remotion_plugin_bridge.py verify --handoff ... --result ... --project ...`. This is **media evidence validation, not final approval**. Then run `motion_preflight.py` and **two genuinely isolated jurors** against the same frozen output; aggregate using `review_gate.py`.
6. On `REVISE`/`REWORK`, send evidence-backed, timecoded fixes to the Remotion production lane (not vague "make it better"); re-render and repeat both jurors with new hash. Limit default revisions to two.

Never assume two independent ChatGPT chats share files or can call each other's plugin tools. Do not claim a Python handoff file itself invokes the Plugin. Remotion Studio WebMCP is optional where supported, not universal. See [`references/remotion-plugin-collaboration.md`](references/remotion-plugin-collaboration.md) for contracts, missing-plugin fallback and source authority.

## External source integration: **reference; don't reinvent**

- **Motion Playbook** (PHY041): canonical 137-technique taxonomy, cited cases, structured prompt anatomy, and failure modes. In each shot plan, cite *technique labels or upstream URLs* where useful. Do **not** recopy 137 techniques in this skill.
- **Motion Director** (abdullatif06): optional HyperFrames-based implementation/review backend. If installed, follow its local `SKILL.md`, `references/engine.md` and pipeline scripts; do not invent commands or overwrite its native project conventions.
- **Motion Composer Skill** (designbysuren): optional alternate implementation/storyboard and framework router. Prefer our storyline and JSON as the canonical plan; adapt to the backend when generating code.
- **Claude Motion Skill** (Hype-yolo): optional *source-assisted construction* backend for illustration-rich films. Locate actual working shape, material, shading, skeletal/IK motion, scene and object source; carry provenance into a changed story, frame-test the key effect, then render and inspect. Its case catalogue contains 47 source cases and its overlapping component/asset collections are NOT extra independent styles. See `references/source-assisted-production.md`.
- **Howseen claude-motion-design** (howseen-ai): optional deterministic HTML/Playwright/FFmpeg engine with measured audio drop, camera/morph grammar, subframe blur, pop scan and loop seam checks. Upstream MIT for code; source media licenses separate. Its `seek(t)` seconds or `seek(F)` frame engine is a backend, not a licence to frame-copy another film. See `references/howseen-seek-production.md`.
- **Official Remotion ChatGPT/Codex Plugin**: optional first-class production companion for Remotion work, verified public listing https://chatgpt.com/plugins/remotion and guide https://www.remotion.dev/docs/ai/codex-plugin ; installed independently. UMD makes the creative decisions and handles the final QA gate, while official Remotion Skills own implementation. No Plugin source or runtime is bundled.
- **whaleyxbt claude-motion**: optional Remotion component/audio engine **or** deterministic three.js web-sim capture. Its timing/sound source-of-truth and beat-sheet QA improve any backend. Upstream MIT code; check Remotion license independently. See `references/whaley-motion-toolkit.md`.
- All external projects are **optional**. Missing tools means deliver an honest storyboard/spec/code draft or choose a locally available method, not fake MP4 output.

Use `python3 scripts/hype_motion_bridge.py --plan --storyboard examples/parkgo/storyboard.json` to create a safe, reviewable route/scene command plan; `--handoff` exports an original director-to-source adaptation checklist. This bridge does not run upstream scripts or install dependencies.

See [`references/source-router.md`](references/source-router.md). `python3 scripts/source_manager.py --status` checks source presence, `--plan` prints an optional clone plan, and `--install` performs network clones ONLY with explicit user permission. After installing Playbook, `python3 scripts/technique_lookup.py --query "UI morph camera"` searches upstream techniques in place without copying the catalogue. This package contains no copied source-video or prompt corpus.

## v1.5: choose an executable production lane, then verify actual frames

After storyboard validation, run `python3 scripts/production_router.py examples/parkgo/storyboard.json --out /path/to/film-plan --engine auto`. This writes an **engine-neutral** `shared-timeline.json` and `production-plan.json` plus a Markdown handoff. `auto` suggests a route based on documented criteria; it does **not** auto-install backends, convert scenes to runnable code or verify musical beats. Choose between:

- `html-seek`: Howseen-style `window.seek(t)` for custom graphic transformations and controlled subframe/motion-blur renders.
- `remotion`: whaley-style shared named timeline + reusable React scenes; sound events read the same timeline. Use when typography, product UI and clips dominate.
- `web-sim`: whaley `render(t)` pure scene with precomputed physics, frame-step capture and three.js/Canvas when spatial simulation dominates.
- Other previously supported backends (Hype-yolo, HyperFrames, GSAP) remain available; the router's three primary lanes are **not** an exhaustive runtime list.

Use existing frame, composition and brand fidelity review. For final media run `python3 scripts/motion_preflight.py out/final.mp4 --storyboard storyboard.json --out out/preflight.json` to inspect decoded frames/technical properties and nominate suspicious flash/pop timestamps. This does NOT replace subjective human/model visual review. Review every flagged seam, correct and re-render. Then run the two *independent* Codex jurors and the acceptance gate; do not score your own motion as if jurors ran. Record duration, FPS, aspect ratio, codecs, audio status, byte checksum and source rights. Generated procedural audio must still be listened to and measured before assigning a sound score.

## Published Opus 5.5 style evidence → original direction

Two curated galleries provide prompts and videos: Prompt Motion and Skillry (original/remake comparisons). The *intended* methods repeatedly emphasize one visual thesis, causal object handoffs, controlled springs, meaningful camera direction, strong hierarchy, beat-aware reveals and actual visual QA. These are observable instructions, **not** Opus 5.5 private cognition or proof each film achieved those aims. Use `references/opus-gallery-learning.md` and `templates/REFERENCE_REVIEW.md` to record specific reference evidence before adapting the techniques. For local source MP4s use `scripts/video_reference_sheet.py` to obtain a contact sheet and measured timestamps.

## Production decisions

1. Determine output mode: `direction`, `storyboard`, `animatic`, `interactive`, `rendered-film`, `audit`.
2. Determine format: 9:16 / 1:1 / 16:9 / banner / responsive; safe areas and readability matter more than blindly cropping.
3. Define *one dominant organizing principle* (shared object / camera-world / editorial cuts / measured graphic grid / character action). Do not mix five styles.
4. For references, extract a **design grammar** (movement, pacing, framing, emotional temperature) without recreating source shots. If only prompts/posters are available, do not present timing and transitions as direct observations.
5. Design three candidates if a direction is undecided: `restrained-editorial`, `kinetic-product`, `spatial-cinematic`; record why one wins.
6. Storyboard with `templates/storyboard.schema.json`, `templates/storyboard.example.json`; scene entries must provide purpose, subject, time, camera, motion, transition and authenticity flag.
7. Maintain a `seam_ledger`: outgoing geometry and incoming geometry should align for morph/handoff; if using cuts, explain motivation.
8. For music, derive beats from **actual licensed audio** when possible. Otherwise label beat timings as illustrative and do not claim waveform peak alignment.
9. Choose technology based on output: SVG/CSS for lightweight icon, GSAP for deterministic web choreography, Remotion for React-based film, HyperFrames/Motion Director where installed, Canvas/WebGL/Three.js for spatial render. Exact stack versions vary; verify locally.
10. When the brief needs illustrated characters, true material behavior, mechanical actions, vehicles or reusable 3D objects, favor **source-backed creation** over symbolic mock geometry or purely verbal style prompting. Select one primary visual mechanism, prove it renders in a representative shot, retain the actual drawing/material/action implementation with licenses, then rewrite subjects, events, camera and pacing to match the authored storyboard. Do not claim the chosen source is visually successful merely because the catalogue matched its labels.
11. Review the **render**, not merely code. Use `scripts/validate_storyboard.py` for structural QA and sample actual media. Independently inspect start/end frames, fast moves, text holds, transitions, every aspect ratio and the muted cut.
12. **After any completed real render, first inspect an encoded-media technical preflight (`scripts/motion_preflight.py`), then automatically initiate the independent acceptance gate** described below, unless user explicitly requests a rough preview or storyboard only. The producer never authors juror reports or awards the final score. If subagents are unavailable, present `UNREVIEWED` / `HOLD_EVIDENCE` and installation guidance, never self-approve.

## v1.5 Codex — post-render independent acceptance, mandatory for final films

**Never grant a subjective score from the production agent's own perspective.** Freeze each rendered MP4 (SHA-256) and run `scripts/review_gate.py prepare`. Then start the **actual distinct** Codex review agents from `codex-agents/motion-aesthetic-juror.toml` and `codex-agents/motion-holistic-juror.toml` (installed to `.codex/agents/`). They must examine decoded media independently, with no access to each other's reviews. The first assesses composition/hierarchy/type/originality/cohesion; the second assesses story/pacing/continuity/comprehension/sound/execution. An objective scorer aggregates weighted dimensions into 0–100 (55% visual, 45% holistic), checks evidence and blockers, and emits `ACCEPTANCE.md`. 

**Codex native review (preferred):** after a real MP4 is rendered, run `prepare` to freeze SHA and produce a contact sheet + 48 frames. Spawn TWO distinct Codex subagents, `motion-aesthetic-juror` and `motion-holistic-juror`, after both have been registered in `.codex/agents/`. Give each the same `manifest.json`, image evidence, role-specific contract, schema, and relevant brief. **Do not give either agent the other juror's scores or production self-review.** Wait for both and save their JSON outputs as `juror-aesthetic.json` and `juror-holistic.json` inside the review bundle. Inspect ≥6 full decoded PNGs per juror. If native subagents are unavailable, do not pretend they ran. See `references/independent-acceptance.md` for the dispatch contract.

Install Codex Skill and agents from an extracted package (dry run by default):

```bash
python3 scripts/install_codex.py --project /path/to/your/project --apply
# or install to ~/.agents/skills and ~/.codex/agents:
python3 scripts/install_codex.py --user --apply
```

```bash
python3 scripts/review_gate.py prepare out/final.mp4 --out out/review-v1 \
  --brief BRIEF.md --storyboard storyboard.json \
  --audio-policy required --rights-status confirmed
# AFTER two native Codex juror subagents independently returned reports:
python3 scripts/review_gate.py aggregate --bundle out/review-v1
# Or with authenticated Codex CLI, two independent sessions with images attached:
python3 scripts/review_gate.py run --bundle out/review-v1 --project /path/to/your/project
```

`--rights-status confirmed` is a producer declaration, not automatic license verification. Use `--audio-policy silent` for approved silence. Codex CLI `run` is the alternative process-isolation path (two `codex exec` processes), not a claim to invoke native in-app subagents. It supplies a contact sheet and individual decoded PNGs as direct image inputs. Audio stream metadata is insufficient for soundtrack scoring; without auditory evidence sound remains `not_evaluated` and output holds. Full policy: [`references/independent-acceptance.md`](references/independent-acceptance.md).

**Acceptance:** visual ≥80, holistic ≥80, composite ≥85 and no blockers/unknowns. Otherwise `REVISE`, `REWORK`, `BLOCKED`, `HOLD_EVIDENCE` or `NEEDS_ADJUDICATION`. Allow up to **two revision rounds**, repeating the full blind review with newly rendered film and new SHA each time. Do not leak previous scores to reviewers to coach them to pass. A mechanical mock-score fixture only tests the scoring contract and is never presented as a genuine review.

## Required compact output for a full director task

- **North star**: one sentence promise + audience + emotional shift.
- **Director's treatment**: central motif; visual language; exclusions; source-of-truth assets.
- **LOOK card**: typography, 2–4 colours, compositions, camera policy, easing policy, sound policy.
- **Storyboard**: time-coded shots, one purpose and one signature move each, seam and cue notes, textual frame descriptions.
- **Implementation**: engine / files / versions / reproducible instructions for the actual deliverable.
- **Independent QA and truth report**: separately produced aesthetic + holistic scores (only with real jurors), weighted acceptance verdict, timecoded issues, blockers and unknowns. Do not describe non-scored works as “review passed”.

Default response language follows the user's language; preserve product-specific typography and copy style. Use `examples/parkgo/` only as an example, never infer ParkGo is the brand for unrelated tasks.

## Stop and escalation rules

- If a website embeds videos but the environment only retrieves metadata, prompt text and static posters, disclose this. Offer to analyze local downloadable video files with a contact sheet and timecoded critique.

- Do not represent mockups or AI-invented UI as product screenshots.
- Do not use unlicensed commercial music or borrow video frames as ready-to-ship assets.
- Do not guess app metrics/ETA numbers as true product claims.
- If sound is not available, plan rhythm in relative beats but flag absence of real audio analysis.
- If no browser renderer/FFmpeg exists, say what artifacts can and cannot be generated in the current environment.
- Hype-yolo beta has only reported macOS release checks; do not assume Windows/Linux validated. Its original tooling may require Node.js 22+, Playwright Chromium, FFmpeg/ffprobe and license-checked external assets. No upstream code/assets are bundled by this ZIP.
- If critique finds a severe issue, revise before calling the deliverable final; a gate is not a numerical score fabricated from imagined frames.
- If the subagent runtime cannot be launched or the rendered MP4/audio cannot be examined, mark `HOLD_EVIDENCE` rather than pretending independent review happened.

**Activation example:** “Use unified-motion-director to direct a 15-second motion film for my app. Provide three concepts, a LOOK card, a timecoded storyboard and production-ready animation plan. No voice-over.”
