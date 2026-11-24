# Motion, camera, editing and transitions

Evidence IDs refer to [source analysis](source-analysis.md). Exact timings below are adaptation starting points. No source animation curves were recovered.

## What was actually observed

- G01: staging changes from figure/receipt to shoulder/monitor/receipt; focal scale matters more than all objects moving at once.
- G02: timed reduction/count changes in a dimensional scene, then a new view through a vault portal; not a perpetual object carousel.
- G06: recurring vault groups have short viewpoint/editorial changes, connector/status changes, reflection and held compositions. The 197.5→197.75s pair is a view change, not proof of a smooth camera move.
- G07: directionally drawn connector builds over roughly a second, followed by a multi-second hold; the destination becomes red. Around 244s a blurred/warped overlap replaces the board with the room.
- G08: a card holds, a final row is added, a stamp lands, then a short field reset and statement reveal. It does not reveal a new unrelated card every beat.
- G12: large number contrast uses short blurred replacements and stable holds; final text appears before the smaller CTA. The ending is visibly held through the last sampled second.

## Proposed deterministic motion rules

For 30fps start here and revise against actual speech:
- Main text/card entrance 12–20 frames; secondary item 4–8 frames later; emphasis stroke 10–18 frames; annotation/stamp 6–10 frames; simple exit 6–12 frames. These are craft defaults, not exact source durations.
- Use clamped eased translation/opacity for paper; a restrained overshoot only if the card's physical action warrants it. Use ease-in-out for deliberate camera travel; no mandatory elastic wobble. Linear time/data progression is appropriate when truthful.
- New fact arrives → stop motion → viewer reads → next operation. Hold important strings at least long enough for their wording and complexity, usually 1.5–3s for a short line and longer for a real quote; validate by reading at target size, not a universal seconds-per-word formula.
- A connector has direction, endpoint and semantic state. Draw the stroke, move one marker if useful, change the receiver, then hold. Do not keep looping pulses once the point is understood.
- Do not scramble/count through invented intermediate data. If an intermediate count is merely illustrative, label it; the final exact value remains accurate.
- If several cards coexist, reveal only the relevant part or active state. Do not animate all panels continuously.

## Camera specification

Choose one shot purpose: establish scale, reveal a hidden relation, follow transfer, or revisit changed state. Specify camera start/end position, target, projection, lens/FOV, duration and occlusion intent in project notes. A zoomed still is not a dolly through a modeled scene.

For a proposed geometry scene, use moderate perspective (roughly 35–50° vertical FOV as a starting point), a small deliberate dolly/lateral movement, stable up vector and a meaningful foreground element. Verify near/far clipping. One clear move is preferable to a long flying tour; stop at the important state for reading. Text may stay as a crisp 2D overlay unless its placement in space is itself the point.

Reference-like dramatic cuts may be better than travel: an establishing room → detail → graphic explanation is valid. Do not invent a source orbit because a single frame has perspective.

## Transition grammar and its cause

- **Hard cut / direct replacement:** new chapter, archive proof, different time or viewpoint. This is often cleaner than a decorative wipe.
- **Brief pale/dark field reset:** reduce complexity before an explanatory board (G06). Proposed 6–12 frames, but never flash white repeatedly.
- **Paper overlap/tilt with short blur:** a new document enters or a claim is revised (G03/G08/G10). Blur must finish before text becomes essential.
- **State continuation:** retain the same card/room and change only the line, stamp, stack or status that matters (G02/G07/G08).
- **Callback cut:** revisit an established metaphor in a changed state or contrast fee versus response time (G11/G12).
- **Optional reduction:** if motion sensitivity/readability requires it, remove smear/warp and use a clean crossfade/cut. The style survives without copying every transition artifact.

Avoid default glitch noise, scanlines, chromatic aberration, aggressive shake, bass-zoom assumptions, unrelated particles and constant lens flares. None is a substitute for the observed paper/data/spatial grammar. Do not prescribe sound hits from silent frame evidence.

## Editorial pacing

Alternate evidence, explanation and implication by meaning. A new scene is justified by a changed idea, not every fixed N seconds. Let real demonstrations/quotes breathe; let a headline make one point. Use more visual density only when the narration explains that density. Maintain a continuity map: initial object/state, mechanism, consequence, final status. End with the conclusion before the CTA; don't truncate narration to fit a preset outro.

## Temporal QA

Inspect frames on both sides of each cut and a short dense sequence around annotations, connector endpoints, camera occlusion and the ending. Look for half-visible text, objects popping between cuts, double exposure obscuring words, red state arriving too early, and a final hold shorter than the narration. Contact sheets alone cannot establish fluent playback, precise easing or audio sync; record whether actual playback/listening was available.
