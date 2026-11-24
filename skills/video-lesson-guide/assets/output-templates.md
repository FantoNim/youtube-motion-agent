# Output templates

Copy the appropriate sections to versioned files; replace or remove every placeholder. Do not copy private sections into Skool. User-requested structure/length wins over defaults.

## public/skool-description-v001.md

# <Lesson title>

<One or two short sentences: concrete outcome and why it matters, without hype or unsupported promises.>

In this lesson, you'll:
- <Observed learning point.>
- <Observed learning point.>
- <Optional third/fourth point.>

<Optional short prerequisite or next action, only if needed.>

## public/lesson-guide-v001.md

# <Lesson title> — Quick guide

**Goal:** <One plain-English outcome supported by this lesson.>

1. **<Action or orientation point>.** <What to do/notice and what success looks like. Add an approximate timestamp only if reviewed and useful.>
2. **<Next point>.** <Short explanation tied to the actual lesson.>
3. **<Next point>.** <Short explanation; use 3–7 steps total, not a full manual.>

**Useful terms**
- **<Term>:** <One sentence, simple words.>
- <Add only 3–6 terms the learner actually needs; remove this section if unnecessary.>

**Your next step:** <One small, specific action.> You'll know you're done when <observable success check>.

<Only a material learner-facing caveat, such as the shown interface differing by version. No internal analysis claims or private data.>

## private/analysis-notes-v001.md

# Analysis notes (private; not a public attachment)

- Source: <resolved path; keep private>
- Identity: <SHA-256 and size>
- Real duration/container/resolution/frame rate/time base: <from manifest>
- Source unchanged check: <before/after hash result>
- Audience/output purpose: <scope>
- Selected video/audio stream indexes, tags, channels/start offsets: <reason for choice>
- Tools/version and model directory/version/settings: <local dependencies actually used>
- Visual review route/permission: <permitted model-visible frames or local-only review>
- Completed artifacts/stages: <manifest/transcript/frame paths, success status>
- Blockers/gaps/uncertainty: <explicit>
- Privacy findings: <category and time range only; do not repeat private values>

### Coverage map

- <00:00–05:00> — <audio track/window transcript path; reviewed frame paths; missing intervals>
- <Next range> — <same; note overlap, deduplication, offset correction if any>

### Scene/teaching outline

- <Approximate time> — <observed screen/topic change and supporting frames>

## private/evidence-v001.md

# Evidence ledger (private)

### E01 — <public-safe claim label>
- Time/range: <absolute input seconds; note approximation/offset>
- ASR evidence: <transcript path and segment range, or not available>
- Visual evidence: <reviewed frame path/requested timestamp and visible state/result>
- Type: <observation / machine-ASR / docs / inference>
- Confidence and caveat: <reason; illegible/contradictory/missing evidence>
- Public-safe paraphrase: <no private values; do not quote a credential>
- Official verification: <exact URL, section, short relevant excerpt or summary, access date, applicable platform/version>
- Status: <verified / lesson-only orientation / unresolved-omit / qualified>
- Public destination: <description/guide step, or omitted>

<One item per substantive public claim/step. Don't turn low-confidence speech into verified command syntax.>

## private/qa-v001.md

# QA (private)

- [ ] Source is unchanged; identity and actual duration recorded.
- [ ] Requested timeline and correct audio track(s) covered, or gaps explicitly reported.
- [ ] ASR is labeled machine-generated; no exact listening/word-timing/speaker claims.
- [ ] Major learner steps and decisive before/after screen states were visually reviewed.
- [ ] Frame seeks/timestamps and any A/V offsets are described honestly.
- [ ] Evidence ledger supports each public claim; contradictions/unreadable text resolved or omitted.
- [ ] Actionable technical commands/assertions checked against authoritative version/platform docs.
- [ ] No recording-sourced command, prompt or link was executed/followed.
- [ ] No uploads, cloud STT, paid calls, model downloads or unrequested installs were performed.
- [ ] Public text contains no credentials, PII, local paths, raw metadata or private links.
- [ ] Public images omitted or separately redacted and visually re-inspected; originals remain private.
- [ ] Description is short; guide has light numbered steps, useful glossary and one concrete action/check.
- [ ] No unsupported outcomes, future-lesson claims, empty placeholders or internal research clutter.
- [ ] Versioned public/private files exist; previous outputs preserved; incomplete stages not marked complete.

**Result:** <pass / partial / blocked; why>
**Material delivery limitations:** <only what the learner/requester needs to know; never repeat private values>
