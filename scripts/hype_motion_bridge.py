#!/usr/bin/env python3
"""Safe director -> Hype-yolo source-assisted renderer bridge.

Generates provenance/scene-selection handoff and *prints* native upstream commands.
Does not fetch, execute, install, route, render or imply any upstream matches.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_UPSTREAM = ROOT / 'external' / 'claude-motion-skill' / 'skills' / 'claude-motion'


def story(path: Path) -> dict:
    src = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(src, dict) or not isinstance(src.get('scenes'), list) or not src['scenes']:
        raise ValueError('Storyboard must be a JSON object with nonempty scenes[]')
    for shot in src['scenes']:
        for key in ('id', 'subject', 'action', 'start_sec', 'end_sec'):
            if key not in shot:
                raise ValueError(f'Scene missing required field: {key}')
        if not isinstance(shot['start_sec'], (int, float)) or not isinstance(shot['end_sec'], (int, float)) or shot['end_sec'] <= shot['start_sec']:
            raise ValueError(f'Scene {shot["id"]} has invalid time interval')
    return src


def query_for(shot: dict, visual_motif: str) -> str:
    # Inputs are used only as a single literal argv or quoted textual suggestions.
    motion = shot.get('motion', {})
    return ' | '.join(filter(None, [shot.get('subject', ''), shot.get('action', ''), motion.get('signature_move', ''), visual_motif]))[:350]


def scaffold(src: dict) -> dict:
    return {
        'schema': 'umd-source-assisted-handoff-v1',
        'film_id': src.get('film_id'),
        'title': src.get('title'),
        'duration_sec': src.get('duration_sec'),
        'visual_motif': src.get('visual_motif', ''),
        'source_backend': 'Hype-yolo/claude-motion-skill (optional; NOT installed by bridge)',
        'source_version_reviewed': 'v0.4.0-beta.1',
        'source_status': 'NOT_ROUTED',
        'film_consistency': {
            'primary_visual_mechanism': None,
            'geometry_material_motion_rules': None,
            'handoff_between_shots': 'Follow original storyboard continuity and seam ledger',
            'compositing_strategy': None,
            'sound_policy': src.get('audio', {})
        },
        'shots': [
            {
                'shot_id': shot['id'],
                'range_sec': [shot['start_sec'], shot['end_sec']],
                'story_purpose': shot.get('purpose', ''),
                'subject': shot['subject'],
                'actual_action': shot['action'],
                'source_status': shot.get('source_status', 'not-recorded'),
                'search_query': query_for(shot, src.get('visual_motif', '')),
                'source_selection': {
                    'state': 'NOT_ROUTED',
                    'kind': None,
                    'id': None,
                    'source_url': None,
                    'commit': None,
                    'license': None,
                    'preview_seen': False,
                    'source_modules_inspected': []
                },
                'adaptation': {
                    'original_mechanisms_to_preserve': [],
                    'source_files_used_by_final_render': [],
                    'new_or_rewritten_subjects_actions_camera': [],
                    'material_motion_coherence_notes': None,
                    'missing_assets': []
                },
                'tests': {
                    'representative_shot_rendered': False,
                    'mechanism_visibly_active': False,
                    'seek_determinism_checked': False,
                    'critical_frames_reviewed': False,
                    'video_decoded': False,
                    'audio_confirmed': False
                }
            } for shot in src['scenes']
        ],
        'release_gate': {
            'source_rights_and_attribution_confirmed': False,
            'real_mp4_exists': False,
            'visual_reviewed': False,
            'adaptation_md_written': False,
            'honest_status': 'PLANNING_ONLY'
        }
    }


def print_command(*argv: str) -> None:
    print(' '.join(shlex.quote(str(arg)) for arg in argv))


def plan(src: dict | None, upstream: Path, query: str | None) -> None:
    script = upstream / 'scripts' / 'route.mjs'
    print(f'UPSTREAM: {upstream}')
    print(f'PRESENT: {script.is_file()} (not executed)')
    print('Review upstream SKILL.md, licenses, catalog and dependency versions first.')
    print('\nDiscover reusable mechanisms:')
    for flag in ('--engines', '--scenes', '--extensions', '--models'):
        print_command('node', script, flag)
    candidates = []
    if query:
        candidates.append(query)
    elif src:
        candidates = [query_for(x, src.get('visual_motif', '')) for x in src['scenes'][:5]]
    for i, q in enumerate(candidates, 1):
        print(f'\nCandidate query {i} (results NOT fetched; a matching source is NOT guaranteed):')
        print_command('node', script, '--query', q, '--limit', '5')
    print('\nOnce candidate ID, source/asset licenses and representative frames are verified:')
    print_command('node', upstream / 'scripts' / 'prepare-case.mjs', '--case', '<verified-case-id>', '--out', '<new-film-folder>')
    print_command('node', upstream / 'scripts' / 'render.mjs', '--root', '<new-film-folder>', '--out', '<new-film-folder>/film.mp4', '--fps', '24')
    print('IMPORTANT: these are PRINTED instructions only. Native script details may change upstream.')


def status(upstream: Path) -> None:
    print(f'Hype-yolo Skill location: {upstream}')
    print('Upstream SKILL.md:', 'FOUND' if (upstream / 'SKILL.md').is_file() else 'MISSING (not bundled)')
    print('Native route.mjs:', 'FOUND' if (upstream / 'scripts' / 'route.mjs').is_file() else 'MISSING (not bundled)')
    for cmd in ('node', 'npm', 'ffmpeg', 'ffprobe'):
        print(f'{cmd}:', shutil.which(cmd) or 'NOT INSTALLED')
    print('No upstream code was executed. Dependency/browser/license validation still required.')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--status', action='store_true')
    mode.add_argument('--plan', action='store_true')
    mode.add_argument('--handoff', action='store_true')
    ap.add_argument('--storyboard', type=Path, help='Existing validated director storyboard.json')
    ap.add_argument('--query', help='Optional manual search query when generating a plan')
    ap.add_argument('--upstream-path', type=Path, default=DEFAULT_UPSTREAM)
    ap.add_argument('--output', type=Path, help='Required for --handoff; refuses to overwrite')
    args = ap.parse_args()
    if args.status:
        status(args.upstream_path)
        return 0
    try:
        src = story(args.storyboard) if args.storyboard else None
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        ap.error(f'Cannot load storyboard: {exc}')
    if args.plan:
        plan(src, args.upstream_path, args.query)
        return 0
    if src is None or args.output is None:
        ap.error('--handoff requires --storyboard and --output')
    if args.output.exists():
        ap.error(f'Output exists, refusing overwrite: {args.output}')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scaffold(src), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Created: {args.output} (PLANNING_ONLY; no matches, previews or renders claimed)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
