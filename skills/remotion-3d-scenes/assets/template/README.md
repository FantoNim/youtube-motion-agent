# Procedural ThreeCanvas starter (silent technical fixture)

This editable set tests genuine Three.js geometry/materials/lights/shadows through React Three Fiber and @remotion/three. It is not a style guide or a finished user video. No narration, TTS, stock media, textures, music or SFX is included. On-screen labels deliberately identify a technical test; remove production metadata for learner-facing work unless explicitly requested.

## Copy and install safely

1. Inspect the target first; use a new empty workspace project directory, e.g. Videos/my-3d-project. Copy this template's files there, not its parent skill. No installer/scaffolder is required.
2. Inspect package.json and the full lock, installed node_modules and any links/junctions. Do not install through a shared junction. Local package cache can be reused by npm; installed dependencies belong only to the new project. Remotion packages must all stay at 4.0.538.
3. Review package-lock origins/integrity and lifecycle inventory. Then, if the missing dependencies are task-authorized, run npm.cmd ci --ignore-scripts --no-fund --no-audit. This performs project-local registry downloads; it does not upload media. No global install or install scripts.
4. Inspect an already installed compatible Chromium executable. Set REMOTION_BROWSER_EXECUTABLE to its absolute path. On the test machine the existing remotion-local project browser is reused read-only, not installed into/shared with this project.
5. Check licensing before actual production; the Remotion package license is not MIT and current personal/evaluation eligibility is not a blanket business license.

## Exact PowerShell commands from the copied project

    npm.cmd ci --ignore-scripts --no-fund --no-audit
    npm.cmd run typecheck
    npm.cmd test
    $env:REMOTION_BROWSER_EXECUTABLE = 'C:/absolute/verified/chrome-headless-shell.exe'
    $env:REMOTION_GL = 'angle'
    node scripts/render-test.mjs --stills
    npm.cmd run render
    npm.cmd run verify

The checked runtime uses Windows x64 Node 26.12.1, npm 11.20.0, FFmpeg/ffprobe 8.1.1 on PATH. The render script requires Remotion 4.0.538 for its process-local loopback guard. Direct Node APIs explicitly receive chromiumOptions.gl; CLI config is not used. angle is a requested backend, not proof of hardware acceleration. notes/browser-*.json logs the actual unmasked renderer. swangle is an explicitly labeled software fallback, not tested by the reference run.

## Source and output contract

- src/camera-path.mjs + camera-path.d.mts: pure frame-indexed camera and test constants.
- src/CoffeeShop.tsx: set, furniture, coffee props, standard materials, lighting/shadows, synchronous camera rig and optional DOM labels.
- src/index.tsx: registered 150-frame / 30fps / 960x540 composition.
- scripts/self-test.mjs: camera invariants, projection/parallax, no accumulated animation API.
- scripts/render-test.mjs: local bundle + first/middle/end/repeated stills, or full H.264 encode; refuses to overwrite proof/output files. Existing work bundles may be refreshed only inside the copied project. This is not a generic production renderer.
- scripts/verify-output.mjs: independent FFprobe/full decode, frame extraction, nonblack scene statistics, exact repeated raw-pixel hash, encoded model-guided color-region parallax and actual backend evidence. This verifier is deliberately fixture-specific; update dimensions/count/feature windows/assertions when adapting the scene. It does not certify arbitrary new videos unchanged.
- exports/coffee-shop-3d-silent-technical-test-v001.mp4: video-only (intentionally no audio).
- proof/encoded-first.png, encoded-middle.png, encoded-last.png, camera-parallax.json, verification-report.json.
- notes/browser-stills.json and browser-encode.json: exact browser path, requested backend and actual WebGL/shadow evidence.

For another run, copy to a fresh directory or deliberately version output/proof paths in your own project; do not delete prior user work. Final delivery: keep a discoverable top-level copy of the exact export filename and notes with SHA256, source and proof paths. Actual frame review and sample/style approval remain separate requirements. No Studio service is required for the encoded technical test.
