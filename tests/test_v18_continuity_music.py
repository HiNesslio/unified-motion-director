"""v1.8 original motion-directing contracts; no OneTake or huashu imports."""
import copy
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import motion_spine
import production_router
import validate_storyboard

BASE = json.loads((ROOT / 'tests/fixtures/storyboard.json').read_text(encoding='utf8'))


def fixture():
    film = copy.deepcopy(BASE)
    scene = film['scenes'][0]
    scene['events'] = [{'action': 'reveal_result', 'time_sec': 0.5}]
    scene['continuity_plan'] = {'mode': 'carry', 'carrier_id': 'focus-ring',
                                'handoff_target': 'S02:title', 'camera_behavior': 'anticipate-then-settle',
                                'reason': 'Selected focus remains legible across the seam'}
    film['audio']['motion_sync_cues'] = [{'id': 'hit-1', 'scene_id': scene['id'],
        'event_action': 'reveal_result', 'picture_time_sec': 0.5, 'audio_anchor_sec': 0.5,
        'priority': 'hero', 'alignment': 'hit', 'source_status': 'illustrative'}]
    return film


class ContinuityMusic(unittest.TestCase):
    def test_old_fixture_is_still_valid(self):
        self.assertEqual(validate_storyboard.validate(copy.deepcopy(BASE))[0], [])

    def test_new_fields_valid_and_backward_compatible(self):
        self.assertEqual(validate_storyboard.validate(fixture())[0], [])
        self.assertEqual(motion_spine.audit(fixture())['status'], 'PLANNING_ONLY')

    def test_carry_needs_subject(self):
        film = fixture()
        film['scenes'][0]['continuity_plan'].pop('carrier_id')
        self.assertTrue(any('requires carrier_id' in v for v in validate_storyboard.validate(film)[0]))

    def test_intentional_cut_is_allowed(self):
        film = fixture()
        film['scenes'][0]['continuity_plan'] = {'mode': 'motivated_cut',
                    'reason': 'A narrative jump to another point of view'}
        self.assertFalse(validate_storyboard.validate(film)[0])

    def test_duplicate_event_cannot_ambiguously_receive_score(self):
        film = fixture()
        film['scenes'][0]['events'].append({'action': 'reveal_result', 'time_sec': .6})
        self.assertTrue(any('exactly one event' in v for v in validate_storyboard.validate(film)[0]))

    def test_unknown_scene_is_rejected(self):
        film = fixture()
        film['audio']['motion_sync_cues'][0]['scene_id'] = 'S9999'
        self.assertTrue(any('unknown scene_id' in v for v in validate_storyboard.validate(film)[0]))

    def test_major_sync_point_requires_audio_anchor(self):
        film = fixture()
        film['audio']['motion_sync_cues'][0].pop('audio_anchor_sec')
        self.assertTrue(any('needs audio_anchor_sec' in v for v in validate_storyboard.validate(film)[0]))
        film['audio']['motion_sync_cues'][0]['alignment'] = 'free'
        self.assertEqual(validate_storyboard.validate(film)[0], [])

    def test_picture_event_must_be_frame_aligned(self):
        film = fixture()
        film['audio']['motion_sync_cues'][0]['picture_time_sec'] = .8
        self.assertTrue(any('half a frame' in v for v in validate_storyboard.validate(film)[0]))

    def test_claimed_measured_music_requires_evidence(self):
        film = fixture()
        film['audio']['motion_sync_cues'][0]['source_status'] = 'measured'
        self.assertTrue(any('measurement_evidence' in v for v in validate_storyboard.validate(film)[0]))
        film['audio'].update({'timing_status': 'measured', 'music': 'owned-original.wav',
                              'measurement_evidence': 'Reviewed original soundtrack WAV onset plot and listened'})
        errs, notes = validate_storyboard.validate(film)
        self.assertEqual(errs, [])
        self.assertTrue(any('producer claim' in n for n in notes))

    def test_planned_offset_warning_not_verified_score(self):
        film = fixture()
        film['audio']['motion_sync_cues'][0]['audio_anchor_sec'] = 0.1
        result = motion_spine.audit(film)
        self.assertTrue(result['warnings'])
        self.assertEqual(result['music_picture_cues'][0]['render_sync_status'], 'NOT_EVALUATED')
        self.assertEqual(result['acceptance_verdict'], 'NOT_EVALUATED')

    def test_optional_score_and_continuity_passed_to_engine(self):
        film = fixture()
        timeline, _ = production_router.build(film, 'remotion')
        self.assertEqual(timeline['motion_sync_cues'][0]['id'], 'hit-1')
        self.assertEqual(timeline['scenes']['S01']['continuity_plan']['mode'], 'carry')

    def test_no_imported_licensed_backend_code(self):
        self.assertFalse((ROOT / 'vendor' / 'onetake').exists())
        self.assertFalse((ROOT / 'vendor' / 'huashu-motion').exists())
        license_txt = (ROOT / 'LICENSE').read_text(encoding='utf-8')
        self.assertIn('MIT License', license_txt)
        docs = (ROOT / 'ATTRIBUTION.md').read_text(encoding='utf-8')
        self.assertIn('PolyForm Noncommercial', docs)
        self.assertIn('do **not** copy', (ROOT / 'references/cinematic-continuity.md').read_text().lower())


if __name__ == '__main__':
    unittest.main()
