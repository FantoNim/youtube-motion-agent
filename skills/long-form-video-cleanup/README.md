# Long-form camera cleanup

Agent selects evidence-backed chronological keeps; helper validates and joins. It does not find repeated takes, transcribe, determine meaning or listen. Default conservative full-message cleanup has no target duration. Reuses sibling local-video-clipping's probe/hash/path/timestamp/verification code; that sibling MUST remain installed and is not modified here.

## Commands (from workspace)

These are shell-tool command strings, not Code Mode JavaScript. Existing Python 3.12 + FFmpeg/ffprobe required; no Python packages required by renderer/tests.

    python -B skills/long-form-video-cleanup/scripts/cleanup_local.py probe --input "<authorized-source.mp4>" --output "<existing-private-parent>/probe-v001"
    python -B skills/long-form-video-cleanup/scripts/cleanup_local.py plan --input "<authorized-source.mp4>" --keep-list "<reviewed-keep-list.json>" --output "<existing-private-parent>/plan-v001" --protect "<existing-cached-model-root>"
    python -B skills/long-form-video-cleanup/scripts/cleanup_local.py render --input "<authorized-source.mp4>" --keep-list "<same-reviewed-keep-list.json>" --output "<existing-private-parent>/render-v001" --protect "<existing-cached-model-root>"

--ffmpeg/--ffprobe may name existing installed executables. Repeat --protect for ALL cached models. Every output must be NEW with an existing parent outside entire source folder, skills and protected/model roots. Rejects traversal, existing dirs and canonical symlink redirects; not a sandbox against concurrent hostile filesystem replacement or malicious decoder inputs. File/pipe protocols only, not a general local-file sandbox. Work only with authorized trusted media and maintained tools.

Optional speech evidence, only after reading sibling video-lesson-guide completely:

    python -B skills/video-lesson-guide/scripts/transcribe_local.py --input "<source>" --output "<new-chunk-directory>" --model "<existing-CTranslate2-snapshot>" --audio-stream <absolute-index> --start <seconds> --end <seconds>

Each chunk <=1800s, next chunk overlaps 1–2s. Existing local dependencies/model only. See [editorial evidence](references/editorial-evidence.md) for coverage and failure handling.

## Input limits — deliberate fail closed

- One unambiguous video + zero/one audio, explicit absolute indexes, retain ALL original A/V. Additional video/audio, subtitles, attached pictures or data streams block rather than get dropped. Stereo/mono are preserved, no downmix.
- H264 8-bit yuv420p, explicitly progressive, even dimensions, SDR narrow-gamut/limited-or-unknown range accepted by sibling gate. Rotation/display/HDR side data blocks. Unknown color stays unknown, never invent a retag; output metadata must match. No implicit deinterlace, crop, autorotate, HDR-to-SDR or framerate conversion.
- Constant decoded frame cadence 1..240fps, zero container/video/audio starts, known continuous timestamps and durations. Audio AAC mono/stereo with 32000/44100/48000/88200/96000Hz; original A/V durations equal to one sample tolerance. No offsets, VFR/gaps, unsupported channel layouts/codecs or unknown field order.
- Noninteger boundary times are half-up rounded to original frame grid and all requested/actual times/deltas audited. With audio, EACH chosen frame boundary must also be an integer original audio sample (error <=0.0001 sample). At 30000/1001 and 48kHz, use frame indexes divisible by five, after evidence/boundary re-review. Others block; no hidden padding/stretch. No-audio has no audio-lattice constraint.
- Minimum keep span two frames, maximum 2000 keeps. Minimum is a corruption/safety gate, NOT editorial policy; normally retain complete phrases. Selected spans with full-span PCM RMS <=1e-5 block (near digital silence, NOT speech recognition). Quiet intentional visual-only intervals need a deliberate extension; do not lower threshold or drop audio silently. No-audio visual material remains no-audio.
- Source metadata/chapter/text tags are not A/V content; metadata/chapters are deliberately removed from output. Raw probe retained privately. Semantic or color/timing extension requires a separate representative fixture, implementation and tests, not removal of guards.

## JSON schema / workflow

Copy [example](assets/keep-list.example.json) to private project storage. It illustrates shape only; placeholders are NOT usable evidence.

Required top-level fields: schema_version=1, source_sha256, video_stream integer, audio_stream integer or null, mapping_reason, selection_basis, limitations, quantization=nearest_frame_reviewed, coverage, keep, deletions. Unknown fields, duplicate JSON keys, nonfinite/bool numeric times rejected. No output names, arbitrary FFmpeg flags, rearrangement or overlap.

coverage: exact shortest-original-A/V duration, basis text and windows spanning whole source without gaps. Windows can overlap for ASR. Each contains start/end, status, evidence, timing_uncertainty_seconds >=0. Status: reviewed_transcript, reviewed_playback, reviewed_visual_only or synthetic_fixture. synthetic_fixture is for generated tests ONLY; reviewed_visual_only is explicitly rejected whenever the selected source has audio in this speech-cleanup scope; no-audio visual coverage remains accepted. Machine fields do not certify evidence exists or is true. Agent must verify artifacts/context and resolve timing uncertainty at boundaries; merely labeling a failed ASR window as reviewed is forbidden.

keep and deletions: chronological source start/end seconds, reason, transcript_evidence and boundary_review. For no speech use an explicit visual/no-speech basis in transcript_evidence, never pretend ASR occurred. Every deleted interval must match EXACTLY the complement of QUANTIZED keep ranges (within 1 microsecond). Calculate nearest-frame values from inspected rate, review them and record these complement intervals. Plan records requested times, source_start/end, source frame indexes, deltas and output frame/second offsets. No cut-list fields are evaluated as code or used as filenames. No automatic selection claim.

plan writes plan.json (planned_not_rendered), planned map/energy/command evidence, never an output video. Inspect it before render. Successful render writes cleaned.mp4, edit-map.json, report.json, commands.jsonl, part-NNNN.mov + metadata/exact-count verification and span proof JPEGs. Planned map and energy checks remain separately auditable. Incomplete marker retained even on success. report.json complete is the completion gate; failed runs retain partial artifacts and need a NEW directory. No overwrites anywhere.

Audio encoded once at final join. Lossless PCM avoids per-part AAC delay/drift; each part must have exact selected video frames and audio samples. Source is decoded from beginning for frame-index correctness for each part: safe but slow O(number of spans x source duration), not a high-performance NLE. Full timestamp scans also cost time/memory. Per-subprocess 1800s timeout; large-file/large-span-memory limits can block long production. Choose a representative short source slice only with explicit new-source provenance, or design/test a streaming optimization; never skip gates. No promise arbitrary hour-long/4K source performance.

## QA and honesty

Full decode/timestamps/frame count/duration, geometry/aspect/color and original audio rate/layout are mandatory. RGB MAE<=16 and PCM correlation>=0.9 sample first/mid/last of each span. RGB first+last covers both visual sides of every join; PCM checks cover inside each span and the immediate 20ms on BOTH sides of each join, plus total decoded sample count (at most one final AAC packet). These are not listening or click-free audio certification. Every proposed speech cut still needs authorized join playback to check clipped words/clicks/natural pace and semantic continuity. If playback unavailable, retain uncertain edit or deliver only a provisional candidate explicitly stating no listening pass. Proofs can expose private content; never auto-attach. model-facing view_image is separate from local extraction, not guaranteed on-device vision.

## Tests

    python -B skills/long-form-video-cleanup/scripts/test_cleanup.py --output Videos/_tests/long-form-video-cleanup/focused-NNN --test test_13_audio_visual_only_coverage_gate
    python -B skills/long-form-video-cleanup/scripts/test_cleanup.py --output Videos/_tests/long-form-video-cleanup/run-NNN
    python -B "<SOURCE_HOME>/AppData/Local/openclaw/deps/portable-node/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py" skills/long-form-video-cleanup
    openclaw skills info long-form-video-cleanup
    openclaw skills check

Resolve installed skill-creator path on other hosts. Resource links/example JSON checked by focused suite. Test outputs retain logs, command arrays, requests, reports, hashes, RGB/PCM comparisons and proof frames. No user recording, speech ASR, semantic repeated-take detection or listening is exercised. See [preflight/implementation](references/implementation.md).
