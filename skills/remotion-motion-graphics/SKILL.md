---
name: remotion-motion-graphics
description: Create, edit, preview and render local Remotion motion graphics, kinetic typography, charts, intros, explainers and captioned or narrated MP4 videos. Use for code-driven animated videos, editing an existing Remotion project, or adding graphics to recorded narration or footage. Local-first OpenClaw workflow; no hosted renderer or media upload.
license: MIT
homepage: https://github.com/haidrrrry/claude-remotion-skill
---

# Local Remotion Motion Graphics

1. **Establish the brief and inspect existing material.** Read the project README, source and package scripts before changing an existing project. Record target size/fps, audience, visual references, palette, deliverable, audio policy and sample approval requirement. Inspect supplied MP4/audio with scripts/inspect-media.mjs (resolve all skill-relative paths against this directory). Read [references/workflow.md](references/workflow.md). Preserve originals; never derive recorded narration length from script word counts. If no user media exists, label generated fixtures as tests, not the requested finished video. **Done:** notes/brief.md, actual stream durations and source inventory exist; unknowns are explicit.

2. **Check licensing, tooling and local privacy.** Read [references/licensing-and-runtime.md](references/licensing-and-runtime.md) and [UPSTREAM.md](UPSTREAM.md). Check Node, npm.cmd, npx.cmd, ffmpeg, ffprobe and disk. Remotion has a separate conditional free/company license, NOT MIT; recheck eligibility for commercial use. Do not buy a license, use paid APIs, upload media, install globally or execute upstream installers. Inspect manifests/scripts before execution; prefer reviewed project-local pinned dependencies with a lockfile and npm.cmd ci --ignore-scripts. Initial package/Chromium downloads require internet; rendering is local. **Done:** runtime and applicable license notes recorded, no payment/privacy blocker left unresolved.

3. **Create an organized editable project.** Use node <skill>/scripts/init-project.mjs "<workspace>/Videos/<project>" only for a new empty path; it refuses to overwrite existing files. The [assets/template/README.md](assets/template/README.md) explains the pinned template, local commands, props and synthetic audio fixture. Use existing adequate Remotion projects rather than rebuilding them. Keep source in src/, original inputs in assets/originals/, browser-served approved assets in public/, and outputs in exports/, proof/, notes/. Set brand colors per project, not in this reusable skill. **Done:** source, manifests, asset attribution and production notes have stable paths.

4. **Time the story to the real recording.** Preserve supplied narration in full unless the user requests editing. For graphics-only output from narrated MP4, extract the audio without a needless quality loss; see workflow reference. Set composition frames to ceil(measuredDurationSeconds * fps) and record rounding. Inspect stream start offsets and trailing silence; do not silently stretch, truncate, replace or synthesize narration. Build notes/storyboard.csv with start/end seconds, transcript phrase, graphic, source, audio and approval state. Use supplied timestamped transcript or manually verified listening/timing where available. Do NOT claim automated transcription or word sync without a verified local STT tool and checked timestamps. **Done:** all recorded audio time is covered by a storyboard; unverified words/times are labeled.

5. **Build purposeful animation.** Read [references/design-and-motion.md](references/design-and-motion.md); the typechecked assets/template/src/motion.tsx supplies reusable entrances, word reveals, chart bars, local media and caption pages. Drive animation from frame/fps, use eased clamped progress or springs for entrances, stagger hierarchy, include deliberate holds and exits. Linear clock/data progression is valid when truthful. Avoid forced grain, motion, sound or color grades that harm accessibility or a clean brief. Load only approved local media with staticFile; use local fonts or explicitly document fallback. **Done:** typography/shapes/charts/media fit the brief, temporal behavior is deterministic, narration is not doubled.

6. **Preview and get sample approval before a full production render.** Typecheck, inspect composition metadata, run local Remotion Studio bound to loopback, and render a short representative MP4 (typically 3–10 seconds, or the requested range). Inspect extracted frames plus playback/audio by an available local browser/desktop route. Use the browser-automation skill if controlling browser UI; never publish a preview portal or upload source media without permission. Show the sample file/proof to the user and wait for style approval before a long final export, unless approval was explicitly waived. Autonomous smoke tests may complete without pretending to be user-approved style. **Done:** sample exists, checks are recorded, and production approval is confirmed or clearly pending.

7. **Render locally, verify the encoded output, then deliver.** Follow [references/verification.md](references/verification.md): H.264 MP4 + AAC audio, probe actual streams/duration/frame count, decode the whole file, inspect first/middle/transition/end frames, and check audio continuity, clipping and sync. Re-render after fixes and inspect fresh files. Report source/assets/export/proof paths, exact commands, runtime/dependency versions, approval state and honest limitations in notes/production-notes.md. **Done:** the finished encode—not only a source still—has evidence of video AND audio verification; no unsupplied user project is claimed complete.

## Tool use in OpenClaw

Use native file read/write tools for files; execute Node/npm/FFmpeg via the available shell exec tool. Code Mode JavaScript calls await exec({command: "...", workdir: "...", title: "...", yieldMs: 1000}); it is not itself a Node shell and cannot import Node modules. Node helpers run as node path/to/helper.mjs through shell exec. On Windows use npm.cmd / npx.cmd to avoid PowerShell's script execution-policy block; do not weaken that policy. Collect long-running process results via the returned process session and completion path. Inspect proof PNGs with view_image; successful execution alone is not visual verification.

## Resources and focused checks

- [scripts/init-project.mjs](scripts/init-project.mjs): guarded template initialization; no network or installs.
- [scripts/inspect-media.mjs](scripts/inspect-media.mjs): local ffprobe JSON, per-stream timing, audio presence; optional explicit ffprobe path.
- [scripts/self-test.mjs](scripts/self-test.mjs): initialization/no-overwrite, deterministic WAV and media inspection tests; run with Node.
- [assets/template/README.md](assets/template/README.md): exact local commands and reusable source template.
- [LICENSE](LICENSE): upstream MIT attribution for the adapted skill only.

Before releasing a skill change: run skill-creator quick_validate.py, node scripts/self-test.mjs, project npm.cmd run typecheck, and a fresh local audiovisual MP4 smoke test. See verification reference for failure gates.
