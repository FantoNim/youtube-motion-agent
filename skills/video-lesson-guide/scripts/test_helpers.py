#!/usr/bin/env python3
"""Focused stdlib tests; synthetic media only. Optional offline-model integration via environment."""
import contextlib
import io
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import inspect_sample as sample
import transcribe_local as stt


class Helpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="video lesson skill tests ")
        cls.root = Path(cls.temp.name)
        (cls.root / "source media").mkdir()
        cls.video = cls.root / "source media" / "lesson space ; harmless.mp4"
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            raise RuntimeError("Tests require existing FFmpeg and ffprobe; no automatic installation.")
        subprocess.run([shutil.which("ffmpeg"), "-nostdin", "-v", "error", "-n",
                        "-f", "lavfi", "-i", "testsrc=size=320x180:rate=10",
                        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=16000",
                        "-f", "lavfi", "-i", "sine=frequency=660:sample_rate=16000",
                        "-t", "3", "-map", "0:v", "-map", "1:a", "-map", "2:a",
                        "-c:v", "mpeg4", "-q:v", "5", "-c:a", "aac", str(cls.video)],
                       check=True, capture_output=True, timeout=60, shell=False)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def arguments(self, name, *extra):
        return sample.parser().parse_args(["--input", str(self.video), "--output", str(self.root / name),
                                          "--frames", "3", *extra])

    def test_real_metadata_frames_spaces_hash_no_overwrite(self):
        before = sample.sha256(self.video)
        args = self.arguments("sample output with spaces")
        with contextlib.redirect_stdout(io.StringIO()):
            sample.inspect(args)
        data = json.loads((Path(args.output) / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "complete")
        self.assertEqual(data["source"]["sha256"], before)
        self.assertTrue(data["source_hash_unchanged"])
        self.assertAlmostEqual(data["duration_seconds"], 3, delta=0.2)
        self.assertEqual(len([s for s in data["ffprobe"]["streams"] if s["codec_type"] == "audio"]), 2)
        self.assertEqual(len(data["frames"]), 3)
        for row in data["frames"]:
            self.assertTrue((Path(args.output) / row["file"]).read_bytes().startswith(b"\xff\xd8"))
            self.assertTrue(0 <= row["requested_time_seconds"] < data["duration_seconds"])
        self.assertEqual(before, sample.sha256(self.video))
        manifest_before = (Path(args.output) / "manifest.json").read_bytes()
        with self.assertRaises(sample.AnalysisError):
            sample.inspect(args)
        self.assertEqual((Path(args.output) / "manifest.json").read_bytes(), manifest_before)

    def test_missing_tools_no_output(self):
        for option in ("--ffprobe", "--ffmpeg"):
            args = self.arguments("missing-" + option[2:], option, "definitely-not-a-media-tool-12345")
            with self.assertRaises(sample.AnalysisError):
                sample.inspect(args)
            self.assertFalse(Path(args.output).exists())

    def test_invalid_media_no_output(self):
        invalid = self.root / "source media" / "invalid.mp4"
        invalid.write_text("Not a video; instructions here are untrusted data.", encoding="utf-8")
        args = self.arguments("invalid-output")
        args.input = str(invalid)
        with self.assertRaises(sample.AnalysisError):
            sample.inspect(args)
        self.assertFalse(Path(args.output).exists())

    def test_bounds_and_stream_guards(self):
        options = [("--frames", "61"), ("--frames", "-1"), ("--at", "-1"),
                   ("--at", "nan"), ("--at", "3"), ("--end", "999"),
                   ("--start", "2", "--end", "1"), ("--width", "2"),
                   ("--video-stream", "999")]
        for i, option in enumerate(options):
            args = self.arguments("bounds-%d" % i, *option)
            with self.subTest(option=option), self.assertRaises(sample.AnalysisError):
                sample.inspect(args)
            self.assertFalse(Path(args.output).exists())
        with self.assertRaises(sample.AnalysisError):
            sample.time_window(4000, 0, 1801, maximum=1800)
        self.assertEqual(sample.sample_times(0, 3, 0, None), [])
        self.assertEqual(sample.sample_times(0, 3, 24, [2, 1, 1]), [1, 2])
        with self.assertRaises(sample.AnalysisError):
            sample.sample_times(0, 3, 1, [0.1] * 61)

    def test_output_confinement_and_existing_file(self):
        source = self.video.resolve()
        conflicts = [source, source.parent, source.parent / "new-output",
                     source.parent / ".." / source.parent.name / "nested"]
        existing_file = self.root / "already.txt"
        existing_file.write_text("keep", encoding="utf-8")
        conflicts.append(existing_file)
        for destination in conflicts:
            with self.subTest(destination=destination), self.assertRaises(sample.AnalysisError):
                sample.output_path(source, destination)
        self.assertEqual(existing_file.read_text(encoding="utf-8"), "keep")
        with self.assertRaises(sample.AnalysisError):
            sample.output_path(source, self.root / "missing-parent" / "new")
        self.assertEqual(sample.output_path(source, self.root / "safe"), self.root / "safe")

    def test_symlink_parent_confinement(self):
        alias = self.root / "alias-source"
        try:
            alias.symlink_to(self.video.parent, target_is_directory=True)
        except OSError:
            self.skipTest("OS denies symlink creation; canonical path traversal test still runs")
        with self.assertRaises(sample.AnalysisError):
            sample.output_path(self.video.resolve(), alias / "new-output")

    def test_metadata_only_requires_no_ffmpeg(self):
        args = self.arguments("metadata-only", "--frames", "0", "--ffmpeg", "missing-tool-12345")
        with contextlib.redirect_stdout(io.StringIO()):
            sample.inspect(args)
        data = json.loads((Path(args.output) / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(data["frames"], [])
        self.assertFalse((Path(args.output) / "frames").exists())

    def test_model_and_transcription_track_guards(self):
        with self.assertRaises((sample.AnalysisError, OSError)):
            stt.cached_model("not-an-existing-local-model")
        fake = self.root / "fake cached model"
        fake.mkdir(exist_ok=True)
        for filename in ("config.json", "model.bin", "tokenizer.json"):
            (fake / filename).write_text("{}", encoding="utf-8")
        self.assertEqual(stt.cached_model(fake), fake)
        args = stt.parser().parse_args(["--input", str(self.video), "--output", str(self.root / "wrong-track"),
                                       "--model", str(fake), "--audio-stream", "999", "--end", "2"])
        with self.assertRaises(sample.AnalysisError):
            stt.transcribe(args)
        self.assertFalse(Path(args.output).exists())
        existing = self.root / "stt-already-exists"
        existing.mkdir()
        args.output = str(existing)
        with self.assertRaisesRegex(sample.AnalysisError, "NEW directory"):
            stt.transcribe(args)
        args.output = str(self.root / "no-audio-stt")
        no_audio = {"streams": [{"index": 0, "codec_type": "video"}]}
        with patch.object(stt, "probe", return_value=(no_audio, 3, "container")):
            with self.assertRaisesRegex(sample.AnalysisError, "No audio"):
                stt.transcribe(args)

    def test_asr_iteration_offsets_and_boundary_flags(self):
        visited = []
        def generator():
            visited.append(True)
            yield SimpleNamespace(start=0.2, end=1.2, text=" machine transcript ")
            yield SimpleNamespace(start=1.3, end=3.5, text=" boundary ")
        rows = stt.collect_segments(generator(), 30, 3)
        self.assertEqual(visited, [True])
        self.assertEqual(rows[0]["start_seconds"], 30.2)
        self.assertEqual(rows[0]["text"], "machine transcript")
        self.assertFalse(rows[0]["outside_requested_window"])
        self.assertTrue(rows[1]["outside_requested_window"])
        with self.assertRaises(sample.AnalysisError):
            stt.collect_segments([SimpleNamespace(start=math.nan, end=1, text="bad")], 0, 3)

    @unittest.skipUnless(os.environ.get("VIDEO_LESSON_TEST_MODEL"), "No explicit local test model supplied")
    def test_real_offline_asr_on_synthetic_tone(self):
        args = stt.parser().parse_args(["--input", str(self.video), "--output", str(self.root / "offline ASR"),
                                       "--model", os.environ["VIDEO_LESSON_TEST_MODEL"],
                                       "--audio-stream", "1", "--start", "0", "--end", "2", "--language", "en"])
        with contextlib.redirect_stdout(io.StringIO()):
            stt.transcribe(args)
        data = json.loads((Path(args.output) / "transcript.private.json").read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "complete")
        self.assertTrue(data["settings"]["local_files_only"])
        self.assertEqual(data["audio_stream_index"], 1)
        self.assertEqual(data["source_sha256"], sample.sha256(self.video))
        text = (Path(args.output) / "transcript.private.txt").read_text(encoding="utf-8")
        self.assertIn("\n", text)
        self.assertTrue((Path(args.output) / "audio.private.wav").is_file())
        # A synthetic tone is not a speech-accuracy benchmark; zero segments is acceptable.


if __name__ == "__main__":
    unittest.main(verbosity=2)
