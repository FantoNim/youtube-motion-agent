# Practical motion design (adapted from upstream)

## Hierarchy, readability, restraint

Use the user's palette in a project theme. One dominant visual idea per scene; purposeful accent, strong contrast, comfortable margins. Use pixel gaps around large type. Test actual longest strings and target aspect ratio. For social vertical formats reserve platform UI safe areas; verify against the requested platform rather than declaring one universal percentage. Local licensed fonts are preferred; a documented system fallback is acceptable for tool smoke tests but not pixel-identical across OSes. Avoid emoji/icon glyph surprises; SVG/CSS shapes are deterministic.

## Timing and composition

Animate from useCurrentFrame/useVideoConfig; no CSS keyframe clocks, Date.now or unseeded Math.random. Springs/ease-out entrances combine opacity, rise and subtle scale, with clamped opacity/progress. Stagger subordinate words/cards around 0.1–0.2s. Holds provide time to read; constant breathing/motion is optional, not mandatory. Exits may be quicker than entrances. Narration dictates scene length; do not force music cuts over important words. Linear progress is correct for a clock/data sweep; easing is a craft choice, not a ban on math.

## Working typechecked patterns

See assets/template/src/motion.tsx:

- Entrance: frame/fps-derived spring, opacity/rise/scale and full-scene exit wrapper in MotionGraphic.tsx.
- WordReveal: actual staggered words; avoid splitting names/phrases that need reading continuity.
- BarChart: labeled bars and truthful values using one eased progress function. Label placeholder data as illustrative; cite actual data in notes.
- LocalMedia: staticFile Img or muted OffthreadVideo. Still zoom is optional; avoid cropping essential evidence. Keep video audio muted if separate narration is used.
- CaptionPages: provided start/end-second pages; non-overlapping verified captions. It does not transcribe or infer word timing.

Use Sequence from rounded second boundaries for multiple scenes. Sequence child frames are relative to that Sequence. Global Audio should sit outside visual scene sequences to prevent cuts/restarts. For transition libraries, install matching-version @remotion/transitions only after manifest/license review; overlaps shorten the combined duration, so recompute total.

## Optional finishing

Background gradients, subtle grade, grain, vignette, parallax or motion blur can unify mismatched media. They are not required for flat clean brand designs, screenshots or accessibility. Do not grade text into poor contrast. Keep motion blur modest and justify its render cost. Prefer reduced flashing and avoid gratuitous fast zooms.

## Audio

Recorded narration stays at its original timing. Music/SFX are opt-in scope; do not synthesize a bed merely because upstream prescribes sound. Use local licensed audio with attribution. Duck music below speech and verify actual levels/listening; a volume=0.2 number is not a loudness guarantee. Caption claims require accurate timestamps. The bundled 4-second generated WAV is a low-level deterministic test tone, not a substitute for narration, music or speech recognition.
