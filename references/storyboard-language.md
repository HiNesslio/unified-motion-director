# Storyboard: make director intent reconstructable

## Shot grammar

Define each shot with: purpose → subject → composition → camera → action → motion law → duration → transition → sound → authenticity.
Use specific, visual language. "Beautiful movement" is not a direction. "One card moves 160 px along x over 18 frames, then line expands into the next scene's route" is actionable (numbers remain illustrative until composition sizes are set).

## Standard camera vocabulary

- Static locked frame: confidence, readability and comparison.
- Slow dolly or track: reveals spatial relation; pick one principal vector.
- Controlled push-in: emphasizes function or detail; avoid automatic zoom-out reset.
- Macro punch: use a purposeful detail (status dot, route number, button) to bridge scale.
- Whip / cut: use only when the semantic change or music accent benefits; preserve direction on entry.
- Pullback reveal: context after close detail; should transform the viewer's understanding.

## Every shot record needs

- `id`, `start`, `end`, `purpose`, `why_this_scene`, `subject`, `composition`, `camera`, `action`, `motion`, `transition`, `sound`, `source_status`, `on_screen_text`, `continuity`.
- Screen direction (left/right/in/out), relative size/anchor, entry and exit state.
- Exit-to-entry **seam ledger** for shared elements, or explicit "hard cut" reason.
- For UI motion, tie gestures and highlights to real user outcomes, no invented interaction capabilities.

## Storyboard approval surface

Produce 4–8 keyframe descriptions or a visual board where helpful. A static storyboard should convey shot framing and transitions, not pretend to be a fully animated video. The built-in script `scripts/storyboard_board.py` creates a lightweight HTML board from validated storyboard JSON.

## Aspect-safe typography

Compose separately for wide and vertical. Keep primary text clear of interface chrome and platform controls; test actual preview at phone size rather than use a universal pixel margin. For languages with longer phrases, measure strings after fonts load and adapt scale at the group level.
