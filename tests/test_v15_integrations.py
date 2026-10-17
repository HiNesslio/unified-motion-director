"""Validate integration contracts; does not render upstream artworks or run real jurors."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import production_router
import motion_preflight

class IntegrationV15Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storyboard=json.loads((ROOT/'tests/fixtures/storyboard.json').read_text())

    def test_two_sources_and_license_metadata(self):
        sources=json.loads((ROOT/'config/sources.json').read_text())['repositories']
        ids={x['id'] for x in sources}
        self.assertIn('howseen-claude-motion-design',ids)
        self.assertIn('whaleyxbt-claude-motion',ids)
        self.assertEqual(len(ids),len(sources))
        for x in sources: self.assertTrue(x['license'])

    def test_timeline_is_contiguous_and_illustrative_status_is_preserved(self):
        tl,plan=production_router.build(self.storyboard,'auto')
        self.assertEqual(tl['duration_sec'],15.0)
        self.assertEqual(tl['fps'],30)
        self.assertEqual(tl['timing_status'],'illustrative')
        self.assertEqual(list(tl['scenes'].values())[0]['start_frame'],0)
        self.assertEqual(list(tl['scenes'].values())[-1]['end_frame_exclusive'],450)
        self.assertEqual(plan['engine'],'remotion')

    def test_explicit_backend_is_unchanged(self):
        for engine in ('html-seek','remotion','web-sim'):
            self.assertEqual(production_router.build(self.storyboard,engine)[1]['engine'],engine)

    def test_invalid_seam_rejected(self):
        a=json.loads(json.dumps(self.storyboard))
        a['scenes'][1]['start_sec']+=.2
        with self.assertRaises(ValueError):production_router.build(a,'auto')

    def test_cli_writes_only_plans(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'plans'
            proc=subprocess.run([sys.executable,str(ROOT/'scripts/production_router.py'),str(ROOT/'tests/fixtures/storyboard.json'),'--out',str(out)],capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertEqual(sorted(x.name for x in out.iterdir()),['PRODUCTION_HANDOFF.md','production-plan.json','shared-timeline.json'])
            self.assertIn('not yet performed', (out/'PRODUCTION_HANDOFF.md').read_text().lower())

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'ffmpeg/ffprobe absent')
    def test_single_frame_flash_is_detected_at_native_fps(self):
        with tempfile.TemporaryDirectory() as td:
            film=Path(td)/'one-frame.mp4'
            cmd=['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=black:s=320x180:r=30:d=1.3',
                 '-vf',"drawbox=x=0:y=0:w=320:h=180:color=white:t=fill:enable='eq(n,12)'",
                 '-c:v','libx264','-pix_fmt','yuv420p',str(film)]
            proc=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            result=motion_preflight.inspect(film)
            self.assertEqual(result['frame_scan']['sample_fps'],30)
            found=result['frame_scan']['suspect_frame_change_candidates']
            self.assertTrue(any(abs(x['time_sec']-.4)<.04 and x['kind']=='one_frame_brightness_excursion' for x in found),found)

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'ffmpeg/ffprobe absent')
    def test_real_encoded_media_preflight_without_claiming_jury(self):
        with tempfile.TemporaryDirectory() as td:
            film=Path(td)/'synthetic.mp4'
            out=Path(td)/'preflight.json'
            cmd=['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=640x360:rate=24:duration=1.5',
                 '-c:v','libx264','-pix_fmt','yuv420p',str(film)]
            p=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            q=subprocess.run([sys.executable,str(ROOT/'scripts/motion_preflight.py'),str(film),'--out',str(out)],capture_output=True,text=True)
            self.assertEqual(q.returncode,0,q.stderr)
            x=json.loads(out.read_text())
            self.assertEqual(x['status'],'TECHNICAL_PREFLIGHT_ONLY')
            self.assertEqual(x['width'],640)
            self.assertEqual(x['fps'],24)
            self.assertEqual(x['audio_streams'],0)
            self.assertGreater(x['frame_scan']['frames_scanned'],2)
            self.assertEqual(len(x['sha256']),64)
            self.assertNotIn('PASS',x['status'])

if __name__=='__main__':unittest.main()
