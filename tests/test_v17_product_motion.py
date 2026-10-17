"""v1.7 contract tests: no real product claims, plugin calls or juror scoring."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import validate_storyboard, production_router, product_truth, mobile_readability, remotion_plugin_bridge

BASE=json.loads((ROOT/'tests/fixtures/storyboard.json').read_text())


def concept_claim():
    return {'schema_version':'1.0','product_id':'anonymous-product','claims':[
        {'id':'alpha','claim':'Illustrative data transforms into a sample result',
         'implementation_status':'experimental','data_status':'illustrative',
         'display_mode':'concept_demo','approved_for_public_copy':False,
         'disclosure':'Concept demonstration','evidence':[]}]}


class ProductMotionV17(unittest.TestCase):
    def test_old_storyboard_still_passes(self):
        errors,_=validate_storyboard.validate(copy.deepcopy(BASE))
        self.assertEqual(errors,[])

    def test_events_typography_and_presets_preserved_in_handoff(self):
        film=copy.deepcopy(BASE)
        film['visual_preset']='kinetic-product'
        scene=film['scenes'][0]
        scene['motion_pattern']='text-to-ui'
        scene['events']=[{'time_sec':.5,'action':'title_reveal'}, {'time_sec':1.8,'action':'ui_arrival'}]
        scene['typography_cues']=[{'text':'Data first','groups':['Data',' first'],'enter_sec':.1,'settle_sec':.5,'exit_sec':2.2,'reading_hold_sec':1.2}]
        err,_=validate_storyboard.validate(film)
        self.assertEqual(err,[])
        tl,plan=production_router.build(film,'auto')
        self.assertEqual(tl['visual_preset'],'kinetic-product')
        self.assertEqual(tl['scenes']['S01']['events'][1]['action'],'ui_arrival')
        self.assertEqual(tl['scenes']['S01']['typography_cues'][0]['groups'],['Data',' first'])
        self.assertEqual(tl['scenes']['S01']['motion_pattern'],'text-to-ui')

    def test_bad_event_and_text_hold_rejected(self):
        film=copy.deepcopy(BASE)
        film['scenes'][0]['events']=[{'time_sec':4,'action':'late'}]
        film['scenes'][1]['typography_cues']=[{'text':'Hello','groups':['Wrong'],'enter_sec':2.5,'settle_sec':2.7,'exit_sec':2.8,'reading_hold_sec':1.5}]
        err,_=validate_storyboard.validate(film)
        self.assertTrue(any('time_sec outside' in e for e in err))
        self.assertTrue(any('groups must match' in e for e in err))
        self.assertTrue(any('reading_hold_sec' in e for e in err))

    def test_missing_manifest_hard_block(self):
        film=copy.deepcopy(BASE);film['scenes'][0]['claim_refs']=['alpha']
        err,_=validate_storyboard.validate(film)
        self.assertTrue(any('requires top-level claims_manifest' in e for e in err))

    def test_truth_gate_experimental_disclosure_and_references(self):
        film=copy.deepcopy(BASE)
        film['scenes'][0]['claim_refs']=['alpha']
        film['scenes'][0]['on_screen_text'].append('Concept demonstration')
        self.assertEqual(product_truth.validate(concept_claim(),film),[])
        film['scenes'][0]['on_screen_text'].pop()
        self.assertTrue(any('exact on-screen disclosure' in e for e in product_truth.validate(concept_claim(),film)))

    def test_factual_claim_requires_reviewer_source_approval(self):
        x=concept_claim();c=x['claims'][0]
        c.update(implementation_status='shipped',data_status='verified',display_mode='factual_demo',approved_for_public_copy=True)
        self.assertTrue(product_truth.validate(x))
        c['evidence']=[{'source':'release-notes.md','checked_at':date.today().isoformat(),'evidence_type':'release_note'}]
        c['evidence_reviewer']='Product owner';c['evidence_reviewed_at']=date.today().isoformat()
        self.assertEqual(product_truth.validate(x),[])
        c['implementation_status']='planned'
        self.assertTrue(any('factual_demo requires shipped/beta' in e for e in product_truth.validate(x)))

    def test_schema_and_bridge_hard_gate(self):
        with tempfile.TemporaryDirectory() as td:
            work=Path(td)
            film=copy.deepcopy(BASE)
            film['claims_manifest']='claims.json'
            film['scenes'][0]['claim_refs']=['alpha']
            film['scenes'][0]['on_screen_text'].append('Concept demonstration')
            story=work/'storyboard.json'; story.write_text(json.dumps(film))
            (work/'claims.json').write_text(json.dumps(concept_claim()))
            errors,_=validate_storyboard.validate(film,work)
            self.assertEqual(errors,[])
            handoff=remotion_plugin_bridge.prepare(story,work/'handoff')
            self.assertEqual(handoff['claims_manifest'],'claims.json')
            (work/'claims.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'invalid storyboard'):
                remotion_plugin_bridge.prepare(story,work/'handoff2')

    def test_mobile_heuristic(self):
        doc={'canvas':{'width':1080,'height':1920},'texts':[
            {'text':'Concise title','x':90,'y':260,'width':600,'height':120,'font_px':54,'settle_sec':1,'exit_sec':3}]}
        a=mobile_readability.inspect_layout(doc)
        self.assertFalse(a['issues'],a)
        doc['texts'][0]['font_px']=26
        doc['texts'][0]['exit_sec']=1.1
        b=mobile_readability.inspect_layout(doc)
        self.assertTrue(any(x['kind']=='font_too_small' for x in b['issues']))
        self.assertTrue(any(x['kind']=='insufficient_read_hold' for x in b['issues']))
        self.assertEqual(mobile_readability.inspect_layout({})['status'],'NOT_EVALUATED')

    def test_no_brand_specific_public_examples(self):
        self.assertFalse((ROOT/'examples').exists())
        for p in [ROOT/'README.md',ROOT/'README.zh-Hant.md',ROOT/'SKILL.md']:
            text=p.read_text().lower()
            self.assertNotIn('examples/',text)

    def test_audio_beat_candidates_not_verified(self):
        try:import numpy as np
        except ImportError:self.skipTest('numpy not installed')
        import analyze_music
        sr=8000;y=np.zeros(sr*12,dtype=np.float32)
        for t in np.arange(.5,11.5,.5):
            start=int(t*sr)
            y[start:start+100]+=np.hanning(100).astype(np.float32)*.65
        z=analyze_music.analyze_samples(y,sr,'f'*64)
        self.assertEqual(z['status'],'candidate_unverified')
        self.assertTrue(len(z['beat_times_sec_candidates'])>2)
        # Ambiguous half-time/double-time cannot be labeled as a confirmed 120 bpm.
        self.assertIn(z['tempo_confidence'],('low','medium','high'))


if __name__=='__main__':unittest.main()
