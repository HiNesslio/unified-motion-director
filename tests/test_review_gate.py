"""Synthetic unit tests only. These mock reports are NOT genuine independent reviews."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import review_gate as g

@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'ffmpeg/ffprobe missing')
class ReviewGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='mock-motion-gate-')
        cls.path=Path(cls.tmp.name)
        cls.video=cls.path/'synthetic.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi',
            '-i','testsrc2=size=320x180:rate=24','-t','2','-c:v','mpeg4',str(cls.video)],check=True)
        proc=subprocess.run([sys.executable,str(ROOT/'scripts'/'review_gate.py'),'prepare',str(cls.video),'--out',str(cls.path/'review'),'--samples','8','--audio-policy','silent','--rights-status','confirmed'],capture_output=True,text=True)
        if proc.returncode: raise RuntimeError(f'review preparation failed: {proc.stderr[-2500:]}')
    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()

    def setUp(self):
        self.bundle=self.path/'review'
        m=g.load_json(self.bundle/'manifest.json')
        self.assertEqual(m['technical_preflight_signals'],m['technical_preflight_signals'])
        self.assertEqual(g.load_json(Path(m['technical_preflight']))['sha256'],m['video_sha256'])
        for role in g.REVIEWERS:
            f=self.bundle/f'juror-{role}.json'
            if f.exists(): f.unlink()

    def make_reports(self,score=9):
        m,frames=g.verified_bundle(self.bundle)
        reviewed=[f.name for f in frames[:6]]
        for role in g.REVIEWERS:
            dims={}
            for name in g.RUBRICS[role]:
                if name=='sound': dims[name]={'score':None,'status':'not_applicable','evidence':[]}
                else: dims[name]={'score':score,'status':'evaluated','evidence':[{'time_sec':0.5,'observation':'Synthetic fixture: test observation only'}]}
            report={'judge':role,'reviewer_name':g.REVIEWERS[role], 'media_sha256':m['video_sha256'],
                 'evidence_level':'DECODED_VIDEO','inspected_frames':reviewed,'dimensions':dims,
                 'blockers':[],'fixes':[{'priority':'P1','time_sec':0.5,'issue':'synthetic test','action':'not a real creative review'}, {'priority':'P2','time_sec':1.5,'issue':'synthetic test','action':'not a real creative review'}],
                 'confidence':0.85,'limitations':['Fixture is a score contract test, not a real agent judgement']}
            (self.bundle/f'juror-{role}.json').write_text(json.dumps(report),encoding='utf8')

    def test_pass_threshold_contract_only(self):
        self.make_reports(9)
        self.assertEqual(g.aggregate_impl(self.bundle),'PASS')
        self.assertEqual(g.load_json(self.bundle/'acceptance.json')['composite_score'],90)

    def test_low_score_blocks_release(self):
        self.make_reports(6)
        self.assertEqual(g.aggregate_impl(self.bundle),'REWORK')

    def test_critical_blocker_overrides_high_score(self):
        self.make_reports(10)
        f=self.bundle/'juror-aesthetic.json';x=g.load_json(f)
        x['blockers']=[{'kind':'missing_product_logo','time_sec':1.0,'reason':'Synthetic critical failure'}]
        f.write_text(json.dumps(x),encoding='utf8')
        self.assertEqual(g.aggregate_impl(self.bundle),'BLOCKED')

    def test_missing_report_cannot_pass(self):
        self.make_reports(10)
        (self.bundle/'juror-holistic.json').unlink()
        self.assertEqual(g.aggregate_impl(self.bundle),'HOLD_EVIDENCE')

    def test_fake_frame_cannot_pass(self):
        self.make_reports(10)
        f=self.bundle/'juror-aesthetic.json';x=g.load_json(f)
        x['inspected_frames'][0]='fake_frame.png';f.write_text(json.dumps(x),encoding='utf8')
        self.assertEqual(g.aggregate_impl(self.bundle),'HOLD_EVIDENCE')

    def test_wrong_sha_invalidates_report(self):
        self.make_reports(10)
        f=self.bundle/'juror-holistic.json';x=g.load_json(f)
        x['media_sha256']='0'*64;f.write_text(json.dumps(x),encoding='utf8')
        self.assertEqual(g.aggregate_impl(self.bundle),'HOLD_EVIDENCE')

    def test_unevaluated_sound_holds(self):
        self.make_reports(10)
        m=g.load_json(self.bundle/'manifest.json');m['audio_policy']='required';(self.bundle/'manifest.json').write_text(json.dumps(m),encoding='utf8')
        f=self.bundle/'juror-holistic.json';x=g.load_json(f)
        x['dimensions']['sound']={'score':None,'status':'not_evaluated','evidence':[]}
        f.write_text(json.dumps(x),encoding='utf8')
        self.assertEqual(g.aggregate_impl(self.bundle),'HOLD_EVIDENCE')
        m['audio_policy']='silent';(self.bundle/'manifest.json').write_text(json.dumps(m),encoding='utf8')

if __name__=='__main__':unittest.main()
