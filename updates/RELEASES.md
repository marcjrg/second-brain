# Second Brain release channel

This is the **public, canonical update entry point**. Installations should link directly here and to [MANIFEST.json](MANIFEST.json). Check when a user requests "Second Brain updates", when running installation, or during an explicitly requested update check. Do not claim proactive notifications without a scheduled monitor or connected capability.

## Current: 1.1.0 — Personalized framework baseline (2026-10-20)
- Added guided onboarding and a five-question personalization protocol.
- Added reusable private workspace template and schema v1.0.
- Added direct private preferences-file URL to the custom-instructions bootstrap.
- Added settings and acceptance-test protocols.
- Added the release channel and non-destructive update procedure.

**Compatibility:** configuration schema 1.0; no private data migration required. Existing private preferences, knowledge and projects remain user-owned. New functionality is available through public operating instructions when fetched; platform custom instructions and connected tools remain subject to their own limits.

## Release policy
Every subsequent release must update this changelog and MANIFEST.json together. Describe new features, behavior changes, compatibility, migration requirements and user actions. Publish additive changes by default. Never require copying the public template over an existing private workspace.

Release announcements are shown when an update check is actually performed and a newer applicable release is found. There is no automatic push notification solely from a GitHub document.
