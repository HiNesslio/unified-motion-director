#!/usr/bin/env python3
"""Render a read-only offline HTML director storyboard board; NOT an animated film."""
import argparse
import html
import json
from pathlib import Path
import sys

from validate_storyboard import validate


def esc(v):
    return html.escape(str(v or ""))


def make_board(data):
    film, duration = esc(data["title"]), data["duration_sec"]
    blocks = []
    for s in data["scenes"]:
        timecode = f"{s['start_sec']:g}–{s['end_sec']:g}s"
        tag = "Concept" if s["source_status"] != "verified" else "Verified source"
        copy = " · ".join(esc(x) for x in s["on_screen_text"]) or "No on-screen text"
        frame = s["frame"]
        notes = "".join(f"<li>{esc(n)}</li>" for n in s["keyframe_notes"])
        pct = 100*(s["end_sec"]-s["start_sec"])/duration
        blocks.append(f'''<section class="shot">
          <div class="shot-top"><span class="shot-id">{esc(s['id'])} <small>{esc(timecode)}</small></span><span class="tag">{tag}</span></div>
          <div class="visual"><div class="visual-kicker">COMPOSITION · {esc(s['camera']['type'])}</div>
            <div class="focus">{esc(s['subject'])}</div><div class="visual-foot">{esc(frame['composition'])}</div></div>
          <h2>{esc(s['purpose'])}</h2><p class="copy">{copy}</p>
          <p>{esc(s['why_this_scene'])}</p>
          <dl><dt>Camera</dt><dd>{esc(s['camera']['movement'])}</dd>
              <dt>Action</dt><dd>{esc(s['action'])}</dd>
              <dt>Motion</dt><dd>{esc(s['motion']['signature_move'])} · {esc(s['motion']['easing'])}</dd>
              <dt>Transition</dt><dd>{esc(s['transition']['type'])}: {esc(s['transition']['seam_note'])}</dd>
              <dt>Sound</dt><dd>{esc(s['sound']['cue_label'])} ({esc(s['sound']['status'])})</dd></dl>
          <details><summary>Keyframes / handoff</summary><ul>{notes}</ul>
          <p><b>Entry:</b> {esc(s['continuity']['entry'])}</p><p><b>Exit:</b> {esc(s['continuity']['exit'])}</p></details>
          <div class="shot-span" style="width:{pct:.4f}%"></div>
        </section>''')
    marks = "".join(f'<div class="mark" style="width:{100*(s["end_sec"]-s["start_sec"])/duration:.4f}%"></div>' for s in data["scenes"])
    css = '''
    :root{color-scheme:light;font-family:Inter,"Noto Sans TC",-apple-system,BlinkMacSystemFont,Arial,sans-serif}
    *{box-sizing:border-box}body{margin:0;background:#f5f5f2;color:#16181c;padding:48px 32px}
    main{max-width:1200px;margin:auto}header{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:28px}
    .eyebrow{letter-spacing:.17em;text-transform:uppercase;color:#6a727b;font-size:11px;font-weight:700}
    h1{font-size:clamp(28px,4vw,46px);letter-spacing:-.05em;line-height:1.05;margin:10px 0}h2{font-size:19px;line-height:1.25;margin:17px 0 8px;letter-spacing:-.025em}
    .desc{font-size:14px;line-height:1.7;color:#626a70;max-width:570px}
    .track{height:11px;display:flex;overflow:hidden;border-radius:30px;gap:2px;margin:24px 0 30px}
    .mark{background:#252f42}.mark:nth-child(even){background:#f6a14a}
    .stats{font-size:12px;color:#687080;white-space:nowrap}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:17px}
    .shot{position:relative;background:#fff;border:1px solid #e0e2e4;border-radius:14px;padding:16px;overflow:hidden;display:flex;flex-direction:column;min-width:0}
    .shot-top{display:flex;align-items:center;justify-content:space-between;margin:0 0 14px}
    .shot-id{font-size:12px;font-weight:800;letter-spacing:.06em}.shot-id small{font-weight:500;color:#727b85;letter-spacing:0;margin-left:6px}
    .tag{font-size:10px;font-weight:650;border:1px solid #d4d8d9;border-radius:20px;padding:5px 8px;color:#616970}
    .visual{aspect-ratio:16/10;background:#eaeef0;border:1px solid #e0e5e9;border-radius:9px;padding:15px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}
    .visual-kicker,.visual-foot{font-size:10px;color:#66737e;letter-spacing:.04em;line-height:1.5}.visual-kicker{text-transform:uppercase}
    .focus{font-size:clamp(19px,2vw,27px);font-weight:700;color:#253044;letter-spacing:-.04em;line-height:1.2;max-width:90%}
    .copy{color:#b0671a;font-size:13px;font-weight:700}.shot p{font-size:12px;line-height:1.6;color:#52606a}
    dl{display:grid;grid-template-columns:75px 1fr;gap:7px 12px;font-size:11px;line-height:1.5;margin:12px 0}dt{color:#838b92}dd{margin:0;color:#26323c}
    details{margin:8px 0 16px;font-size:11px;line-height:1.65;color:#52606a}summary{font-size:11px;font-weight:650;cursor:pointer;color:#243040}
    ul{padding-left:16px}.shot-span{height:4px;background:#f6a14a;position:absolute;bottom:0;left:0}
    footer{font-size:12px;color:#79818a;margin-top:27px}@media(max-width:1000px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
    @media(max-width:640px){body{padding:25px 15px}header{display:block}.grid{grid-template-columns:1fr}.stats{margin-top:10px}}
    @media print{body{padding:0;background:white}.shot{break-inside:avoid}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}details{display:block}footer{margin:6px}}
    '''
    return ("<!doctype html><html lang='zh-Hant'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{film} — Director board</title><style>{css}</style></head><body><main>"
            f"<header><div><div class='eyebrow'>Unified Motion Director · planning artifact</div><h1>{film}</h1>"
            f"<div class='desc'>{esc(data['concept'])}</div></div>"
            f"<div class='stats'>{duration:g}s · {esc(data['fps'])}fps · {esc(', '.join(data['aspect_ratios']))}</div></header>"
            f"<div class='track'>{marks}</div><div class='grid'>{''.join(blocks)}</div>"
            "<footer>Planning storyboard only. Frames are schematic text descriptions, not actual rendered product screens or a final film.</footer>"
            "</main></body></html>")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("storyboard", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    try:
        data = json.loads(args.storyboard.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Cannot load storyboard: {e}",file=sys.stderr)
        return 2
    errors, _ = validate(data)
    if errors:
        print("Invalid storyboard: " + "; ".join(errors), file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(make_board(data),encoding="utf-8")
    print(f"Created {args.output} (storyboard preview, not video)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
