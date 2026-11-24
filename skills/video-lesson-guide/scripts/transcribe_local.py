#!/usr/bin/env python3
"""Explicit cached faster-whisper model only; bounded local WAV, timestamped private ASR."""
import argparse
import importlib.metadata
import math
import os
from pathlib import Path
import sys

from inspect_sample import (AnalysisError, output_path, probe, run_tool, sha256,
                            source_file, time_window, tool_path, write_json)


def cached_model(value):
    model = Path(value).expanduser().resolve(strict=True)
    if not model.is_dir() or not all((model / name).is_file() for name in
                                     ("model.bin", "config.json", "tokenizer.json")):
        raise AnalysisError("Supply an existing CTranslate2 model directory with model.bin, config.json and tokenizer.json; no download is attempted.")
    return model


def collect_segments(segments, offset, window_length):
    result = []
    for segment in segments:  # Must exhaust the lazy generator; creation alone is not completion.
        start, end = float(segment.start), float(segment.end)
        if not all(math.isfinite(t) for t in (start, end)) or not 0 <= start <= end:
            raise AnalysisError("ASR produced invalid timestamps; retain as unverified, not lesson evidence.")
        # Slight overshoot can occur at a decoded window boundary. Keep raw values, flag it.
        result.append({"start_seconds": offset + start, "end_seconds": offset + end,
                       "text": segment.text.strip(), "outside_requested_window": end > window_length + 0.1,
                       "avg_logprob": getattr(segment, "avg_logprob", None),
                       "no_speech_probability": getattr(segment, "no_speech_prob", None)})
    return result


def transcribe(args):
    source = source_file(args.input)
    output = output_path(source, args.output)
    model_path = cached_model(args.model)
    if output == model_path or model_path in output.parents or output in model_path.parents:
        raise AnalysisError("Output must be separate from the cached model directory.")
    ffprobe, ffmpeg = tool_path(args.ffprobe), tool_path(args.ffmpeg)
    metadata, duration, origin = probe(source, ffprobe)
    start, end = time_window(duration, args.start, args.end, maximum=1800)
    audio = [s for s in metadata["streams"] if s.get("codec_type") == "audio"]
    if not audio:
        raise AnalysisError("No audio stream: use visual-only analysis and state the limitation.")
    if not any(s["index"] == args.audio_stream for s in audio):
        raise AnalysisError("Selected absolute audio stream index does not exist; never silently choose a different track.")
    # Process-local guards; explicit path plus local_files_only are mandatory, not model names.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    try:
        from faster_whisper import WhisperModel
        version = importlib.metadata.version("faster-whisper")
    except ImportError as exc:
        raise AnalysisError("Local faster-whisper dependency is missing; do not upload or install automatically.") from exc
    digest = sha256(source)
    output.mkdir()
    write_json(output / "manifest.incomplete.json", {
        "status": "incomplete", "source_sha256": digest, "window_seconds": [start, end],
        "privacy": "PRIVATE: speech, metadata and local paths may contain credentials or personal data"})
    wav = output / "audio.private.wav"
    run_tool([ffmpeg, "-nostdin", "-v", "error", "-n", "-protocol_whitelist", "file,pipe",
              "-ss", str(start), "-i", str(source), "-t", str(end - start),
              "-map", "0:%d" % args.audio_stream, "-vn", "-ac", "1", "-ar", "16000",
              "-c:a", "pcm_s16le", str(wav)], timeout=300)
    try:
        model = WhisperModel(str(model_path), device="cpu", compute_type="int8", local_files_only=True)
        segments, info = model.transcribe(str(wav), language=args.language, beam_size=5,
                                          vad_filter=True, word_timestamps=False)
        rows = collect_segments(segments, start, end - start)
    except Exception as exc:
        # Library exceptions can include filenames/text. Do not echo them into chat.
        raise AnalysisError("Local ASR failed; incomplete private output retained. No transcript claimed.") from exc
    if sha256(source) != digest:
        raise AnalysisError("Source changed during ASR; do not use this run.")
    data = {"schema_version": 1, "status": "complete", "kind": "machine-generated ASR; not verified exact listening",
            "privacy": "PRIVATE: redact before any public use", "source_path": str(source),
            "source_sha256": digest, "source_hash_unchanged": True, "duration_seconds": duration,
            "duration_origin": origin, "window_seconds": [start, end], "audio_stream_index": args.audio_stream,
            "model_directory": str(model_path), "faster_whisper_version": version,
            "settings": {"device": "cpu", "compute_type": "int8", "local_files_only": True,
                         "vad_filter": True, "word_timestamps": False, "beam_size": 5},
            "language": info.language, "language_probability": info.language_probability,
            "segments": rows, "coverage_note": "Only this audio track/window; no segments does not prove silence."}
    write_json(output / "transcript.private.json", data)
    with (output / "transcript.private.txt").open("x", encoding="utf-8") as handle:
        handle.write("Machine-generated local ASR; segment times are approximate; private, not word-verified.\n")
        for row in rows:
            handle.write("[%.2f -> %.2f] %s\n" % (row["start_seconds"], row["end_seconds"], row["text"]))
    print("Complete: %d private ASR segments for selected track/window; no uploads or attachments." % len(rows))


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True, help="NEW directory outside source/model folders")
    p.add_argument("--model", required=True, help="explicit existing local CTranslate2 model directory")
    p.add_argument("--audio-stream", type=int, required=True, help="absolute ffprobe stream index")
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--end", type=float, required=True, help="absolute end seconds; at most 1800 seconds per run")
    p.add_argument("--language", help="optional verified ISO language code; omit to detect")
    p.add_argument("--ffmpeg", default="ffmpeg")
    p.add_argument("--ffprobe", default="ffprobe")
    return p


if __name__ == "__main__":
    try:
        transcribe(parser().parse_args())
    except (AnalysisError, OSError) as exc:
        print("ERROR: " + (str(exc) if isinstance(exc, AnalysisError) else "Local path or filesystem failure."), file=sys.stderr)
        sys.exit(2)
