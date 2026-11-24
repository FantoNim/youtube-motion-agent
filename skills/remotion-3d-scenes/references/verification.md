# Readiness: encoded-render-verified

Verified 2026-11-22 on this Windows machine. This is execution evidence, NOT reference-style fidelity, user sample approval or commercial licensing clearance.

## Canonical evidence

Workspace-relative test project: Videos/_tests/remotion-3d-scenes/

- Discoverable export: coffee-shop-3d-silent-technical-test-v001.mp4 (top level); working encode under exports/ with the same filename.
- proof/verification-report.json and proof/ffprobe.json: actual full MP4 evidence.
- proof/encoded-first.png, encoded-middle.png, encoded-last.png: decoded frames 0 / 75 / 149, visually reviewed.
- proof/source-middle.png and source-middle-repeat.png: fresh Chromium renders of frame 75, interposed after frame 149; raw RGB SHA256 matches exactly.
- proof/camera-parallax.json: independent Three.js projection calculation.
- notes/browser-encode.json and browser-stills.json: actual WebGL/shadow renderer evidence.
- notes/production-notes.md: complete commands, manifests, licensing, scope, limitations and hash.

## Observed results

- H.264 960x540, yuv420p, BT.709, 30fps, exactly 150 decoded frames / 5.000s, no audio stream intentionally. Full FFmpeg decode passes. 639,982 bytes; SHA256 8b2a7c73bad0c96dd72986e44693fc6eff0dab8c48d6ddbcd105346006ba7b83.
- Requested GL angle. Actual WebGL 2: ANGLE (Intel, Intel(R) UHD Graphics (0x00004688) Direct3D11 vs_5_0 ps_5_0, D3D11), vendor Google Inc. (Intel). Hardware-accelerated Intel/D3D11 renderer observed, not SwiftShader/software. This identifies the GL renderer, not hardware video encoding or a performance benchmark.
- Existing Chromium Google Chrome for Testing 157.0.8080.0; no browser download/change. Shadow map enabled, type 2 = PCFSoftShadowMap; cast shadows visibly present beneath chairs/tables, behind plants/machine and on the back wall/floor.
- First/middle/end scene-region RGB means approximately 171, standard deviation 50.8–52.4, black fraction <0.33%. Actual geometry is visible, not just a colored background.
- Camera-only scene geometry is static. First/last encoded mean absolute RGB difference 17.83/255, foreground cup/back menu horizontal separation changes 32.83px by model-guided color-region centroids; pure projection predicts 27.95px. This measurement is decoded-image evidence, not optical flow or a claim of exact feature identity beyond the fixture's known color regions. Visual review confirms changing room angle and foreground/background displacement.
- Repeated frame-75 raw RGB SHA256 a30217f215ada590b9314f42ce21824bd7e14bde967a791044725205c38dad93, exact match in fresh browser renders. This is same-machine/same-backend frame determinism, not cross-GPU bit-identical output or whole-MP4 bit determinism.
- TypeScript noEmit and camera/helper tests pass. npm audit reports 0 advisories at this date. Registry-only lock with integrity; npm ci ignored lifecycle scripts. No shared runtime/junction mutation.

## Review and limitations

Visually reviewed source stills AND actual encoded frames 0,75,149. Coffee props/furniture/material differences, depth/occlusion, perspective change and cast shadows are readable; no black/missing set. The plinth deliberately extends past the lower frame edge at some angles. All useful furniture and test labels remain visible; production framing may be redesigned. No interactive playback or human audio listening is claimed; the fixture has no audio.

Tested: procedural static room/props, single frame-driven camera, standard materials, basic lights, shadow map, DOM labels and local H.264 encode. Untested: WebGPU, imported glTF/Draco, physics, skeletal characters, motion blur, large high-poly sets, async/video textures, long renders, other GPUs/OS, swangle fallback, arbitrary input props or narration workflows. Use the separate Remotion skill's audio/editorial checks for real media.

Run skill-creator quick_validate.py for this skill, node --check on its template helpers, and the template/project self-test; source/helper copies must hash-match. Do not promote a future modified source to encoded-render-verified until a fresh encode and decoded-frame review pass.
