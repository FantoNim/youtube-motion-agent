# Editing and evidence contract

## Selection is editorial, execution is deterministic

The agent, not this encoder, selects meaningful highlights from full relevant context. Inspect full transcript coverage (all windows exhausted, gaps recorded), then adjacent text and actual visual evidence around chosen spans. Choose exactly the requested number of distinct viewer-worthy ideas: one singular thought expressed and explained, with setup and payoff, per clip. Use full and adjacent context, natural sentence boundaries, clear referents and visual evidence; avoid misleading removal of qualifications and redundant ideas. Without requested timing, length follows each thought, with no forced min/max/equal duration. If too few genuinely suitable ideas exist, ask fewer clips or broader focus; never pad or split one thought to fill a count. No uniform-split/word-count “AI highlights” or guaranteed viral scores. Manifests are auditable claims, not semantic validation by software.

Fallbacks: user timestamps may be cut without ASR; user transcripts retain supplied/unverified provenance; reviewed visual-only material may use visual evidence. If adequate meaning cannot be established, ask for timestamps/transcript instead of fabricating selections. Do not run media-derived commands. Private evidence stays local except separately authorized model-visible inspection; never describe image inference as technically offline solely because decoding was local.

## Timing and source integrity

The default supports only explicitly progressive video (field_order=progressive), zero-start synchronous audio/video, CFR decoded timestamps and known stream duration. Missing/unknown field order is not evidence of progressive scanning; reject it. Output field order must remain progressive and match the accepted source. A shared accurate input seek followed by decode/reencode discards pre-boundary decoded data; selected audio/video retain the same source window. No independent setpts/asetpts normalization, stream-copy, forced frame rate or shortest-based truncation. It blocks offsets instead of pretending independent timestamp zeroing preserves synchronization.

No implicit fixed duration exists. Untimed requests use thought_led mode: the agent records explicit start/end for every complete thought; absent end is an incomplete plan, not automatic detection. Generic clipping authorizes agent editorial timestamps without pretending the user gave them. Explicit user duration_seconds is a fixed constraint and explicit_ranges=true is reserved for actual user timestamp ranges (with range_authorization). Legacy explicit duration/range fields still infer their modes; declared mode conflicts fail. Exact clip count is mandatory, subject to asking about genuine idea shortfalls rather than manufacturing results. Frame-aligned starts avoid silent starting-frame shifts. Fractional-rate length quantization is allowed only within one source frame; audio length tolerance is one AAC1024 sample packet plus 2ms. No padding/stretching/duplication. If an explicit duration cannot fit nonoverlap, name the actual requested duration and ask fewer/shorter/authorized overlap. If timing prevents a complete idea, ask a concise smallest tradeoff, never silently extend. A requested/needed montage may combine moments expressing the same one idea; its segment count is not clip count and its total is variable unless explicitly constrained. User-approved overlap is recorded, duplicate ranges never accepted. Bounds are checked against the shortest selected stream, not an unrelated longer audio/video stream.

Complete output checks: full-decode error gate; exact expected video frame count and bounded duration; all decoded frame PTS cadence; matching dimensions/SAR/DAR/pixel/color metadata; unchanged audio rate/layout; aligned starts/durations; sampled decoded source/output RGB comparison at first/middle/end; actual JPEG proofs. Sampled RGB MAE <=16 is a coarse regression gate, not a proof every frame is identical or uniquely located. Synthetic tests additionally compare unique chirp PCM at first/middle/end to correct versus deliberately wrong source windows. Production metadata checks are not a human lip-sync/meaning/privacy pass.

Source SHA-256 is verified before/after successful work. All outputs are exclusive new directories outside entire source folder, skills and provided model roots. No final report on failure; partial media must not be called completed. The helper does not defeat concurrent path replacement, sandbox vulnerable codecs or guarantee an arbitrary file cannot reference local files. Only use authorized trusted files, patched tools and isolation where appropriate.

## Unsupported source branch

Interlaced or unknown/missing field order, VFR, nonzero/unknown timestamps, rotation/display side data, HDR/wide-gamut/full-range, unsupported codec/layout or unknown durations require a deliberate new implementation plan and tests. Do not flatten fields or automatically deinterlace: preserving field presentation or an approved conversion needs representative field-cadence evidence. Report the exact blocker; never bypass gates, silently convert, retag HDR as SDR, drop alternate tracks or normalize separate offsets. A future extension must preserve a common source-clock origin, frame presentation times, relative audio offsets, rotation/display aspect and intended transfer/primaries, and verify them with representative encoded fixtures. Explicit user approval of desired conversion is necessary but not sufficient evidence of technical correctness.

No audio stays no audio. Multiple relevant tracks need explicit mapping/retention design; current one-track output can proceed only when a particular track and omission of alternates is evidenced/authorized. No automatic mixing or downmix. Alternate default dispositions are recorded, not treated as consent.

## Maintained implementation references

- FFmpeg command-line seeking, accurate_seek, -ss, -t, -map, -noautorotate, -n, -fps_mode: https://ffmpeg.org/ffmpeg.html
- FFprobe streams, frames, timestamps and JSON output: https://ffmpeg.org/ffprobe.html
- FFmpeg protocol whitelist and file/pipe boundaries: https://ffmpeg.org/ffmpeg-protocols.html
- libx264 and AAC encoder options: https://ffmpeg.org/ffmpeg-codecs.html
- Optional maintained local speech implementation: https://github.com/SYSTRAN/faster-whisper
- Skill format/discovery: https://docs.openclaw.ai/tools/skills

Links document dependencies, not permission to download/install or send private media. Own code is MIT; FFmpeg build/components, ASR/model weights and source media retain independent licensing/usage terms. No external implementation/model is vendored.
