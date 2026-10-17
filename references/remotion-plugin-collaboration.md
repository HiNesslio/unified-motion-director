# Remotion Plugin × Unified Motion Director — collaboration contract (v1.6)

## Verified public integration

Remotion is an official ChatGPT/Codex Plugin: https://chatgpt.com/plugins/remotion . Docs: https://www.remotion.dev/docs/ai/codex-plugin and https://www.remotion.dev/docs/ai/plugins . It supplies Remotion Agent Skills and local project creation/editing tools. Installing this UMD Skill **does not install, connect or invoke Remotion**. Plugin availability varies per Codex runtime, workspace and user installation. A `plugin_invoked` field in a manifest is not independent proof; actual runtime execution records are authoritative.

Machine-readable optional integration metadata: `config/remotion-plugin.json`. Use **one Codex conversation / workspace and one repository**. Run the two skills in the same context when available rather than expecting two unrelated chat sessions to share hidden state. The director owns the creative brief; the Remotion plugin owns React implementation. **No circular re-planning.**

## Authority and artifact boundary

| Phase | Responsible | Immutable / editable artifacts |
|---|---|---|
| Creative brief and aesthetic | `$unified-motion-director` | BRIEF.md, LOOK.md, storyboard.json, asset provenance |
| Canonical handoff | UMD bridge script | remotion-handoff.json, shared-timeline.json, REMOTION_PLUGIN_TASK.md |
| Composition / animation | `$remotion` and official Remotion Skills (if installed) | React components, project lockfile, Composition(s), audio, previews |
| Draft critique and technical preflight | UMD + Codex | time-coded sheets, actual FFmpeg inspections |
| Blind aesthetic and holistic review | separate juror subagents | two JSON juror outputs tied to final film hash |
| Gate / delivery | `review_gate.py` | ACCEPTANCE.md, manifest, actual exported file(s) |

### Installation

Install Remotion Plugin separately through Codex / ChatGPT desktop Plugins, selecting the official listing. Official documentation describes `$remotion` invocation in Codex; confirm the plugin is discoverable in the *active* workspace. The alternative when unavailable is `npx skills add remotion-dev/skills` to install the official Remotion Agent Skills and the ordinary Remotion CLI; do not pretend that is equivalent to a ChatGPT Plugin installation. Never silently install dependencies or incur video rendering charges.

### Planning-to-render

```bash
python3 scripts/validate_storyboard.py path/to/storyboard.json
python3 scripts/remotion_plugin_bridge.py prepare path/to/storyboard.json --out path/to/handoff --brief path/to/BRIEF.md --look path/to/LOOK.md
```

The main Codex agent must read the generated `REMOTION_PLUGIN_TASK.md`, then invoke the official Remotion Plugin **in that same Codex workspace** (for example ask `Use $remotion to implement REMOTION_PLUGIN_TASK.md`). Which internal Remotion skill is used depends on the problem:

- `remotion-create` new project, `remotion-markup` JSX/components/timings, `remotion-studio` live preview, `remotion-render` actual output.
- `remotion-maps` for animated routes/map visuals (useful for your product), `remotion-captions` subtitles, `remotion-interactivity` editable Studio controls, `remotion-docs` to check current API compatibility; others only when appropriate.
- Studio WebMCP is optional for a browser/Codex configuration that supports it; it is **not** guaranteed to work through every chat surface. Official docs: https://www.remotion.dev/docs/ai/webmcp .

Use the `shared-timeline.json` scene start/end frames and named cues as the *single timing truth*. Picture and sound derive from it. Remotion native `useCurrentFrame()` maps into timeline state. Keep randomness seeded, animations frame-deterministic. Use design tokens and source files; no placeholder footage pretending to be product screens. Separate aspect-ratio compositions should be recomposed, not merely cropped.

### Output manifest

Remotion implementation writes `remotion-result.json` following [`templates/remotion-result.example.json`](../templates/remotion-result.example.json). **Only report products actually produced**. `plugin_invoked=true` is a claim and must be backed by actual recorded tool usage. Do not fake outputs to pass the bridge. Verify that it belongs to the exact storyboard and decodeable files:

```bash
python3 scripts/remotion_plugin_bridge.py verify \
  --handoff path/to/handoff/remotion-handoff.json \
  --result path/to/remotion-result.json \
  --project path/to/video-project \
  --out path/to/verify.json
```

The bridge checks media SHA-256, identity, safe paths, file presence and decoded duration; it **does not** claim the plugin was used, sound checked, aesthetics passed, or rights verified.

Only then: `python3 scripts/motion_preflight.py ...`; inspect suspicious frames, read contact sheets, listen to actual sound, run two independent Codex jurors using `review_gate.py prepare` / isolated dispatch / aggregate. Keep pass threshold: aesthetic ≥80, holistic ≥80, weighted ≥85, no blocking claims/rights/technical issues. Up to two correction loops. Whenever the film changes, recalc SHA and re-review both agents. **Never feed the jurors draft scores or pressure them to pass**.

### Plugin absent or unavailable

1. Report clearly: Remotion Plugin not confirmed in this runtime.
2. Use installed Remotion Agent Skills / `npx create-video` / local Remotion CLI as a fallback, provided software execution is available.
3. Preserve the same handoff/result contract and independent reviews. Otherwise stop at truthful planning artifacts and mark `HOLD_EVIDENCE`.

### Boundaries

Do not use the Plugin as a subjective reviewer of its own work. Do not let it arbitrarily alter the director-approved storyline, duration or verified copy to accommodate a technical shortcut. Changes requiring concept approval go back to the director; implementation bug fixes stay with Remotion. Never assert automatic model-to-model collaboration across isolated ChatGPT conversations. No warranties of specific output quality before real rendered frame review.
