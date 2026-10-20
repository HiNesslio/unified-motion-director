# Mografy: optional local Canvas production lane (v1.9)

Upstream: https://github.com/zz41354899/mografy · upstream code MIT. Read the **currently installed** `.agents/skills/mografy/SKILL.md` and its scene-authoring reference before executing commands. This Skill does not contain the Mografy runtime, media, source components, fonts or installation scripts.

## When to route here

Choose `mografy` when a film benefits from a **native deterministic Canvas 2D composition**, compact vector/shape animation, text/numeric motion, portrait social graphics, a local scrubbable player, or Chinese/Japanese typography. Keep **Remotion Plugin** the preferred route for React/UI-centric filmmaking and Three.js/web-sim for complex spatial simulation. A film can use multiple engines only with a deliberate interchange/render/compositing plan; the UMD storyboard and product truth still belong to the director.

- Local editing: Mografy compiles and performs a Chromium trial render before updating the player; its preview is not final-media evidence.
- Scene contract: `scenes/main.ts` exports `meta`, `params`, optional `setup(ctx)` and synchronous `renderFrame(ctx, time, params)`. Each pixel must depend on absolute time, prepared assets, and seeded data, not prior frames or wall-clock randomness. `Math.random`, `Date.now`, `performance.now` are invalid inside renderFrame.
- `mografy.json` is configuration (scene path, assets/fonts/params/review settings) **not** a copy of our storyboard or animation keyframes. Map scene IDs and named absolute times from `shared-timeline.json` into source code.
- Native scene aspect is important: portrait should be **authored** at 1080×1920 rather than merely cropping landscape. Review each requested aspect separately.
- Use actual project `style.md` only when present or when the user approved durable style decisions; precedence: current user request → approved project style → defaults. Scene contract and truth requirements always apply.
- `ctx.beat(time)` is available only when Mografy has audio timing. It does **not** automatically turn guessed beats into verified music synchronization.

## Installation and production

Mografy upstream currently requires Node.js >=22.12 and pnpm; its `pnpm install` builds, downloads Chromium and installs the launcher. **Do not install or update third-party code without explicit consent**. If `mografy` is absent, produce a handoff only; do not imply the runtime or player ran.

From the Unified Motion Director directory:

```bash
python3 scripts/production_router.py film/storyboard.json --engine mografy --out film/route
python3 scripts/mografy_bridge.py prepare film/storyboard.json --out film/mografy-handoff
```

These commands produce a **planning contract**, not a runnable Canvas scene or a rendered video. In the audited, installed Mografy workspace, an agent creates a project with `mografy init projects/<film>` (agent-facing), reads its generated manifest and `style.md` if any, implements the director-approved scenes, and then runs:

```bash
mografy dev projects/<film>
mografy check projects/<film>
mografy review projects/<film>
mografy export projects/<film> --format mp4
```

The CLI also advertises WebM / Lottie / SVGA outputs; **only real encoded MP4/WebM** go through UMD's film verification/jury flow. For social portrait film, use `--orientation portrait --resolution 1080p` on export, but do not assume that alone reflows scene geometry. Mografy extras `cinema.ts` (camera/transition) and `cjk.ts` (vertical text, CJK line-break behavior) are *optional*, not installed by the core template; copy only after inspecting source and licenses. Source components (16 examples) are creative references, not production UI/brand evidence. Noto font subsets are OFL-licensed and separate.

## Evidence and acceptance

```bash
python3 scripts/mografy_bridge.py verify \
  --handoff film/mografy-handoff/mografy-handoff.json \
  --video projects/<film>/renders/final.mp4 --out film/mografy-handoff/verified-media.json
python3 scripts/motion_preflight.py projects/<film>/renders/final.mp4 --storyboard film/storyboard.json --out film/preflight.json
python3 scripts/review_gate.py prepare projects/<film>/renders/final.mp4 --out film/review --storyboard film/storyboard.json
```

`verify` confirms an unchanged storyboard SHA and real encoded video metadata (duration, fps, orientation) then hashes the file; it **does not** verify the Mografy render provenance, audio quality, Product Truth, or visual taste. Run upstream `mografy check` and `review`, inspect actual frames at entry/extreme/settle, reading holds and all scene seams, and listen to final audio. UMD's two isolated jurors and its 55/45 SHA-pinned acceptance **remain mandatory** for any release-ready claim. If frames/audio/subagents are not available: `HOLD_EVIDENCE`, not PASS.

Prefer a measured, simple Canvas motion mechanism over a gratuitous effect. Upstream docs are operational references; don't copy their project templates into this MIT repository.
