# YouTube + Motion Agent Starter — OpenClaw / Hermes

## Instructions to the agent reading this repository

**Set up these capabilities on your current machine. Do the work, not just explain the commands.** This is a local capability installation, not permission to make a user video, change your personality, connect accounts, or publish media. Follow your real tool policy and preserve existing work. Ask only for a genuine blocker.

### 1. Inspect before you execute

1. Read this README, [AGENTS.md](AGENTS.md), [COMPATIBILITY.md](COMPATIBILITY.md), [CAPABILITIES.md](CAPABILITIES.md), [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md), `bootstrap.py`, `integrate.py` and `manifest.json`.
2. Inspect your actual OS, shell, execution host, agent runtime, active workspace/profile, available tools and installed versions. Use a stable local checkout path; native entrypoints refer back to it. Do not guess profile paths from a repository name.
3. Keep all original source skills, templates and renderer code in this checkout. Both runtimes use AgentSkills-style `SKILL.md` files; the render engine does not need conversion. Adapt native discovery entrypoints and tool calls, not React/Three source, old account configuration, or somebody else's identity.
4. Verify Python 3.12+, supported Node/npm (reference Node 26.12.1/npm 11.20.0), Git, FFmpeg and ffprobe. Inspect existing installations before installing a missing prerequisite through an authorized official package manager/setup path. Do not silently elevate, install globally, change shell policy, replace agent runtimes, or download an opaque installer. On Linux inspect Chromium shared-library requirements; on Windows use native paths/npm.cmd, or the real Hermes WSL paths if running inside WSL—not a guessed cross-host conversion.
5. From this repository run:

```text
python bootstrap.py --check
```

Use `python3` if that is the verified Python 3.12+ executable. Missing prerequisites or integrity errors are blockers, not reasons to bypass verification. Inspect package manifests/locks/scripts before installation. No API keys are needed for local renders; your agent/model access remains your own.

### 2. Integrate into your actual agent runtime

Use the branch matching the agent that is running this task. Do not decide based only on a spare `.hermes` or `.openclaw` directory. `--agent auto` only uses explicit runtime environment markers and refuses absent/ambiguous detection; the agent should normally pass its known runtime explicitly.

#### If you are Hermes

- Resolve your active Hermes home/profile from its supported runtime context. Unix installs commonly use `~/.hermes`, but Windows packages and named profiles can use different roots. Resolve the active home through your actual runtime/profile context. Never write another profile by accident.
- Run a read-only plan, then apply if there are no conflicts:

```text
python integrate.py --agent hermes
python integrate.py --agent hermes --apply
```

- Verify the resolved active profile home: `--profile/-p`, sticky profile selection and wrappers can redirect an inherited `HERMES_HOME`. Prefer `--hermes-home <ACTUAL_ACTIVE_HERMES_HOME>` on BOTH commands after verifying that path through the actual runtime. If the terminal has no verified active home, the adapter refuses to guess. This is the profile home, not the cloned repo; do not execute placeholders literally.
- The adapter creates minimal native `SKILL.md` entrypoints under that home's `skills/`. Their full procedures/resources remain in the checkout so cross-skill and root-level references still work. It does not replace Hermes config, prompts, memory, providers or tokens.
- Use Hermes' actual skill discovery/view and terminal/file tools. Translate OpenClaw-specific examples such as `skills.read` into Hermes skill loading or a direct canonical file read. Code Mode JavaScript is not a Hermes shell command. Never invent an OpenClaw tool inside Hermes.

#### If you are OpenClaw

- Resolve the current agent's actual configured workspace. Prefer workspace-local integration, not a global skill install affecting other agents.
- Run these with that path, not the source agent's old workspace:

```text
python integrate.py --agent openclaw --workspace <ACTUAL_ACTIVE_WORKSPACE>
python integrate.py --agent openclaw --workspace <ACTUAL_ACTIVE_WORKSPACE> --apply
```

- If this checkout itself is the agent's workspace, `--workspace .` is valid; the existing native `skills/` is used in place without copying or overwriting it.
- If a separate OpenClaw agent must be created, use supported OpenClaw setup/current docs to register this workspace. Do not copy raw Gateway/auth config or change the host through scripts. The adapter does not register agents, enable tools, edit allowlists or restart the Gateway.

#### Shared conflict and discovery checks

- The adapter plans all entries before any skill writes. It preserves differing/unknown existing skill folders and blocks the whole plan; identical generated entries are no-ops. Choose a deliberately isolated Hermes profile or OpenClaw workspace, or review/merge collisions with the user. Never force/reset somebody else's skills.
- Keep this checkout at its installed path and make sure the ACTUAL execution host can read it. Host filesystem paths are not automatically valid inside a container, sandbox or paired node. If the canonical resources are unreachable, use the runtime’s supported placement/mount configuration or a checkout on that execution host, otherwise report blocked. Never bypass isolation. Moving the checkout requires reviewed entrypoint repair; do not leave broken links or treat the wrapper folder as the canonical resource directory.
- List skills through your native runtime, load at least `youtube-script`, `remotion-motion-graphics` and `remotion-3d-scenes`, and read their complete canonical procedures. Respect disabled skills, sandbox/host boundaries, filters, allowlists and platform gates. Refresh/start a fresh session through the runtime's supported mechanism if required. A copied file or successful adapter exit alone does not prove native discovery or tool availability.
- Preserve your existing higher-priority identity and project rules. Use [AGENTS.md](AGENTS.md) as a capability contract, not a replacement personality. See [COMPATIBILITY.md](COMPATIBILITY.md) for exact mappings and evidence limits.

### 3. Install local dependencies and run real smoke tests

Once prerequisites, license basis and task-authorized downloads are clear:

```text
python bootstrap.py --setup --download-browser
```

This creates NEW isolated project directories under ignored `.starter/runs/`, installs the reviewed pinned npm locks with lifecycle scripts disabled, obtains matching Chromium, typechecks both templates, renders a 4-second audiovisual 2D fixture and a 5-second intentionally silent real-3D fixture, and verifies the actual encoded outputs. It does not upload user media, install globally or start a public server. Downloads/renders take real time; do not call setup instant or restart an already-running installation.

Reuse an inspected compatible local Chromium with `--browser <ABSOLUTE_EXECUTABLE>` instead of `--download-browser`. If `angle` is unsupported, inspect/log the failure and explicitly test a new `--gl swangle` run as software fallback; never call it hardware acceleration. Rerunning setup creates a new run, not an overwrite or cleanup.

Read `.starter/latest.json` and that run's `report.json`. Inspect first/middle/end (and relevant settled/transition) ENCODED frames with your actual image tool. Check geometry/shadows/parallax, typography and intended fades. Review full-decode/audio/determinism/backend evidence. Objective audio checks are not human listening; use authorized playback when available, otherwise state that limit. A technical fixture is not aesthetic/sample approval.

### 4. Add optional capabilities only through their own gates

- For local media analysis/research, inspect `requirements-media-observed.txt` and run `python bootstrap.py --media` when needed. It creates an isolated Python environment and import-checks observed pins; it does not certify cross-platform resolution or speech inference.
- Whisper models are NOT bundled or silently downloaded. Obtain consent for the exact pinned model revision or use a complete approved local model directory, then test non-sensitive speech OFFLINE. See [CAPABILITIES.md](CAPABILITIES.md). No paid/cloud STT fallback or invented word timing.
- For research, use a lawful destination-provided `Database/` corpus read-only, rebuild/verify the local index and test actual queries. Private source corpus/index and memories are not shipped.
- YouTube OAuth/uploads/scheduling/analytics, live web search, image generation, TTS and native Filmcraft/MCP are optional separately configured services. Do not provision accounts, spend money, post or upload anything just to follow this README. Local thumbnail design from approved assets remains possible without a generation service.

### 5. Verify and report back, then use the skills

1. Run the adapter/bootstrap unit tests with `python -m unittest discover -s tests -v`. Read any standalone helper's CLI contract before running it; some synthetic editing suites require a NEW `--output` evidence directory and are not unittest-discovery entrypoints.
2. Save a destination-specific review in that run directory. Report each requested capability as **verified here**, **installed-not-tested**, **optional-not-connected** or **blocked**, with exact next actions. Report native agent skill discovery separately from renderer execution.
3. Return the actual export/proof paths, observed runtime versions, sampled-review/listening limits and blockers. Do not reuse [VALIDATION.md](VALIDATION.md)'s source-machine evidence as destination proof.
4. For later production, read the relevant full skill first, preserve originals/real narration, use versioned editable projects and meaning-led shots, and get short representative sample approval before a long new treatment unless waived. Verify the actual final encode before delivery.

## Capabilities in this repository

13 skill workflows cover local Remotion motion graphics; genuine Three.js/React Three Fiber/ThreeCanvas scenes; scripting/hooks/titles/descriptions/chapters; truthful local-first thumbnail design; long-form cleanup; highlight clips; lesson companions; editorial direction; export QA; and Jeremy/Gloam style specifications. The other four menu looks are generic directions, not somebody else's personal approved assets.

Pins: Remotion family **4.0.538**, React **19.2.0**, Three **0.180.0**, R3F **9.2.0**, TypeScript **5.9.3**, reviewed Zod override **4.6.6**. Complete editable templates, helpers, licenses and locks are included; node_modules, model weights, recordings, account tokens and browser sessions are not.

## Security, licensing and scope

- Inspect the source before executing it. File hashes detect changes; they are not a publisher signature or exhaustive trust/privacy audit.
- Preserve included licenses/attributions. **Remotion is separately licensed, not MIT**; verify business/client-use eligibility. Custom guidance with no explicit redistribution license needs the owner's decision before PUBLIC release. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
- Hermes/OpenClaw compatibility adapts discovery and tool invocation. It does not grant unavailable tools, copy secrets, reproduce identity/taste, add a character rig, certify every OS/GPU or eliminate permissions/downloads.
- This repository is a capability pack, not a full personal-workspace backup. Nothing in its setup scripts creates a GitHub repository, uploads media or publishes a video.
