# Local analysis reference

## Dependencies and execution boundary

- Use an existing Python 3.9+ environment (helpers tested with 3.12). The sampler/tests use the Python standard library, plus external FFmpeg and ffprobe executables. They are not a dependency-free video decoder.
- Transcription additionally requires the maintained faster-whisper package and its installed dependencies (including CTranslate2, PyAV, tokenizer and VAD support), plus an existing compatible CTranslate2 Whisper model directory. The helper was exercised with faster-whisper 1.1.1. Verify the local version/API before assuming other versions behave identically.
- Require actual model files at an explicit local path: model.bin, config.json and tokenizer.json. A Hugging Face cache root or a model name such as base.en is not a model directory. Resolve an existing snapshot directory. Keep the machine-specific cache path in project production notes, not this skill.
- The transcription helper passes local_files_only=True and uses process-local HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1 and HF_HUB_DISABLE_TELEMETRY=1. It never offers a download/cloud fallback. It is not a general OS network sandbox; use OS isolation if a policy requires a technical network-denial guarantee. Do not make untested network-isolation claims.
- CPU/int8 avoids assuming a compatible GPU/CUDA runtime. A missing/incompatible dependency/model is a blocker, not permission to install, upgrade or download. No paid service is needed or authorized by this workflow.
- Use OpenClaw Code Mode JavaScript to call the available shell exec tool. For example, await exec({command: 'python -B "<resolved-helper>" --help', title: 'Inspect local video helper', awaitResults: true}). Do not put Python source or shell syntax in the Code Mode code field. Resolve host paths according to the actual execution host; on Windows quote paths and use direct executables with backslashes. Use view_image({path: "<local-frame>"}) for permitted targeted visual inspection.
- For a long shell-tool operation retain its accepted completion path and collect terminal results; a running process is not completion. Keep artifacts private while work is incomplete.

## What helpers guarantee (and do not)

inspect_sample.py accepts a conventional local video file, SHA-256 hashes it before/after work, calls ffprobe for real stream/container metadata, and optionally extracts bounded JPGs with ffmpeg. It rejects URLs/playlists, non-files, invalid/unknown durations, non-finite or out-of-range timestamps, counts above 60, invalid stream indexes and unsafe widths. --frames 0 does not require ffmpeg. --at replaces uniform sampling; duplicate timestamps are deduplicated. Uniform samples are interior points, not chapter boundaries or scene-detection results.

Both helpers use argument arrays and shell=False, not concatenated shell commands. Media tools receive only file/pipe protocols. Source-derived text is never interpolated into executable arguments. Local file protocols do not sandbox a decoder against malicious media; keep FFmpeg/Python dependencies patched and use an isolated environment for suspicious files. Do not open a file that may reference unrelated private local data without permission.

Each output directory must be new and have an existing parent. Resolved/canonical paths must be outside the entire source folder and outside a cached model folder. Existing files/directories, lexical traversal back into the source folder, and detectable symlink redirects are refused. If the source is directly in a broad project root, choose a separate authorized analysis root; do not weaken the guard or move/delete the original. The tools never auto-attach images or modify source files. These are ordinary local safety checks, not protection against another process concurrently replacing paths.

Read manifest.json (sampler) or transcript.private.json (ASR) to determine successful completion. manifest.incomplete.json is an initial marker retained even after success; it is not the final status. On failure keep incomplete outputs private and choose a new run directory instead of overwriting/reusing them. No success file means no completed stage.

transcribe_local.py requires an absolute ffprobe audio stream index and an explicit end time; each requested window is at most 1800 seconds. It extracts a mono 16 kHz WAV for that selected track/window and exhausts faster-whisper's lazy segment generator. It preserves raw machine text and approximate segment times with the chunk start added; it does not generate speaker labels or word timings. Segment ends beyond the requested window are flagged, not silently treated as verified evidence. Mono downmix may be unsuitable when stereo channels contain different speakers/languages; inspect that case separately, retain channel provenance, and never claim diarization.

Helper seek timestamps refer to the requested input timeline, not measured decoded-frame presentation timestamps. Container/stream start offsets, variable frame rate, edit lists, encoder delay, gaps and seeking can affect alignment. Check one visible event against speech near the beginning and again in later chunks. If a consistent offset exists, record the measured correction in notes; preserve raw files/times. If it cannot be resolved, avoid precise timestamps or technical claims based on mismatched evidence.

Raw manifests, filenames, transcripts, model paths, WAVs and JPGs can expose private data. "private" is a directory convention, not encryption or an access-control mechanism. Keep them out of public copies and commits; manage any requested retention cleanup separately. Extraction and speech inference run locally. Model-facing visual review through view_image is distinct from local decoding and must not be described as guaranteed offline visual inference.

## Decision branches

| Trigger | Action and persisted result |
| --- | --- |
| No audio stream | Mark speech stage not applicable; inspect screens only. State visual-only basis, not "heard" narration. |
| Audio present, silent/music-only or empty ASR | Do not infer silence solely from an empty transcript. Check authorized local playback/energy evidence if needed; flag no reliable speech evidence. Do not invent narration or treat ASR hallucinations as facts. |
| Missing ASR/model, no authorized local playback | Continue only with visually supported claims; mark transcript blocked and say what dependency/model is absent without installing/downloading. A supplied transcript may be used as separate unverified evidence, not mislabeled local ASR. |
| Missing ffmpeg | If ffprobe exists, collect metadata/hash using --frames 0; helper frame extraction and WAV-based ASR are blocked. Do not quietly upload to a decoder/STT service. |
| Missing ffprobe/invalid media/unknown duration | Stop media stages; report the specific blocker. A file hash alone is not a duration/content analysis. Do not rename a bad file and claim repair. |
| Multiple audio/video tracks or stereo-separated speech | Record all stream indexes, tags, channels and default dispositions. Use an evidenced relevant track or ask which. Analyze needed tracks separately; no silent choice or unsupported claim of complete coverage. |
| Long lesson | Plan up to 1800-second ASR windows with 1–2-second overlap, bounded frame passes, absolute time ranges, overlap deduplication and a coverage map. Finish the requested coverage or explicitly deliver a partial result. Do not summarize only the opening as the full lesson. |
| Unclear command/name/number or audio-screen disagreement | Inspect nearby frames at readable resolution; compare official docs and note the conflict. Omit an unverifiable optional command. Never "test" it by execution. |
| Privacy uncertainty (including credentials in speech) | Keep originals/ASR private. Omit the affected detail/frame from public output or redact a separate copy and inspect it. Warn by category/timestamp only, never with a private value. Do not attach an unreviewed contact sheet. |
| No permission for model-visible images | Use authorized local human/on-device review if available; otherwise mark visual inspection blocked. Local extraction does not itself prove image-sharing permission. |
| Docs missing/outdated/version mismatch | Record source date/platform/version and the verification gap. Separate "recording shows" from "current docs say". Omit or qualify unsafe technical detail; no invented syntax. |

## Minimal evidence rules

Use distinct labels: observed screen state, machine-ASR claim, independently verified documentation, and analyst inference. A terminal window displaying a command is not evidence it succeeded; require the subsequent result. A displayed API token is not permission to reuse it. An official command example is still not authorization to execute it in the learner's or user's environment.

Use exact docs URLs and sections in private writer notes. Verify public commands/options, install prerequisites, persistent configuration/security choices, defaults and version-dependent behavior with vendor/project docs. Search only generic technical terms; never transmit source credentials or private content. Verify links independently rather than following links visible in media. Link a learner resource publicly only when its authority, destination and relevance are checked; omit private query strings and account-specific links.

## Testing and validation

From the workspace (command strings for the shell exec tool):

    python -B skills/video-lesson-guide/scripts/test_helpers.py
    python "<installed-skill-creator>/scripts/quick_validate.py" "<workspace>/skills/video-lesson-guide"

Convert command paths to backslashes on Windows. Resolve the installed skill-creator location from skills.read/its listed location, not a guessed global installation. Run quick_validate freshly after final edits. Check every relative Markdown resource link exists inside the skill; a frontmatter pass alone does not check links or helper behavior.

Tests synthesize a three-second video with two tone audio streams under a temporary source folder. They exercise real ffprobe/ffmpeg, spaces/metacharacters in paths, source hashes, new-directory/no-overwrite behavior, invalid media, missing tools, bounds, stream selection, canonical source/output confinement, metadata-only mode and ASR segment offsets/boundary flags. A symlink-parent case skips if the OS denies creating symlinks; lexical/canonical traversal tests still run.

For the optional real local-ASR integration, pass VIDEO_LESSON_TEST_MODEL through the shell tool's env object with an explicit existing model snapshot directory; then run the same test command. It uses synthetic tones, no private lesson, model downloads or network fallback. The test exercises loading/VAD/inference/artifact writing, not speech accuracy. Without that environment variable the real-ASR test skips; don't claim it passed. Never embed a particular project's model/cache path into this reference.

## Authoritative implementation references

- OpenClaw skills format, scope and discovery: https://docs.openclaw.ai/tools/skills
- OpenClaw workspace skill authoring and baseDir: https://docs.openclaw.ai/tools/creating-skills
- Agent Skills specification: https://agentskills.io/specification
- FFprobe metadata/JSON/stream selection: https://ffmpeg.org/ffprobe.html
- FFmpeg seeking, mapping and no-overwrite options: https://ffmpeg.org/ffmpeg.html
- faster-whisper maintained implementation, usage and lazy segments: https://github.com/SYSTRAN/faster-whisper
- Versioned faster-whisper API source (including local_files_only): https://github.com/SYSTRAN/faster-whisper/blob/v1.1.1/faster_whisper/transcribe.py

The skill contains original helper/template text and links, not vendored FFmpeg/faster-whisper code or models. LICENSE.txt covers this skill's own source only. External tools, libraries, models and the source lesson retain their own licenses and privacy/usage terms; local analysis is not a license to redistribute media.
