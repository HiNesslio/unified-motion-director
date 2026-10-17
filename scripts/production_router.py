#!/usr/bin/env python3
"""Produce an advisory production handoff and canonical named time anchors.

This is not a runnable Remotion/HTML renderer. Music beat estimates must come
from measured audio and are deliberately not generated here.
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone


def route(film, engine='auto'):
    if engine != 'auto':
        return engine, 'Explicitly selected by producer; check technical fitness.'
    shots = film.get('scenes', [])
    text = ' '.join(str(s.get(k,'')) for s in shots for k in ('subject','purpose','action')).lower()
    sim_terms = ('simulation','particle','swarm','crowd of agents','fly-through','fluid physics',
                 'physics simulation','engine chamber','agents moving')
    if any(x in text for x in sim_terms):
        return 'web-sim', 'Storyboard suggests many independently moving agents or spatial simulation.'
    if film.get('engine_preference') in ('html-seek','remotion','web-sim'):
        return film['engine_preference'], 'Storyboard engine preference.'
    if 'ui' in text or 'screen' in text or 'app' in text or any(s.get('on_screen_text') for s in shots):
        return 'remotion', 'Editable React UI/typography makes scene-component composition a reasonable default.'
    return 'html-seek', 'Custom graphical choreography with a deterministic time-seeking browser is a reasonable default.'


def build(film, engine):
    duration=float(film['duration_sec'])
    fps=int(film['fps'])
    if not 0<fps<=240 or duration<=0:
        raise ValueError('positive fps/duration required')
    scenes=sorted(film['scenes'], key=lambda s: float(s['start_sec']))
    if not scenes: raise ValueError('At least one scene required')
    # Strictly no overlap/gap and exact duration, scene continuity checked elsewhere.
    prev=0.0
    timeline={'schema':'umd.shared-timeline.v1', 'film_id':film.get('film_id','untitled'),
              'fps':fps,'duration_sec':duration,'timing_status':film.get('audio',{}).get('timing_status','unknown'),
              'source':'storyboard.json', 'scenes':{}}
    for scene in scenes:
        begin=float(scene['start_sec']); end=float(scene['end_sec'])
        if abs(begin-prev)>1e-5 or end<=begin:
            raise ValueError(f'gap/overlap/negative duration at scene {scene["id"]}: {begin}, expected {prev}')
        cue=scene.get('sound',{})
        ct=cue.get('cue_time_sec')
        if ct is not None and not 0<=float(ct)<=duration:
            raise ValueError(f'sound cue out of bounds in {scene["id"]}')
        # Preserve provenance of all sound times; no fake alignment.
        timeline['scenes'][scene['id']]={
            'start':begin,'end':end,'start_frame':round(begin*fps),
            'end_frame_exclusive':round(end*fps),
            'sound_cue_sec':ct,'sound_cue_status':cue.get('status','unknown'),
            'sound_cue_label':cue.get('cue_label',''),
            'transition_type':scene.get('transition',{}).get('type','unknown'),
        }
        prev=end
    if abs(prev-duration)>1e-5:
        raise ValueError(f'last scene ends at {prev}, expected {duration}')
    chosen,reason=route(film,engine)
    profiles={
      'html-seek':{'source':'howseen-claude-motion-design','entry':'window.seek(t) in seconds','qa':['four key stills','fast draft','subframe master within shots','suspect pop strips','true final encode']},
      'remotion':{'source':'whaleyxbt-claude-motion','entry':'Remotion frame + shared named times','qa':['draft','named-beat contact sheets','sound cue sheet','full encode','audio waveform']},
      'web-sim':{'source':'whaleyxbt-claude-motion','entry':'precompute simulation + pure window.SIM.render(t)','qa':['arbitrary-order seek probes','beat stills','3D camera clipping','frame stepped capture']}
    }
    selected=profiles[chosen]
    plan={'film_id':timeline['film_id'],'engine':chosen,'reason':reason,'source_repo_id':selected['source'],
          'entry_contract':selected['entry'],'qa_stages':selected['qa'],
          'does_not_automatically': ['download upstream source','install dependencies','produce code or MP4','verify actual audio beats','grant media rights','assign subjective jury scores'],
          'handoff_requirements':['audit third-party checkout/license','map shared-timeline.json into engine-native code','verify brand assets and actual claims','build and play draft','inspect frame sheets and post-render preflight','dispatch two isolated juror agents only on frozen MP4']}
    return timeline, plan


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('storyboard',type=Path)
    p.add_argument('--engine',choices=['auto','html-seek','remotion','web-sim'],default='auto')
    p.add_argument('--out',required=True,type=Path)
    a=p.parse_args()
    film=json.loads(a.storyboard.read_text(encoding='utf-8'))
    tl,plan=build(film,a.engine)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out/'shared-timeline.json').write_text(json.dumps(tl,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (a.out/'production-plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    lines=['# Engine-neutral production handoff','',f'Film: {plan["film_id"]}',f'Engine: **{plan["engine"]}**',
      f'Why: {plan["reason"]}',f'Backend source: `{plan["source_repo_id"]}`',
      f'Clock: `{plan["entry_contract"]}`','',
      '## Execution requirements (not yet performed)']
    lines += [f'- [ ] {x}' for x in plan['handoff_requirements']]
    lines += ['', '## Named scene anchors', '', '| Scene | Start | End | Frames | Audio status |','|---|---:|---:|---|---|']
    for scene,v in tl['scenes'].items():
        lines += [f'| {scene} | {v["start"]:.2f}s | {v["end"]:.2f}s | {v["start_frame"]}–{v["end_frame_exclusive"]-1} | {v["sound_cue_status"]} |']
    lines += ['', '## Status', '', 'Planning only. No upstream runtime, soundtrack, frames or jury were executed.']
    (a.out/'PRODUCTION_HANDOFF.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Route: {plan["engine"]}. Wrote 3 handoff files under {a.out}')

if __name__=='__main__': main()
