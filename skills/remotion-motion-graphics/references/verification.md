# Local preview, rendering and evidence

Run from the project directory after reading its package.json. Exact scripts are in assets/template/package.json.

    npm.cmd run typecheck
    .\node_modules\.bin\remotion.cmd compositions src/index.ts --props=props.example.json
    .\node_modules\.bin\remotion.cmd browser ensure
    npm.cmd run studio

Use the template's version-guarded scripts/studio-local.cjs launcher (npm.cmd run studio). Raw Remotion Studio defaults to all interfaces and ignores an unsupported --host flag. The launcher forces the shared internal getPortConfig binding to 127.0.0.1 in-process only. Verify the actual listener is 127.0.0.1:3100 with Get-NetTCPConnection -LocalPort 3100 -State Listen on Windows. Never publish a portal/tunnel without permission. Inspect preview via an available browser tool after reading the browser-automation skill. A CLI compositions listing and typecheck are useful but do not prove playback was inspected. If browser navigation to loopback is policy-blocked, do not bypass it with a tunnel or alternate connection: inspect locally rendered sample/encoded frames using permitted tools and state that interactive playback was not verified. Objective audio checks do not constitute a human listening pass. Stop only the Studio process you started when finished.

## Sample then final

For a short composition:

    .\node_modules\.bin\remotion.cmd render src/index.ts MotionGraphic exports/sample-v001.mp4 --props=props.example.json --codec=h264 --audio-codec=aac --crf=18 --pixel-format=yuv420p --concurrency=2

For a range from a long composition, use --frames=<start>-<end> with actual frame bounds; record that the output is only a sample. Inspect and request style approval. Do not represent a sample as an approved final. After approval, render all intended frames to exports/final-v001.mp4. Never upload media to render.

## Verify the real encoded output

    node "<skill>/scripts/inspect-media.mjs" exports/sample-v001.mp4 > proof/sample-probe.json
    ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames,width,height,r_frame_rate,duration -of json exports/sample-v001.mp4
    ffmpeg -v error -i exports/sample-v001.mp4 -f null -
    ffmpeg -n -ss 0.5 -i exports/sample-v001.mp4 -frames:v 1 proof/start.png
    ffmpeg -n -ss 2 -i exports/sample-v001.mp4 -frames:v 1 proof/middle.png
    ffmpeg -n -ss 3.7 -i exports/sample-v001.mp4 -frames:v 1 proof/end.png
    ffmpeg -hide_banner -i exports/sample-v001.mp4 -af volumedetect -vn -f null -

Times above are only for a 4s test; choose actual start, midpoint, transition boundaries and last visible frame for each production. Use view_image on the extracted PNGs; source remotion stills alone do not verify encoding. Inspect gaps, clipping, contrast, line breaks, safe zones, duplicate/missing assets and end timing. Decode failure, absent expected audio, clipped/blank frames, wrong duration or unexplained silence are failures to fix, not footnotes.

Audio checks: probe AAC/audio channels/sample rate and duration; decode all streams; check nonzero energy and peaks; compare source/output timing and listen to speech sync where playback is available. If audio cannot be heard in the tool environment, say so explicitly: objective mux/decoding/energy checks are not a listening pass. Synthetic tones prove mux compatibility, not human intelligibility. Check original/copied MP4 AAC packets if preserving narration, with a local hash of extracted streams where practical.

## Skill release check

    python "<skill-creator-directory>/scripts/quick_validate.py" "<skill-directory>"
    node "<skill-directory>/scripts/self-test.mjs"
    npm.cmd run typecheck

Then render an actual 3–5s local MP4 using audio extracted from a synthetic local MP4 fixture, probe/decode it, inspect encoded PNGs, and record exact dependency/runtime versions. The template's generate-fixture.mjs writes its own deterministic WAV without network access; test code must never overwrite a user's recording. Record limitations honestly and do not say the user's unsupplied video is complete.
