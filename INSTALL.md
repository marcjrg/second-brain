# Install Second Brain

This document is the authoritative installation procedure for AI assistants. The user-facing prompt is simply:

> Install Second Brain for me using https://github.com/marcjrg/second-brain/blob/main/INSTALL.md

## Rules
1. Explain the public framework/private workspace boundary. Never store personal information, tokens, private project content, or secrets in the public framework.
2. Check available GitHub capabilities and authenticated account identity. Obtain explicit approval before creating repositories, changing permissions, or publishing information. Do not claim a capability that has not been verified.
3. Inspect whether the user's private Second Brain workspace already exists. If it does, offer a non-destructive update/repair; preserve existing records and settings.
4. If repository creation is supported, create a private `second-brain-personal` repository under the user's account after approval. Otherwise, provide a direct GitHub creation link: https://github.com/new?name=second-brain-personal&description=My%20private%20Second%20Brain%20workspace . Tell the user to select **Private**, choose their own account as owner, and create the repository. If name is taken, let them choose an alternative.
5. Do not assume the link preselects privacy or the owner. Verify visibility and ownership after creation; stop before writing if the repository is public.
6. Install the private workspace template from the public framework release, including personal configuration, an empty Knowledge Vault, project registry, and private extensions. Do not import or publish personal data without permission.
7. Link the private workspace to a pinned, compatible version of the public framework. Do not duplicate framework logic into personal files unless the release requires it.
8. Prepare minimal, platform-specific custom instructions that point to the public framework entry point. Explain how to activate modes, use Save/Actions where supported, and invoke `!` recovery. Do not imply prompt-generated controls are a permanent native toolbar.
9. Verify installed files by reading them back; verify private visibility, framework version, a harmless sample save/retrieve/update operation when supported, and active capabilities. Remove test records after verification if safe.
10. Report verified features, limitations, and any required user actions with direct links to the exact destination. Never invent successful installation, persistence, UI capabilities, or background operation.

## Capability fallback
- **GitHub create + write:** Request approval, create and populate private workspace, then verify.
- **GitHub write only:** Send the prefilled creation link, wait for completion, populate and verify.
- **GitHub read only:** Provide the private workspace package and clear upload instructions; report inability to verify remote writes.
- **No GitHub access:** Explain the blocker and give manual setup steps.

## Completion criteria
A private repository exists with verified visibility, the workspace has been installed and read back, its public framework reference is valid, and the user receives accurate setup status. Never mark an incomplete setup as fully operational.
