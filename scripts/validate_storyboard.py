#!/usr/bin/env python3
"""Stdlib-only structural and timeline QA for Unified Motion Director storyboards.
Optional JSON Schema compliance: pip install jsonschema; falls back to built-in checks.
Does not validate media assets, rendered frames or licenses.
"""
import argparse
import json
import math
from pathlib import Path
import re
import sys

FIELDS = {"id", "start_sec", "end_sec", "purpose", "why_this_scene", "subject",
          "source_status", "on_screen_text", "frame", "camera", "action", "motion",
          "transition", "sound", "continuity", "keyframe_notes"}
SUBFIELDS = {
    "frame": {"composition", "focal_point", "safe_area"},
    "camera": {"type", "movement"},
    "motion": {"motivation", "easing", "signature_move"},
    "transition": {"type", "shared_element", "seam_note"},
    "sound": {"cue_label", "status"},
    "continuity": {"entry", "exit"},
}


def validate(data, base_dir=None):
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ["Top-level storyboard must be an object"], warnings
    for k in ("film_id", "title", "concept", "duration_sec", "fps", "aspect_ratios", "scenes"):
        if k not in data:
            errors.append(f"Missing film field: {k}")
    fps = data.get("fps")
    if isinstance(fps, bool) or not isinstance(fps, int) or fps <= 0 or fps > 120:
        errors.append("fps must be an integer in 1..120")
        fps = 30
    duration = data.get("duration_sec")
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
        errors.append("duration_sec must be a positive finite number")
        duration = 0
    if not isinstance(data.get("aspect_ratios"), list) or not data["aspect_ratios"]:
        errors.append("aspect_ratios must be a nonempty list")
    else:
        for r in data["aspect_ratios"]:
            if not isinstance(r, str) or not re.fullmatch(r"[1-9][0-9]*:[1-9][0-9]*", r):
                errors.append(f"Invalid aspect ratio: {r!r}")
    pref = data.get("engine_preference")
    if pref is not None and pref not in ("html-seek", "remotion", "web-sim", "mografy"):
        errors.append("engine_preference must name a supported production engine")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes must be a nonempty array")
        return errors, warnings
    last_end = 0.0
    scene_ids = set()
    for i, s in enumerate(scenes):
        ctx = f"scene[{i}]"
        if not isinstance(s, dict):
            errors.append(f"{ctx}: expected object")
            continue
        for missing in sorted(FIELDS - set(s)):
            errors.append(f"{ctx}: missing {missing}")
        sid = s.get("id")
        if not isinstance(sid, str) or not re.fullmatch(r"S\d+", sid):
            errors.append(f"{ctx}: id must look like S01")
        elif sid in scene_ids:
            errors.append(f"{ctx}: duplicate scene id {sid}")
        scene_ids.add(sid)
        st, en = s.get("start_sec"), s.get("end_sec")
        if any(isinstance(n, bool) or not isinstance(n, (int,float)) or not math.isfinite(n) for n in (st,en)):
            errors.append(f"{ctx}: start/end must be finite numbers")
        else:
            if st < 0 or en <= st:
                errors.append(f"{ctx}: invalid interval {st}..{en}")
            if st < last_end - 0.5/fps:
                errors.append(f"{ctx}: overlaps preceding scene by {last_end-st:.3f}s")
            if st > last_end + 0.5/fps:
                errors.append(f"{ctx}: gap before scene {st-last_end:.3f}s")
            if en > duration + 0.5/fps:
                errors.append(f"{ctx}: exceeds declared duration")
            for t in (st, en):
                delta = abs(t*fps - round(t*fps))
                if delta > 0.1:
                    warnings.append(f"{ctx}: time {t:g}s is not exactly on {fps}fps frame boundary")
            last_end = max(last_end, en)
        for k, sub in SUBFIELDS.items():
            v = s.get(k)
            if not isinstance(v, dict):
                errors.append(f"{ctx}.{k}: expected object")
            else:
                for missing in sorted(sub-set(v)):
                    errors.append(f"{ctx}.{k}: missing {missing}")
        for k in ("purpose", "why_this_scene", "subject", "action"):
            if not isinstance(s.get(k), str) or not s[k].strip():
                errors.append(f"{ctx}.{k}: cannot be empty")
        if not isinstance(s.get("on_screen_text"), list) or not all(isinstance(x,str) for x in s["on_screen_text"]):
            errors.append(f"{ctx}.on_screen_text: expected list of strings")
        if not isinstance(s.get("keyframe_notes"), list) or not s["keyframe_notes"]:
            errors.append(f"{ctx}.keyframe_notes: at least one keyframe required")
        # v1.7 additive fields; the original storyboard contract stays valid.
        claim_refs=s.get('claim_refs', [])
        if not isinstance(claim_refs,list) or not all(isinstance(x,str) and x for x in claim_refs) or len(set(claim_refs))!=len(claim_refs):
            errors.append(f"{ctx}.claim_refs: must be unique nonempty IDs")
            claim_refs=[]
        if claim_refs and not data.get('claims_manifest'):
            errors.append(f"{ctx}: claim_refs requires top-level claims_manifest (Product Truth hard gate)")
        for j, event in enumerate(s.get('events', [])):
            if not isinstance(event,dict):errors.append(f"{ctx}.events[{j}]: expected object");continue
            t=event.get('time_sec')
            if isinstance(t,bool) or not isinstance(t,(int,float)) or not math.isfinite(t) or not isinstance(st,(int,float)) or not isinstance(en,(int,float)) or t<st-1e-8 or t>en+1e-8:
                errors.append(f"{ctx}.events[{j}]: time_sec outside owning scene")
            if not isinstance(event.get('action'),str) or not event['action'].strip(): errors.append(f"{ctx}.events[{j}]: action required")
            if not isinstance(event.get('claim_refs',[]),list) or any(x not in claim_refs for x in event.get('claim_refs',[])):
                errors.append(f"{ctx}.events[{j}]: event claims must be declared by the owning scene")
        # v1.8 continuity intent: optional, explicit only when author opts in.
        continuity = s.get('continuity_plan')
        if continuity is not None:
            if not isinstance(continuity, dict) or continuity.get('mode') not in ('carry','anchor','motivated_cut','montage_hit','endcard'):
                errors.append(f"{ctx}.continuity_plan: invalid mode")
            elif continuity['mode'] in ('carry','anchor') and not continuity.get('carrier_id'):
                errors.append(f"{ctx}.continuity_plan: carry/anchor requires carrier_id")
            if not isinstance(continuity, dict) or not isinstance(continuity.get('reason'), str) or len(continuity['reason'].strip()) < 6:
                errors.append(f"{ctx}.continuity_plan: describe the visual meaning of the seam")
        for j,cue in enumerate(s.get('typography_cues', [])):
            if not isinstance(cue,dict):errors.append(f"{ctx}.typography_cues[{j}]: expected object");continue
            times=[cue.get(k) for k in ('enter_sec','settle_sec','exit_sec')]
            if not all(isinstance(t,(int,float)) and not isinstance(t,bool) and math.isfinite(t) for t in times) or not (st<=times[0]<=times[1]<=times[2]<=en):
                errors.append(f"{ctx}.typography_cues[{j}]: time order must be within owning scene")
            groups=cue.get('groups')
            if not isinstance(groups,list) or not groups or not all(isinstance(g,str) and g.strip() for g in groups):
                errors.append(f"{ctx}.typography_cues[{j}]: semantic groups required")
            elif ''.join(''.join(groups).split())!=''.join(str(cue.get('text','')).split()):
                errors.append(f"{ctx}.typography_cues[{j}]: concatenated groups must match the actual text")
            hold=cue.get('reading_hold_sec')
            if hold is not None and (not isinstance(hold,(int,float)) or isinstance(hold,bool) or hold<0 or (isinstance(times[1],(int,float)) and isinstance(times[2],(int,float)) and hold>times[2]-times[1]+1e-8)):
                errors.append(f"{ctx}.typography_cues[{j}]: reading_hold_sec exceeds settled interval")
        source = s.get("source_status")
        if source not in ("verified", "concept", "illustrative"):
            errors.append(f"{ctx}.source_status: invalid {source!r}")
        elif source != "verified":
            warnings.append(f"{ctx}: {source} material cannot be presented as real shipped product UI")
        sound = s.get("sound")
        if isinstance(sound,dict):
            cue = sound.get("cue_time_sec")
            if cue is not None and (not isinstance(cue,(int,float)) or isinstance(cue,bool) or not math.isfinite(cue) or cue < 0 or cue > duration):
                errors.append(f"{ctx}.sound.cue_time_sec: invalid cue")
            if sound.get("status") not in ("measured", "illustrative", "none"):
                errors.append(f"{ctx}.sound.status: invalid")
            if sound.get("status") == "measured" and data.get("audio", {}).get("timing_status") != "measured":
                errors.append(f"{ctx}: cue says measured but soundtrack metadata does not")
    if abs(last_end-duration) > 0.5/fps:
        errors.append(f"Story ends at {last_end:.3f}s but film duration is {duration:.3f}s")
    if data.get("audio", {}).get("timing_status") == "measured" and not data.get("audio", {}).get("music"):
        errors.append("Measured music timing needs a music source in audio.music")
    # v1.8 picture/audio anchors: a timeline contract, never proof of audible sync.
    soundtrack = data.get('audio') or {}
    scene_by_id = {s['id']:s for s in scenes if isinstance(s,dict) and isinstance(s.get('id'),str)}
    seen_cues = set()
    for i,cue in enumerate(soundtrack.get('motion_sync_cues', [])):
        label=f'audio.motion_sync_cues[{i}]'
        if not isinstance(cue,dict): errors.append(f'{label}: expected object');continue
        cid=cue.get('id')
        if not isinstance(cid,str) or not cid.strip() or cid in seen_cues:
            errors.append(f'{label}: cue id must be unique/nonempty')
        seen_cues.add(cid)
        parent=scene_by_id.get(cue.get('scene_id'))
        if parent is None:
            errors.append(f'{label}: unknown scene_id')
            continue
        target=cue.get('picture_time_sec')
        events=[ev for ev in parent.get('events',[]) if isinstance(ev,dict) and ev.get('action')==cue.get('event_action')]
        if len(events)!=1:
            errors.append(f'{label}: event_action must identify exactly one event in scene')
        if isinstance(target,bool) or not isinstance(target,(int,float)) or not math.isfinite(target) or not parent['start_sec']<=target<=parent['end_sec']:
            errors.append(f'{label}: picture_time_sec outside scene')
        elif len(events)==1 and isinstance(events[0].get('time_sec'),(int,float)) and abs(target-events[0]['time_sec'])>0.5/fps+1e-8:
            errors.append(f'{label}: picture_time_sec must match identified event to half a frame')
        anchor=cue.get('audio_anchor_sec')
        if anchor is not None and (isinstance(anchor,bool) or not isinstance(anchor,(int,float)) or not math.isfinite(anchor) or not 0<=anchor<=duration):
            errors.append(f'{label}: audio_anchor_sec invalid')
        if anchor is None and cue.get('priority') in ('hero','primary') and cue.get('alignment') != 'free':
            errors.append(f'{label}: sync to music needs audio_anchor_sec (or alignment free)')
        offset=cue.get('intentional_offset_sec',0)
        if isinstance(offset,bool) or not isinstance(offset,(int,float)) or not math.isfinite(offset) or abs(offset)>10:
            errors.append(f'{label}: intentional_offset_sec invalid')
        if cue.get('source_status')=='measured':
            if soundtrack.get('timing_status')!='measured' or not soundtrack.get('music') or not soundtrack.get('measurement_evidence') or anchor is None:
                errors.append(f'{label}: measured sync requires soundtrack, audio anchor and measurement_evidence')
            else:
                warnings.append(f'{label}: measured is a producer claim; listening/render QA not performed here')
        elif cue.get('source_status') in ('illustrative','candidate_unverified'):
            warnings.append(f'{label}: timing is not verified against real audio')
    bg=data.get('beat_grid')
    if bg is not None and (not isinstance(bg,dict) or bg.get('status') not in ('candidate_unverified','human_verified','illustrative')):
        errors.append('beat_grid status invalid')
    claims_path=data.get('claims_manifest')
    if claims_path:
        if not isinstance(claims_path,str):errors.append('claims_manifest must be a filename')
        elif base_dir is not None:
            path=(Path(base_dir)/claims_path).resolve()
            if not path.is_relative_to(Path(base_dir).resolve()):
                errors.append('claims_manifest must remain within storyboard folder')
            elif not path.is_file(): errors.append(f'claims_manifest missing: {claims_path}')
            else:
                try:
                    from product_truth import load_and_validate
                    errors.extend('Product Truth: '+e for e in load_and_validate(path,None))
                    import json as _json
                    entries=_json.loads(path.read_text()).get('claims',[])
                    ids={e['id']:e for e in entries if isinstance(e,dict) and 'id' in e}
                    for scene in scenes:
                        if not isinstance(scene,dict):continue
                        for ref in scene.get('claim_refs',[]):
                            if ref not in ids: errors.append(f'{scene.get("id","?")}: unknown claim {ref}')
                            elif ids[ref].get('display_mode')=='omitted': errors.append(f'{scene.get("id","?")}: omitted claim {ref}')
                            elif ids[ref].get('display_mode')=='concept_demo' and ids[ref].get('disclosure') not in scene.get('on_screen_text',[]):
                                errors.append(f'{scene.get("id","?")}: concept claim {ref} missing exact on-screen disclosure')
                except (OSError,ValueError) as e:errors.append('Product Truth manifest parse error: '+str(e))
        else: warnings.append('claims_manifest named but no base_dir passed; run CLI for Product Truth validation')
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("storyboard", type=Path)
    ap.add_argument("--json", action="store_true", help="Machine-readable report")
    args = ap.parse_args()
    try:
        data = json.loads(args.storyboard.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot load storyboard: {e}", file=sys.stderr)
        return 2
    errors, warnings = validate(data, args.storyboard.resolve().parent)
    try:
        import jsonschema
        schema = json.loads((Path(__file__).resolve().parents[1]/"templates"/"storyboard.schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        for e in validator.iter_errors(data):
            msg = f"schema: {'/'.join(map(str,e.path))}: {e.message}"
            if msg not in errors:
                errors.append(msg)
    except ImportError:
        warnings.append("jsonschema package not installed; ran built-in checks only")
    result = {"ok":not errors,"errors":errors,"warnings":warnings,"scenes":len(data.get("scenes", []))}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if result["ok"] else "FAIL", args.storyboard)
        for e in errors:
            print("  ERROR:", e)
        for w in warnings:
            print("  NOTE:", w)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
