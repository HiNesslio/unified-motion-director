#!/usr/bin/env python3
"""Safe, engine-specific Mografy storyboard handoff and encoded-media identity check.

Neither subcommand installs Mografy, calls its runtime, creates scene code,
confirms media provenance, auditions audio or performs independent jury review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import production_router
import validate_storyboard


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return data


def sample_times(timeline: dict) -> list[float]:
    """Planning samples aligned to actual storyboard FPS; not observed images."""
    fps = int(timeline["fps"])
    duration = float(timeline["duration_sec"])
    maxframe = max(0, round(duration * fps) - 1)
    frames = {0, maxframe}
    for shot in timeline["scenes"].values():
        start = int(shot["start_frame"])
        last = min(maxframe, int(shot["end_frame_exclusive"]) - 1)
        frames.update((start, (start + last) // 2, last))
        # Three contiguous frame samples centered at every boundary.
        frames.update(n for n in (start - 1, start + 1, last - 1) if 0 <= n <= maxframe)
        for e in shot.get("events", []):
            t = e.get("time_sec")
            if isinstance(t, (int, float)) and not isinstance(t, bool):
                f = round(float(t) * fps)
                frames.update(n for n in (f - 1, f, f + 1) if 0 <= n <= maxframe)
    return [round(f / fps, 6) for f in sorted(frames)]


def prepare(storyboard: Path, out: Path) -> dict:
    storyboard = storyboard.expanduser().resolve()
    film = read_json(storyboard)
    errors, warnings = validate_storyboard.validate(film, storyboard.parent)
    if errors:
        raise ValueError("Invalid storyboard: " + "; ".join(errors[:8]))
    timeline, plan = production_router.build(film, "mografy")
    digest = sha256(storyboard)
    ratios = film.get("aspect_ratios", [])
    supported = {"16:9", "9:16"}
    unsupported = [x for x in ratios if x not in supported]
    out.mkdir(parents=True, exist_ok=True)
    timeline_file = out / "shared-timeline.json"
    timeline_file.write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    preview = sample_times(timeline)
    handoff = {
        "schema": "umd.mografy-handoff.v1",
        "state": "PLANNING_ONLY",
        "film_id": film["film_id"],
        "storyboard_source": str(storyboard),
        "storyboard_sha256": digest,
        "engine": "mografy",
        "engine_runtime": "EXTERNAL_NOT_INVOKED",
        "source_reference": "https://github.com/zz41354899/mografy",
        "timeline": timeline_file.name,
        "duration_sec": timeline["duration_sec"],
        "fps": timeline["fps"],
        "aspect_ratios": ratios,
        "unsupported_native_aspect_ratios": unsupported,
        "suggested_review_times_sec": preview,
        "scene_ids": list(timeline["scenes"]),
        "claims_manifest": film.get("claims_manifest"),
        "beat_grid": film.get("beat_grid"),
        "sound_status": timeline["timing_status"],
        "creative_authority": "unified-motion-director",
        "execution_owner": "installed-mografy-canvas-runtime",
        "final_acceptance_owner": "umd-two-independent-jurors",
        "warnings": warnings + ([f"No documented native Mografy preset for {unsupported}; validate custom layouts or choose another engine."] if unsupported else []),
        "does_not_assert": ["Mografy installation", "scene implementation", "preview inspection",
                            "music verification", "rendered output", "UI fidelity",
                            "subjective review", "rights clearance"],
    }
    (out / "mografy-handoff.json").write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = [
        "# Mografy production task — planning only", "",
        f"Film: **{handoff['film_id']}**",
        f"Story SHA-256: `{digest}`",
        f"Duration: {timeline['duration_sec']}s at {timeline['fps']}fps",
        f"Aspect ratios: {', '.join(ratios)}", "",
        "## Engine-specific production", "",
        "Read the Mografy Skill from the **installed upstream checkout** (not from this handoff).",
        "Respect the director's shared-timeline.json, on-screen claims, graphic continuity, beat uncertainty and asset ledger.",
        "Use project style.md only if present or the user approved lasting style choices.",
        "Create native portrait/landscape scene layout rather than pretending export cropping equals layout.",
        "Adapt the installed component templates or optional CJK/camera extras only after source/asset license checks.",
        "Implement scenes in scenes/main.ts or local scene modules as pure renderFrame(ctx, time, params).",
        "Leave mografy.json for project configuration; do not store scene keyframes in it.",
        "Do not invent data, product capabilities, finished frames or a soundtrack audition.", "",
        "## Execute only in a user-approved, installed Mografy workspace", "",
        "```bash",
        "mografy init projects/<film>   # agent-facing; creates real Mografy project files",
        "mografy dev projects/<film>    # optional live preview",
        "mografy check projects/<film>",
        "mografy review projects/<film>",
        "mografy export projects/<film> --format mp4",
        "```", "",
        "Inspect generated check/review images at the prescribed times and at nearby seam frames.",
        "Copy/record the actual final video path, then run mografy_bridge.py verify and UMD preflight / independent jury.",
        "Passing check/review is technical evidence, not an aesthetic score.", "",
        "## Planning review timestamps (seconds)", "",
        ", ".join(str(x) for x in preview), "",
        "## Known limitations", "",
        *(f"- {x}" for x in handoff["warnings"]),
        "- No Mografy runtime was executed by this preparer.",
        "- No audio was listened to, no original video was generated, and no jury was run.",
    ]
    (out / "MOGRAFY_TASK.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return handoff


def probe_video(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,format_name:stream=codec_type,width,height,avg_frame_rate",
        "-of", "json", str(path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"ffprobe unavailable or timed out: {exc}") from exc
    if result.returncode:
        raise ValueError(f"ffprobe failed for encoded video: {result.stderr.strip()[:250]}")
    obj = json.loads(result.stdout)
    streams = [s for s in obj.get("streams", []) if s.get("codec_type") == "video"]
    if not streams:
        raise ValueError("No encoded video track found")
    s = streams[0]
    rate = str(s.get("avg_frame_rate", "0/1"))
    try:
        numerator, denominator = rate.split("/")
        fps = float(numerator) / float(denominator)
        duration = float(obj["format"]["duration"])
        width, height = int(s["width"]), int(s["height"])
    except (ValueError, ZeroDivisionError, KeyError) as exc:
        raise ValueError("Invalid encoded-video metadata") from exc
    return {"fps": fps, "duration_sec": duration, "width": width, "height": height,
            "format": obj["format"].get("format_name", ""),
            "audio_present": any(s.get("codec_type") == "audio" for s in obj.get("streams", []))}


def verify(handoff_path: Path, video_path: Path, output_path: Path) -> dict:
    handoff = read_json(handoff_path)
    if handoff.get("schema") != "umd.mografy-handoff.v1" or handoff.get("state") != "PLANNING_ONLY":
        raise ValueError("Unrecognized or altered Mografy planning handoff")
    storyboard = Path(handoff["storyboard_source"])
    if not storyboard.is_file() or sha256(storyboard) != handoff["storyboard_sha256"]:
        raise ValueError("Storyboard SHA-256 mismatch: frozen handoff is obsolete")
    video = video_path.expanduser().resolve()
    if not video.is_file() or video.suffix.lower() not in (".mp4", ".webm"):
        raise ValueError("A real encoded MP4 or WebM video is required")
    metadata = probe_video(video)
    expected_fps = int(handoff["fps"])
    expected_duration = float(handoff["duration_sec"])
    if abs(metadata["fps"] - expected_fps) > 0.15:
        raise ValueError(f"Encoded FPS {metadata['fps']:.3f} differs from storyboard FPS {expected_fps}")
    if abs(metadata["duration_sec"] - expected_duration) > max(0.15, 2.0 / expected_fps):
        raise ValueError("Encoded video duration differs from storyboard duration")
    actual_ratio = metadata["width"] / metadata["height"]
    if not any(
        abs(actual_ratio - int(w) / int(h)) < 0.02
        for r in handoff["aspect_ratios"]
        for w, h in [r.split(":")]
    ):
        raise ValueError("Encoded aspect ratio is not listed in the storyboard")
    result = {
        "schema": "umd.mografy-media-verification.v1",
        "status": "MEDIA_IDENTITY_ONLY_NOT_ACCEPTED",
        "film_id": handoff["film_id"],
        "storyboard_sha256": handoff["storyboard_sha256"],
        "media_path": str(video),
        "media_sha256": sha256(video),
        "media": metadata,
        "not_verified": [
            "rendered_by_mografy", "project_source_provenance", "original_brand_asset_fidelity",
            "audio_content_or_sync", "independent_juror_review", "Product_Truth_attestation"
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="Build an engine-specific planning contract; no render")
    p.add_argument("storyboard", type=Path)
    p.add_argument("--out", type=Path, required=True)
    v = sub.add_parser("verify", help="Verify actual media and frozen storyboard identity; not acceptance")
    v.add_argument("--handoff", type=Path, required=True)
    v.add_argument("--video", type=Path, required=True)
    v.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = prepare(args.storyboard, args.out) if args.command == "prepare" else verify(args.handoff, args.video, args.out)
        print(json.dumps({"status": result.get("state", result.get("status")), "film_id": result["film_id"]}, ensure_ascii=False))
        return 0
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
