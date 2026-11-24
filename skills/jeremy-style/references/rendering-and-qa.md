# Rendering, approval and failure gates

## Preflight

Read the local renderer's own skill and exact project manifests. Record operating system, package/lockfile versions, codec tools, local font availability, 3D dependency/license eligibility, hardware and output directory. Do not infer a verified 3D runtime from the presence of this skill. No new production was rendered during the reference-analysis task; all procedural geometry/light values are design starting points.

Keep reference source and extracted frames outside browser-served public assets. Use original, approved or independently licensed models/textures/fonts/music. Link to the source video for provenance; do not redistribute source screenshots, audio or video in the skill's public-facing example package.

## Minimum representative sample

Choose a brief-appropriate short range, typically 5–10 seconds, with: a clear full/three-quarter character view, a changed expression and meaningful hand gesture, a foreground/background occlusion or camera angle that tests genuine depth, a gold-label/pink-line information cue, and a transition to/from an explanatory board. A scene that contains only a sphere on a blank background does not validate the whole style.

Record sample approval separately from technical success. A sample may pass render/decode and still fail creative approval. Wait before a long full render unless the user explicitly waives that gate.

## Objective checks

- Run the chosen project's typecheck/build/lint as applicable; execute any helper that is newly authored or changed. Inspect scene source/manifests rather than calling a documentation template executable.
- Inspect composition metadata and verify frame count covers measured narration plus intended tail. Confirm fps, dimensions, sample rate and actual stream offsets.
- Encode a local deliverable such as H.264 MP4/AAC when compatible with the brief. Probe the encoded file, not just the source composition. Decode the whole encoded file and retain exit status/log.
- Confirm audio presence, duration and no double narration/restarted sequences. A tiny video/audio stream length difference can be codec framing; record it instead of arbitrarily trimming the master.
- Save a frame list and fresh encoded proof frames at first/last picture, every key beat, both sides of important cuts, changes in pose/focus/overlays and the final spoken word/end card.
- Test deterministic rendering by comparing repeated selected frames when procedural animation/shader randomness is used; do not claim determinism from source inspection alone.

## Visual/temporal review

Review motion in authorized local playback or sufficiently dense sequential frames; a contact sheet is a coverage overview, not continuous playback. Inspect quarter-frame/quarter-second boundaries according to the actual risk. Check:

1. Identity: fixed costume/identifier, proportions and expression vocabulary; no unapproved likeness redesign.
2. Acting: distinct poses support actual narration; eyes look at the relevant character/prop; no perpetual smile or identical waving silhouette.
3. Physical integrity: no hands through desks, sliding feet, dislocated wrists, orbiting props, mouth decals detached from the head, z-fighting or camera clips.
4. Camera: correct spatial geography and screen direction; stable near/far clipping; motivated view changes; no constant aimless orbit or aggressive wide-angle face distortion.
5. Lighting/materials: readable face in night shots; soft form cues and grounding shadows; no blown-out emissive heads, mirror-like skin, floating feet or crushed foreground.
6. Typography: licensed font, correct spelling, safe margins, legible gold/cream contrast and enough hold time at delivery size. Keep labels sharp outside camera DOF.
7. Overlays: semantic lines/counters track their intended subjects and do not imply unsupported quantities; no decorative random heart metrics.
8. Continuity: no accidental costume changes, props swapping hands, inconsistent light direction, unmotivated scene cuts or line paths that change meaning.
9. Narrative: diagrams answer the nearby spoken question; an emotional reaction gets a real hold; full narration and last words are preserved.
10. Delivery/privacy: style name stays in notes, private source media stays private, no credentials/UI exposure, editable project and final file remain findable.

For audio, use available actual listening for intelligibility, distracting music, clipping, joining and sync. Signal measurements can support but cannot replace listening. If unavailable, disclose measured/ASR-only review and avoid a verified-audio claim.

## Common failures and repairs

- Flat circles called 3D → use actual geometry/camera/light for spatial turns, or rename the treatment 2.5D and get approval.
- Hyper-real texture/noisy faces → simplify surfaces and preserve graphic expressions.
- Purple wash everywhere → restore neutral pale heads, local set colors, warm type and a readable key light.
- Endless bobbing or smiling → replace with narration-specific expression/pose keys and real holds.
- UI buried in blur/glow → screen-space text, lower bloom, increased contrast and larger copy.
- Full transcript filling the frame → keep only explanatory labels; supply a separate accurate caption layer when requested.
- Every cut uses glitch → reserve distortion for a specific information/emotional change and use clean cuts otherwise.
- Thousands of unique crowd rigs → instance geometry/use distance-appropriate cutouts; verify wide-shot memory/time on a sample.
- Single shot proves all readiness → add a perspective exchange, depth cue, overlay tracking and board transition to the sample.
- Copied source statistics/story → use original scenario and separately verified factual inputs; source style is not a research citation for claims.
- Written specification called a finished video → report only the files/tests actually created; do not claim encoded output or user approval.
