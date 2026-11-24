# Motion, editing, transitions and voice-first timing

## Source-supported motion grammar

- Early hook: a face closeup changes to a view from behind the head between requested 1.25 and 1.5s; the next frames retain gym geography. This is a view/cut observation, not proof of a continuous camera orbit (E01).
- Reveal/title: 64–65.75s keeps a front-facing protagonist with a pink light path, arm movement and changing framing; around 66s a title becomes visible as the figure/frame treatment changes (E03). A gradual opacity/crossfade-like treatment is supported; the exact ease and duration are not.
- Acting within a held composition: 145–147.75s keeps two people at the same bench while the green character's raised hand lowers toward the tabletop and a small monetary label appears (E04). This demonstrates a purposeful gesture beat rather than a cut for every spoken word.
- Spatial edit: the corridor encounter remains in a near view through 437.5s, then changes to a high wider view by 437.75s, making many relationship lines visible (E10).
- Motif tail: 624–626.75s follows a pink line and bright endpoint across a star-dark field; some frames change more than others (E12). Sampling supports line movement, not its exact continuous velocity.
- Localized wavy/distorted frames occur near 58.425, 122.162 and 280s (E02/E05/E07). Treat them as brief stylized disruption, not a global VHS/noise overlay.

## Editorial grammar

Make a concrete social situation the home stage. Alternate action and reaction, then insert a compact diagram when the narration needs explanation, comparison or scale. Return to the same cast/location so the explanatory detour has a visible consequence. Use scale changes for escalation: individual → classmates → crowd/venue. Use quiet/private scenes for consequences; dense crowd/stage shots should not be the default background for every sentence.

Do not set a mandatory cut every N seconds. Scene duration follows the spoken idea, the action's completion and reading time. Retain establishing geography before reverse angles. Preserve eyelines, character identifiers and hand/prop continuity across cuts. A closeup should answer whose feeling matters now. An explanatory label should appear when it becomes relevant, not solely because the frame is empty.

## Recording-first timing procedure

1. Probe the supplied recording and select the actual audio track. Record start offset, duration and meaningful intentional silence. Preserve all audio unless editing is requested.
2. Use an optional supplied script as a checking aid, not as a replacement clock. If no script exists, use verified existing local ASR or available listening, then mark uncertain words/times. A segment timestamp is not word-accurate alignment.
3. Divide speech into thought units: setup, action, revelation, explanation, consequence, resolution. For each unit write the viewer's question and the picture that answers it.
4. Put action cues beside the relevant phrase. Let the audience register a pose or relationship before adding another label. Hold a meaningful face after the line when an emotional consequence needs processing. Do not stretch the recording to fit a preset scene.
5. Place cuts at information or emotional changes; split a long thought into two views only if the second view adds understanding. Use a diagram when spatial/causal relationships are clearer than acting alone.
6. Round event boundaries to frames and use ceil(measuredAudioDuration × fps) for full coverage. Keep a source-to-program map if cleanup was authorized. Include the final spoken word and the intended audio tail.
7. Review early, middle and late visual-to-speech anchors. If the ASR and visible event disagree, inspect the event and label uncertainty; do not silently force a precise sync claim.

## Proposed temporal defaults (not measurements)

At 30fps, try a 6–12-frame hand/face preparation, a 10–20-frame main pose change, and a 12–30-frame reaction hold, then adjust to the actual recording. Use a 6–12-frame fade for a diagram entrance when needed; a clean hard cut is often clearer. Start a restrained camera push at roughly 3–6% framing change across a complete thought, not a constant zoom. Delay a secondary information label by about 4–8 frames after the primary element if hierarchy benefits; do not stagger the letters of a long sentence merely to create motion.

For labels, allow enough time to read at the deliverable size; a starting check is at least about one second for a short phrase and longer for a sentence, but verify with actual copy rather than treating that as a source rule. Keep full captions separate from decorative labels if accessibility captions are requested.

## Transition decision tree

- Same location, a reaction matters: direct cut to a closer view while preserving screen direction.
- New location/time: establish the new set, optionally use a short fade; do not let a wipe substitute for geography.
- Narrative needs explanation: move to the purple board or a diagram overlay, preserving the relevant character/line/number motif.
- Information grows in scale: reveal more spatial context or cut to a wide overview rather than adding more tiny labels.
- Deliberate disruption: a brief distortion can communicate a changed perception, but protect readability and avoid repeated flash effects. Confirm user comfort and necessity.
- Ending: resolve the character beat first, then simplify to the question/choice card. Do not let the CTA overrun the last sentence.

## Audio boundary

The analysis uses local machine ASR for speech content, not a human listening pass. It does not establish the narrator's timbre, actor identity, synthesis provider, music genre, sound design, mixing or loudness. Do not copy a presumed voice or music bed. In new production use the supplied recording unchanged; add licensed local music/SFX only when requested, and verify actual levels and intelligibility by an available listening route. An RMS/peak measurement alone cannot establish genre, mood or clarity.
