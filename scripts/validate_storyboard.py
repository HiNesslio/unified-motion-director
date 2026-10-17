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


def validate(data):
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
    errors, warnings = validate(data)
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
