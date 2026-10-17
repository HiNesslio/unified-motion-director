#!/usr/bin/env python3
"""Suggest tempo, beat and energy/drop candidates from real audio (not verified sync).

Requires NumPy. Supports 16-bit PCM WAV via stdlib; other formats through FFmpeg.
All automatic times are marked candidate_unverified until a human checks music.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import wave


def decode_audio(path, target_rate=11025):
    try: import numpy as np
    except ImportError as e: raise RuntimeError('Install numpy to analyze audio') from e
    path=Path(path)
    if path.suffix.lower()=='.wav':
        try:
            with wave.open(str(path),'rb') as f:
                channels,sw,sr=f.getnchannels(),f.getsampwidth(),f.getframerate()
                if sw!=2: raise ValueError('WAV must be 16-bit PCM for native decode')
                samples=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768
                return samples.reshape(-1,channels).mean(axis=1),sr
        except (ValueError,wave.Error): pass
    cmd=['ffmpeg','-v','error','-i',str(path),'-ac','1','-ar',str(target_rate),'-f','f32le','-acodec','pcm_f32le','-']
    p=subprocess.run(cmd,capture_output=True)
    if p.returncode:raise RuntimeError(f'ffmpeg decode failed: {p.stderr.decode(errors="replace")[-250:]}')
    return np.frombuffer(p.stdout,dtype='<f4'),target_rate


def analyze_samples(y,sr,source_sha=None):
    import numpy as np
    if sr<100 or len(y)<sr*3: raise ValueError('Need at least 3 seconds of audio')
    hop=max(1,round(sr*0.0232));size=hop*2
    n=1+max(0,(len(y)-size)//hop)
    if n<10: raise ValueError('Insufficient windows')
    # Energy/onset envelopes, not a musicological beat transcription.
    frames=np.lib.stride_tricks.sliding_window_view(y,size)[::hop][:n]
    rms=np.sqrt(np.mean(frames.astype(np.float64)**2,axis=1))
    onset=np.maximum(0,np.diff(rms,prepend=rms[0]))
    if onset.max()>0:onset=onset/onset.max()
    step=hop/sr
    # Autocorrelation between 65–180 BPM, reduce degeneracy on silence.
    centered=onset-np.mean(onset)
    norms=float(centered@centered)
    possible=[]
    for bpm in range(65,181):
        lag=round(60/(bpm*step))
        if lag>=len(centered)//2:continue
        score=float(np.dot(centered[:-lag],centered[lag:]))/(norms+1e-10)
        possible.append((score,bpm,lag))
    possible.sort(reverse=True)
    confidence='low'
    peaks=[]
    energy=float(np.max(rms))
    if energy>1e-4 and possible:
        best=possible[0]
        # Determine beat phase using onset near predicted periodic grid.
        _,bpm,lag=best
        phase_scores=[sum(onset[i::lag]) for i in range(lag)]
        phase=int(np.argmax(phase_scores))
        # Only include actual beats within the waveform duration.
        beats=[round((phase+k*lag)*step,3) for k in range((len(onset)-phase+lag-1)//lag)]
        conf_score=max(0.0,min(1.0,best[0]))
        confidence='medium' if conf_score>=.16 else 'low'
        if conf_score>=.36:confidence='high'
        peaks=[{'bpm':p[1],'autocorr_score':round(max(0.0,p[0]),4)} for p in possible[:5]]
    else:
        bpm=None;beats=[];conf_score=0.0
    # Compare smoothed energy before/after each second; strongest growth could be a drop.
    sec=int(len(y)/sr)
    block=[]
    for k in range(sec):
        seg=y[k*sr:(k+1)*sr]
        block.append(float(np.sqrt(np.mean(seg.astype(np.float64)**2))))
    changes=[]
    for k in range(2,len(block)-1):
        before=sum(block[max(0,k-2):k])/min(k,2)
        after=sum(block[k:min(len(block),k+2)])/min(len(block)-k,2)
        if before>1e-5 and after>before*1.65:
            changes.append({'time_sec':k,'energy_ratio':round(after/before,3)})
    changes.sort(key=lambda x:x['energy_ratio'],reverse=True)
    return {'schema':'umd.beat-analysis.v1','status':'candidate_unverified',
            'source_sha256':source_sha,'sample_rate':sr,'duration_sec':round(len(y)/sr,3),
            'tempo_bpm_candidate':bpm,'tempo_confidence':confidence,'tempo_score':round(conf_score,4),
            'alternate_tempos':peaks,'beat_times_sec_candidates':beats[:1500],
            'energy_drop_candidates':changes[:8],
            'disclaimer':'Algorithmic candidates only. Listen to the actual track and verify beat, downbeat and drop manually before locking picture.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('audio',type=Path);p.add_argument('--out',type=Path)
    a=p.parse_args()
    try:
        y,sr=decode_audio(a.audio)
        result=analyze_samples(y,sr,hashlib.sha256(a.audio.read_bytes()).hexdigest())
    except (OSError,RuntimeError,ValueError) as e: print('ERROR:',e,file=sys.stderr);return 1
    payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(payload)
    else:print(payload)
    return 0

if __name__=='__main__':sys.exit(main())
