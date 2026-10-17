#!/usr/bin/env python3
"""FFmpeg-based pre-jury technical checks of real encoded video.

This tool detects review candidates; it does NOT assess aesthetic merit or
approve the film. The only acceptance authority is the independent jury gate.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


def ffprobe(path):
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames,sample_rate','-of','json',str(path)],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(f'ffprobe failed: {p.stderr.strip()[:500]}')
    return json.loads(p.stdout)


def scan_candidates(path, fps, width=64, max_seconds=180):
    """Scan encoded frames at native FPS up to 60fps to catch one-frame pops.

    Avoid arbitrary memory use; capped duration. Frames are scaled to 64px,
    so candidates need full-resolution strip review, especially near cuts.
    """
    scan_rate=min(round(fps),60)
    cmd=['ffmpeg','-v','error','-i',str(path),'-t',str(max_seconds),'-vf',f'fps={scan_rate},scale={width}:{width},format=gray','-f','rawvideo','-']
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    n=width*width
    means=[]; diffs=[]; prev=None; frame=0
    try:
        while frame < scan_rate*max_seconds:
            buf=proc.stdout.read(n)
            if len(buf)<n:break
            # estimate brightness and inter-frame differences (efficient built-in ops)
            brightness=sum(buf)/(n*255)
            means.append(brightness)
            if prev is not None:
                diffs.append(sum(abs(x-y) for x,y in zip(prev,buf))/(n*255))
            prev=buf;frame+=1
    finally:
        proc.stdout.close()
        stderr=proc.stderr.read().decode('utf-8','replace')
        rc=proc.wait()
    if rc:raise RuntimeError(f'ffmpeg decode failed: {stderr[:500]}')
    hits=[]
    for i in range(1,len(diffs)-1):
        neighbor=max(diffs[i-1],diffs[i+1],0.005)
        if diffs[i]>max(0.08,2.8*neighbor):
            hits.append({'time_sec':round((i+1)/scan_rate,3),'jump':round(diffs[i],3), 'neighbor':round(neighbor,3),'kind':'isolated_change'})
    # A one-frame flash often has TWO adjacent large difference spikes (entry + exit).
    # Catch it by looking for a luma excursion whose adjacent frames agree.
    for i in range(1,len(means)-1):
        base=(means[i-1]+means[i+1])/2
        if abs(means[i-1]-means[i+1]) < 0.07 and abs(means[i]-base)>0.12:
            hits.append({'time_sec':round(i/scan_rate,3),'jump':round(abs(means[i]-base),3),
                         'neighbor':round(abs(means[i-1]-means[i+1]),3),'kind':'one_frame_brightness_excursion'})
    hits.sort(key=lambda x:(x['time_sec'],x['kind']))
    return {'sample_fps':scan_rate,'frames_scanned':frame,'covered_seconds':round(frame/scan_rate,2),
            'first_frame_mean_luma':round(means[0],4) if means else None,
            'suspect_frame_change_candidates':hits[:100], 'candidate_count':len(hits),
            'limit_note':f'Scanned encoded frames at {scan_rate} fps (up to 60 fps and {max_seconds}s), downscaled spatially; full-resolution cut strips still required.'}


def inspect(path, storyboard=None, sample=True, max_seconds=180):
    path=Path(path)
    if not path.is_file():raise FileNotFoundError(path)
    h=hashlib.sha256()
    with path.open('rb') as inp:
        for piece in iter(lambda:inp.read(1024*1024),b''):
            h.update(piece)
    blob=h.hexdigest()
    data=ffprobe(path)
    streams=data.get('streams',[])
    video=next((x for x in streams if x.get('codec_type')=='video'),None)
    if video is None:raise RuntimeError('file has no video track')
    audio=[x for x in streams if x.get('codec_type')=='audio']
    rate=video.get('avg_frame_rate') or video.get('r_frame_rate','0/1')
    num,den=map(int,rate.split('/'))
    if den==0 or num<=0:raise RuntimeError('cannot determine FPS')
    fps=num/den
    duration=float(data.get('format',{}).get('duration',0))
    issues=[]
    if duration<=0:issues.append({'type':'invalid_duration','severity':'BLOCKER'})
    if video.get('width',0)<480:issues.append({'type':'low_resolution','severity':'REVIEW'})
    requested=None
    cut_times=[]
    if storyboard:
        film=json.loads(Path(storyboard).read_text(encoding='utf-8'))
        requested={'duration_sec':film.get('duration_sec'),'fps':film.get('fps'),'aspect_ratios':film.get('aspect_ratios')}
        if abs(duration-float(film['duration_sec']))>max(0.1,2/fps):
            issues.append({'type':'duration_mismatch','severity':'REVIEW','actual_sec':duration,'expected_sec':film['duration_sec']})
        if abs(fps-float(film['fps']))>0.1:
            issues.append({'type':'fps_mismatch','severity':'REVIEW','actual_fps':fps,'expected_fps':film['fps']})
        cut_times=[round(float(s['start_sec']),3) for s in film.get('scenes',[])[1:]]
    result={'status':'TECHNICAL_PREFLIGHT_ONLY','video_file':str(path.resolve()),'sha256':blob,
      'width':video.get('width'),'height':video.get('height'),'fps':round(fps,4),
      'duration_sec':round(duration,4),'video_codec':video.get('codec_name'),
      'audio_streams':len(audio),'audio_codec':audio[0].get('codec_name') if audio else None,
      'requested':requested,'issues':issues,
      'disclaimer':'Cannot award PASS, evaluate copyrighted asset licenses, actually listen to sound, or replace independent jurors.'}
    if sample:
        scan=scan_candidates(path,fps,max_seconds=max_seconds)
        scan['suspect_frame_change_candidates']=[dict(h,near_storyboard_scene_start=any(abs(h['time_sec']-c)<0.25 for c in cut_times)) for h in scan['suspect_frame_change_candidates']]
        result['frame_scan']=scan
        if scan['first_frame_mean_luma'] is not None and scan['first_frame_mean_luma']<0.02:
            issues.append({'type':'very_dark_first_frame','severity':'REVIEW','reason':'Might be a deliberate opening. Check platform thumbnail and brief.'})
        if scan['candidate_count']:
            issues.append({'type':'flash_or_cut_review_candidates','severity':'REVIEW','count':scan['candidate_count']})
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('video',type=Path)
    ap.add_argument('--storyboard',type=Path)
    ap.add_argument('--out',type=Path)
    ap.add_argument('--no-frame-scan',action='store_true')
    ap.add_argument('--max-scan-seconds',type=int,default=180)
    a=ap.parse_args()
    try:
        report=inspect(a.video,a.storyboard,not a.no_frame_scan,a.max_scan_seconds)
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as e:
        ap.exit(2,f'Preflight failed: {e}\n')
    x=json.dumps(report,indent=2,ensure_ascii=False)+'\n'
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(x,encoding='utf-8')
        print(f'Preflight saved: {a.out} ({len(report["issues"])} review/blocker notes)')
    else:print(x)

if __name__=='__main__':main()
