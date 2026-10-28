# Second Brain

A modular, publicly shareable, ambient assistant framework with private per-user workspaces.

## Install with ChatGPT

Copy and paste this one sentence into a new ChatGPT conversation:

> Install Second Brain for me using https://github.com/marcjrg/second-brain/blob/main/INSTALL.md

The installer guides creation and verification of a private workspace and personalized custom instructions. Actual features depend on available tools and platform support.

## Everyday use
Second Brain offers **Always On** or **On Demand** activation and operates quietly when enabled, using [Collaborative / One-on-One Instructor Mode](modes/COLLABORATIVE.md) by default. Ordinary questions get ordinary answers.

Where supported, a single collapsed **Second Brain** control expands to **Modes → Save → Actions**. This is a preferred response-level UI, not a guaranteed permanent ChatGPT toolbar.

Send **`!`** alone for recovery, or **`?`** alone for general help, options, explanations, next steps or status.

For personalized setup see [onboarding/PROTOCOL.md](onboarding/PROTOCOL.md), [schema/PREFERENCES.md](schema/PREFERENCES.md), [settings/PROTOCOL.md](settings/PROTOCOL.md) and [tests/ACCEPTANCE.md](tests/ACCEPTANCE.md). See [SECOND_BRAIN.md](SECOND_BRAIN.md) for the operating contract.

## Optional Codex multi-agent watchdog
Software development workflows can use the [Codex orchestration integration](integrations/codex/README.md): up to **three specialist agents**, Project Mode anti-loop safeguards, task-level failure isolation, and explicit approval boundaries. It includes native configuration templates and a specification for **independent runtime supervision**, which requires a separate running, verified controller; this repository does not start one. This integration is optional and does not change the normal Second Brain interface or private workspace.

## Updates
Second Brain evolves through a public [release channel](updates/RELEASES.md), [version manifest](updates/MANIFEST.json), and [safe update protocol](updates/PROTOCOL.md). Ask **“Check Second Brain updates”** to compare versions when GitHub is accessible. Private repositories are never automatically overwritten by public releases. Notifications require an actual monitoring mechanism.
