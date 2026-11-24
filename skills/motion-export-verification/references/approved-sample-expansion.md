# Expand an approved sample into a full film

1. Record explicit sample approval and hash the delivered sample, silent picture and editable source before extending the film, because approval should lock the demonstrated look rather than trigger a redesign. Save the lock manifest under project notes, write extensions into a new versioned source directory, and check protected hashes again before delivery.

2. Keep the complete original narration as the final timing master, because concatenating narrated sample exports can duplicate or restart speech. Reuse only the approved sample's silent picture. Extract compatible original AAC with ffmpeg -n -i SOURCE -map 0:a:0 -vn -c:a copy narration.m4a, substituting the inspected audio track when multiple tracks exist.

3. Partition the full picture into integer frame ranges before rendering, because an approved excerpt can begin between frame boundaries. Compute N = ceil(audio_seconds * fps), P = round(source_sample_start * fps), and M = the approved picture's measured decoded frame count. Assign prefix [0, P-1], approved core [P, P+M-1], and suffix [P+M, N-1]; require nonnegative lengths and an exact gapless partition of N frames. Derive the suffix from P+M rather than independently rounding its start. Record P/fps - source_sample_start and the final picture-only rounding tail without shifting or stretching audio.

4. Render only new prefix and suffix when the approved silent segment is compatible, because reusing the encoded core avoids unnecessary rendering and approval drift. Match dimensions, rational fps, encoder profile/level, pixel format, color signaling and time base. Compare each segment using:

    ffprobe -v error -select_streams v:0 -show_data -show_entries stream=codec_name,profile,level,width,height,pix_fmt,r_frame_rate,avg_frame_rate,time_base,color_range,color_space,color_transfer,color_primaries,extradata -of json SEGMENT

Compare codec extradata as well as visible dimensions, because matching resolution alone does not establish safe stream-copy concatenation. Preserve set geography and compatible action states at both joins.

5. Copy-concatenate compatible silent segments from a local concat-demuxer list, because this preserves the approved encoded picture without re-encoding. Put one file entry per segment in timeline order and use:

    ffmpeg -n -f concat -safe 0 -i segments.txt -map 0:v:0 -c:v copy -an full-picture.mp4
    ffmpeg -v error -i full-picture.mp4 -f null -
    ffprobe -v error -select_streams v:0 -show_packets -show_entries packet=pts,dts,duration,pts_time,dts_time -of json full-picture.mp4

Decode each input too, because a valid container does not prove a compatible decoded segment. Require the planned count, unique uniformly spaced presentation timestamps after sorting, increasing decode timestamps and expected packet durations at joins. Allow packet-order PTS reordering for B-frames instead of treating it as discontinuity. If signatures or decoding fail, render a new full picture from locked scene functions and verify the approved region rather than forcing unsafe concatenation.

6. Compare every approved core frame's decoded RGB hash against the assembled region, because source-code similarity or a few stills cannot prove motion preservation. Generate reference and core frame hashes with:

    ffmpeg -v error -i approved-picture.mp4 -map 0:v:0 -vf format=rgb24 -f framemd5 approved.framemd5
    ffmpeg -v error -i full-picture.mp4 -map 0:v:0 -vf "trim=start_frame=<P>:end_frame=<P_PLUS_M>,format=rgb24,setpts=PTS-STARTPTS" -f framemd5 core.framemd5

Replace both placeholders with computed integers before execution. Compare the ordered per-frame hash column and require exactly M matching rows; ignore comment headers and container timestamp text. Describe a rerender as visually matched rather than bit-exact unless decoded hash identity actually passes.

7. Extract first/last frames, both sides of every cut and concat seam, and dense intervals around new acting, because assembly checks do not establish physical continuity or readable expressions. Batch large select filters into at most 40 frame terms per FFmpeg invocation, because bounded expression depth keeps proof extraction reliable. Pass filters through argument arrays with exactly one backslash before each comma; for example, use the filter value select=eq(n\,0)+eq(n\,6)+eq(n\,12), with -fps_mode vfr and an output image pattern. Map output ordinals back to requested frame numbers. Repair proof-only extraction failures in a fresh proof directory without rerendering an already verified picture. Open temporal sheets and decisive full-size frames with view_image, check phone-size readability where relevant, and label dense-frame review separately from continuous playback.

8. Mux one continuous original audio track after picture assembly, because picture segment boundaries must not become audio edits:

    ffmpeg -n -i full-picture.mp4 -i narration.m4a -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -movflags +faststart FINAL.mp4

Omit -shortest and duration limits. Apply the main skill's full AAC packet and decoded PCM identity checks, inspect the actual final boundaries, and preserve inherited source levels rather than silently normalizing them. Confirm final picture elementary-stream identity when relying on the already reviewed picture evidence, because mux verification must establish that tested images are delivered images.

9. Deliver the complete verified MP4 through the current surface's native media attachment and retain exact filenames, source, timing map, manifests and proof under the workspace project, because a saved path is not a playable delivery. Continue the existing task after sample approval without requesting the same approval again. State sampled visual and objective audio-check limits without claiming a human listening pass, and report local saving separately from Git commit or remote synchronization.
