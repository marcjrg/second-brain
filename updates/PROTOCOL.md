# Safe update protocol

**Discovery:** On explicit "Second Brain updates", "Check Second Brain version", or installation/update, fetch the public [MANIFEST.json](MANIFEST.json) and [RELEASES.md](RELEASES.md) directly. Never read a private repository to discover where the public update channel lives; keep this public URL in the bootstrap. A scheduled update notification requires an actual monitoring mechanism; do not promise one from instructions alone.

**Compare:** Read the user's private `config/installation.yaml` if authorized and available; compare installed `framework_version`, `schema_version`, and the public manifest. If inaccessible, state that installed version cannot be confirmed. Treat missing or malformed versions as unknown, not automatically outdated.

**Present:** Summarize newly available features, behavioral changes, compatibility, private impact, and any action required. Offer an update preview. Do not silently replace user preferences.

**Apply:** For compatible public instructions, use updated public modules when available; do not rewrite private files solely because a public version changed. For approved private metadata updates, fetch the current file SHA, preserve all other fields, write the new version and read back. For schema migrations, validate compatibility, show a proposed diff and rollback plan, request explicit approval, and preserve a recoverable previous version before writing. Never overwrite `config/preferences.yaml`, knowledge records, project registry or extensions from a template. For breaking changes, request explicit consent and stop if not granted.

**Bootstrap:** Only propose a revised custom-instructions snippet if a URL, activation semantics or essential bootstrap rule changed. User must apply it where the platform cannot edit settings. Preserve their unrelated custom instructions.

**Failures:** Do not claim success when a read, write, or verification fails. Existing private workspace must remain intact. Recovery (!) and Help (?) never authorize update writes.

**Publisher checklist:** Update manifest and release notes together, verify links and compatibility, distinguish public behavior changes from private schema migrations, document tests, and avoid claims of automatic cross-chat notifications.

## Version handshake on startup
When Second Brain is activated and repository access is available, compare the public manifest's `latest_version`, `minimum_supported_schema` and `schema_version` with private `config/installation.yaml` (`framework_version`) and `config/preferences.yaml` (`schema_version`). Always On: perform this check on the first framework-relevant access in a chat, not for every ordinary factual question. On Demand: check on explicit activation. An explicit update request always checks. A fresh-chat check is best effort, never guaranteed without tool access.

Classify: **current** when versions match and schema supported; **compatible_update** when public is newer and private schema is supported; **migration_required** when schema is unsupported or manifest requires migration; **unknown** when a source is inaccessible, invalid or version comparison cannot be established. Public and private schema numbers need not equal the framework version. Compare numeric dotted version segments, not lexicographic strings; unknown versions must not be guessed.

On a compatible update, give a concise new-feature notice when relevant; the public modules may be used without overwriting private data. Do not automatically bump private `framework_version`: it denotes the release last **verified/adopted** in that workspace, not the latest seen. Only update private metadata after user approval and successful verification. On migration-required, explain and request explicit consent before any private write. On unknown, proceed using available bootstrap rules and do not claim successful synchronization. Never block ordinary assistance solely for an update check.
