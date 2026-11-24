# Local Remotion project template

Adapted from haidrrrry/claude-remotion-skill at 1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383, MIT (see copied LICENSE). Remotion itself has separate licensing; consult the skill licensing reference before commercial use.

## Local PowerShell commands

Run in this project after reviewing package.json. All exact dependencies are pinned; all Remotion packages use 4.0.538. Node 26.12.1/npm 11.20.0 Windows x64 was smoke tested. No API key, hosted renderer, cloud upload, paid API or global npm installation is needed.

    npm.cmd ci --ignore-scripts --no-fund --no-audit
    npm.cmd run typecheck
    npm.cmd run fixture
    .\node_modules\.bin\remotion.cmd browser ensure
    npm.cmd run compositions
    npm.cmd run studio
    npm.cmd run sample

For first-time lock generation only if no package-lock exists, use npm.cmd install --ignore-scripts --no-fund --no-audit, then inspect/save the lock. A reviewed zod 4.6.6 override fixes GHSA-mrhx-c7xc-m3w5 in the upstream transitive 4.5.4; do not run audit fix blindly. This intentional same-major override produces a Remotion Zod-version warning (expects vulnerable 4.5.4); template typecheck/render/Studio build were tested with 4.6.6, but arbitrary schema/editor features need separate checks. Network is needed for npm and initial Chromium downloads, not a hosted render. Avoid unpinned npx downloads. Stop the exact Studio process when done. npm.cmd run studio uses scripts/studio-local.cjs: raw Remotion Studio defaults to all interfaces, and --host is not a supported binding flag. The version-guarded wrapper forces the pinned shared internal getPortConfig provider to 127.0.0.1 for this process only. It does not edit installed packages/config. Re-review it for a Remotion update and verify the actual listener. node scripts/studio-local.cjs --check-binding checks the guard without starting Studio.

The 4s deterministic synthetic audio fixture is for tool verification ONLY; it is not narration or a soundtrack. Production should replace audioSrc in props.example.json with a real approved public/ path and set durationSeconds to its actual measured selected-stream duration. Empty audioSrc is deliberately silent. The template does not auto-transcribe or auto-detect audio length. Use the skill's inspect-media helper; preserve originals; copy/extract recorded audio without unrequested edits. The default chart values are illustrative, not factual claims.

## Editable source

- src/Root.tsx: props-driven duration/fps/size; frames use ceil(seconds*fps).
- src/MotionGraphic.tsx: deterministic type/card/chart scene and continuous Audio outside graphics.
- src/motion.tsx: spring entrance, staggered words, eased bar chart, local image/video, provided-timestamp captions.
- src/theme.ts and props.example.json: replace neutral example palette with the project's brand. This generic template does not prescribe any user's colors.
- mediaSrc/mediaKind: optional local image or muted video inside the card; no remote URLs.
- captionPages: optional {startSeconds,endSeconds,text} objects with checked timestamps. No local speech model or verified STT workflow is configured; the CLI can include unused optional API integrations transitively.

Design stage is landscape 1280x720 and scales as a unit; portrait production requires a deliberate layout redesign, not an automatic crop. Arial is a documented test fallback, not a cross-machine font guarantee. Add a licensed local font for exact production typography.

## Production handoff

Keep original assets in assets/originals, local served copies in public, editable code in src, versioned MP4s in exports, encoded output checks in proof, and brief/storyboard/approval/commands in notes. Inspect encoded frames and audio before delivery. Get sample style approval before the full-length production render unless waived. No user recording is included in this template.
