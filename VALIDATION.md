# Validation — starter 0.2.0

## 0.2.0 compatibility adaptation (2026-11-23)

- Agent-directed README and plan/apply native entrypoint adapter for Hermes/OpenClaw; no config/identity replacement or renderer rewrite.
- Adapter/bootstrap suite: 28 tests, 26 passed, 2 skipped (host symlink restrictions). All 13 real skills integrated into isolated runtime roots.
- Hermes v0.23.1 / commit 3b421578588243f920886e6fe79a6faa87ea026e: native CLI listed 13/13 enabled local entries in an isolated home. That CLI prepared dependencies within the isolated test home. Native skill_view(name, preprocess=False) then successfully loaded 13/13 wrappers; canonical files were read and hashed. No model call or active profile change.
- OpenClaw adapter/filesystem fixtures passed; a new registered OpenClaw agent/session was not created for native discovery.
- 30 renderer/template/helper/license files are byte-identical to the preserved 0.1.0 deliverable, including both npm locks and actual render source. See verification/compatibility-source-host.json for sanitized per-file evidence. No extra encode was needed for this adapter-only change; fresh destination encodes remain required.
- The renderer evidence below belongs to 0.1.0 on this source host, not an end-to-end Hermes agent session or a recipient rebuild. Re-run README gates at the destination.

## 0.1.0 renderer baseline (retained)

Verified 2026-11-23 on the source Windows 11 x64 host using fresh project-local npm installs from the EXPORTED kit. This is not a fresh-machine/OS rebuild, cross-platform certification, destination agent registration or user style approval.

## Passed here

- 13 packaged skill headers validated with the installed AgentSkills validator.
- 11 bootstrap failure/integrity tests: 10 passed; 1 host-restricted symlink-creation test skipped. Guards cover missing/changed/unlisted files, path traversal/absolute paths, lock origins/integrity/pins and empty manifests.
- Motion skill helper self-test: 9 checks passed, including guarded initialization, no-overwrite, resource links and deterministic synthetic audio.
- Local clipping: all 12 real-FFmpeg synthetic regression tests passed.
- Long-form cleanup: all 13 real-FFmpeg synthetic regression tests passed. These do not establish semantic editorial judgment or human listening.
- Fresh isolated npm ci --ignore-scripts and TypeScript checks passed for BOTH rendering templates; no shared node_modules junction or global install used.
- Matching Chromium ensureBrowser retrieval succeeded into a fresh project-local cache; Chrome for Testing 157.0.8080.0. The full corrected bootstrap reused that verified browser via --browser. The same helper's download API route was tested separately, not a second full --download-browser bootstrap run.
- **2D encode:** H.264 1280x720, 30fps, 120 frames/4.000s; AAC test-tone audio 4.011s; full decode passed; source/output PCM correlation 0.9999957, peak 0.155, RMS 0.0703. Reviewed actual encoded frames 0,60,108,119: readable type/chart/cards, purposeful build and expected final fade to the pale stage. No speech/music/TTS included.
- **3D encode:** H.264 960x540, 30fps, 150 frames/5.000s, silent by design; full decode passed. Repeated frame-75 raw pixels matched exactly; decoded feature-region parallax was 32.8273px. Actual backend evidence identifies ANGLE/Intel UHD/D3D11 hardware GL (not a video-encoder acceleration claim). Reviewed actual encoded frames 0,75,149: geometry, props, occlusion, cast shadows and changing perspective are visible, with no black renderer defect. The plinth extends past the lower frame edge by design; useful objects/labels remain visible.

## Fix made during validation

An early motion verifier incorrectly required high image variation on the final frame despite the template's documented fade-out. Inspection confirmed the intended ending. The fixture-specific test now checks content frames separately and explicitly verifies the final pale-stage fade; a complete fresh corrected bootstrap passed. No production source was altered to hide a test failure.

## Not verified / not provisioned

- No new destination agent/model-driven session was created. Isolated Hermes native listing/reader evidence is recorded above; destination runtime discovery still needs its own check.
- Optional Python media environment, real speech inference/model download, destination research corpus/index, local thumbnail image tooling and online account services were not newly provisioned/tested in this packaging task. Their exact gates are in CAPABILITIES.md.
- No continuous video playback/human listening, exhaustive privacy clearance, artist-fidelity approval, photorealism/complex rigs/physics benchmark, GPU portability or speed guarantee. swangle fallback and other operating systems remain untested.
- No account credential is exported. GitHub publication is separate from capability validation; local files/commits are not evidence of a pushed remote. Public redistribution/license choices for unlicensed local guidance still need the owner's review; see THIRD-PARTY-NOTICES.md.

## Runtime and reproduction

Source runtime: Python 3.12.7, Node 26.12.1, npm 11.20.0, FFmpeg/ffprobe 8.1.1; renderer package pins are in manifest.json. Destination instructions are README.md; START-HERE.md is the short handoff. Bootstrap reports and proof frames are destination-local under ignored .starter/runs/. Historical source report paths, personal machine paths, recordings, private source corpus and model weights are intentionally not bundled.
