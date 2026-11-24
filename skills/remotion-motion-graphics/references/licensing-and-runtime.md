# Runtime, privacy and licenses

## Licensing gate (checked 2026-10-25; recheck for new use/version)

The upstream skill is MIT. Remotion 4.0.538 is separately "SEE LICENSE IN LICENSE.md"; its installed package LICENSE.md is authoritative for that pinned version. https://www.remotion.dev/license redirects to https://github.com/remotion-dev/remotion/blob/main/LICENSE.md . The current text permits free use by individuals, for-profit organizations with up to 3 employees, nonprofits/not-for-profits, and noncommercial evaluation. Other entities need a Company License. Current main also warns the license will change in Remotion 5. Do not promise "always free", assume the skill's MIT covers Remotion, or purchase anything without approval. Local evaluation smoke testing is within the stated evaluation category. If commercial eligibility is genuinely unclear, ask one concise licensing question before commercial production. React/typescript/other dependencies and FFmpeg/Chromium have separate licenses.

## Preflight

PowerShell (read-only):

    Get-Command node,npm.cmd,npx.cmd,git,ffmpeg,ffprobe -ErrorAction SilentlyContinue
    node --version
    npm.cmd --version
    Get-PSDrive C | Select-Object Used,Free

Template tested with Node 26.12.1 on Windows 11 x64; this is evidence, not a claim every Remotion release supports every Node version. Pin the tested versions (all Remotion packages identical). Keep package-lock.json. Review package.json scripts before running; inspect dependency lifecycle scripts and install with --ignore-scripts. Use npm.cmd ci --ignore-scripts --no-fund --no-audit with a reviewed lock, or install --ignore-scripts for first lock creation. Review audit results separately; never run audit fix blindly. The template pins a zod 4.6.6 override: Remotion 4.0.538 transitively pins vulnerable 4.5.4 (GHSA-mrhx-c7xc-m3w5, constrained-collection memory exhaustion). The same-major patched override was metadata-reviewed, installed with lifecycle scripts disabled, audited, typechecked and rendered. Reassess the override when updating Remotion. The CLI emits an expected Zod version-mismatch warning because upstream requires 4.5.4; do not blindly follow its recommendation to downgrade to the vulnerable release. The template typecheck/render and Studio build pass with 4.6.6; wider Zod schema/editor compatibility is not guaranteed. No global installation, npx @latest scaffold or upstream installer is required.

The Remotion CLI uses a local Chromium headless shell; after dependency review run .\node_modules\.bin\remotion.cmd browser ensure. The first download is external software retrieval, not media upload. Chromium/FFmpeg/native dependencies consume disk; allow several GB for caches/frames and more for long high-resolution exports. Do not delete unrelated caches to make room. Prefer the installed local binary over npx auto-install behavior.

FFmpeg/ffprobe on PATH are preferred. If absent, inspect the matching installed @remotion/compositor-* package for bundled ffmpeg/ffprobe executables and license; pass an explicit path to inspect-media.mjs. Do not invent a binary location. If ffprobe is unavailable, install a reviewed local tool or use an already-installed supported metadata parser; label the inspection blocked rather than guessing duration. Remotion still renders can verify source frames but do not replace encoded-audio/duration checks.

## Local-only boundary

Use staticFile paths to public/ assets, local fonts, loopback Studio and local render commands. IMPORTANT: pinned Remotion Studio defaults to 0.0.0.0/::; --host is not a supported binding flag. The template scripts/studio-local.cjs overrides the pinned renderer shared getPortConfig provider in this Node process only to force 127.0.0.1, with a version guard. It does not edit installed code or system configuration. Use npm.cmd run studio, not the raw Studio CLI, for loopback-only preview. Verify the actual listener address; re-review the wrapper before changing Remotion versions. Do not add remote Img/Audio/video URLs, Google font fetches, analytics, cloud render APIs, dLazy, credentials, upload scripts or public tunnels. Package registry/Chromium downloads are needed once; this is not a claim the machine makes zero internet requests. An offline re-render after downloads can be used for stronger operational assurance. CLI licensing/telemetry behavior can change: inspect the pinned CLI and current docs rather than claiming undisclosed telemetry is disabled. Never invent environment variables to disable it.

## Common Windows recovery

- npm.ps1 execution-policy error: use npm.cmd / npx.cmd; do not change policy.
- PowerShell 5 strict ErrorActionPreference=Stop plus native 2>&1 log capture can treat the known CLI Zod warning as a terminating NativeCommandError. For that capture only, use Continue and explicitly check LASTEXITCODE after each native command, or use a reviewed cmd.exe redirection. Do not interpret a stderr warning as an encode failure or ignore a nonzero exit code.
- ffmpeg/ffprobe path has spaces: call with PowerShell & and quote it; helper's optional second argument is an explicit ffprobe executable.
- Node failure: inspect installed package engines and retry with a supported existing Node if available; never change the Gateway's portable Node installation.
- Browser download failure: use an already-installed compatible browser via --browser-executable="C:/.../chrome.exe" only after inspecting its path/version, or report a concrete download blocker.
- Native dependency missing after --ignore-scripts: review that package's lifecycle script before a narrowly scoped rebuild; do not enable all scripts globally.
