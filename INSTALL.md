# Install Second Brain

This file is the authoritative, self-contained installation and onboarding procedure for an AI assistant. The **entire public installation prompt** is:

> Install Second Brain for me using https://github.com/marcjrg/second-brain/blob/main/INSTALL.md

Do not require users to paste any other technical instructions.

## Installation principles
- Automate safe, authorized steps; ask for intervention only when a necessary capability or approval is missing. Explain unfamiliar actions in plain language and provide direct destination links.
- Public framework: https://github.com/marcjrg/second-brain . Operating contract: [SECOND_BRAIN.md](SECOND_BRAIN.md).
- Personal data, private preferences, records and project references belong in the user's own **private** repository, never the public framework.
- Verify identity, permissions, visibility, files and tool results; do not claim a completed step without evidence.
- Be resumable and idempotent. If a workspace exists, inspect it and offer non-destructive repair/update. Never overwrite existing records or user custom instructions without review.
- Obtain appropriate approval before creating repositories, publishing information, changing permissions or making consequential modifications.

## Guided installation sequence

### 1. Welcome and capability detection
Briefly explain Second Brain and why it needs a private workspace. Determine whether the assistant can access GitHub and create/read/write repositories, and whether it can present interactive controls. Do not infer capabilities from the existence of these instructions. Explain only user actions that are actually required.

### 2. Create or locate the private workspace
Find the user's authenticated GitHub owner and check for an existing `second-brain-personal` repository. If creation is supported, request approval and create it with **Private** visibility. If creation is unavailable, provide the direct GitHub link:
https://github.com/new?name=second-brain-personal&description=My%20private%20Second%20Brain%20workspace

Instruct the user to select their own account as owner, select **Private**, create the repository, and return to the chat. The URL does **not** guarantee privacy or owner selection. Verify ownership and privacy after creation; do not write personal data until confirmed. If the name is unavailable, support an alternate name and use its actual verified URL.

### 3. Install and verify
Install the compatible private workspace template from an **actually available and verified** framework release. If no published template/release exists, disclose that and provide the necessary minimal files from verified sources; never invent a release. Private workspace should include personal config, Knowledge Vault structure, project registry and private extensions where available. Link to a pinned compatible public framework version when versioned releases exist; otherwise identify the exact verified commit as the provisional reference. Never silently import private data. Read back installed files; test authorized harmless save/retrieve/update if the implementation supports it, and clean up test records safely. Record limitations.

### 4. Configure ChatGPT
Generate **personalized minimal bootstrap custom instructions** with the verified public framework URL and user's real private repository URL. Tell the user how to open ChatGPT personalization/custom instructions; if a direct settings deep link is not verified, give ordinary Settings → Personalization navigation instead of guessing.

The generated instructions must include these essential rules (adapt length and format to the platform's limits):

```text
Use Second Brain as my operating framework. Its public operating contract is https://github.com/marcjrg/second-brain/blob/main/SECOND_BRAIN.md . My private workspace is [VERIFIED_PRIVATE_REPO_URL]. Read authoritative files when accessible; never claim unavailable state was loaded.

If my entire message is "!", invoke Recovery: attempt a fresh read of https://github.com/marcjrg/second-brain/blob/main/core/recovery/PROTOCOL.md , audit modes, instructions and task state, restore only verified context, report gaps, and do not repeat consequential actions.

If my entire message is "?", invoke General Help: use current context or read https://github.com/marcjrg/second-brain/blob/main/core/help/PROTOCOL.md when needed; offer explanations, options, next steps, capabilities or status. Preserve modes and task state; do not execute actions merely from Help.

Use compact Modes → Save → Actions controls when supported; otherwise offer conversational equivalents. Preview private saves and request approval. Do not claim a persistent native toolbar.
```

Present the instructions in a copyable block and explain that the user must paste/enable them if the assistant cannot update settings directly. Avoid copying private tokens or personal records into custom instructions.

### 5. Introduce the interface and shortcuts
Teach these prominently once:
- **`!` = Recover Second Brain** (fresh instruction/state audit; full protocol at [core/recovery/PROTOCOL.md](core/recovery/PROTOCOL.md)).
- **`?` = Help me** (explanations, options, recommended next steps, capabilities, task status; full protocol at [core/help/PROTOCOL.md](core/help/PROTOCOL.md)).
- Compact quick bar **Modes → Save → Actions**, without permanent `!` or `?` buttons. Details: [core/interaction/STANDARD.md](core/interaction/STANDARD.md).

Interactive UI is best-effort, not a guaranteed globally pinned toolbar. Offer conversational equivalents.

### 6. First-use onboarding
Offer short radio/select choices when the platform supports them, otherwise a numbered text menu: **Explore Modes**, **Try Knowledge Vault**, **Start/Resume a Project**, **Explore Actions**, **Get Help**. Give a contextual recommendation and guide one real, authorized, verifiable action. Do not force a long preferences questionnaire.

### 7. Completion report
Report separately: verified private repository and privacy, installed files/version, custom instructions **provided versus actually applied**, verified persistence tests, supported controls, unsupported features, and any user action still needed. Do not mark installation complete until necessary verified criteria are met.

## Capability fallback
- **GitHub create + write:** Request approval, create and populate private workspace, verify.
- **GitHub write only:** Supply the direct creation link, wait for completion, populate and verify.
- **GitHub read only:** Provide verified manual files and instructions; report remote writes unverified.
- **No GitHub access:** Provide direct setup guidance; explain that persistence and installation cannot be verified.

## Recovery and update behavior
Rerunning this installer must detect existing configuration, compare versions, preserve user data, and ask before breaking changes. A user sending `!` or `?` is **not** authorizing installation, repository mutation or an upgrade.

## Completion criteria
The user has a verified private workspace with readable installed configuration, an accessible framework reference, a truthful custom-instructions setup status, and a clear introduction to controls and shortcuts. Never claim unsupported features are working.
