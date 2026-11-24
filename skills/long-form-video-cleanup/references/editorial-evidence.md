# Editorial and evidence contract

## Coverage before cuts

For an N-second source choose windows [0,min(1800,N)], next [previous_end-2,min(previous_end+1798,N)] until actual end. Track chunk id, source hash, absolute audio stream, requested and completed bounds, ASR status/artifact, overlap/dedup lines, confidence, uncertain names/numbers, time-alignment anchors and gaps. Run through ALL chunks; never call only opening analysis full coverage. Exhaust the transcription generator; a started task is not a transcript.

Preserve raw ASR JSON/text and provenance. Derive an editorial transcript with absolute times and overlap deduplicated; never delete original evidence. ASR is segment timing, not verified word timing. Check a visible/spoken event near beginning and in later chunks/end, recording any measured correction separately. If a chunk fails, is empty or has overshoot/gaps: retry within authorized local infrastructure, use supplied transcript with honest provenance, or authorized playback. Empty ASR is not proof of silence. Do not cut uncertain speech based on energy or VAD; missing dependency/model is a blocker, never install/download/upload automatically.

Coverage windows in keep-list are a machine-checkable ledger, not proof of reading/listening. A reviewed_transcript status requires reading the complete timestamped transcript and adjacent context, plus evidence of any timing correction. reviewed_playback requires actual local review with range and reviewer recorded. reviewed_visual_only is adequate only for genuinely visual/no-speech decisions; not a workaround for missing speech. Record unresolved uncertainty; retain uncertain content or block editing if meaning is not established.

## Take comparison ledger

Per intended passage, list every candidate take with exact span and nearby transcript lines; classify complete/restart/partial/intentional recap; list essential propositions, qualifiers, negations, conditions and demonstration state. Compare natural delivery, completeness, accuracy and visual/action continuity. Best complete take wins, NOT latest by default. Preserve unique useful material from another take only at defensible phrase/sentence joins. Never make a fluent but false composite, remove a correction that changes truth or retain a stronger claim after deleting its qualification.

Deletion categories: clear abandoned false start; redundant failed take superseded by identified complete take; excessive production reset/dead time; accidental repeated word only if playback confirms natural clean boundary. Reason must name retained alternative and why no unique message is lost. Intentional emphasis, breathing, rhetorical repetition, natural hesitation, self-correction with useful meaning, accessibility-related speech patterns and characteristic fillers are not automatic mistakes. No all-um/all-stutter regex filter, universal silence threshold or automatic last-take heuristic.

## Boundary acceptance

For each deletion inspect at least adjacent sentences and several seconds around both ends; listen to original and proposed join with context when possible. ASR token edges rarely equal acoustic word boundaries. Leave enough attack/release/breath room; check cut consonants, doubled words, pronoun referents, rhythm, background changes, gestures and demonstrations. Nearest-frame rounding may move by half a frame; inspect quantized time, not just requested transcript time. For fractional cadence/audio lattice choose the nearby exact common boundary only if meaning/words still fit, otherwise retain more material or ask one timing tradeoff question. Never fix a failed boundary by padding/stretching/forced CFR, crossfades over words or unrequested generative repairs.

Default hard cuts preserve speech and source pacing. If a click or visible jump remains, move boundary using source room, retain a wider interval or propose an explicitly approved transition with a new tested plan; helper has no crossfade flag. Keep normal breath gaps; no target compression percentage or forced final duration.

Every keep and deletion needs reason, timestamped transcript path+segment/line references (including adjacent context) and actual boundary evidence paths/review outcome. Source -> output map must retain requested and quantized ranges, frame indexes, chronological output offsets, source/output hashes and all removed complements. Naming evidence is not verification; agent must inspect actual files.

## Review claims

Separate machine ASR, sampled visual review, objective full decode/timing checks, authorized listening and semantic/editorial judgment. No synthetic fixture establishes natural-language understanding, word accuracy, perfect lip sync, exhaustive privacy clearance or production performance. Private proof frames/transcripts may contain credentials/PII and directory naming is not encryption. Deliver provisional candidates if no listening occurred; do not claim professionally reviewed final speech cleanup. No automatic publishing, transcription-to-captions, music, crop or enhancement.
