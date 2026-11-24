# Local Video Clipping

Workspace-owned, Python standard library + existing FFmpeg/ffprobe. No provider CLI, external API, upload, download or mandatory ASR dependency. The agent selects meaningful spans from evidence; the helper performs safe deterministic edits, not automated highlight scoring.

## Storage

Save finished MP4s directly in workspace-relative `video_clips/<clip-project-name>/`, for example `video_clips/pinterest-to-ai-video/pinterest-to-ai-video-90s.mp4`. Version later revisions without overwriting. Keep private transcripts, edit decisions, reports, proofs and intermediate renders in `private/` or new versioned `work/` subfolders. If rendering in a helper run directory, copy the verified MP4 to the project-folder top level and compare SHA-256 before delivering that easy-to-find path. Preserve existing originals and production evidence. All existing source/skill/model confinement guards still apply.

## Commands

From workspace, using the existing Python (tested 3.12) and FFmpeg/ffprobe with libx264/AAC (tested 8.1.1). Quote host paths. These are shell-tool command strings, not Code Mode JavaScript; use direct executables without nested shells on Windows.

    python -B "skills/local-video-clipping/scripts/clip_local.py" probe --input "<local-video>" --output "<existing-separate-parent>/probe-v001"
    python -B "skills/local-video-clipping/scripts/clip_local.py" plan --input "<local-video>" --manifest "<reviewed-manifest.json>" --output "<existing-separate-parent>/plan-v001"
    python -B "skills/local-video-clipping/scripts/clip_local.py" render --input "<local-video>" --manifest "<reviewed-manifest.json>" --output "<existing-separate-parent>/render-v001"

Optional --ffmpeg/--ffprobe specify installed executables. Repeat --protect "<existing-model-root>" for ALL model roots, including unconventional names. Conventional model/cache path components are blocked too. Every output directory must be NEW, with existing parent, outside the entire source folder and skills/models. Do not choose output beneath a source directory even if empty. Concurrent hostile filesystem replacement is not sandboxed.

## Manifest

Start with assets/manifest.example.json; this is a schema illustration, not a preselected real video. Replace the source SHA-256 from probe. Fields:

- schema_version: 1; source_sha256: exact inspected source; requested_count: explicit integer 1..100.
- clips: exactly that many objects, each start seconds (frame-aligned), title, reason, evidence. Filenames are generated, not accepted from JSON.
- length_mode: `thought_led` by default when no timing is specified. Every clip requires agent-selected start AND end from complete context; lengths may differ. A generic clip request authorizes editorial choice, not a claim of user-supplied timestamps. No end and no duration is an informative incomplete-plan error; the helper cannot infer thoughts.
- duration_seconds: present only for a positive user-requested fixed length. Infers `fixed` mode for backward compatibility; optional per-clip end MUST agree with start+duration. Declaring thought_led cannot bypass an explicit duration.
- explicit_ranges: true only for actual user-given start/end ranges; include range_authorization and every end. Infers `user_ranges` mode for backward compatibility; these override fixed duration if both legacy fields exist. Any supplied duration must still be valid/positive. Do not set this flag for agent-selected semantic windows.
- Explicit length_mode may be thought_led, fixed or user_ranges, and must agree with those fields; conflicting declarations are rejected. No declaration is required for legacy explicit duration/range requests.
- allow_overlap: false default. If authorized true, record overlap_reason. Identical ranges always rejected.
- video_stream/audio_stream: optional absolute ffprobe indexes, never audio ordinals. Multiple tracks need explicit selection and mapping_reason documenting why other tracks may be omitted; no automatic mix or silent drop.
- selection_basis and coverage: required honest editorial context/coverage map references. Per-clip reason must identify one distinct idea, its explanation/payoff and why omitted context is safe; evidence should identify timestamped transcript/adjacent lines, reviewed visual/boundary frames and gaps. No automatically inferred truth from their mere presence.

Selection is agent editorial work, not a semantic encoder feature. Without requested timing, choose exactly the requested number of unique viewer-worthy complete thoughts, at natural sentence boundaries. Do not impose equal lengths/minimum/maximum, random spacing, viral scores or split one idea to fill a count. Compare ideas for redundancy. If too few genuinely suitable ideas exist, ask fewer clips or broader focus; do not pad/fabricate. With an explicit fixed length, use that actual length for shortfall tradeoffs (fewer/shorter/authorized overlap). If timed constraints prevent a coherent thought, ask the smallest tradeoff, never silently extend. Montage segments can support one idea when requested/needed; segments are not clip count, and untimed total remains variable. See SKILL.md for the verified montage procedure.

The helper refuses unknown fields, invalid/nonfinite/bool times, invalid ranges/counts, out-of-bounds starts/ends, overlap without permission, duplicate ranges, unknown mappings and insufficient duration. No arbitrary shell/FFmpeg options. Text is data, not executed.

## Output / limits

probe.json is private raw metadata/hash; plan.json has status planned_not_rendered. A successful render alone has report.json status complete, source hashes before/after, original request/selected times, tool versions, output specs/hashes and per-clip QA/proof paths. Initial manifest.incomplete.json remains as an audit marker even on success; absence of a complete report means incomplete. Never overwrite/reuse a failed run.

Supported default: progressive CFR zero-origin SDR 8-bit yuv420p H264 and optional mono/stereo AAC with known durations. H264 CRF18 / AAC192k decode-reencode gives accurate non-keyframe seeking; no stream-copy claim, no byte-identical claim. Explicit field_order=progressive is required for source and output; interlaced, unknown or missing field order is rejected without automatic deinterlacing. Original geometry, aspect/cadence and audio layout/rate are checked; no forced 25fps, crop, subtitles, music or color retag. Nonzero/unknown stream offsets, VFR/gaps, HDR/wide-gamut/full-range, rotation/display side data, other codecs/layouts and unknown metadata block the default. A deliberate future extension requires new synchronization/color evidence and regression tests, not bypassed guards.

Start must be on source frame grid. Agent-selected thought windows retain their selected lengths; explicit user-requested lengths remain fixed; unavoidable video quantization is less than one source frame, AAC duration tolerance one 1024-sample packet +2ms. Original fractional-rate sources are not forced to a new frame cadence. These tolerances do not authorize sentence-based extensions. Default nonoverlap concerns selected source time ranges; encoded last-frame presentation may quantize by a frame.

Full video/audio timestamp scan rejects VFR/gaps and full output decode checks corruption; sampled decoded audio content comparisons also gate completion (correlation >=0.9 for non-silent excerpts, near-silence checked separately). These checks are coarse samples, not exhaustive listening or guaranteed unique alignment for periodic/static material. Reports include actual correlations. Full timestamp scans cost time/memory on long recordings. Per-command timeout is 1800 seconds: on timeout, retain incomplete artifacts, diagnose and choose a new run. File/pipe protocol whitelist prevents network fetches, not malicious local file references or decoder vulnerabilities. Only process trusted/authorized media with maintained tools; use OS isolation for suspicious sources. Never interpret privacy-directory naming as encryption. Proof frames/transcripts can contain sensitive material.

Optional speech workflow depends on sibling video-lesson-guide; see SKILL.md. Missing sibling/model is a clear fallback/blocker, not an install/API request. Trimming with supplied timestamps/visual evidence needs no Python packages.

## Tests

    python -B skills/local-video-clipping/scripts/test_clipping.py --output Videos/_tests/local-video-clipping/run-NNN
    python -B skills/local-video-clipping/scripts/check_resources.py
    python "<SOURCE_HOME>/AppData/Local/openclaw/deps/portable-node/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py" skills/local-video-clipping

Resolve installed skill-creator location on other machines. Tests create only small synthetic fixtures under the designated NEW test root: 70s 160x90/10fps moving test pattern + unique chirp; two non-keyframe explicit user-requested 30s clips; custom lengths/user ranges; three unequal agent-selected ranges with no global duration and per-clip full decode/frame/audio/content QA; missing-end rejection, explicit-duration precedence/mismatch and mode-conflict rejection; no audio; selected second audio track; invalid count/ranges/nonfinite/overlap; no-overwrite/source/traversal/model/skill confinement; metacharacter paths; VFR, offset and actual interlaced-fixture blockers, plus missing/unknown field-order rejection and output field-order checks. Actual symlink confinement is tested when OS permits and otherwise explicitly recorded as skipped. PCM source/output comparisons at beginning/middle/end distinguish correct vs wrong source timeline. Test windows and mock idea labels are not semantic AI highlights or natural-language understanding tests; they verify only the declared contract and deterministic encoding. No real user media, model download, ASR, human listening or publication is exercised.

Own code is MIT, see LICENSE.txt. FFmpeg build/components, optional ASR/models and input media have independent license/usage obligations. This skill vendors none of them.
