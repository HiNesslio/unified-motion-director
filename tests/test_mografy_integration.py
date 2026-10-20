"""Native Mografy is optional; tests validate independent contract, not render claims."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import mografy_bridge
import production_router
import validate_storyboard

FIXTURE = ROOT / "tests" / "fixtures" / "storyboard.json"


class MografyIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.film = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_optional_upstream_has_license_metadata(self):
        entries = json.loads((ROOT / "config" / "sources.json").read_text())["repositories"]
        hits = [s for s in entries if s["id"] == "mografy"]
        self.assertEqual(len(hits), 1)
        self.assertIn("MIT", hits[0]["license"])
        self.assertEqual(hits[0]["url"], "https://github.com/zz41354899/mografy.git")

    def test_explicit_engine_and_preference(self):
        self.assertEqual(production_router.build(self.film, "mografy")[1]["engine"], "mografy")
        film = copy.deepcopy(self.film)
        film["engine_preference"] = "mografy"
        self.assertEqual(production_router.build(film, "auto")[1]["engine"], "mografy")
        self.assertEqual(validate_storyboard.validate(film)[0], [])

    def test_existing_automatic_remotion_selection_unchanged(self):
        self.assertEqual(production_router.build(self.film, "auto")[1]["engine"], "remotion")

    def test_explicit_canvas_heuristic(self):
        film = copy.deepcopy(self.film)
        film["scenes"][0]["subject"] = "Native Canvas 2D animation"
        self.assertEqual(production_router.build(film, "auto")[1]["engine"], "mografy")

    def test_bad_engine_rejected(self):
        with self.assertRaises(ValueError):
            production_router.build(self.film, "does-not-exist")
        film = copy.deepcopy(self.film)
        film["engine_preference"] = "not-a-renderer"
        self.assertTrue(validate_storyboard.validate(film)[0])

    def test_prepare_has_exact_real_storyboard_hash_and_stage(self):
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / "handoff"
            actual = mografy_bridge.prepare(FIXTURE, dest)
            self.assertEqual(actual["state"], "PLANNING_ONLY")
            self.assertEqual(actual["engine_runtime"], "EXTERNAL_NOT_INVOKED")
            self.assertEqual(actual["storyboard_sha256"], mografy_bridge.sha256(FIXTURE))
            self.assertTrue((dest / "MOGRAFY_TASK.md").exists())
            self.assertTrue((dest / "shared-timeline.json").exists())
            self.assertTrue((dest / "mografy-handoff.json").exists())
            self.assertGreaterEqual(len(actual["suggested_review_times_sec"]), 3)
            self.assertEqual(actual["scene_ids"], [s["id"] for s in self.film["scenes"]])

    def test_timeline_retains_events_and_claims(self):
        film = copy.deepcopy(self.film)
        film["scenes"][0]["events"] = [{"time_sec": 0.5, "action": "reveal_result"}]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "storyboard.json"
            p.write_text(json.dumps(film), encoding="utf-8")
            out = Path(td) / "handoff"
            mografy_bridge.prepare(p, out)
            timeline = json.loads((out / "shared-timeline.json").read_text())
            self.assertEqual(timeline["scenes"]["S01"]["events"][0]["time_sec"], 0.5)

    def test_prepare_rejects_invalid_scene_time(self):
        film = copy.deepcopy(self.film)
        film["scenes"][0]["end_sec"] = -1
        with tempfile.TemporaryDirectory() as td:
            story = Path(td) / "invalid.json"
            story.write_text(json.dumps(film))
            with self.assertRaises(ValueError):
                mografy_bridge.prepare(story, Path(td) / "out")

    def test_verify_missing_media_does_not_fabricate_result(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "handoff"
            mografy_bridge.prepare(FIXTURE, out)
            result = Path(td) / "verification.json"
            with self.assertRaises(ValueError):
                mografy_bridge.verify(out / "mografy-handoff.json", Path(td) / "not-real.mp4", result)
            self.assertFalse(result.exists())

    def test_verify_obsolete_storyboard_hash_fails(self):
        with tempfile.TemporaryDirectory() as td:
            story = Path(td) / "story.json"
            story.write_text(FIXTURE.read_text())
            out = Path(td) / "handoff"
            mografy_bridge.prepare(story, out)
            story.write_text(story.read_text() + " ")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                mografy_bridge.verify(out / "mografy-handoff.json", Path(td) / "film.mp4", Path(td) / "verify.json")

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg unavailable")
    def test_real_encoded_test_video_is_identity_only_not_juried(self):
        with tempfile.TemporaryDirectory() as td:
            storyboard = copy.deepcopy(self.film)
            storyboard["duration_sec"] = 1
            storyboard["scenes"] = [copy.deepcopy(storyboard["scenes"][0])]
            storyboard["scenes"][0]["start_sec"] = 0
            storyboard["scenes"][0]["end_sec"] = 1
            storyboard["scenes"][0]["keyframe_notes"] = ["A neutral synthetic testing scene"]
            storyboard["scenes"][0]["sound"]["cue_time_sec"] = None
            s = Path(td) / "story.json"
            s.write_text(json.dumps(storyboard))
            out = Path(td) / "handoff"
            mografy_bridge.prepare(s, out)
            video = Path(td) / "synthetic.mp4"
            command = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                       "color=c=black:s=640x360:r=30:d=1", "-c:v", "libx264",
                       "-pix_fmt", "yuv420p", str(video)]
            task = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(task.returncode, 0, task.stderr)
            verified = mografy_bridge.verify(out / "mografy-handoff.json", video, Path(td) / "result.json")
            self.assertEqual(verified["status"], "MEDIA_IDENTITY_ONLY_NOT_ACCEPTED")
            self.assertEqual(len(verified["media_sha256"]), 64)
            self.assertIn("rendered_by_mografy", verified["not_verified"])

    def test_no_runtime_or_fonts_vendor_copied(self):
        self.assertFalse((ROOT / "vendor" / "mografy").exists())
        self.assertFalse((ROOT / "external" / "mografy").exists())
        self.assertIn("OFL", (ROOT / "references" / "mografy-canvas-production.md").read_text())


if __name__ == "__main__":
    unittest.main()
