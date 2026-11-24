#!/usr/bin/env python3
"""Read-only local metadata/hash and bounded private frame sampling. Python stdlib + FFmpeg."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

MEDIA_SUFFIXES = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4v", ".mpg", ".mpeg"}


class AnalysisError(Exception):
    pass


def source_file(value):
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_file() or path.suffix.lower() not in MEDIA_SUFFIXES:
        raise AnalysisError("Use an existing conventional local video file; playlists/URLs are unsupported.")
    return path


def output_path(source, value):
    raw = Path(value).expanduser()
    if raw.exists() or raw.is_symlink():
        raise AnalysisError("Output must be a NEW directory; overwrite is refused.")
    path = raw.resolve()
    # Preserve the entire source folder. Symlinked parents resolve before this check.
    if path == source.parent or source.parent in path.parents or path in source.parents:
        raise AnalysisError("Output conflicts with the source directory; choose a separate analysis directory.")
    if not path.parent.is_dir():
        raise AnalysisError("Output parent must already exist.")
    return path


def tool_path(value):
    result = shutil.which(str(value))
    if not result:
        raise AnalysisError("Required local executable is missing: " + Path(value).name)
    return result


def run_tool(args, timeout=120):
    try:
        result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=timeout, shell=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AnalysisError("Local media tool failed or timed out; no successful analysis claimed.") from exc
    if result.returncode:
        # Do not echo media metadata or raw stderr; either may contain private values.
        raise AnalysisError("Local media tool rejected input or options; inspect privately, not in public copy.")
    return result.stdout


def probe(source, ffprobe):
    raw = run_tool([ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe", "-show_format",
                    "-show_streams", "-of", "json", str(source)])
    try:
        data = json.loads(raw)
        candidates = [data.get("format", {}).get("duration")]
        candidates += [s.get("duration") for s in data.get("streams", [])]
        durations = []
        for value in candidates:
            try:
                number = float(value)
                if math.isfinite(number) and number > 0:
                    durations.append(number)
            except (TypeError, ValueError):
                pass
        if not durations:
            raise AnalysisError("No usable duration; stop and investigate metadata privately.")
        # Container duration takes precedence; stream fallback is explicit in manifest.
        container = candidates[0]
        try:
            duration = float(container)
        except (TypeError, ValueError):
            duration = 0
        origin = "container"
        if not math.isfinite(duration) or duration <= 0:
            duration, origin = max(durations), "longest_reported_stream"
        if not data.get("streams"):
            raise AnalysisError("No media streams found.")
        return data, duration, origin
    except (ValueError, TypeError, KeyError) as exc:
        raise AnalysisError("Invalid ffprobe JSON; no successful analysis claimed.") from exc


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def time_window(duration, start=0, end=None, maximum=None):
    end = duration if end is None else end
    if not all(math.isfinite(n) for n in (duration, start, end)):
        raise AnalysisError("Time bounds must be finite numbers.")
    if not 0 <= start < end <= duration:
        raise AnalysisError("Require 0 <= start < end <= media duration.")
    if maximum and end - start > maximum:
        raise AnalysisError("Window too long; use explicit bounded chunks.")
    return start, end


def sample_times(start, end, count, explicit):
    if not 0 <= count <= 60:
        raise AnalysisError("Frame count must be 0 through 60.")
    if explicit:
        if len(explicit) > 60 or any(not math.isfinite(t) or not start <= t < end for t in explicit):
            raise AnalysisError("At most 60 timestamps, each inside [start, end), are allowed.")
        return sorted(set(explicit))
    # Interior points avoid duration/end-of-file and sample a short clip usefully.
    return [start + (end - start) * (i + 0.5) / count for i in range(count)]


def write_json(path, data):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")


def inspect(args):
    source = source_file(args.input)
    output = output_path(source, args.output)
    if not 320 <= args.width <= 3840:
        raise AnalysisError("Width must be between 320 and 3840 pixels.")
    ffprobe = tool_path(args.ffprobe)
    metadata, duration, duration_origin = probe(source, ffprobe)
    start, end = time_window(duration, args.start, args.end)
    times = sample_times(start, end, args.frames, args.at)
    videos = [s for s in metadata["streams"] if s.get("codec_type") == "video"
              and not s.get("disposition", {}).get("attached_pic")]
    video = None
    if times:
        if not videos:
            raise AnalysisError("No playable video stream; use --frames 0 for metadata only.")
        video = videos[0] if args.video_stream is None else next(
            (s for s in videos if s["index"] == args.video_stream), None)
        if video is None:
            raise AnalysisError("Selected absolute video stream index does not exist.")
    ffmpeg = tool_path(args.ffmpeg) if times else None
    digest = sha256(source)
    stat = source.stat()
    output.mkdir()  # Atomic exclusive claim; never merge with an existing directory.
    manifest = {
        "schema_version": 1, "status": "incomplete", "privacy": "PRIVATE: may contain credentials or personal data",
        "source": {"path": str(source), "size_bytes": stat.st_size, "sha256": digest},
        "duration_seconds": duration, "duration_origin": duration_origin,
        "window_seconds": [start, end], "video_stream_index": video["index"] if video else None,
        "timestamp_basis": "requested seek seconds on input timeline; not verified decoded-frame PTS",
        "sampling": "explicit timestamps" if args.at else "uniform interior points; not scene detection",
        "frames": [], "ffprobe": metadata,
    }
    write_json(output / "manifest.incomplete.json", manifest)
    if times:
        (output / "frames").mkdir()
    for i, timestamp in enumerate(times):
        filename = "frames/frame-%03d.jpg" % (i + 1)
        run_tool([ffmpeg, "-nostdin", "-v", "error", "-n", "-protocol_whitelist", "file,pipe",
                  "-ss", "%.6f" % timestamp, "-i", str(source), "-map", "0:%d" % video["index"],
                  "-frames:v", "1", "-vf", "scale=w='min(%d,iw)':h=-2" % args.width,
                  "-q:v", "3", "-update", "1", str(output / filename)])
        frame = output / filename
        if not frame.is_file() or frame.stat().st_size == 0:
            raise AnalysisError("Requested frame was not decoded; incomplete output retained privately.")
        manifest["frames"].append({"file": filename, "requested_time_seconds": timestamp})
    if source.stat().st_size != stat.st_size or sha256(source) != digest:
        raise AnalysisError("Source changed during analysis; do not use this run.")
    manifest["status"] = "complete"
    manifest["source_hash_unchanged"] = True
    write_json(output / "manifest.json", manifest)
    print("Complete: private metadata/hash and %d sampled frames; no uploads or attachments." % len(times))


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True, help="NEW directory outside the entire source folder")
    p.add_argument("--frames", type=int, default=24, help="uniform interior samples, 0..60")
    p.add_argument("--at", type=float, action="append", help="explicit seconds; replaces uniform sampling")
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--end", type=float)
    p.add_argument("--video-stream", type=int, help="absolute ffprobe stream index")
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--ffmpeg", default="ffmpeg")
    p.add_argument("--ffprobe", default="ffprobe")
    return p


if __name__ == "__main__":
    try:
        inspect(parser().parse_args())
    except (AnalysisError, OSError) as exc:
        print("ERROR: " + (str(exc) if isinstance(exc, AnalysisError) else "Local path or filesystem failure."), file=sys.stderr)
        sys.exit(2)
