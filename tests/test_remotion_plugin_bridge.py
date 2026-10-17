"""Real file-based contract tests; do not exercise any ChatGPT Plugin or taste jurors."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import remotion_plugin_bridge as bridge


class RemotionBridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.storyboard = ROOT / 'examples' / 'parkgo' / 'storyboard.json'
        self.out = self.root / 'handoff'
        self.handoff = bridge.prepare(self.storyboard, self.out)

    def test_handoff_identity_and_timeline_preserved(self):
        doc = json.loads((self.out / 'remotion-handoff.json').read_text())
        tl = json.loads((self.out / 'shared-timeline.json').read_text())
        self.assertEqual(doc['handoff_id'], bridge.canonical_id(self.storyboard))
        self.assertEqual(doc['storyboard_sha256'], bridge.digest(self.storyboard))
        self.assertEqual(doc['duration_sec'], tl['duration_sec'])
        self.assertEqual(list(tl['scenes'].values())[-1]['end_frame_exclusive'], 450)
        self.assertEqual(doc['plugin_capability_status'], 'NOT_CHECKED')
        self.assertIn('Remotion Plugin', (self.out / 'REMOTION_PLUGIN_TASK.md').read_text())

    def test_brief_is_optional_but_has_checksum(self):
        brief = self.root / 'BRIEF.md'
        brief.write_text('Verified brief\n')
        pl = bridge.prepare(self.storyboard, self.out, brief=brief)
        self.assertEqual(pl['brief_sha256'], hashlib.sha256(brief.read_bytes()).hexdigest())
        self.assertEqual((self.out / 'BRIEF.md').read_text(), brief.read_text())

    def test_reject_invalid_storyboard(self):
        bad = json.loads(self.storyboard.read_text())
        bad['scenes'][0]['subject'] = ''
        source = self.root / 'bad.json'
        source.write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, 'invalid storyboard'):
            bridge.prepare(source, self.root / 'bad-handoff')

    def test_no_claim_of_built_media_with_missing_output(self):
        project = self.root / 'project'
        project.mkdir()
        result = self._result(project)
        self._write_result(result)
        verdict = bridge.verify(self.out / 'remotion-handoff.json', project / 'remotion-result.json', project)
        self.assertEqual(verdict['status'], 'HOLD_EVIDENCE')
        self.assertTrue(any('missing at' in x for x in verdict['errors']))
        self.assertFalse(verdict['plugin_execution_independently_confirmed'])

    def test_outside_project_rejected_even_if_exists(self):
        project = self.root / 'project'
        project.mkdir()
        result = self._result(project)
        result['outputs']['final_mp4'] = '../outside.mp4'
        self._write_result(result)
        verdict = bridge.verify(self.out / 'remotion-handoff.json', project / 'remotion-result.json', project)
        self.assertEqual(verdict['status'], 'HOLD_EVIDENCE')
        self.assertTrue(any('outside project' in x for x in verdict['errors']))

    def test_different_storyboard_hash_rejected(self):
        project = self.root / 'project'
        project.mkdir()
        result = self._result(project)
        result['storyboard_sha256'] = '0'*64
        self._write_result(result)
        verdict = bridge.verify(self.out / 'remotion-handoff.json', project / 'remotion-result.json', project)
        self.assertEqual(verdict['status'], 'HOLD_EVIDENCE')
        self.assertTrue(any('storyboard_sha256 mismatch' in x for x in verdict['errors']))

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'ffmpeg and ffprobe needed')
    def test_decodable_real_media_allows_only_technical_handoff(self):
        project = self.root / 'project'
        (project / 'out').mkdir(parents=True)
        film = project / 'out' / 'final.mp4'
        args = ['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=blue:s=160x90:r=15:d=15',
                '-c:v','libx264','-pix_fmt','yuv420p',str(film)]
        subprocess.run(args, check=True, capture_output=True)
        subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=black:s=160x90:r=1:d=1', '-frames:v','1', str(project / 'out' / 'contact.png')], check=True, capture_output=True)
        result = self._result(project)
        result['plugin_invoked'] = True  # self-claim is explicitly NOT treated as verified
        result['final_sha256'] = bridge.digest(film)
        self._write_result(result)
        verdict = bridge.verify(self.out / 'remotion-handoff.json', project / 'remotion-result.json', project)
        self.assertEqual(verdict['status'], 'READY_FOR_TECHNICAL_PREFLIGHT_AND_JURORS', verdict['errors'])
        self.assertFalse(verdict['plugin_execution_independently_confirmed'])
        self.assertEqual(verdict['verified_outputs']['final_mp4']['sha256'], bridge.digest(film))
        result['final_sha256'] = '0'*64
        self._write_result(result)
        verdict = bridge.verify(self.out / 'remotion-handoff.json', project / 'remotion-result.json', project)
        self.assertEqual(verdict['status'], 'HOLD_EVIDENCE')
        self.assertTrue(any('final_sha256 mismatch' in x for x in verdict['errors']))

    def _result(self, project):
        return {
            'schema': 'umd.remotion-result.v1',
            'handoff_id': self.handoff['handoff_id'],
            'storyboard_sha256': self.handoff['storyboard_sha256'],
            'engine': 'remotion-cli',
            'plugin_invoked': False,
            'composition_id': 'Demo',
            'outputs': {'final_mp4':'out/final.mp4', 'contact_sheet':'out/contact.png'},
            'final_sha256':'x'
        }

    def _write_result(self, data):
        (self.root / 'project' / 'remotion-result.json').write_text(json.dumps(data))


if __name__ == '__main__':
    unittest.main()
