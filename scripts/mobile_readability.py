#!/usr/bin/env python3
"""Heuristic mobile legibility preflight from renderer-supplied text boxes.

Requires measured geometry; never infer successful readability without input.
Schema: {"canvas":{"width":1080,"height":1920},"texts":[{"text":"...",
"x":120,"y":300,"width":500,"height":80,"font_px":40,
"settle_sec":1.0,"exit_sec":2.5,"language":"zh-Hant"}]}.
"""
import argparse
import json
from pathlib import Path
import math
import sys


def inspect_layout(doc,target_width=360):
    problems=[]
    canvas=doc.get('canvas',{})
    w,h=canvas.get('width'),canvas.get('height')
    if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and x>0 for x in (w,h)):
        return {'status':'NOT_EVALUATED','issues':[{'kind':'invalid_canvas'}],'measurements':[]}
    if not isinstance(doc.get('texts'),list):
        return {'status':'NOT_EVALUATED','issues':[{'kind':'missing_text_boxes'}],'measurements':[]}
    margin=0.05*w; scale=target_width/w; measures=[]
    for i,x in enumerate(doc['texts']):
        try:
            vals={k:float(x[k]) for k in ('x','y','width','height','font_px','settle_sec','exit_sec')}
            if not all(math.isfinite(v) for v in vals.values()):raise ValueError('nonfinite geometry')
        except (KeyError,TypeError,ValueError):
            problems.append({'index':i,'kind':'missing_or_invalid_geometry'});continue
        text=str(x.get('text',''))
        font=vals['font_px']*scale; hold=vals['exit_sec']-vals['settle_sec']
        label={'index':i,'text':text,'font_px_at_target':round(font,2),'hold_sec':round(hold,3)}
        measures.append(label)
        if font<14:problems.append({'index':i,'kind':'font_too_small','observed_px':round(font,2),'threshold_px':14})
        if vals['x']<margin or vals['y']<margin or vals['x']+vals['width']>w-margin or vals['y']+vals['height']>h-margin:
            problems.append({'index':i,'kind':'outside_mobile_safe_area'})
        # Chinese ideographs are not treated as whitespace-delimited words.
        meaningful=sum(1 for c in text if not c.isspace())
        needed=max(.9, min(3.5, .65+.10*meaningful))
        if hold+1e-5<needed:problems.append({'index':i,'kind':'insufficient_read_hold','observed_sec':round(hold,3),'suggested_min_sec':round(needed,3)})
        if vals['width']<=0 or vals['height']<=0 or vals['font_px']<=0:problems.append({'index':i,'kind':'nonpositive_box'})
    return {'status':'CANDIDATE_ISSUES' if problems else 'GEOMETRY_HEURISTICS_CLEAR_NOT_VISUAL_APPROVAL',
            'target_width_px':target_width,'issues':problems,'measurements':measures,
            'limitations':['Requires trusted actual render geometry','No OCR, font fallback confirmation or subjective reading test performed']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('layout',type=Path);p.add_argument('--out',type=Path);p.add_argument('--width',type=int,default=360)
    a=p.parse_args()
    try:result=inspect_layout(json.loads(a.layout.read_text()),a.width)
    except (OSError,ValueError) as e:print('ERROR:',e,file=sys.stderr);return 1
    payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(payload)
    else:print(payload)
    return 0

if __name__=='__main__':sys.exit(main())
