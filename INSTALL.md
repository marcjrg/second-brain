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
Follow [onboarding/PROTOCOL.md](onboarding/PROTOCOL.md). Briefly introduce Second Brain, ask whether to proceed, and offer the five optional personalization questions (or accept defaults) before any private configuration write. Briefly explain Second Brain and why it needs a private workspace. Determine whether the assistant can access GitHub and create/read/write repositories, and whether it can present interactive controls. Do not infer capabilities from the existence of these instructions. Explain only user actions that are actually required.

### 2. Create or locate the private workspace
Find the user's authenticated GitHub owner and check for an existing `second-brain-personal` repository. If creation is supported, request approval and create it with **Private** visibility. If creation is unavailable, provide the direct GitHub link:
https://github.com/new?name=second-brain-personal&description=My%20private%20Second%20Brain%20workspace

Instruct the user to select their own account as owner, select **Private**, create the repository, and return to the chat. The URL does **not** guarantee privacy or owner selection. Verify ownership and privacy after creation; do not write personal data until confirmed. If the name is unavailable, support an alternate name and use its actual verified URL.

### 3. Install and verify
Validate selections against [schema/PREFERENCES.md](schema/PREFERENCES.md); use [template/private/README.md](template/private/README.md) and its template files as the source for new private workspaces. Install the compatible private workspace template from an **actually available and verified** framework release. If no published template/release exists, disclose that and provide the necessary minimal files from verified sources; never invent a release. Private workspace should include personal config, Knowledge Vault structure, project registry and private extensions where available. Standardize the primary preferences file at `config/preferences.yaml` on the verified default branch; create and read it back only after private visibility and write authorization are verified. If another configuration path already exists, preserve it and use its actual verified path instead of inventing a file. Link to a pinned compatible public framework version when versioned releases exist; otherwise identify the exact verified commit as the provisional reference. Never silently import private data. Read back installed files; test authorized harmless save/retrieve/update if the implementation supports it, and clean up test records safely. Record limitations.

### 4. Choose activation and configure ChatGPT
Use the activation choice already captured during the five-question onboarding flow. If unanswered, ask **one concise question** before generating instructions:

**How should Second Brain run?**
- **Always On (recommended):** Apply the framework quietly from the start of each chat. Collaborative / One-on-One Instructor is the initial style, unless the user has chosen another.
- **On Demand:** Keep the user's existing assistant behavior until they say **"Activate Second Brain"** or **"Second Brain on"**. **"Deactivate Second Brain"** or **"Second Brain off"** returns to the user's normal instructions. Explicit `!` and `?` commands remain available in either state.

Do not presume the user's choice. Explain that activation is conversational/configurational, not a guaranteed cross-chat persisted toggle. With On Demand, a new chat starts inactive unless the user explicitly changes that preference. With Always On, each new configured chat starts active. The user may change their preference later.

**Preserve existing custom instructions.** Ask users to review their current instructions and **append or merge** the minimum compatible Second Brain bootstrap rather than replace unrelated preferences. Avoid duplication and conflicting directions; ask before altering existing text. Favor a compact addition and disclose if the platform character limit prevents it. Provide a copyable snippet, not a full rewrite unless requested. Detailed behaviors stay in GitHub.

Use the verified public URLs and the user's **actual verified private workspace URL AND direct private preferences-file URL**, never the maintainer's private workspace. Obtain the repository default branch and confirm the preferences file exists and is readable before putting its URL in custom instructions. A GitHub URL is not access permission; verify authorized private read access separately. Keep these four paths explicit, with one-line fallback descriptions:
- Operating contract: https://github.com/marcjrg/second-brain/blob/main/SECOND_BRAIN.md
- Collaborative / One-on-One Instructor: https://github.com/marcjrg/second-brain/blob/main/modes/COLLABORATIVE.md
- `!` Recovery: https://github.com/marcjrg/second-brain/blob/main/core/recovery/PROTOCOL.md
- `?` General Help: https://github.com/marcjrg/second-brain/blob/main/core/help/PROTOCOL.md

#### Compact bootstrap template
Replace `[ACTIVATION]` with one of the activation sentences below, `[VERIFIED_PRIVATE_REPO_URL]` with the verified private repository URL, and `[VERIFIED_PRIVATE_CONFIG_FILE_URL]` with the verified direct URL to its configuration file.

```text
Second Brain framework: https://github.com/marcjrg/second-brain/blob/main/SECOND_BRAIN.md
[ACTIVATION]
Default when active: Collaborative / One-on-One Instructor (answer directly; teach clearly when useful): https://github.com/marcjrg/second-brain/blob/main/modes/COLLABORATIVE.md
Private workspace: [VERIFIED_PRIVATE_REPO_URL]. Preferences: [VERIFIED_PRIVATE_CONFIG_FILE_URL] (load directly when relevant and authorized; do not search the public repository to discover my private path).
"!" alone = Recovery (check instructions, modes and verified state; don't repeat actions): https://github.com/marcjrg/second-brain/blob/main/core/recovery/PROTOCOL.md
"?" alone = Help (explain, show options, next steps or status; preserve task): https://github.com/marcjrg/second-brain/blob/main/core/help/PROTOCOL.md
Second Brain updates: https://github.com/marcjrg/second-brain/blob/main/updates/RELEASES.md (check when asked; preserve my private workspace).
Answer ordinary questions normally. When supported, use one collapsed Second Brain control opening Modes → Save → Actions; otherwise use conversational commands. Suggest capabilities sparingly. Preview private saves and request approval. Never claim inaccessible tools, state or persistent UI.
```

**Always On activation sentence:** `Second Brain is active from the start of each chat; its controls are optional, not an on/off switch.`

**On Demand activation sentence:** `Second Brain starts inactive each chat. "Activate Second Brain"/"Second Brain on" enables it for this chat; "Deactivate Second Brain"/"Second Brain off" disables it. While inactive, follow my other instructions; ! and ? still work.`

At the start of a new chat, the custom-instructions bootstrap already supplies both locations. Apply its activation preference and immediate fallback behavior; read the **private preferences file directly when personalization materially matters**, and read relevant public modules when their detailed rules are needed. Do not fetch GitHub for every simple factual question. If either read fails, continue with known bootstrap rules and clearly disclose the missing information only when relevant. If the private file is missing, create/verify it as an authorized installation step before presenting a final snippet; otherwise mark configuration incomplete rather than printing an invented URL.

The generated snippet is **an example to merge**, not permission to overwrite the user's existing instructions. If space is severely limited, offer a shorter minimal variant preserving the central contract, activation choice and both shortcut URLs, with optional modules loaded from the contract.

Explain Settings → Personalization navigation unless a verified direct settings link exists. The user must paste/apply instructions when the assistant lacks settings-write access. Never insert private credentials into custom instructions.

### 5. Introduce the interface and shortcuts
Teach these prominently once:
- **`!` = Recover Second Brain** (fresh instruction/state audit; full protocol at [core/recovery/PROTOCOL.md](core/recovery/PROTOCOL.md)).
- **`?` = Help me** (explanations, options, recommended next steps, capabilities, task status; full protocol at [core/help/PROTOCOL.md](core/help/PROTOCOL.md)).
- **Activation follows the user's onboarding choice:** Always On starts active; On Demand starts inactive until explicitly activated. When active, [Collaborative / One-on-One Instructor](modes/COLLABORATIVE.md) is the default style. A single collapsed **Second Brain** control expands to **Modes → Save → Actions** where supported; the control does not turn the framework on. No permanent `!` or `?` buttons. Details: [core/interaction/STANDARD.md](core/interaction/STANDARD.md).

Interactive UI is best-effort, not a guaranteed globally pinned toolbar. Offer conversational equivalents. Answer ordinary factual questions normally without forcing Second Brain menus, explanations or feature suggestions.

### 6. First-use orientation
After the five-question personalization and verified installation, offer short radio/select choices when the platform supports them, otherwise a numbered text menu: **Explore Modes**, **Try Knowledge Vault**, **Start/Resume a Project**, **Explore Actions**, **Get Help**. Give a contextual recommendation and guide one real, authorized, verifiable action. Do not repeat the questionnaire or force additional questions.

### 7. Completion report
Report separately: verified private repository and privacy, installed files/version, verified direct private preferences-file path and authorized read access, custom instructions **provided versus actually applied**, verified persistence tests, supported controls, unsupported features, and any user action still needed. Do not mark installation complete until necessary verified criteria are met.

## Capability fallback
- **GitHub create + write:** Request approval, create and populate private workspace, verify.
- **GitHub write only:** Supply the direct creation link, wait for completion, populate and verify.
- **GitHub read only:** Provide verified manual files and instructions; report remote writes unverified.
- **No GitHub access:** Provide direct setup guidance; explain that persistence and installation cannot be verified.

## Settings and acceptance tests
Use [settings/PROTOCOL.md](settings/PROTOCOL.md) for settings and migrations. Run and report [tests/ACCEPTANCE.md](tests/ACCEPTANCE.md), distinguishing GitHub-verified checks from fresh-chat and UI tests requiring user participation.

## Public release channel
Every installation must include the direct public update entry point: https://github.com/marcjrg/second-brain/blob/main/updates/RELEASES.md and machine-readable manifest: https://github.com/marcjrg/second-brain/blob/main/updates/MANIFEST.json . On explicit update requests, follow https://github.com/marcjrg/second-brain/blob/main/updates/PROTOCOL.md . Add the compact line `Second Brain updates: https://github.com/marcjrg/second-brain/blob/main/updates/RELEASES.md (check when I ask; preserve my private workspace).` to the generated bootstrap. Public updates do not require copying templates over existing private files. Show new features and compatibility; never promise unsolicited alerts without an actual monitor.

## Version check during setup and use
Follow [updates/PROTOCOL.md](updates/PROTOCOL.md) to compare the public release manifest with private `config/installation.yaml` and `config/preferences.yaml`. During installation, perform this check once files are accessible. During normal use, check on first framework-relevant access when Always On is active, or on explicit activation when On Demand is selected; explicit update requests always check. Do not delay ordinary factual answers for GitHub. Compatible public updates require no private data replacement; migrations and private version metadata changes require preview and approval. If inaccessible, report unverified status rather than assuming versions match.

## Recovery and update behavior
Rerunning this installer must detect existing configuration, compare versions, preserve user data, and ask before breaking changes. A user sending `!` or `?` is **not** authorizing installation, repository mutation or an upgrade.

## Completion criteria
The user has a verified private workspace with readable installed configuration, an accessible framework reference, a verified direct private configuration file and path, a recorded activation preference (Always On or On Demand), a truthful custom-instructions setup status, and a clear introduction to controls and shortcuts. Never claim unsupported features are working.
