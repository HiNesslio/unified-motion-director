# Source router: complementary projects, one editorial owner

## Authority order

1. User goals, assets and explicit restrictions.
2. This skill's creative/QA standards and verified product truth.
3. Engine-specific constraints in the installed upstream project.
4. Research catalogue and examples, used as optional technique suggestions.

If standards conflict, prioritize product truth and explicit user requirements, then engine requirements. Never let an engine preset decide a film's concept.

## Project roles and READ points

### A. PHY041 / claude-motion-playbook (technique research)
- https://github.com/PHY041/claude-motion-playbook
- Read `docs/techniques.md` selectively for camera, handoffs, UI, typography, audio and QA moves.
- Read `docs/prompt-patterns.md` for six-section structured briefs and constraints, not "magic phrases".
- Read `docs/skills.md` to select an existing execution backend when one fits.
- `catalog/` contains linked references; creator videos/prompts remain at their original websites. Don't assume catalog supplies production files.

### B. abdullatif06 / claude-motion-director (default OPTIONAL coded film backend)
- https://github.com/abdullatif06/claude-motion-director
- Read upstream `SKILL.md`, `references/house-rules.md`, `references/engine.md`, `references/motion.md`, `references/sound.md`, `references/workflow.md`, then use existing upstream scripts.
- Use this backend for production when available. HyperFrames and dependencies are not shipped here.

### C. designbysuren / motion-composer-skill (optional cross-media router)
- https://github.com/designbysuren/motion-composer-skill
- Read upstream `SKILL.md` and needed references for Remotion, code animation, cinematic commercials and AI video shot structure.
- Use to complement tool decisions, not replace our canonical brief/storyboard/critical review.

## Integration boundaries

- This is a coordination layer **not** a fork, bundle, brand affiliation or automatic full engine installer.
- Running `source_manager.py --install` only clones or fetches third-party repos when user authorizes it. Installing dependencies and running their code requires separate review/action.
- The upstream implementation code remains licensed by authors; preserve their `LICENSE` files. If distributing a combined package with copied content, re-evaluate terms.
- Motion Playbook writing/classification CC BY 4.0; Playbook's templates CC0. Source videos and full third-party prompts excluded.
- Motion Director MIT; Motion Composer MIT. Dependency-specific licenses (HyperFrames, GSAP, Remotion etc.) must be checked before public/commercial release.

## Example route

User: "Build a 15-s no-voice app film"

1. This Skill decides concept, visual bible, 5–7 shots, authentic footage/UI, shot handoffs, text.
2. Query Playbook for relevant shared-element/mask/camera/audio/QA techniques.
3. Use Motion Director if installed for HyperFrames project scenes, beats and physical rendering, otherwise choose a valid local animation engine.
4. Keep storyboard IDs and timing, adapt to backend project structure explicitly.
5. Review decoded output independently, not because upstream says pass.


## D. Public example galleries — evidence-based design research (NOT runtime engines)
- https://prompt-motion.com/ — original prompts, category tags, selected poster frames, and structured templates. Use `opus-gallery-learning.md` and `opus-casebook.md`.
- https://skillry.dev/ai-videos/opus-5-5 — original/remake comparison pages; actual pairwise visual critique only after both video files have been decoded/viewed.
- These galleries are NOT drop-in code backends and their creators retain rights. Do not scrape or redistribute their audiovisual corpus as part of this package.

## E. Hype-yolo / claude-motion-skill (optional *working source*, not just theory)
- https://github.com/Hype-yolo/claude-motion-skill
- Version reviewed: v0.4.0-beta.1 (2026-10-17); upstream evolves independently.
- Read `skills/claude-motion/SKILL.md`, `references/how-it-works.md`, `references/installation.md`, `references/runtime.md`, then `THIRD_PARTY_NOTICES.md` and the specific catalogue entry before reusing anything.
- Choose this backend for nontrivial shapes, true material shaders, silhouettes, character/animal gait, mechanical actions, papercraft, low-poly objects, rich illustrative or 3D scenes. Do NOT treat all source cases as independently validated or automatically beautiful. 47 cases, 20 components, 30 object entries, 14 scene entry points and 5 systems are *overlapping* classes.
- Handoff bridge: `python3 scripts/hype_motion_bridge.py --plan --storyboard path/to/storyboard.json`; for editable shot-by-shot provenance checklist `--handoff --storyboard ... --output ...`. Commands are printed but not executed by the bridge.
- Upstream actual route: `node <skill>/scripts/route.mjs --query "visual subject + material + action" --limit 5`; after inspecting preview/source/licensing, optionally `prepare-case.mjs`, `create-engine.mjs`, `create-scene.mjs`, `create-extension.mjs`, `create-model.mjs`. Never select by the ranking score alone; never just swap a title or palette.
- Upstream code render contract is seek deterministic (`scene.js` exports width/height/duration/render(ctx,t); page entry alternative). Use its native exporter and environment after audit. Full clip must be decoded and visually reviewed. `ADAPTATION.md` must record actual function/file/asset reuse, rewritten shots, source commit and licenses.
- Prefer **one coherent renderer/art direction per film or scene**. Crossing incompatible independent renderers requires an explicit compositing and color-management plan; otherwise use Hype as the sole illustrative engine, with this Skill remaining director/editor.
- See [`source-assisted-production.md`](source-assisted-production.md) for escalation and acceptance criteria.
