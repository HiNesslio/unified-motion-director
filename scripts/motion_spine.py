#!/usr/bin/env python3
"""Advisory continuity and picture-to-music planning audit.

Reads Unified Motion Director storyboard data. It DOES NOT analyze rendered
frames, hear audio, confirm beat onsets, or award acceptance scores.
Original stdlib-only implementation: no OneTake or Huashu runtime code used.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def audit(film: dict) -> dict:
    scenes = film.get('scenes', [])
    fps = film.get('fps', 30)
    audio = film.get('audio', {})
    warnings = []
    observations = []
    seams = []
    active_scenes = {s['id']: s for s in scenes}
    durations = [float(s['end_sec']) - float(s['start_sec']) for s in scenes]
    mean = sum(durations) / len(durations) if durations else 0
    cv = (math.sqrt(sum((d - mean) ** 2 for d in durations) / len(durations)) / mean) if mean else 0
    for index, scene in enumerate(scenes[:-1]):
        following = scenes[index + 1]
        plan = scene.get('continuity_plan')
        boundary = round(float(scene['end_sec']), 3)
        if plan:
            mode = plan['mode']
            carrier = plan.get('carrier_id')
            reason = plan.get('reason', '')
            status = 'DOCUMENTED'
        else:
            mode = 'unspecified'
            carrier = scene.get('transition', {}).get('shared_element') or None
            reason = ''
            status = 'NEEDS_DIRECTION'
            warnings.append(f"{scene['id']} → {following['id']} @ {boundary:g}s: describe continuity_plan or an intentional cut")
        seams.append({'from': scene['id'], 'to': following['id'], 'at_sec': boundary,
                      'mode': mode, 'carrier_id': carrier, 'reason': reason,
                      'planning_status': status,
                      'render_observation': 'NOT_EVALUATED'})
    cues = []
    for cue in audio.get('motion_sync_cues', []):
        scene = active_scenes.get(cue['scene_id'], {})
        picture = cue.get('picture_time_sec')
        score = cue.get('audio_anchor_sec')
        offset = cue.get('intentional_offset_sec', 0.0)
        drift = round(float(picture) - float(score) - float(offset), 4) if picture is not None and score is not None else None
        priority = cue.get('priority', 'secondary')
        if drift is not None and priority in ('hero', 'primary') and abs(drift) > max(2 / fps, .08):
            warnings.append(f"Music cue {cue['id']}: planned visual/audio offset is {drift:+.3f}s after intended offset; check at actual render")
        if cue.get('source_status') != 'measured':
            observations.append(f"Music cue {cue['id']} uses {cue.get('source_status','unverified')} timing; no confirmed audio sync")
        cues.append({'id': cue['id'], 'scene_id': cue['scene_id'],
                     'event_action': cue.get('event_action'), 'priority': priority,
                     'visual_frame': round(float(picture) * fps) if picture is not None else None,
                     'audio_anchor_sec': score, 'intentional_offset_sec': offset,
                     'planned_drift_sec': drift, 'source_status': cue.get('source_status', 'unverified'),
                     'render_sync_status': 'NOT_EVALUATED'})
    if len(scenes) >= 4 and cv < 0.12:
        observations.append('Low shot-duration variation; check if the uniform cadence is intentional, especially for montage')
    if not cues:
        observations.append('No motion_sync_cues; sound-to-picture choreography not specified (valid for intentional silence)')
    if not seams and len(scenes) > 1:
        observations.append('Continuity audit needs two or more scenes')
    return {
        'schema': 'umd.motion-spine.v1', 'film_id': film.get('film_id'),
        'status': 'PLANNING_ONLY', 'acceptance_verdict': 'NOT_EVALUATED',
        'film_audio_timing_status': audio.get('timing_status', 'none'),
        'seams': seams, 'music_picture_cues': cues,
        'cadence': {'scene_count': len(scenes), 'duration_variation_cv': round(cv, 4)},
        'warnings': warnings, 'observations': observations,
        'limits': ['No actual encoded frames inspected', 'No acoustic listening or beat verification',
                   'Timing metadata does not prove rendered alignment',
                   'Two independent film jurors remain responsible for subjective acceptance']
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('storyboard', type=Path)
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    from validate_storyboard import validate
    film = json.loads(args.storyboard.read_text(encoding='utf-8'))
    errors, _ = validate(film, args.storyboard.parent)
    if errors:
        ap.error('invalid storyboard: ' + '; '.join(errors[:5]))
    result = audit(film)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding='utf-8')
    else:
        print(payload, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
