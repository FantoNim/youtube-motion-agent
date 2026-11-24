# Provenance and adaptation audit

- Source: https://github.com/haidrrrry/claude-remotion-skill.git
- Exact reviewed upstream commit: 1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383 (HEAD checked 2026-10-25).
- Reviewed clone: <SOURCE_HOME>/AppData/Local/Temp/openclaw-remotion-upstream-1dcbe5e (outside skill discovery).
- Original author/license: Copyright (c) 2025 haidrrrry, MIT. LICENSE retained verbatim.
- Read README.md, LICENSE, CONTRIBUTING.md, examples/README.md, original SKILL.md, assets/theme.ts, both references, examples/package.json and ALL executable upstream helpers before any execution.
- Script inventory: scripts/build-skill.sh removes/rebuilds a Claude .skill ZIP; examples/scripts/gen-sfx.mjs writes local WAVs (some Math.random noise/phase); examples/scripts/gen-track.mjs writes a deterministic local WAV. NONE was executed. No upstream installer was used. The .skill archive and upstream demo binaries were not installed.
- Upstream techniques adapted: springs, multi-property entrances, staggered words/cards, centralized theme, fps-relative motion, bar counters, local media, mandatory render/extract/inspect/fix loop.
- Rewritten for OpenClaw tools, Windows PowerShell npm.cmd/npx.cmd, local pinned npm and Chromium, recorded-audio duration/timing, sample approval and source/export organization. Claude installation paths, shell ZIP packaging and model-specific commands removed.
- Deliberate corrections: Remotion is NOT MIT or unconditionally free; optional layer/texture/micro-motion and sound are design choices, not universal requirements; counters may progress linearly; no fabricated Whisper/STT availability; no network fonts/media; no hosted renderer or API key.
- New helper and template source is distributed with the same MIT notice. This notice does not relicense Remotion, React, FFmpeg, Chromium or third-party assets.
- Future updates: review the upstream diff, scripts, license and dependency changes before selectively adapting; never git-pull or copy an unreviewed tree directly into active skills.
