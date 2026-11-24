# Production specification and review

Modified editorial adaptation; see [SOURCES.md](../SOURCES.md). Numerical choices below must be set per project; none is a guarantee of good editing.

## Turn adjectives into reproducible choices

Use [the spec template](../assets/spec-template.md) and record:

- Output dimensions, aspect, rational frame rate, color assumptions, measured source duration and actual timing master.
- Palette roles: reading foundation, text, a restrained accent, and what deserves that accent. Keep a reference's intentional dark stage instead of applying an unrelated house style.
- Typeface/source/license, actual type sizes/weights/line lengths, text/background contrast and safe margins. Do not shrink an unreadable paragraph to fit.
- Scene layouts, face/hand/screen protected areas, hero/focal point and source-crop rules. Preserve geometry unless reframing is authorized.
- Animation purpose, named easing or deterministic curve, durations and stagger in frames, entrance/hold/exit, and how the eye passes between shots. Keep important text still while it is read.
- Audio policy. Preserve supplied voice; do not add music, replace speech or synthesize missing words by default.
- Shot timing in program seconds/frames, original source ranges when applicable, approved assets and review checkpoints.
- Per-project pitfalls: excessive jump cuts, busy motion, tiny screenshots, generic card repetition or lost explanation. Do not ban every visual style globally.

## Distinguish technical and editorial QA

A valid file is not a good edit. Metadata checks answer whether streams, geometry, rate, color and duration are plausible; full decoding finds corruption. Sampled images reveal some composition problems. Neither establishes a human listening pass, every motion frame, perfect sync or factual correctness.

1. Check the source/cleaned master identity, stream mapping and edit map. Every graphic after cleanup uses the cleaned program clock; a deleted five-second take changes later timing.
2. Inspect a beat sheet covering the actual sequence. At each beat, describe the intended picture and its job in one sentence. Confirm it shows the thing it names without an extra explanation.
3. Inspect transition/join frames immediately before and after edits; examine a short range around the major move and important spoken boundaries. A middle-of-shot still can hide a bad cut.
4. Review at intended delivery size. For phone viewing, also inspect a 360-pixel-wide proof, while retaining full-size checks for desktop lessons. Account for player overlays and actual text reading windows.
5. Check the whole logical sequence against the transcript/context. Keep definitions, demonstrations, caveats, questions and answers that depend on each other. Distinguish removable retakes from intentional repetition.
6. Review audio by authorized playback when available, especially cut words, breaths, harsh joins, channel changes, clicks and A/V correspondence. If unavailable, retain the limitation and avoid claiming listened approval from waveform/level checks.
7. Write each defect as time + location + problem + exact proposed change + what must stay. Fix P0 meaning/readability/privacy/technical failures before P1 pacing/continuity and P2 polish. Recheck fresh affected outputs.
8. Save the weakest remaining shot, deliberate warnings and untested items. A style sample only approves its demonstrated look, not every final join or content choice.

Use [the review template](../assets/review-template.md). Require a final encoded-file check in the renderer/cleanup workflow rather than treating an editor command's success as sufficient.
