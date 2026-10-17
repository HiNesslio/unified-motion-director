# Independent post-render acceptance: film-first, score-second

## Required architecture

- Production (director/implementer) **stops editing** once a candidate MP4 is frozen. Hash the video and generate a review evidence bundle (`scripts/review_gate.py prepare`). Every re-render has a *new* SHA-256 and must be scored anew.
- Launch **two independent reviewers**, one `motion-aesthetic-juror`, one `motion-holistic-juror`, in separate agent contexts. Do NOT show either juror the producer's self-review or the other's response. They must open real decoded imagery, not merely see storyboard or prompts.
- Separate review contexts are an operational requirement, not an instruction to the producer to pretend to be two characters. If the runtime cannot start independent agents, report `UNREVIEWED`, not a numerical score or PASS. See `scripts/install_codex.py` and `scripts/review_gate.py`.
- A third role is deterministic `review_gate.py`: validates video presence, frame decode, hash, report schemas, coverage, evidence timestamps, scores, and writes final acceptance JSON/Markdown. This is **not** an LLM reviewer and cannot judge taste.
- A score must be **reproducibly calculated** from submitted dimensional scores, not the writer's gut estimate. Editing source or a different video after the decision invalidates it.

## Required direct evidence

1. A real locally present MP4; ffprobe metadata; 48 uniformly timecoded PNGs (or a justified equivalent). Codex v1.5 `prepare` additionally writes `technical-preflight.json` with frame-change candidates and binds its checksum to the MP4. These automated candidates need visual confirmation and are NOT a score. Real audio evidence if sound/music is part of the goal.
2. A contact sheet and **at least 6 actually inspected full frames per reviewer**. Evidence should reference concrete frame files or accurate timecodes.
3. Frozen source brief, aspect-ratio target, product/assets list and licensing caveats (when provided).
4. A juror report for that exact media SHA; do not use design intent as proof of rendered effect.

If any reviewer reports a blind/untested sample, score is **not validated**. Missing or inferred evidence never automatically passes.

## Weighted scoring (0–100)

**Independent juror A — VISUAL (55% of overall)**: composition 30%, hierarchy 25%, typography 15%, distinctiveness 20%, cohesion 10%.

**Independent juror B — FILM (45% of overall)**: story 25%, timing 20%, continuity 20%, comprehension 15%, sound 10%, execution 10%.

Both raters score each dimension on 0–10 with direct timestamped evidence. For intentionally silent videos with evidence-backed `sound` = not_applicable, exclude sound and re-normalize the other five. If soundtrack is required or present but not **actually audited**, sound must be `not_evaluated` (null) and the verdict is `HOLD_EVIDENCE`, not an invented score. Metadata-only detection of an audio stream is insufficient for sound scoring.

Final = 0.55 × visual_score + 0.45 × film_score, expressed 0–100, rounded to one decimal. The deterministic validator never guesses a missing score.

## Acceptance policy

- `PASS`: final ≥ 85.0 AND each juror ≥ 80.0 AND **no** critical blocker AND evidence verified AND required formats/audio/rights are cleared in review.
- `REVISE`: 70.0–84.9 without release blockers, or 85+ with a juror under 80; issue the top 3 high-impact edits.
- `REWORK`: below 70.0, requiring new direction/timeline rather than polishing.
- `BLOCKED`: one or more concrete critical failures/rights or authenticity issue; even a 99 cannot release.
- `HOLD_EVIDENCE`: missing video, insufficient visual access, unreviewed required sound, unsupported or incomplete reviewer report, or unverifiable evidence. Never convert to PASS by scoring default zeros or guessing.
- `NEEDS_ADJUDICATION`: when scores disagree by 20+ absolute points and no objective blocker; do not silently average and approve.

**Rubric anchors**: 0–2 broken/incomplete; 3–4 serious problems; 5–6 functional but generic/uneven; 7–8 professional with noticeable issues; 9 exceptional and evidence-backed; 10 rare, exceptional across the whole piece. An 8 in one dimension is not automatically a release pass.

## Revision protocol

1. Export candidate `v1`, freeze hash, review with jurors; record status and timecodes.
2. Producer groups critiques into **top 3 highest-impact visual/structural revisions**, implements and re-renders to `v2`. Never instruct jurors to raise marks or tell them the needed threshold. New evidence pack, fresh independently blind reviews. Keep old reports for diffing, not for priming the judges.
3. Max **two revision rounds** by default. If still blocked, provide unresolved issues and decision to the user; do not loop indefinitely or conceal the failed grade.
4. `PASS` means the defined gate passed for the inspected deliverable, **not** a guarantee that every viewer likes it or a claim of formal professional certification.

## Native Codex integration

Official Codex Skills live at `.agents/skills/<skill-name>/SKILL.md` (repo) or `~/.agents/skills/<skill-name>/SKILL.md` (user). The two *custom* subagents are standalone TOMLs under `.codex/agents/` or `~/.codex/agents/`, not Markdown files in the skill's `agents/` UI metadata directory. Install with `scripts/install_codex.py --project PROJECT --apply` or `--user --apply`. Restart or refresh Codex if necessary.

**Native orchestration (Codex App / CLI chat / IDE):**

1. Director freezes actual MP4 and executes `review_gate.py prepare`. Review bundle contains manifest SHA, contact sheet and decoded full frames. User/parent must verify evidence exists and is readable by agents.
2. Spawn `motion-aesthetic-juror` and `motion-holistic-juror` as TWO independent Codex subagent threads. Each reviews a **separate context** containing the role instructions, same immutable bundle, no peer findings, no director self-score. Assign them distinct report filenames, but they should return JSON to the director; only director writes each JSON file (prevents agents changing production or each other's files).
3. Reviewers **must actually open ≥6 distinct full PNG frames and inspect contact sheet**, rather than infer visuals from a file path or storyboard. If missing tools, report unreviewed, not an invented rating. The second juror must treat music as `not_evaluated` unless audio was genuinely heard/analysed using an appropriate tool.
4. Director writes `juror-aesthetic.json` and `juror-holistic.json`, one per separate agent, and runs `python3 scripts/review_gate.py aggregate --bundle <bundle>`.
5. For REVISE/REWORK, director updates and renders a fresh MP4, creates new review bundle with new SHA, spawns new independent reviews. At most two revision rounds by default.

**Alternative noninteractive Codex CLI:** `python3 scripts/review_gate.py run --bundle <bundle> --project PROJECT` launches two **separate** `codex exec --sandbox read-only` sessions with the same contact sheet and ≥8 decoded frame images attached through `--image`. This is process isolation, not an in-app custom subagent spawn. Requires installed/authenticated Codex CLI and image-capable model, and may be limited by audio access. Failed invocations cannot pass.

Sources: https://developers.openai.com/codex/skills and https://developers.openai.com/codex/multi-agent , https://learn.chatgpt.com/docs/cli/reference .
