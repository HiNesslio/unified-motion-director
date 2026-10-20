# Unified Motion Director

**Product storytelling and precision motion for Codex.** Understand what a real product does, plan a truthful visual story, hand off to Remotion or a deterministic rendering backend, and subject the final encoded film to independent review.

<p align="center"><img src="./assets/readme/workflow.svg" width="100%" alt="Director-led production: storyboard, Remotion, actual media verification, and two independent jurors"></p>

[繁體中文](README.zh-Hant.md) · [Codex Skill](SKILL.md) · [Changelog](CHANGELOG.md) · [Source attribution](ATTRIBUTION.md)

## v1.9 — Mografy Canvas production (optional)

[Mografy](https://github.com/zz41354899/mografy) is now an additional **native Canvas 2D production lane** for motion typography, numeric/shape animations, localized CJK text and portrait motion graphics. **Remotion Plugin stays the default for React/UI-led films**; the core director, Product Truth hard gate, and two independently run Codex jurors are unchanged.

```bash
python3 scripts/production_router.py film/storyboard.json --engine mografy --out film/route
python3 scripts/mografy_bridge.py prepare film/storyboard.json --out film/mografy-handoff

# Separately, in an approved installed Mografy workspace:
mografy check projects/<film>
mografy review projects/<film>
mografy export projects/<film> --format mp4

# On a real final encoded output:
python3 scripts/mografy_bridge.py verify \
  --handoff film/mografy-handoff/mografy-handoff.json \
  --video projects/<film>/renders/final.mp4 --out film/media-identity.json
```

The handoff writes a frozen storyboard SHA, engine-neutral named times, planning review samples and a Mografy production task. It **does not install Mografy or render a video**. `verify` examines actual encoded video properties and identity, **not** Mografy provenance, frame quality, audio sync or juror acceptance. Mografy currently requires Node.js 22.12+ and a separate local installation. See the [full Mografy integration and licensing guidance](references/mografy-canvas-production.md).

## v1.8 — continuity and music choreography

Director Intelligence now includes **subject-carry continuity**, deliberate camera anticipation/settle, motivated cuts, and **score-aware picture landmarks**. Read [Cinematic continuity](references/cinematic-continuity.md) and [Music-to-picture choreography](references/music-picture-choreography.md). These are **original MIT-licensed editorial contracts**, inspired by public writings from [OneTake](https://github.com/feitangyuan/onetake) and [huashu-motion](https://github.com/alchaincyf/huashu-motion). No third-party engine, samples or code are bundled. OneTake is separately PolyForm Noncommercial; the UMD Skill remains MIT.

```bash
python3 scripts/validate_storyboard.py path/to/storyboard.json
python3 scripts/motion_spine.py path/to/storyboard.json --out motion-spine.json
```

This produces **planning-only** scene continuity and picture/audio-cue diagnostics, *not* proof of finished visual quality or confirmed musical beat sync. Remotion and the existing independent acceptance workflow remain unchanged.

## What it does

- **Product Story Intelligence**: turn product mechanics into a causal sequence of visible events instead of decorating unrelated features.
- **Product Truth Gate**: link on-screen product claims to dated supporting evidence, mark concept demos, and block unsubstantiated public claims.
- **Beat-aware motion**: estimate tempo and strong musical events from a real audio file, explicitly retain uncertainty, and use one named timeline for visuals and sound.
- **Kinetic typography**: language-aware semantic grouping, readable holds and controlled entrances without a forced house style.
- **Reusable motion grammar**: Text → UI, UI → Data, Path Draw, Data → Number, Progress Along Path, State Color Transition, Number → UI, Object → Brand.
- **Studio-ready handoff**: delegate React scene implementation and rendering to the optional official [Remotion Plugin](https://chatgpt.com/plugins/remotion); HTML `seek(t)` and Three.js remain supported.
- **Trustworthy QA**: frame preflight, geometry-based mobile legibility warnings, verified media hashes, and **two isolated Codex jurors**.

The original acceptance bar is unchanged: **55% visual + 45% holistic; combined ≥85, each ≥80**, with no critical issue. Product truth is a **separate hard gate**, not a way to trade accuracy for aesthetics.

## Install

Python 3.11+ is required. The Skill installs locally; Remotion, FFmpeg and audio-analysis dependencies are optional separate tools.

```bash
python3 scripts/install_codex.py --user --apply
# or install into a particular project:
python3 scripts/install_codex.py --project /path/to/project --apply
```

The installer previews changes until `--apply` is supplied. It requires `--force` to replace an existing installation. Reload Codex, then invoke `$unified-motion-director`.

## First use

```text
$unified-motion-director

Create a truthful, director-led product film. First map product capabilities
and evidence to visual cause-and-effect. Prepare the brief, look, claims
manifest, storyboard and named scene events. Use a real licensed music file
if one is available, and hand production to $remotion when installed.
Inspect the render, run technical and readability QA, then independently
review it with both Codex jurors. Never mark release-ready unless the truth
and acceptance gates pass.
```

### Production workflow

```text
Product evidence → Truth gate → Director & presets → Storyboard & events
                → Beat timeline → Remotion / seek(t) / web-sim
                → Rendered MP4 → Technical + mobile checks
                → Two isolated jurors → Evidence-bound acceptance
```

```bash
# Validate actual product claims and a storyboard together:
python3 scripts/validate_storyboard.py /path/to/film/storyboard.json
python3 scripts/product_truth.py /path/to/film/claims.json --storyboard /path/to/film/storyboard.json

# Analyze a licensed local song (NumPy required; FFmpeg for non-WAV):
python3 scripts/analyze_music.py /path/to/track.wav --out /path/to/film/beat-analysis.json

# Select a rendering backend / generate a named timeline:
python3 scripts/production_router.py /path/to/film/storyboard.json --out /path/to/film/handoff
python3 scripts/remotion_plugin_bridge.py prepare /path/to/film/storyboard.json --out /path/to/film/remotion-handoff

# Once an actual film and optional UI text-layout manifest exist:
python3 scripts/motion_preflight.py /path/to/film/final.mp4 --layout-manifest /path/to/film/layout.json --out /path/to/film/preflight.json
python3 scripts/review_gate.py prepare /path/to/film/final.mp4 --out /path/to/film/review --storyboard /path/to/film/storyboard.json --rights-status confirmed
```

Products that do not have a claims manifest can use the general creative workflow; any film declaring claim references must pass the Product Truth Gate before a release verdict. The music analyzer outputs **unverified beat candidates**, not music facts. The optional layout analyzer flags measurable text-size/margin/hold violations, not artistic merit. Actual licensed assets and authorized product claims must be supplied by the producer.

See [product storytelling](references/product-storytelling.md), [kinetic typography](references/kinetic-typography.md), [motion patterns](references/product-motion-patterns.md), [visual direction presets](references/visual-presets.md) and [independent acceptance](references/independent-acceptance.md).

## Tests and limits

```bash
python3 -m unittest discover -s tests -v
```

Unit tests use neutral technical fixtures, not a brand case study. FFmpeg-dependent tests skip if unavailable. **Passing automated tests does not prove a finished film, a real Plugin invocation, or actual juror scores.** Product evidence still requires a producer to verify it; the audio beat grid and mobile readability pass require creative review. The code and original orchestration content use [MIT](LICENSE); external references and media have separate rights ([attribution](ATTRIBUTION.md)).
