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
