# Portrait preview rendering

1. Derive the preview scale from the measured composition dimensions, because a rounded decimal can leave fractional encoder dimensions after bundling. For a 1080×1920 composition targeting 720×1280, calculate the value and validate both dimensions before rendering:

       node -e "const s=2/3;const d=[1080*s,1920*s];if(d.some(x=>!Number.isInteger(x)||x%2))process.exit(1);console.log(s,d)"

   Require the output scale 0.6666666666666666 and dimensions [720,1280] for that example, because the encoder requires integer dimensions and yuv420p requires even dimensions. Substitute the actual measured dimensions for other compositions. Pass the calculated value unchanged to --scale.

2. Render a continuous source-clock interval with inclusive frame bounds, because the sample must retain narration synchronization. Calculate count=endFrame-startFrame+1, startSeconds=startFrame/fps and durationSeconds=count/fps; record all four values in notes before invoking the renderer. Keep the native composition size and rate unchanged, because preview scaling is not a production timeline change.

3. Use the installed renderer’s supported PNG-to-BT709 path when available, because this produces a directly masterable SDR picture without a needless second video encode:

       remotion render src/index.ts COMPOSITION exports/sample-picture-v001.mp4 --frames=START-END --scale=SCALE --bundle-cache=false --codec=h264 --crf=18 --pixel-format=yuv420p --color-space=bt709 --image-format=png --concurrency=1

   Set TEMP and TMP to the active project’s existing .tmp directory on Windows, because temporary render ownership must remain separate from a shared dependency runtime. Retain the reviewed package versions and inspect supported flags before using the command.

4. Probe the actual picture before muxing with ffprobe -v error -show_streams -of json exports/sample-picture-v001.mp4, because requested flags alone do not establish encoded color or geometry. Require the calculated integer dimensions, source fps, expected frame count, yuv420p, tv range and bt709 matrix/transfer/primaries for this SDR workflow. Extract encoded RGB proof frames and inspect the palette, because metadata checks do not establish visual color fidelity. Use the parent skill’s measured-input conversion procedure only when the actual picture needs conversion.

5. Extract an accurately bounded voice excerpt and mux it once, because a picture-only sample cannot approve narrated motion:

       ffmpeg -v error -n -ss START_SECONDS -i public/narration.m4a -t DURATION_SECONDS -map 0:a:0 -c:a aac -b:a 192k exports/sample-narration-v001.m4a
       ffmpeg -v error -n -i exports/sample-picture-v001.mp4 -i exports/sample-narration-v001.m4a -map 0:v:0 -map 1:a:0 -c copy -map_metadata -1 -movflags +faststart exports/style-sample-v001.mp4

   Label this audio as an excerpt encoded for accurate bounds, because it is not a claim of compressed-track identity. Check start/middle/end waveform lag against the corresponding source interval before delivery.

6. Remove preview scaling and range flags for the approved full-resolution render, because a preview must not silently become the production deliverable. Mux the entire original AAC master without -shortest or a duration cap; verify complete original/extracted/final packet hashes and decoded PCM identity where available. Investigate a small audio container-duration discrepancy against those full-track identities before treating it as lost speech.
