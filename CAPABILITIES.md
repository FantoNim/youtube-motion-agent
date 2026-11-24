# Capability/readiness contract

| Capability | Shipped | Destination readiness gate |
| --- | --- | --- |
| Motion graphics | Complete local source/lock/helper/skill | Fresh setup render + encoded/audio checks + image review |
| Real 3D | ThreeCanvas procedural scene/lock/helper/skill | Fresh stills + MP4 + decode + repeated pixel hash + encoded parallax + backend evidence + image review |
| Scripting/titles/description | Agent workflow, versioned artifacts | Actual agent can read/discover skills and write/review a synthetic draft |
| Thumbnail design | Local-first procedure | Actual local image tool + lawful assets + fresh full/small export review |
| Cleanup/highlights | Tested executor source and editorial procedures | Run bundled unit tests; fresh synthetic media round trip; meaning checked separately |
| Lesson companions | ASR/visual-evidence procedures/helpers | Local media environment + model + non-sensitive speech/screen test |
| Research | SQLite FTS/PDF code and tests | Local environment + supplied corpus + rebuilt fresh index/queries |
| Style library | Complete Jeremy/Gloam skill references; generic other looks | Fresh representative aesthetic sample + user approval |
| Online YouTube/account actions | No login or account connector | Separately configured authorized tools/OAuth and task approval |
| Image generation/TTS/live search | No service provisioned | Available authorized provider, separate cost/privacy consent |
| Native Filmcraft editing | Not installed | Separate supported Filmcraft runtime/MCP round-trip setup |

## Runtime baseline

Source observed Windows 11 x64; Python 3.12.7; Node 26.12.1/npm 11.20.0; FFmpeg/ffprobe 8.1.1. Other platforms/GPUs are not certified by a Windows test. Use appropriate native binaries; record deviations and rerun tests. Linux Chromium may need system libraries. No privileged package manager or execution-policy change is embedded.

Pinned packages: Remotion family 4.0.538; React/react-dom 19.2.0; TypeScript 5.9.3; R3F 9.2.0; Three/types 0.180.0; Zod override 4.6.6. Preserve full lockfiles. The intentional Zod mismatch warning is documented in the renderer skills; do not run blind audit fix.

## Offline speech recognition

Optional package pins live in requirements-media-observed.txt. They are observed, not a transitive cross-platform lock. Bootstrap --media installs/import-checks packages only. Model downloads need explicit consent; do not call online model names at inference time and let them download silently.

- Systran/faster-whisper-base.en revision 3d3d5dee26484f91867d81cb899cfcf72b96be6c
- Systran/faster-whisper-small.en revision d1d751a5f8271d482d14ca55d9e2deeebbae577f

With permission, retrieve the exact revision using the installed Hugging Face client's snapshot_download into a destination-local model directory. Preserve upstream model licenses and transfer complete resolved files rather than broken cache links. Instantiate faster_whisper.WhisperModel with the explicit existing local path and local_files_only=True, e.g. CPU/int8 where supported. Save timestamped output as an ASR draft, check uncertain names/meaning/sync points, and verify a non-sensitive speech fixture before readiness. No cloud fallback or guaranteed phoneme timing.

## What bootstrap does NOT certify

Agent registration/skill discovery; personal style/likeness; copyright/privacy clearance; Remotion business license eligibility; human listening/playback; YouTube authentication; source-data access; complex rigs/simulation; production speed; bit-identical results across GPUs. The bootstrap report labels machine checks separately. The setup agent must review fresh encoded frames and save its own review before claiming visually verified.
