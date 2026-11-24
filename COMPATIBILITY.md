# Hermes / OpenClaw compatibility

## Adaptation boundary

Both runtimes accept AgentSkills directories with YAML-frontmatter SKILL.md. All 13 complete canonical procedures/resources stay in this checkout. The adapter generates minimal name/description native entrypoints, translating tool invocation and resolving canonical resources; React/Three renderer source and package locks are not rewritten.

| Concern | OpenClaw | Hermes |
| --- | --- | --- |
| Scope | Actual selected agent workspace/skills | Actual selected profile home/skills |
| Selection | Explicit --workspace | Explicit verified --hermes-home, or verified active HERMES_HOME |
| Loading | Available native skill reader/file tools | skill_view(name), then canonical file read |
| Tool calls | Actual OpenClaw schemas; Code Mode is not a shell | Translate examples to actual skill/file/terminal schemas |
| Metadata | Minimal shared name/description | Same fields; no automatic deps or inline shell |
| Config/identity/permissions | Not changed | Not changed |

## Safe integration

- Read-only plan first; --apply only after review. Prefer explicit --agent. Auto mode uses environment markers only, rejects absent/ambiguous markers and is not proof of active runtime identity.
- Resolve the ACTUAL profile/workspace through supported runtime context. Hermes selection can involve --profile/-p, sticky profiles and wrappers; an inherited HERMES_HOME alone is not authoritative. Verify the resolved home before applying. Native Windows defaults can be %LOCALAPPDATA%/hermes rather than ~/.hermes; named profiles and overrides vary. Never guess.
- Preflight all collisions before writes. Identical generated entries and source-in-place layouts are no-ops; differing/unknown existing skill folders block the whole plan. Preserve disabled skills, identities, config, credentials, allowlists and permissions. No force/reset.
- Keep the checkout stable and readable from the ACTUAL execution host/sandbox. Resolve relative links from each CANONICAL skill directory, not the wrapper. Use supported placement/mount setup if needed; otherwise blocked. Never bypass isolation. Moving the checkout requires reviewed entrypoint repair.
- On Hermes, skill_view loads the entrypoint; its linked-file reader is restricted to that wrapper's directory. Read canonical resources with available file/terminal tools, not ../ escapes through skill_view. Translate OpenClaw-only examples; never evaluate Code Mode JavaScript as a shell command.
- New work belongs in the destination active project/workspace. Canonical templates/helpers/specifications are read-only resources.

## Native discovery and refresh

OpenClaw: workspace skills have highest precedence. Allowlist, OS/bin/config gates, tool policy and snapshot/session refresh still apply. A new or supported refreshed session is the verification boundary; file creation alone is not proof of model-visible availability. Host and sandbox materialized paths can differ.

Hermes upstream reviewed behavior: trusted project skills > profile-local > skills.create_dir > skills.external_dirs. Project roots include .hermes/skills and .agents/skills and require explicit trust/scanning; this adapter uses profile-local entries, not automatic project trust. Disabled and surface-specific choices remain intact. Higher tiers shadow lower tiers; same-tier differing duplicates can require path identifiers, and disabling a winner is not dependable fallback. Do not auto-enable, rename or overwrite collisions. /reload-skills refreshes slash commands; catalog caches and conversation snapshots have separate refresh timing. Verify through a fresh native listing/load, respecting the installed version's actual help.

Neither repo AGENTS.md nor a wrapper replaces higher-priority identity/project rules. Hermes can merge Git-root-to-cwd AGENTS.md guidance; when working outside the canonical checkout, read this kit's AGENTS.md explicitly as a capability contract.

## Observed validation

- Adapter suite: 28 tests, 26 passed, 2 skipped because this Windows host cannot create test symlinks.
- All 13 actual exported skills integrated into isolated Hermes and OpenClaw roots, preserving active profiles.
- Local Hermes v0.23.1, commit 3b421578588243f920886e6fe79a6faa87ea026e: native CLI listing found all 13 enabled local skills in an isolated home. The CLI prepared dependencies inside that test home.
- Native Hermes tools.skills_tool.skill_view(name, preprocess=False) loaded all 13 wrappers; resolved home and wrapper paths were asserted, and canonical files were readable. This is native loader API evidence, not a model-driven end-to-end agent session. No paid model call.
- OpenClaw wrapper content/filesystem behavior is tested; no new registered OpenClaw agent/session was created solely for native discovery testing.
- Renderer evidence is source-host 0.1.0 evidence. A byte-identity check for renderer templates/locks/helpers accompanies 0.2.0 packaging; it is not fresh destination proof. See VALIDATION.md and run README.md gates on the recipient.

## Not provisioned

Existing identities/prompts/private memory, provider credentials, sessions, runtime configuration, tool permissions, YouTube OAuth, online publishing, image/TTS accounts, private corpus, model weights and native Filmcraft/MCP. A skill creates no unavailable tool.

## Official references and version boundary

Official Hermes upstream review: main at b98c388a880b1b6fd303c9c2821a3946651a0b4c (2026-11-23). This is distinct from the local observed revision above; do not assume every release has identical behavior.

- [Hermes skills format/discovery/refresh](https://github.com/NousResearch/hermes-agent/blob/b98c388a880b1b6fd303c9c2821a3946651a0b4c/website/docs/user-guide/features/skills.md)
- [Hermes profile selection](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Hermes context files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)
- [Hermes native skill reader](https://github.com/NousResearch/hermes-agent/blob/b98c388a880b1b6fd303c9c2821a3946651a0b4c/tools/skills_tool.py)
- [Hermes disabled/collision handling](https://github.com/NousResearch/hermes-agent/blob/b98c388a880b1b6fd303c9c2821a3946651a0b4c/agent/skill_utils.py)
- [OpenClaw loading/precedence/gates/refresh](https://docs.openclaw.ai/tools/skills), checked against installed docs during adaptation.
