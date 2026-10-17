#!/usr/bin/env python3
"""Make a timecode contact sheet from a locally supplied, legally obtained video.
Does not fetch remote videos or assert that extracted samples prove beat synchronization.
"""
import argparse, json, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def media_info(video):
    if not shutil.which('ffprobe'):
        raise RuntimeError('ffprobe missing')
    cmd = ['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]
    data = json.loads(subprocess.run(cmd, capture_output=True, check=True, text=True).stdout)
    vids=[s for s in data['streams'] if s['codec_type']=='video']
    if not vids: raise ValueError('No video stream')
    d=float(data.get('format',{}).get('duration') or vids[0].get('duration') or 0)
    if d<=0: raise ValueError('Unknown/invalid duration')
    s=vids[0]
    return {'duration_s':d,'width':s.get('width'),'height':s.get('height'),'frame_rate':s.get('avg_frame_rate'),'codec':s.get('codec_name'), 'audio_present':any(t['codec_type']=='audio' for t in data['streams'])}


def timecode(seconds):
    return f'{int(seconds // 60):02d}:{seconds % 60:06.3f}'


def main():
    pa=argparse.ArgumentParser(description='Export timecoded video sample frames + contact sheet')
    pa.add_argument('video', type=Path)
    pa.add_argument('--out', type=Path, default=Path('reference-review'))
    pa.add_argument('--samples',type=int,default=20,help='uniform samples; min 4 max 120')
    pa.add_argument('--columns',type=int,default=4)
    a=pa.parse_args()
    if not a.video.is_file(): pa.error(f'Video not found: {a.video}')
    if not shutil.which('ffmpeg'): pa.error('ffmpeg missing')
    if not (4<=a.samples<=120): pa.error('--samples must be 4..120')
    if not (1<=a.columns<=8): pa.error('--columns must be 1..8')
    meta=media_info(a.video)
    a.out.mkdir(parents=True,exist_ok=True)
    frame_dir=a.out/'frames';frame_dir.mkdir(exist_ok=True)
    # Leave a safe final-frame margin: container duration can exceed the last decodeable frame.
    rate=meta.get('frame_rate') or '30/1'
    try:
        num,den=rate.split('/')
        fps=float(num)/float(den)
    except (ValueError,ZeroDivisionError):
        fps=30.0
    tail=max(0.11,2.0 / fps)
    moments=[(i / (a.samples-1)) * max(meta['duration_s']-tail,0) for i in range(a.samples)]
    tiles=[]
    for i,t in enumerate(moments):
        fname=frame_dir/f'{i:03d}_{t:09.3f}s.png'
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',f'{t:.3f}','-i',str(a.video),'-frames:v','1','-vf','scale=390:220:force_original_aspect_ratio=decrease,pad=390:220:(ow-iw)/2:(oh-ih)/2:color=black','-pix_fmt','rgb24',str(fname)]
        subprocess.run(cmd,check=True)
        if not fname.exists(): raise RuntimeError(f'No frame at {t}')
        with Image.open(fname) as im: tiles.append(im.copy())
    cols=min(a.columns,a.samples); rows=math.ceil(a.samples/cols)
    tile_w,tile_h=390,250
    board=Image.new('RGB',(cols*tile_w,rows*tile_h),(248,248,248));draw=ImageDraw.Draw(board)
    for i,(frame,t) in enumerate(zip(tiles,moments)):
        x=(i%cols)*tile_w; y=(i//cols)*tile_h
        board.paste(frame,(x,y)); draw.text((x+8,y+226),f'#{i:02d} · {timecode(t)}',fill=(20,20,20))
    out=a.out/'contact-sheet.jpg';board.save(out,quality=92)
    meta['video_source']=str(a.video.resolve());meta['sampling']='uniform; missing cuts between samples possible';meta['sample_timecodes']=[round(t,3) for t in moments];meta['evidence_level']='DECODED_VIDEO frames only; audio not examined'
    (a.out/'metadata.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'contact_sheet':str(out),'metadata':str(a.out/'metadata.json'),'frame_count':len(tiles),'duration_s':meta['duration_s']},ensure_ascii=False))

if __name__=='__main__':main()
