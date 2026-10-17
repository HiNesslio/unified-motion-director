# Motion choreography: causal and time-addressable

## Vocabulary — choose deliberately

1. **Object continuity:** a real shape, brand mark, dot, line or UI tile carries the meaning across shots.
2. **Shared-element morph:** one shape changes dimensions / curvature / context, rather than dissolve to unrelated shapes.
3. **Masked typography:** letters or words enter from a measured mask; group phrases by reading order.
4. **Anticipation and settle:** small anticipatory movement and physically plausible landing, sparingly.
5. **Camera-as-editor:** a world transform recontextualizes an object; for multi-scale zooms interpolate log(scale).
6. **Editorial cut:** use a strong change of image scale, direction or contrast without random movement.
7. **Graphic rhythm:** align movement endpoints and transitions with meaningful sound events, not every object to every beat.
8. **Data reveal:** a counter or graph only if the underlying data is real; otherwise mark it as a visual illustration.

For the complete researched catalogue of 137 moves, refer to https://github.com/PHY041/claude-motion-playbook/blob/main/docs/techniques.md . Do not silently transplant creator works or prompts.

## Motion recipe format

`trigger` (event/time), `owner` (element), `from`, `to`, `path`, `easing`, `duration_frames`, `overshoot`, `mask`, `hand_off_to`, `reason`.

Favor one major movement at a time. Group secondary animation so it reinforces the dominant action rather than competes.

## Deterministic rendering principles

- `state(t) = f(t, fixed_assets, static_config)`.
- Use exact frame times `frame/fps`, stable seeded pseudo-randomness or pre-generated paths.
- Avoid accumulated integrations or unseeded random updates when a renderer seeks frames out of order.
- Closed-form spring response or analytical cubic easing is preferable for seek-based systems.
- `from` states must be explicit; otherwise seeking to a middle frame produces pops.
- Motion blur must be tested on actual output; many samples can create ghosting when fast elements have hard edges.

## Handoff check

At each seam compare: identity, position, apparent size, velocity direction, colour, shape, focus, semantic context, sound. A mismatch may be intended as a hard cut; document why. Do not force seamless morphs where an honest cut works better.

## Interaction-specific

Interactive web / native UI has different rules from a pre-rendered film: respond to actual state and accessibility settings; reduce motion where requested; support pauses and reduced-motion preference. Deterministic-seek requirements apply to reproducible offline renders, not all live interaction.
