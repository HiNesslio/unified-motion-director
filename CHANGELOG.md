## v1.9 — Mografy native Canvas production lane (2026-10-20)

- Added an optional, separately installed [Mografy](https://github.com/zz41354899/mografy) local Canvas 2D backend for graphics/kinetic type/CJK, with unchanged Remotion-first policy for React/UI-heavy work.
- Added `mografy` engine routing and optional `engine_preference` storyboard schema with backward-compatible defaults.
- Added `scripts/mografy_bridge.py`: validate storyboard and Product Truth references, freeze original SHA, export shared timeline/review sampling/production contract; independently verify actual encoded MP4/WebM metadata and SHA without self-approving.
- Documented Mografy's upstream scene contract, Node.js requirement, 16 component references, optional CJK/cinema extras, and `check → review → export` workflow.
- No upstream source, bundled fonts, assets, third-party binaries, demos or renderer licenses were imported. Mografy source MIT; CJK fonts OFL and other media separately licensed.
- The existing director workflow, Product Truth hard gate, Remotion collaboration, score/music planning and isolated dual-juror 55/45 acceptance are unchanged.
- New regression tests use neutral fixtures or synthetic FFmpeg media, **not** actual Mografy visual/audio acceptance.

## v1.8 — Cinematic Continuity & Music-Picture Direction (2026-10-19)

- Studied OneTake high-continuity film grammar and Huashu score-first sound/visual choreography without incorporating either project's runtime or assets. UMD remains MIT; OneTake stays separately PolyForm Noncommercial.
- Added concise original editorial references for seamless subject carry, operator-style camera arrival and intentionally motivated cuts, and for meaningful audio/visual anchors.
- Added optional `continuity_plan` per scene and `audio.motion_sync_cues` bound to named storyboard events, validated without invalidating v1.7 storyboards.
- Added stdlib-only `scripts/motion_spine.py` to report seam documentation, cadence and **planned** picture/music offsets, strictly marked PLANNING_ONLY.
- Propagated new fields into engine-neutral `shared-timeline.json` and therefore Remotion handoff.
- Added regression tests covering compatibility, invalid cues, documentation, sound status and MIT-only provenance.
- Original independent dual-juror SHA-bound review, Product Truth Gate and 55%/45% weighting remain unchanged.

## v1.7 — Product Storytelling & Precision Motion (2026-10-17)

- Product Story Intelligence (causal product-to-motion story decisions), editable visual direction presets, and eight semantic motion patterns.
- Product Truth evidence manifest schema, explicit factual/concept policies, source/approval attestation, storyboard-reference checks and review-gate hash binding.
- Intra-shot event anchors, semantic typography cues and optional beat/visual-preset metadata, backward compatible with earlier storyboard files.
- NumPy audio-onset/energy analysis for *candidate only* BPM, beat and drop suggestions (with file hash, not mislabelled as human-verified).
- Renderer-measured mobile text geometry/hold heuristics, optional in `motion_preflight.py`, never mistaken for aesthetic approval.
- Remotion shared-timeline handoff preserves new precision/claim fields; existing dual Codex juror 55/45 acceptance remains unchanged.
- Removed all product-specific public examples and related documentation; tests now use neutral fixture data.

# Changelog

## v1.6 — Remotion Plugin collaborative production (2026-10-17)

- Verified Remotion official ChatGPT/Codex Plugin listing and published Codex Agent Skills / Studio WebMCP docs. Plugin installation and active availability are independent of this ZIP.
- Added `references/remotion-plugin-collaboration.md` to define single-workspace dual-Skill orchestration: UMD owns creative direction, Remotion owns implementation/render, two read-only jurors own final independent acceptance.
- Added deterministic `scripts/remotion_plugin_bridge.py` for version-bound handoff (`prepare`) and evidence-bound output verification (`verify`). Outputs: `remotion-handoff.json`, `shared-timeline.json`, `REMOTION_PLUGIN_TASK.md`; explicit media SHA verification and ffprobe duration checks.
- Added `templates/remotion-result.example.json`, `config/remotion-plugin.json`, README activation instructions and Codex-focused authority contract. No third-party Remotion runtime or plugin code included.
- Preserved all previous technical-preflight, source-routing, Codex juror and score thresholds. Plugin absent -> official Agent Skills/CLI fallback, not fabricated execution.
- Tested handoff generation, structural storyboard validation, schema, video/image decoding, media identity and file-traversal protections with real synthetic video test fixtures (25 tests passed); no claim of real Plugin invocation or actual human/model aesthetic rating.

## v1.5 — Codex production-lane integration (2026-10-17)

- Studied source README, published SKILL.md files, render scripts and licenses from `howseen-ai/claude-motion-design` and `whaleyxbt/claude-motion` using GitHub connector.
- Added two source registry entries, attribution, new engineering reference documents. No runtime/model/music/photo code/assets copied.
- Added `scripts/production_router.py` → engine-neutral time anchors and three backend advisory routes: deterministic HTML `seek(t)`, Remotion scene composition + sound, and pure `render(t)` web simulations.
- Added `scripts/motion_preflight.py` → actual encoded MP4 introspection, SHA-256, native-fps gray frame-change and isolated single-frame flash candidates, story-duration checks. Candidates require visual follow-up.
- `review_gate.py prepare` now automatically creates pre-jury technical-preflight JSON bound to the exact film hash; blind independent Codex jurors continue to be mandatory for subjective scoring.
- Updated Codex documentation, technical guide and example plans; preserved 55% visual / 45% holistic juror weights, SHA proof and score thresholds.
- Added independent integration tests including an actual synthetic 1-frame flash and real ffprobe decode; 18 local unit tests passed on 2026-10-17. No upstream film rendered and no authentic Codex reviewers executed.

## v1.4

Codex native installation and two distinct independent jurors, retaining earlier guide/technique integrations.
