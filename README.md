# Unified Motion Director

**Director-led motion design for Codex.** Take a product idea from concept and shot list to a rendered film, with one shared timeline, optional Remotion collaboration, and independent post-render acceptance.

[![Codex Skill](https://img.shields.io/badge/Codex-Agent%20Skill-273448?style=flat-square)](https://developers.openai.com/codex/skills)
[![Remotion optional](https://img.shields.io/badge/Remotion-optional%20plugin-365D8D?style=flat-square)](https://chatgpt.com/plugins/remotion)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-444?style=flat-square)](https://www.python.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-555?style=flat-square)](LICENSE)

<p align="center"><img src="./assets/readme/workflow.svg" width="100%" alt="Pipeline: direct with a structured storyboard, build in Remotion, verify the rendered film, then review with two independent jurors."></p>

**[繁體中文](README.zh-Hant.md)** · [Skill instructions](SKILL.md) · [Example storyboard](examples/parkgo/storyboard.json) · [Source & attribution](ATTRIBUTION.md)

## See the workflow

A **15-second ParkGo example** is included as actual structured production material—not as a claimed finished film. Explore the [director brief](examples/parkgo/BRIEF.md), [look direction](examples/parkgo/LOOK.md), [scene storyboard](examples/parkgo/storyboard.json), and [Remotion handoff](examples/parkgo/remotion-handoff/REMOTION_PLUGIN_TASK.md). The example's [HTML storyboard board](examples/parkgo/storyboard-board.html) visualizes shot planning.

| Stage | What the Skill produces |
| --- | --- |
| **Direct** | Verified brief, visual look, narrative arc, camera and shot decisions |
| **Storyboard** | Frame-bound scene descriptions, readable holds, transitions and a shared timeline |
| **Build** | An appropriate lane: **Remotion**, deterministic `seek(t)` HTML, or Three.js simulations |
| **Inspect** | Decoded media, frame-contact sheets, timestamped technical findings and asset provenance |
| **Review** | Two **separately scoped** jurors: visual aesthetic and holistic film quality |
| **Accept** | Evidence-gated verdict tied to the final MP4 checksum; revise or rework if necessary |

The key design choice: **production agents do not grade their own film.** The review verdict only counts after the actual output exists and each juror inspects evidence from the same immutable render.

## Quick start

### 1. Install the Codex Skill

Requires **Python 3.11+**. Clone this repository, then run the installer from the repository root:

```bash
python3 scripts/install_codex.py --user --apply
```

This installs the Skill to `~/.agents/skills/unified-motion-director/` and the two jurors to `~/.codex/agents/`. To add it only to a project:

```bash
python3 scripts/install_codex.py --project /path/to/project --apply
```

The installer is **dry-run by default** (remove `--apply` to preview its actions) and refuses overwrites unless `--force` is explicitly added. Refresh Codex after installation.

### 2. Optionally enable Remotion

The [official Remotion Plugin](https://chatgpt.com/plugins/remotion) is installed **separately**, when supported in your workspace. The Skill does **not** install or impersonate that Plugin. Without it, the same storyboard can be handed to a local Remotion CLI setup, or routed to a deterministic HTML or simulation pipeline.

### 3. Give Codex a production brief

```text
$unified-motion-director

Make a 15-second product film for my app. Use a restrained editorial
style, one accent colour, real UI captures and a single visual thread.
Create the brief, look direction, storyboard and shared timeline first.
If $remotion is available, hand the scene spec to it for rendering.
After rendering, run technical preflight and two independent juror reviews.
Fix concrete defects and repeat review (at most two rounds).
Do not claim release-ready unless the acceptance gate passes.
```

## Shared timeline → Remotion handoff

Generate an exact storyboard-and-time handoff from the included example:

```bash
python3 scripts/remotion_plugin_bridge.py prepare \
  examples/parkgo/storyboard.json \
  --out /tmp/parkgo-remotion-handoff
```

This emits `remotion-handoff.json`, `shared-timeline.json`, and `REMOTION_PLUGIN_TASK.md`. Once a real Remotion film has been rendered, write `remotion-result.json` with actual project-relative output paths and verify it:

```bash
python3 scripts/remotion_plugin_bridge.py verify \
  --handoff /tmp/parkgo-remotion-handoff/remotion-handoff.json \
  --result /path/to/video-project/remotion-result.json \
  --project /path/to/video-project \
  --out /tmp/parkgo-verification.json
```

The verification checks existence, decodability, storyboard identity, duration, and media hashes. It **does not** certify that a Plugin ran, or that the film looks good. See [the Remotion integration contract](references/remotion-plugin-collaboration.md).

## Review standard

Two separate Codex agents, if the runtime supports agent spawning, score the **same rendered film** independently. A deterministic gate combines their evaluations:

| Juror | Weight | Focus |
| --- | ---: | --- |
| Aesthetic juror | **55%** | Composition, typography, art direction, motion quality, visual coherence |
| Holistic juror | **45%** | Message, pacing, storytelling, sound, clarity and delivery |

To pass, the composite score must be **≥85/100**, each juror **≥80/100**, and no critical defect or evidence error may remain. Low scores request revision or rework; missing output or reviewer evidence blocks release. Frame SHA, reviewer independence and timestamped evidence are part of the acceptance contract. Read [the independent acceptance guide](references/independent-acceptance.md).

## What is — and is not — included

Included: the orchestration Skill, Codex juror configurations, shot/storyboard schemas, production bridges, local QA scripts, tests, and the ParkGo **planning** example. **Not included:** a Remotion runtime or subscription, the external motion repositories' full source, model weights, third-party videos, copyrighted music, commercial fonts, or a pre-rendered finished ParkGo film.

The workflows were validated with **25 local tests** using structural and synthetic media checks. That is **not** a claim of an executed cross-Plugin film, live Codex subagent judging, or aesthetic scores from an actual deliverable. Install tools and provide real assets to run those steps.

## Development and project layout

```text
SKILL.md               Main Codex production instructions
codex-agents/          Independent juror configurations
references/            Direction, source routing, sound, quality, provenance
scripts/               Installer, storyboard, Remotion bridge, QA and gates
templates/             Storyboard and evaluator schemas
examples/parkgo/       Example brief, storyboard and handoff
assets/readme/         Editable README diagram
```

Run the unit tests:

```bash
python3 -m unittest discover -s tests -v
```

Some media-related cases require `ffmpeg` and `ffprobe` on `PATH`; tests that need unavailable tools are skipped. `pytest` is not required. See [Changelog](CHANGELOG.md) for feature history and [Attribution](ATTRIBUTION.md) for credited influences and asset boundaries.

## Provenance and license

The orchestration code and documentation are licensed under [MIT](LICENSE). Public techniques were researched from [Claude Motion Playbook](https://github.com/PHY041/claude-motion-playbook), [Howseen claude-motion-design](https://github.com/howseen-ai/claude-motion-design), [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion), [Hype-yolo/claude-motion-skill](https://github.com/Hype-yolo/claude-motion-skill), [Prompt Motion](https://prompt-motion.com), and [Skillry](https://skillry.dev/ai-videos/opus-5-5). Their individual licenses and creators' media rights remain separate. [Full attribution →](ATTRIBUTION.md)

This project extracts **observable design patterns** from public work; it does not copy another model's internal reasoning or claim an affiliation with Anthropic, OpenAI or Remotion.
