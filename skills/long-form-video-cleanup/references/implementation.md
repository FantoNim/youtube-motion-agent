# Existing-solutions preflight and implementation boundary

Read-only preflight 2026-11-08, no executable/model downloads or installation:

- Auto-Editor official README: https://github.com/WyattBlue/auto-editor and https://raw.githubusercontent.com/WyattBlue/auto-editor/master/README.md . Describes first-pass dead-space removal using loudness/motion, margins, editor exports. Source public domain; binary licenses separate.
- Official method reference https://auto-editor.com/ref/edit documents audio amplitude thresholds, motion, blackdetect and subtitle/word/regex BoolArray methods. These do NOT establish semantic recognition of duplicate takes, false starts or preservation of qualifications. Silence detection can suggest candidates, not decide cleanup.
- Official docs/ref indexes: https://auto-editor.com/docs/ and https://auto-editor.com/ref/ . Fetched read-only; repository metadata https://api.github.com/repos/WyattBlue/auto-editor was accessible. No downloaded code executed.
- Local check: Get-Command auto-editor returned none; python -m pip show auto-editor reported package not found. No installation authorized.
- Existing repository local-video-clipping helper outputs contiguous separate clips. Its SKILL.md already documents chronological joined montage with H264+PCM intermediates and one final AAC encode, but no executable audited keep-list join helper. Reuse its probe/hash/confinement/compatibility/timestamp/full-decode/metadata QA; implement only narrow keep-list+deletion coverage/quantization/map/intermediate/join glue, no NLE, ASR or semantic engine.
- Historical initial preflight (2026-11-08, before parent runtime setup): Filmcraft operator skill existed, but runtime/CLI was not on PATH or connected/tested in that task context. This is historical evidence, NOT current readiness. Consult project-level Apps/filmcraft-local/README.md and verify the actual installed MCP/runtime through the Filmcraft operator skill before handoff. JSON edit-map is audit evidence, not .fcproj or a native cut-list import; do not promise JSON/EDL interoperability. Importing a rendered cleaned master as one linked A/V clip does not reconstruct the original takes/cuts natively. Remotion is an existing graphics route, not needed for source-footage cleanup.

## Exact timing and audio design

Conservative shared zero-origin CFR inputs only. Original video frame index bounds and matching integer audio samples are trimmed from the SAME original common clock; setpts/asetpts are applied only AFTER exact synchronized trim with equal durations verified. Never independently normalize an offset source. Reencode original geometry/rate H264 parts with PCM s24le audio at original rate/layout; verify exact frame/sample counts. Concatenate generated fixed safe relative part filenames with explicit durations, remux those already reencoded video packets, encode original-channel AAC once. Original cuts are NOT keyframe stream-copy. Final full decode and continuous timestamps plus source/output RGB/PCM samples catch drift/regressions; AAC encoder padding tolerated only as one final packet (1024/sourceHz +2ms), not per-cut additions. No apad, aresample async, atempo, shortest truncation, tpad or forced fps.

Frames/sample lattice restrictions deliberately block unrepresentable exact join times. At 29.97 fps/48kHz use multiples of five source frames; no claim every arbitrary frame has an exact sample boundary. Requested non-frame times round half-up <=half-frame, recorded in plan; agent must inspect before render and deletion complements use actual quantized values.

Geometry/aspect/color/audio verification reuse the sibling gate. Unknown color is preserved as unknown, not a technical color-management guarantee. Unsupported HDR/rotation/full-range/wide-gamut/interlace/unknown field order/offset/VFR/data tracks block. Original metadata tags/chapters explicitly stripped, raw probe retained. Exact byte content cannot survive lossy reencode; original SHA-256 remains unchanged.

## Performance/security limitations

No external APIs, media uploads or package downloads. Python standard library + installed FFmpeg/ffprobe. Bounded 30s PCM batches for energy scan; intermediate sample counts sum decoded ffprobe audio-frame nb_samples instead of loading full PCM. ffprobe frame JSON still consumes memory. Source is decoded from start per span to avoid imprecise seek/frame index translation; potentially very slow on hour-long/4K recordings and many cuts. 1800-second subprocess timeout; no tested arbitrary-long performance guarantee. Streaming/seek optimization must be a separately tested extension, not hidden gate relaxation.

Paths resolve symlinks before source/skills/model confinement, with exclusive NEW directories and no overwrite; provide every model root via --protect. This is not a hostile multi-process filesystem sandbox or malicious codec isolation. Only authorized trusted files. JSON text remains data; safe generated filenames only; no arbitrary FFmpeg flags. Whole-source transcript/evidence truth and naturalness remain agent/human responsibility.

## Maintained references

- FFmpeg trim/atrim/concat/setpts/asetpts: https://ffmpeg.org/ffmpeg-filters.html
- Mapping, codecs, stream-copy and input/output behavior: https://ffmpeg.org/ffmpeg.html
- Concat demuxer duration/safe syntax: https://ffmpeg.org/ffmpeg-formats.html#concat
- ffprobe streams/frames JSON: https://ffmpeg.org/ffprobe.html
- faster-whisper local/offline usage: https://github.com/SYSTRAN/faster-whisper

Links are documentation, not installation/execution permission. Own original code is MIT; sibling is MIT and external tools/codecs/models/media have independent rights. No external implementation vendored.
