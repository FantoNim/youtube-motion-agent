# Pinned local runtime and licensing

## Inspected compatibility

The reference test pins Remotion, @remotion/cli, @remotion/renderer, @remotion/bundler and @remotion/three at **4.0.538**; React/react-dom **19.2.0**; @react-three/fiber **9.2.0**; Three.js and @types/three **0.180.0**; TypeScript **5.9.3**; React types **19.2.2**. All top-level versions are exact; retain the full reviewed lockfile. R3F 9.2.0 peers React ^19 and Three >=0.156; @remotion/three 4.0.538 peers matching remotion, R3F >=8 and Three >=0.137. Three 0.180.0 was already in the npm cache; missing R3F/Remotion-Three packages were installed only in the dedicated test project. No shared node_modules junction was used.

The inherited narrow Zod 4.6.6 override avoids upstream 4.5.4's known constrained-collection DoS advisory. Re-audit for every dependency update; never blindly run npm audit fix. A Zod mismatch warning does not itself prove render failure. Lock review must reject unexpected origins/missing integrity and inspect lifecycle inventory; --ignore-scripts is required. This is a tested combination, not every feature's compatibility guarantee.

Test machine: Windows 11 x64, Node 26.12.1, npm 11.20.0, FFmpeg/ffprobe 8.1.1. The test reads existing compatible Chromium Headless Shell from the separate remotion-local project without changing it. For another workspace, set REMOTION_BROWSER_EXECUTABLE to an inspected compatible local browser. No silent automatic download in the renderer helper. Package registry downloads are external software retrieval, not media upload; rendering is local, not a network-traffic audit.

## License boundary

Read installed remotion/LICENSE.md for this exact version (snapshot in the test notes). It is NOT MIT. Remotion 4 permits eligible individuals, for-profit organizations up to three employees, nonprofits, and noncommercial evaluation; larger/different businesses may require a Company License. Current personal-use authorization/evaluation does not establish eligibility for every future commercial/client project. Recheck for business use and new versions; do not purchase a license without permission. Three/R3F/React, FFmpeg, Chromium, fonts and assets have separate licenses.

Original template scene/helpers here are local procedural work. The official starter's API/structure was reviewed rather than cloned or executed. Its minimal Composition + ThreeCanvas pattern is MIT (copyright 2021 Jonny Burger); Remotion remains separately licensed. No upstream installer, bundled phone/tablet media, phone geometry, video-texture hook, Rspack config or remote font was copied into the project.

## GL and local servers

Official Remotion 4 docs recommend angle for desktop Three.js; defaults can fail black. Use chromiumOptions: {gl: 'angle'} on selectComposition/renderStill/renderMedia. If unsupported, swangle is an explicit software fallback. Capture actual WebGL unmasked renderer and browser version to distinguish acceleration; requested backend/powerPreference alone is not evidence of GPU use.

The helper has a version-guarded in-process RenderInternals.getPortConfig override to bind render servers to 127.0.0.1. This is a pinned internal API, not a public stability promise. Re-review on upgrade. It edits no installed code, Gateway config or system settings. No Studio/public portal is required for encoded proof. Do not use unsupported --host flags or tunnels to bypass local browser policy.

## Official sources reviewed 2026-11-22

- https://www.remotion.dev/docs/three
- https://www.remotion.dev/docs/three-canvas
- https://www.remotion.dev/docs/gl-options
- https://www.remotion.dev/license and installed 4.0.538 LICENSE.md
- https://github.com/remotion-dev/template-three/tree/691540390727b7d07daf4099c592464659a1ca64 (manifest, src/Scene.tsx, src/Root.tsx, remotion.config.ts, LICENSE.md)
- https://github.com/remotion-dev/remotion/blob/v4.0.538/packages/three/src/ThreeCanvas.tsx

Official template currently uses Three 0.178.0 and R3F 9.2.0. We selected cached compatible Three 0.180.0 + matching types, retained existing React/Remotion versions and tested rather than importing its floating ^4.0.0 dependencies or React version wholesale. No use of newer ThreeWebGPUCanvas is claimed for this pinned project.
