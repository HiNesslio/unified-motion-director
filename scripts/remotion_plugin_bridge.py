#!/usr/bin/env python3
"""Remotion Plugin <-> Unified Motion Director file handoff.

Prepare: deterministic, verifiable director contract (no Plugin execution).
Verify: assert a claimed output belongs to the same storyboard and exists as media.
Neither command installs or invokes ChatGPT Plugins, renders a film, nor gives taste scores.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import production_router
import validate_storyboard


def digest(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def canonical_id(storyboard:Path):
    return 'remotion-'+digest(storyboard)[:16]


def prepare(storyboard:Path,out:Path,brief=None,look=None):
    data=json.loads(storyboard.read_text(encoding='utf-8'))
    structural_errors,structural_warnings=validate_storyboard.validate(data, storyboard.resolve().parent)
    if structural_errors:
        raise ValueError('invalid storyboard: '+'; '.join(structural_errors[:6]))
    timeline,_=production_router.build(data,'remotion')
    out.mkdir(parents=True,exist_ok=True)
    payload={
      'schema':'umd.remotion-handoff.v1',
      'handoff_id':canonical_id(storyboard),
      'film_id':timeline['film_id'],
      'storyboard_sha256':digest(storyboard),
      'storyboard_source':str(storyboard.resolve()),
      'duration_sec':timeline['duration_sec'],'fps':timeline['fps'],
      'aspect_ratios':data.get('aspect_ratios',[]),
      'timeline':'shared-timeline.json',
      'composition_strategy':'One canonical composition per target aspect ratio; re-layout, do not simply crop.',
      'creative_authority':'unified-motion-director',
      'execution_owner':'remotion-plugin-if-available-else-codex-remotion',
      'acceptance_owner':'two-independent-codex-jurors',
      'claims_and_assets':data.get('assets',[]),
      'claims_manifest':data.get('claims_manifest'),
      'visual_preset':data.get('visual_preset'),
      'beat_grid':data.get('beat_grid'),
      'audio':data.get('audio',{}),
      'scenes':data['scenes'],
      'storyboard_warnings':structural_warnings,
      'plugin_capability_status':'NOT_CHECKED',
      'requirements':[
        'Use installed Remotion Plugin Agent Skills if discoverable; never assert invoked without actual tool/skill execution.',
        'Keep shared-timeline.json as source of scene times, intra-shot events and typographic cues for picture and sound.',
        'Treat Product Truth Gate as separate mandatory blocker for any claim_refs. Concept-demo disclosures must remain visible.',
        'Create a Remotion Studio-previewable source project, do not overwrite storyboard or director brief.',
        'Present key stills and draft before final render; refine from review evidence.',
        'Deliver a final MP4, time-stamped contact sheet and output manifest; no invented video or metadata.',
        'Do not represent missing app screenshots, assets or illustrative ETA figures as real.',
        'Invoke technical preflight and real, isolated aesthetic/holistic jurors after freeze.'
      ]
    }
    for k,src in (('brief',brief),('look',look)):
        if src:
            src=Path(src)
            if not src.is_file():raise ValueError(f'file not found: {src}')
            target=out/(k.upper()+'.md')
            target.write_bytes(src.read_bytes())
            payload[k+'_sha256']=digest(src)
            payload[k+'_file']=target.name
    (out/'shared-timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'remotion-handoff.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Remotion Plugin — Codex production handoff','',
      f'Film: **{payload["film_id"]}** · {payload["duration_sec"]}s · {payload["fps"]} fps',
      f'Handoff ID: `{payload["handoff_id"]}`',
      f'Storyboard SHA-256: `{payload["storyboard_sha256"]}`','',
      '## Assignment / 責任分工','',
      '- Unified Motion Director owns creative direction, shot intention, transitions, visual constraints, truthfulness and final jury gate.',
      '- Remotion Plugin (if installed) owns implementation, React composition, Studio preview and rendering; use its current official Skills, not stale copied API snippets.',
      '- Codex main agent integrates changes, reviews actual artifacts and coordinates two genuinely separate jurors.',
      '', '## Plugin discovery — no fabricated invocation','',
      'Prefer the official Remotion Plugin in ChatGPT/Codex. If the installed plugin is visible, invoke its `$remotion` entry and relevant official Skills (`remotion-create`, `remotion-markup`, `remotion-render`, `remotion-studio`; `remotion-maps` etc when required).',
      'If unavailable, use Remotion CLI + official Agent Skills as fallback. Do not claim a direct ChatGPT Plugin API was called from this Python program.',
      '', '## Non-negotiable implementation contract','',
      '1. Read `remotion-handoff.json` plus `shared-timeline.json` before writing source.',
      '2. Build scenes to the specified times, with true source assets only. Use seeded randomness / `useCurrentFrame` for deterministic render.',
      '3. Preview in Studio when possible. Check aspect ratios as independent compositions, not stretched/cropped frames.',
      '4. Create time-coded draft contact sheets and inspect transition seams and mobile readability.',
      '5. Render final MP4. Save explicit paths, SHA-256, runtime and composition IDs in `remotion-result.json` following `templates/remotion-result.example.json`.',
      '6. Run `remotion_plugin_bridge.py verify`, then `motion_preflight.py` and two independent jurors. Treat missing audio evidence and unknown rights as blockers.',
      '', '## Scene map', '', '| Scene | Interval | Intent | Transition | Data status |', '|---|---|---|---|---|']
    for s in data['scenes']:
        tr=s.get('transition',{}).get('type','unspecified')
        lines.append(f'| {s["id"]} | {s["start_sec"]}–{s["end_sec"]}s | {s.get("purpose","").replace("|","/")} | {tr} | {s.get("source_status","unknown")} |')
    lines+=['', '## Production checkpoints', '',
      '- Gate 1: storyboard and LOOK aligned.',
      '- Gate 2: minimum 4 representative stills or equivalent beat sheet inspected.',
      '- Gate 3: draft video + time-coded sheet inspected and corrections applied.',
      '- Gate 4: final encoded media and real evidence manifest verified.',
      '- Gate 5: two independent jurors and deterministic acceptance gate; 85+ composite, both 80+, no blockers.',
      '', '**This handoff alone does not prove the Plugin is installed, invoked or a video has been rendered.**']
    (out/'REMOTION_PLUGIN_TASK.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return payload


def _within(project:Path, candidate:str)->Path:
    p=Path(candidate)
    resolved=(p if p.is_absolute() else project/p).resolve()
    if not resolved.is_relative_to(project):
        raise ValueError(f'output path outside project: {candidate}')
    return resolved


def verify(handoff:Path,result_file:Path,project:Path):
    inp=json.loads(handoff.read_text(encoding='utf-8'))
    result=json.loads(result_file.read_text(encoding='utf-8'))
    project=project.resolve()
    errors=[]; evidence={}
    if result.get('schema')!='umd.remotion-result.v1':errors.append('invalid result schema')
    for k in ('handoff_id','storyboard_sha256'):
        if result.get(k)!=inp.get(k):errors.append(k+' mismatch: different storyboard/handoff')
    for k in ('composition_id','engine'):
        if not result.get(k):errors.append('missing '+k)
    assets=result.get('outputs',{})
    if not isinstance(assets,dict):errors.append('outputs must be an object');assets={}
    for k in ('final_mp4','contact_sheet'):
        rel=assets.get(k)
        if not rel: errors.append('missing '+k);continue
        try:p=_within(project,rel)
        except ValueError as e:errors.append(str(e));continue
        if not p.is_file():errors.append(k+' missing at '+str(p));continue
        if p.stat().st_size==0:errors.append(k+' empty');continue
        evidence[k]={'path':str(p),'sha256':digest(p),'bytes':p.stat().st_size}
    mp=evidence.get('final_mp4')
    if 'contact_sheet' in evidence and shutil.which('ffprobe'):
        img=evidence['contact_sheet']['path']
        pr=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',img],capture_output=True,text=True)
        if pr.returncode:
            errors.append('contact_sheet cannot be decoded')
        else:
            try:
                v=json.loads(pr.stdout)['streams'][0]
                w,h=int(v['width']),int(v['height'])
                if w<32 or h<32:errors.append('contact_sheet dimensions unexpectedly tiny')
                else:evidence['contact_sheet']['dimensions']={'width':w,'height':h}
            except (KeyError,IndexError,ValueError,TypeError):errors.append('contact_sheet missing image dimensions')
    if mp:
        given=result.get('final_sha256','')
        if not given:errors.append('final_sha256 absent')
        elif given!=mp['sha256']:errors.append('final_sha256 mismatch: media changed')
        if shutil.which('ffprobe'):
            p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',mp['path']],capture_output=True,text=True)
            if p.returncode:errors.append('ffprobe cannot decode final_mp4')
            else:
                try:
                    dur=float(json.loads(p.stdout)['format']['duration'])
                    evidence['decoded_duration_sec']=dur
                    if abs(dur-float(inp['duration_sec']))>max(.25,2/float(inp['fps'])):
                        errors.append(f'film duration inconsistent: {dur:.2f} s vs {inp["duration_sec"]:.2f} s')
                except (KeyError,ValueError,TypeError) as e: errors.append('invalid ffprobe duration: '+str(e))
        else: errors.append('ffprobe unavailable: media cannot be independently decoded')
    status='READY_FOR_TECHNICAL_PREFLIGHT_AND_JURORS' if not errors else 'HOLD_EVIDENCE'
    return {'schema':'umd.remotion-verification.v1','status':status,'handoff_id':inp.get('handoff_id'),
            'engine_claim':result.get('engine'), 'plugin_execution_claim':result.get('plugin_invoked',False),
            'plugin_execution_independently_confirmed':False,
            'verified_outputs':evidence,'errors':errors,
            'notice':'Manifest verification does not equal aesthetic acceptance or proof the ChatGPT Plugin was invoked.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='op',required=True)
    a=sub.add_parser('prepare');a.add_argument('storyboard',type=Path);a.add_argument('--out',type=Path,required=True)
    a.add_argument('--brief',type=Path);a.add_argument('--look',type=Path)
    b=sub.add_parser('verify');b.add_argument('--handoff',type=Path,required=True)
    b.add_argument('--result',type=Path,required=True);b.add_argument('--project',type=Path,required=True)
    b.add_argument('--out',type=Path)
    x=p.parse_args(argv)
    if x.op=='prepare':
        y=prepare(x.storyboard,x.out,x.brief,x.look)
        print('Prepared Remotion plugin handoff',y['handoff_id'],'in',x.out)
    else:
        y=verify(x.handoff,x.result,x.project)
        if x.out:
            x.out.parent.mkdir(parents=True,exist_ok=True)
            x.out.write_text(json.dumps(y,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(y,ensure_ascii=False,indent=2))
        if y['errors']:return 2
    return 0

if __name__=='__main__':sys.exit(main())
