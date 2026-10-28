# Second Brain release channel

This is the **public, canonical update entry point**. Installations should link directly here and to [MANIFEST.json](MANIFEST.json). Check when a user requests "Second Brain updates", when running installation, or during an explicitly requested update check. Do not claim proactive notifications without a scheduled monitor or connected capability.

## Current: 1.2.0 — Optional Codex agent orchestration strategy (2026-10-27)
- Added `integrations/codex/` with a three-specialist default ceiling, native Codex configuration example, task and dependency contracts, and reusable `AGENTS.md` clauses.
- Introduced a documented two-layer watchdog design: existing Project Mode instruction checkpoints plus an **independent runtime controller only when separately installed and tested**.
- Defined bounded recovery, task-local blocking with dependency-aware continuation, progress evidence, global cross-session worker leasing, and explicit human approval boundaries.
- Added Codex smoke-test and independent-controller acceptance gates; native per-session subagent settings **do not** enforce a cross-session ceiling.
- Linked the optional integration from the operating contract, README and installer without changing the standard Second Brain UI or normal chat behavior.

**Delivery status:** Public policy and project templates are published. No Codex runtime controller has been installed, deployed or verified through this release; independent runtime monitoring is **NOT ACTIVE** solely because Second Brain is installed. Implementation and live fault-injection verification are separate future steps.

**Compatibility:** Compatible with private configuration schema 1.0. No migration, private writes or new custom-instructions bootstrap required. Does not modify the separate Project Mode repository.

## Previous: 1.1.3 — UI-first hybrid startup (2026-10-20)
- Split startup behavior into a concise custom-instructions UI bootstrap and a detailed public interaction standard.
- On the first assistant turn of a configured chat, request one read of the public UI standard when authorized GitHub access is available. Do not repeat it for each ordinary question.
- Clarified that the first-response button comes from the bootstrap and does **not** depend on a successful GitHub read; the public read enriches the context-aware submenus.
- Updated the installation bootstrap and added acceptance tests for supported, missing, and failed repository access.

**Compatibility:** compatible with schema 1.0; no migration or private data writes. ChatGPT cannot guarantee that it will execute a GitHub request on every fresh-chat turn or provide a permanent native toolbar; any claimed startup read must be verified. The user must manually adopt the shortened custom-instructions bootstrap.

## Previous: 1.1.2 — Generic launcher and contextual submenus (2026-10-20)
- Specified an unchanging three-button Second Brain launcher: Modes, Save, Actions. No contextual replacement labels or suggested tasks in the collapsed control.
- Each button now routes to its own contextual menu in the next assistant response. Opening a submenu never directly changes modes, saves data, or executes actions.
- Defined submenu content for available modes, save candidates with preview/approval, and useful feasible next actions; added navigation-only button instruction examples.
- Aligned the installation bootstrap and extended the acceptance plan to test all three routes.

**Compatibility:** compatible patch for schema 1.0. No private migration; existing preferences and records remain untouched. Apply the latest bootstrap wording in custom instructions and verify UI behavior in a separate conversation. Native response-level UI remains best effort.

## Previous: 1.1.1 — Consistent compact-control startup (2026-10-20)
- Clarified that Always On begins with the first assistant reply using the available custom-instructions bootstrap; it does not depend on a preliminary GitHub read.
- Made the compact collapsed Second Brain response control the default for every reply, including short factual replies, when functional controls are supported and higher-priority requirements permit.
- Updated the installation bootstrap wording and added an explicit fresh-chat, first-response acceptance test.

**Compatibility:** compatible with private configuration schema 1.0. No migration or private-record changes required. The button remains a best-effort response-level control, not a guaranteed permanent native toolbar. Apply the revised bootstrap wording manually in ChatGPT custom instructions; verify behavior in a separate fresh chat.

## Previous: 1.1.0 — Personalized framework baseline (2026-10-20)
- Added guided onboarding and a five-question personalization protocol.
- Added reusable private workspace template and schema v1.0.
- Added direct private preferences-file URL to the custom-instructions bootstrap.
- Added settings and acceptance-test protocols.
- Added the release channel and non-destructive update procedure.

**Compatibility:** configuration schema 1.0; no private data migration required. Existing private preferences, knowledge and projects remain user-owned. New functionality is available through public operating instructions when fetched; platform custom instructions and connected tools remain subject to their own limits.

## Release policy
Every subsequent release must update this changelog and MANIFEST.json together. Describe new features, behavior changes, compatibility, migration requirements and user actions. Publish additive changes by default. Never require copying the public template over an existing private workspace.

Release announcements are shown when an update check is actually performed and a newer applicable release is found. There is no automatic push notification solely from a GitHub document.
