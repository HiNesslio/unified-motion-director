# Remotion Plugin — Codex production handoff

Film: **parkgo-mobility-15s-concept** · 15.0s · 30 fps
Handoff ID: `remotion-fabf30d4d07885ad`
Storyboard SHA-256: `fabf30d4d07885adfe616e402beecd1c786db5a96dd71cca7ffcc23ce119708a`

## Assignment / 責任分工

- Unified Motion Director owns creative direction, shot intention, transitions, visual constraints, truthfulness and final jury gate.
- Remotion Plugin (if installed) owns implementation, React composition, Studio preview and rendering; use its current official Skills, not stale copied API snippets.
- Codex main agent integrates changes, reviews actual artifacts and coordinates two genuinely separate jurors.

## Plugin discovery — no fabricated invocation

Prefer the official Remotion Plugin in ChatGPT/Codex. If the installed plugin is visible, invoke its `$remotion` entry and relevant official Skills (`remotion-create`, `remotion-markup`, `remotion-render`, `remotion-studio`; `remotion-maps` etc when required).
If unavailable, use Remotion CLI + official Agent Skills as fallback. Do not claim a direct ChatGPT Plugin API was called from this Python program.

## Non-negotiable implementation contract

1. Read `remotion-handoff.json` plus `shared-timeline.json` before writing source.
2. Build scenes to the specified times, with true source assets only. Use seeded randomness / `useCurrentFrame` for deterministic render.
3. Preview in Studio when possible. Check aspect ratios as independent compositions, not stretched/cropped frames.
4. Create time-coded draft contact sheets and inspect transition seams and mobile readability.
5. Render final MP4. Save explicit paths, SHA-256, runtime and composition IDs in `remotion-result.json` following `templates/remotion-result.example.json`.
6. Run `remotion_plugin_bridge.py verify`, then `motion_preflight.py` and two independent jurors. Treat missing audio evidence and unknown rights as blockers.

## Scene map

| Scene | Interval | Intent | Transition | Data status |
|---|---|---|---|---|
| S01 | 0–1.8s | Hook — one quiet line that becomes a route | continuity-carrier | concept |
| S02 | 1.8–4.2s | Show real-time bus view | shared-element | concept |
| S03 | 4.2–6.8s | Reveal arrival estimates without fake times | match move | concept |
| S04 | 6.8–9.5s | Connect bus mobility to parking | continuity-carrier | concept |
| S05 | 9.5–12.5s | Real parking information as second payoff | shared-element | concept |
| S06 | 12.5–15s | Resolve single route motif into ParkGo identity | shared-element end | concept |

## Production checkpoints

- Gate 1: storyboard and LOOK aligned.
- Gate 2: minimum 4 representative stills or equivalent beat sheet inspected.
- Gate 3: draft video + time-coded sheet inspected and corrections applied.
- Gate 4: final encoded media and real evidence manifest verified.
- Gate 5: two independent jurors and deterministic acceptance gate; 85+ composite, both 80+, no blockers.

**This handoff alone does not prove the Plugin is installed, invoked or a video has been rendered.**
