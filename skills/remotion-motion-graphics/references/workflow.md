# Brief, narration, timing and project layout

## Branch contract

- New graphics-only brief -> storyboard + editable source + approved sample + local MP4.
- Recorded narration/MP4 -> measured audio/video streams + preserved narration + timed graphics + sample approval + local MP4.
- Existing Remotion project -> inspect complete relevant source/manifests first, preserve conventions, modify narrowly, typecheck and re-render the requested composition.
- Captions -> provided/manually verified timestamps, or a verified installed local STT workflow; unverified transcription is a blocker to a claim of word-level accuracy, not a reason to fabricate it.
- Local tool smoke test -> explicitly synthetic 3–5s clip, deterministic fixture, audio mux/encode proof; not a user video or style approval.

## Assets and measurements

Keep original files byte-for-byte in assets/originals; record hashes with Get-FileHash. Copy only needed browser-served files into public. Avoid filename changes without inventory mapping. Run:

    node "<skill>/scripts/inspect-media.mjs" "assets/originals/narration.mp4" > notes/source-probe.json

Inspect per-stream duration, start_time, channels/sample rate, fps, dimensions and format duration. Container length alone can include trailing video; audio stream duration is the narration baseline for graphics-over-audio, while retaining original picture uses original media coverage. Choose and record offset handling; test it. To extract an AAC track from a compatible MP4 losslessly:

    ffmpeg -n -i assets/originals/narration.mp4 -map 0:a:0 -vn -c:a copy public/narration.m4a

If stream copy/container compatibility fails, keep original intact and produce a documented local WAV intermediate:

    ffmpeg -n -i assets/originals/narration.mp4 -map 0:a:0 -vn -c:a pcm_s16le public/narration.wav

No denoise, trim, speed change, silence removal, TTS replacement, or normalization without user scope. Muxing/rendering commonly re-encodes to AAC, so do not claim final encoded audio is bit-identical. The source and copied intermediate can be hash/packet verified. Do not double audio by combining unmuted OffthreadVideo with a separate Audio of the same track.

## Storyboard and transcript

Copy the script/transcript if supplied, but time it to the recording, not reading-speed estimates. Add columns: start_seconds,end_seconds,spoken_text,visual,asset_source,audio,verification,approval. Start <= end; no unintended gaps/overlap; coverage includes final spoken word and intended tail. Record timestamps as measured/provided/estimated. Listen via local playback where available; if no audio-capable tool or transcript exists, state the limitation and request timing input only when truly needed. Never call a synthetic tone a narration test of intelligibility. STT/model downloads must be explicit, licensed, local and independently verified; no speech model or configured local transcription workflow is bundled here. CLI dependencies may include unused optional API integration libraries; that is not proof that transcription is available or authorized.

Use frame = round(seconds * fps) for event boundaries; ceil(durationSeconds * fps) for full recording coverage. Fractional-frame padding should be <1 frame. Props durationSeconds is manually supplied from the probe result, not magical automatic discovery. For multiple audio streams select the intended language/track explicitly.

## Project tree

    Videos/<slug>/
      README.md
      package.json + package-lock.json
      src/                     editable React/TypeScript
      assets/originals/        untouched originals and license records
      public/                  approved local media/fonts
      exports/sample-v001.mp4
      exports/final-v001.mp4
      proof/                   extracted encoded frames and probe JSON
      notes/brief.md
      notes/storyboard.csv
      notes/production-notes.md

Use new versioned output names or intentional --overwrite only inside the project. Keep commands, source references, approvals, render settings, runtime versions, tests, unresolved limitations and original/output duration in production notes. Deliver source + assets + MP4 + proof, not just a screenshot. Keep a long final render gated on sample style approval unless waived.
