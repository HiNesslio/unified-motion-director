#!/usr/bin/env python3
"""Post-render independent juror review and deterministic scoring.
Never produces a passing score without two externally generated, evidence-backed reviews.
Use: prepare VIDEO --out DIR; run --bundle DIR --project PROJECT; aggregate --bundle DIR.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
RUBRICS = {
    'aesthetic': {'composition':30, 'hierarchy':25, 'typography':15, 'distinctiveness':20, 'cohesion':10},
    'holistic': {'story':25, 'timing':20, 'continuity':20, 'comprehension':15, 'sound':10, 'execution':10},
}
REVIEWERS = {'aesthetic':'motion-aesthetic-juror', 'holistic':'motion-holistic-juror'}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''): digest.update(block)
    return digest.hexdigest()


def load_json(path:Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def normalize_json_reply(stdout:str):
    """Accept one strict Codex JSON result."""
    data=json.loads(stdout.strip())
    if isinstance(data, dict) and isinstance(data.get('result'), str):
        return json.loads(data['result'].strip())
    return data


def audio_policy(policy, meta, storyboard: Path | None):
    if policy!='auto': return policy
    if storyboard and storyboard.is_file():
        obj=load_json(storyboard)
        music=str((obj.get('audio') or {}).get('music') or '').strip().lower()
        if any(x in music for x in ['none','silent','無聲','無音樂','沒有音樂']): return 'silent'
        if music: return 'required'
    if meta['audio_present']: return 'required'
    return 'unknown'


def prepare(a):
    video=a.video.expanduser().resolve()
    if not video.is_file() or not video.stat().st_size:
        raise ValueError('A real non-empty rendered video is required. Concept storyboard alone cannot be scored.')
    if not shutil.which('ffprobe') or not shutil.which('ffmpeg'):
        raise RuntimeError('ffmpeg + ffprobe required to verify rendered film and extract evidence')
    out=a.out.expanduser().resolve(); out.mkdir(parents=True,exist_ok=True)
    from video_reference_sheet import media_info
    info=media_info(video)
    info['sha256']=sha256_file(video)
    args=[sys.executable, str(ROOT/'scripts'/'video_reference_sheet.py'), str(video), '--out', str(out/'visual-evidence'), '--samples', str(a.samples)]
    subprocess.run(args,check=True)
    frame_meta=load_json(out/'visual-evidence'/'metadata.json')
    evidence_frames=sorted((out/'visual-evidence'/'frames').glob('*.png'))
    if len(evidence_frames)!=a.samples: raise RuntimeError('Decoded frame count incomplete; cannot begin juror review')
    brief=a.brief.expanduser().resolve() if a.brief else None
    storyboard=a.storyboard.expanduser().resolve() if a.storyboard else None
    if brief and not brief.is_file(): raise ValueError('Brief does not exist')
    if storyboard and not storyboard.is_file(): raise ValueError('Storyboard does not exist')
    # Codex v1.5: technical evidence is advisory, never an aesthetic judgement.
    from motion_preflight import inspect as technical_inspect
    technical=technical_inspect(video, storyboard, sample=True)
    if technical['sha256']!=info['sha256']:
        raise RuntimeError('Preflight/checksum mismatch: video changed while preparing review')
    technical_file=out/'technical-preflight.json'
    technical_file.write_text(json.dumps(technical,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    policy=audio_policy(a.audio_policy, info, storyboard)
    manifest={
        'schema_version':'1.3', 'created_at':datetime.now(timezone.utc).isoformat(),
        'video':str(video), 'video_sha256':info['sha256'], 'file_size_bytes':video.stat().st_size,
        'media':info, 'brief':str(brief) if brief else None,
        'storyboard':str(storyboard) if storyboard else None,
        'audio_policy':policy, 'rights_status':a.rights_status,
        'contact_sheet':str(out/'visual-evidence'/'contact-sheet.jpg'),
        'frames_dir':str(out/'visual-evidence'/'frames'),
        'sample_timecodes':frame_meta['sample_timecodes'],
        'technical_preflight':str(technical_file),
        'technical_preflight_signals':[x.get('type') for x in technical['issues']],
        'review_status':'NOT_REVIEWED',
    }
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'bundle':str(out),'video_sha256':info['sha256'],'frame_count':len(evidence_frames),'audio_policy':policy,'review_status':'NOT_REVIEWED'},ensure_ascii=False,indent=2))


def verified_bundle(bundle:Path):
    m=load_json(bundle/'manifest.json')
    video=Path(m['video'])
    if not video.is_file() or sha256_file(video)!=m['video_sha256']:
        raise ValueError('Video missing or SHA-256 mismatch: report invalidated by re-render/replacement')
    if not Path(m['contact_sheet']).is_file(): raise ValueError('Contact sheet not found')
    frames=sorted(Path(m['frames_dir']).glob('*.png'))
    if len(frames)<6: raise ValueError('At least 6 decoded frames are required')
    return m, frames


def judge_prompt(judge, manifest, frames):
    # Separate contexts; neither sees the other report, prior iterations, or author's self-review.
    instructions=(ROOT/'references'/'reviewers'/f'{REVIEWERS[judge]}.md').resolve()
    return (f'Perform an INDEPENDENT {judge} review of this real rendered film. Follow your role instructions. '
      'Inspect attached contact sheet and full-resolution PNG images; do not rate from prompts alone. '
      'Do not read the other agent\'s files, other scoring results or the production implementation. '
      'Return ONLY valid JSON according to the schema.\n'
      f'Role file: {instructions}\n'
      f'Report schema: {(ROOT/"templates"/"juror-report.schema.json").resolve()}\n'
      f'Rubric: {(ROOT/"references"/"independent-acceptance.md").resolve()}\n'
      f'Video: {manifest["video"]}\nSHA-256: {manifest["video_sha256"]}\n'
      f'Contact sheet: {manifest["contact_sheet"]}\n'
      f'Full frame directory: {manifest["frames_dir"]} (inspect at least six distinct timecoded files)\n'
      f'Selected frame names: {[f.name for f in frames[:3]]} ... {[f.name for f in frames[-3:]]}\n'
      f'Duration seconds: {manifest["media"]["duration_s"]}\n'
      f'Audio policy: {manifest["audio_policy"]}; audio stream present: {manifest["media"]["audio_present"]}. '
      'Do not claim sound quality or sync without actual audio playback/analysis evidence.\n'
      f'Rights status (producer declaration, not independent proof): {manifest["rights_status"]}\n'
      f'Brief: {manifest["brief"] or "not provided"}\n'
      f'Storyboard: {manifest["storyboard"] or "not provided"}\n'
      f'Technical preflight: {manifest.get("technical_preflight", "not supplied")}. ' 
      f'Suspected technical concerns (not final findings): {manifest.get("technical_preflight_signals",[])}. ' 
      'Verify suspect times by examining actual decoded transition frames, not by trusting automated detection.\n'
      'Set inspected_frames to 6+ actual PNG basenames that YOU OPENED, not a guessed sampling list. '
      'Dimensions and fixes must include precise timecodes. Your verdict is not required; aggregation is external.')


def selected_frame_paths(frames, max_frames=8):
    """Select broadly spaced decoded PNGs for explicit input attachment."""
    if len(frames) <= max_frames: return frames
    indices=sorted(set(round(i*(len(frames)-1)/(max_frames-1)) for i in range(max_frames)))
    return [frames[i] for i in indices]


def codex_command(cli, manifest, frames, output_file):
    # --image ensures these are actually presented as image input, not only named in text.
    images=[Path(manifest['contact_sheet']), *selected_frame_paths(frames)]
    cmd=[cli,'exec','--sandbox','read-only','--skip-git-repo-check',
         '--output-last-message',str(output_file)]
    for img in images: cmd.extend(['--image',str(img)])
    cmd.append('-')
    return cmd, images


def run(a):
    """Two separate authenticated Codex CLI sessions, each with actual image attachments.

    No native subagents spawned here; that is an *alternative* interactive workflow.
    Both paths share the same deterministic aggregate validation.
    """
    bundle=a.bundle.expanduser().resolve()
    manifest, frames=verified_bundle(bundle)
    cli=shutil.which('codex')
    if not cli:
        raise RuntimeError('Codex CLI unavailable. No independent jurors launched, no scores generated. Use native Codex subagents or install/login to Codex CLI.')
    project=a.project.expanduser().resolve()
    if not project.is_dir(): raise ValueError(f'Codex project directory not found: {project}')
    def invoke(judge):
        prompt=judge_prompt(judge,manifest,frames)
        images=[Path(manifest['contact_sheet']), *selected_frame_paths(frames)]
        prompt += ('\nATTACHED MEDIA: the first image is the contact sheet; the following images are actual full-resolution '
                   'decoded PNGs named in order: '+', '.join(img.name for img in images[1:])+
                   '. Mark inspected_frames with only individual PNGs you truly inspected. '
                   'These represent sampled instants, so qualify inferences about motion. '
                   'DO NOT claim audio was audited unless you separately inspected/listened to sound. '
                   'If required music is unaudited, sound MUST be not_evaluated/null and result will be HOLD_EVIDENCE. '
                   'Read the juror role contract included next. Do not change files or access peer ratings.\n'
                   +(ROOT/'references'/'reviewers'/f'{REVIEWERS[judge]}.md').read_text(encoding='utf8'))
        with tempfile.TemporaryDirectory(prefix=f'codex-motion-{judge}-') as td:
            last=Path(td)/'last-message.json'
            cmd, attached=codex_command(cli,manifest,frames,last)
            try:
                p=subprocess.run(cmd,input=prompt,cwd=project,capture_output=True,text=True,timeout=a.timeout)
            except subprocess.TimeoutExpired:
                return judge,False, f'{judge}: Codex review timeout after {a.timeout}s'
            if p.returncode != 0:
                return judge,False, f'{judge}: codex exec failed ({p.returncode}): {p.stderr[-900:]}'
            try:
                payload=last.read_text(encoding='utf8') if last.exists() else p.stdout
                result=normalize_json_reply(payload)
                if not isinstance(result,dict): raise ValueError('not a JSON object')
            except Exception as e:
                return judge,False, f'{judge}: response not usable as JSON ({e})'
        (bundle/f'juror-{judge}.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
        return judge,True,str(bundle/f'juror-{judge}.json')
    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes=list(pool.map(invoke,REVIEWERS.keys()))
    print(json.dumps({'reviewer_sessions':'two independent codex exec sessions (not in-app subagents)',
                      'results':outcomes},indent=2,ensure_ascii=False))
    if not all(ok for _,ok,_ in outcomes):
        raise RuntimeError('One or both Codex reviewers failed: no acceptance PASS possible.')
    aggregate_impl(bundle)


def valid_report(report, role, manifest, frame_names, errors):
    if not isinstance(report, dict):
        errors.append(f'{role}: report must be JSON object'); return None
    if report.get('judge')!=role or report.get('reviewer_name')!=REVIEWERS[role]:
        errors.append(f'{role}: wrong reviewer identity'); return None
    if report.get('media_sha256')!=manifest['video_sha256']:
        errors.append(f'{role}: SHA mismatch with rendered video'); return None
    if report.get('evidence_level')!='DECODED_VIDEO':
        errors.append(f'{role}: not based on decoded frames'); return None
    seen=report.get('inspected_frames')
    if not isinstance(seen,list) or len(set(seen))<6 or any(Path(f).name!=f or f not in frame_names for f in seen):
        errors.append(f'{role}: need 6+ distinct actual decoded frame basenames in inspected_frames'); return None
    confidence=report.get('confidence')
    if type(confidence) not in (int,float) or not 0<=confidence<=1 or confidence<0.5:
        errors.append(f'{role}: missing/low confidence (<0.5)'); return None
    dim=report.get('dimensions')
    if not isinstance(dim,dict) or set(dim)!=set(RUBRICS[role]):
        errors.append(f'{role}: score dimension set mismatch'); return None
    duration=float(manifest['media']['duration_s'])
    score_acc=0.; weights=0.
    for name,weight in RUBRICS[role].items():
        data=dim.get(name)
        if not isinstance(data,dict): errors.append(f'{role}.{name}: expected object'); continue
        status=data.get('status'); val=data.get('score'); ev=data.get('evidence')
        if status=='not_applicable' and role=='holistic' and name=='sound' and manifest['audio_policy']=='silent':
            if val is not None: errors.append(f'{role}.sound: not_applicable must have null score')
            continue
        if status=='not_evaluated' and role=='holistic' and name=='sound':
            if val is not None: errors.append('holistic.sound: unevaluated must be null')
            errors.append('holistic.sound: not audited, cannot release yet')
            continue
        if status!='evaluated' or type(val) not in (int,float) or not 0<=val<=10:
            errors.append(f'{role}.{name}: missing evaluated numeric score 0..10')
            continue
        if not isinstance(ev,list) or not ev:
            errors.append(f'{role}.{name}: missing timestamped evidence')
            continue
        for item in ev:
            if not isinstance(item,dict) or type(item.get('time_sec')) not in (int,float) or not 0<=item['time_sec']<=duration or not isinstance(item.get('observation'),str) or len(item['observation'].strip())<6:
                errors.append(f'{role}.{name}: invalid timecode/observation')
        score_acc+=float(val)*weight
        weights+=weight
    fixes=report.get('fixes')
    if not isinstance(fixes,list) or len(fixes)<2:
        errors.append(f'{role}: at least two actionable fixes required')
    else:
        for fix in fixes:
            if not isinstance(fix,dict) or fix.get('priority') not in ('P1','P2','P3') or type(fix.get('time_sec')) not in (int,float) or not 0<=fix['time_sec']<=duration or not str(fix.get('action','')).strip() or not str(fix.get('issue','')).strip():
                errors.append(f'{role}: invalid fix/timecode')
    blockers=report.get('blockers')
    if not isinstance(blockers,list): errors.append(f'{role}: blockers must be a list')
    else:
        for item in blockers:
            if not isinstance(item,dict) or not str(item.get('reason','')).strip() or not str(item.get('kind','')).strip(): errors.append(f'{role}: invalid blocker')
    if weights<=0: return None
    return round(score_acc/weights*10,1)


def md_report(bundle, manifest, scored, final, verdict, errors, blockers, fixes):
    md=['# Independent Motion Design Acceptance Report', '',f'**Status:** {verdict}',
        f'**Video:** `{manifest["video"]}`',f'**SHA-256:** `{manifest["video_sha256"]}`',
        f'**Evidence:** `{manifest["contact_sheet"]}`',
        f'**Audio policy:** {manifest["audio_policy"]} · **Rights declaration:** {manifest["rights_status"]}',
        '', '| Reviewer (isolated) | Score / 100 | Weight |', '|---|---:|---:|',
        f'| Visual aesthetic | {scored.get("aesthetic", "N/A")} | 55% |',
        f'| Holistic film | {scored.get("holistic", "N/A")} | 45% |',
        f'| **Total** | **{final if final is not None else "N/A"}** | **100%** |',
        '', '## Release blockers']
    md+= [f'- {s}' for s in blockers] if blockers else ['- None found in submitted reports (not proof of absence)']
    md+=['','## Unverified evidence / structural validation']
    md += [f'- {s}' for s in errors] if errors else ['- Required structure and evidence references validated']
    md+=['','## Top revisions']
    md+= [f'{i}. **{x.get("priority","P1")} · {x.get("time_sec","?")}s** — {x.get("issue","")}: {x.get("action","")}' for i,x in enumerate(fixes[:3],1)] if fixes else ['- Need verified judge reports']
    md+=['','## Review provenance','- Two reviewer output files are required, one per separately executed juror.', '- Scores describe this exact hash only; after a new render, run both jurors again.', '- Human aesthetic agreement is not guaranteed; no creator score substituted.']
    (bundle/'ACCEPTANCE.md').write_text('\n'.join(md)+'\n',encoding='utf-8')


def aggregate_impl(bundle):
    manifest,frames=verified_bundle(bundle)
    errors=[]; scored={}; blockers=[]; fixes=[]; reports={}
    frame_names={f.name for f in frames}
    for role in REVIEWERS:
        f=bundle/f'juror-{role}.json'
        if not f.is_file(): errors.append(f'{role}: independent report not found'); continue
        try: report=load_json(f)
        except Exception as e: errors.append(f'{role}: invalid JSON: {e}'); continue
        reports[role]=report
        score=valid_report(report,role,manifest,frame_names,errors)
        if score is not None: scored[role]=score
        for b in report.get('blockers',[]):
            if isinstance(b,dict): blockers.append(f'{role}: {b.get("kind","issue")} @ {b.get("time_sec","?")}s — {b.get("reason","")}')
        for item in report.get('fixes',[]):
            if isinstance(item,dict): fixes.append(item)
    if manifest['audio_policy']=='unknown': errors.append('Audio intent unknown: set --audio-policy required or silent')
    if manifest['audio_policy']=='required' and not manifest['media']['audio_present']:
        blockers.append('Missing required soundtrack: MP4 has no audio stream')
    if manifest['rights_status']!='confirmed':
        errors.append('Rights/asset provenance not confirmed; --rights-status confirmed only after checking licenses and real product assets')
    if manifest['audio_policy']=='silent' and manifest['media']['audio_present']:
        errors.append('Silent policy conflicts with detected audio stream')
    final=None
    if set(scored)==set(REVIEWERS) and not errors:
        final=round(scored['aesthetic']*.55+scored['holistic']*.45,1)
    if errors: verdict='HOLD_EVIDENCE'
    elif blockers: verdict='BLOCKED'
    elif abs(scored['aesthetic']-scored['holistic'])>=20: verdict='NEEDS_ADJUDICATION'
    elif final<70: verdict='REWORK'
    elif final<85 or min(scored.values())<80: verdict='REVISE'
    else: verdict='PASS'
    fixes.sort(key=lambda x: {'P1':0,'P2':1,'P3':2}.get(x.get('priority'),3))
    record={'verdict':verdict,'composite_score':final,'judge_scores':scored,'weights':{'aesthetic':.55,'holistic':.45},'critical_blockers':blockers,'evidence_errors':errors,
       'top_fixes':fixes[:3], 'video_sha256':manifest['video_sha256'],'evaluated_at':datetime.now(timezone.utc).isoformat(), 'reviewer_count':len(reports)}
    (bundle/'acceptance.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
    md_report(bundle, manifest, scored,final,verdict,errors,blockers,fixes)
    print(json.dumps({'acceptance':str(bundle/'ACCEPTANCE.md'),**record},ensure_ascii=False,indent=2))
    return verdict


def main():
    pa=argparse.ArgumentParser(description='Evidence-gated independent subagent review; never fabricate taste scores')
    sub=pa.add_subparsers(dest='command',required=True)
    p=sub.add_parser('prepare',help='Freeze video and decode timecoded evidence')
    p.add_argument('video',type=Path);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--brief',type=Path);p.add_argument('--storyboard',type=Path)
    p.add_argument('--samples',type=int,default=48)
    p.add_argument('--audio-policy',choices=('auto','silent','required'),default='auto')
    p.add_argument('--rights-status',choices=('unknown','confirmed'),default='unknown')
    q=sub.add_parser('run',help='Run two isolated Codex CLI sessions with image attachments; then aggregate')
    q.add_argument('--bundle',type=Path,required=True);q.add_argument('--project',type=Path,required=True)
    q.add_argument('--timeout',type=int,default=600,help='Seconds per juror CLI session')
    r=sub.add_parser('aggregate',help='Validate two independent report JSON files and calculate gate')
    r.add_argument('--bundle',required=True,type=Path)
    a=pa.parse_args()
    try:
        if a.command=='prepare':
            if not 6<=a.samples<=120: raise ValueError('--samples must be 6..120')
            prepare(a)
        elif a.command=='run': run(a)
        else: aggregate_impl(a.bundle.expanduser().resolve())
    except (ValueError,FileNotFoundError,RuntimeError,subprocess.CalledProcessError,subprocess.TimeoutExpired,json.JSONDecodeError) as e:
        print(f'ERROR: {e}',file=sys.stderr);sys.exit(2)

if __name__=='__main__': main()
