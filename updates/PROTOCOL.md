# Safe update protocol

**Discovery:** On explicit "Second Brain updates", "Check Second Brain version", or installation/update, fetch the public [MANIFEST.json](MANIFEST.json) and [RELEASES.md](RELEASES.md) directly. Never read a private repository to discover where the public update channel lives; keep this public URL in the bootstrap. A scheduled update notification requires an actual monitoring mechanism; do not promise one from instructions alone.

**Compare:** Read the user's private `config/installation.yaml` if authorized and available; compare installed `framework_version`, `schema_version`, and the public manifest. If inaccessible, state that installed version cannot be confirmed. Treat missing or malformed versions as unknown, not automatically outdated.

**Present:** Summarize newly available features, behavioral changes, compatibility, private impact, and any action required. Offer an update preview. Do not silently replace user preferences.

**Apply:** For compatible public instructions, use updated public modules when available; do not rewrite private files solely because a public version changed. For approved private metadata updates, fetch the current file SHA, preserve all other fields, write the new version and read back. For schema migrations, validate compatibility, show a proposed diff and rollback plan, request explicit approval, and preserve a recoverable previous version before writing. Never overwrite `config/preferences.yaml`, knowledge records, project registry or extensions from a template. For breaking changes, request explicit consent and stop if not granted.

**Bootstrap:** Only propose a revised custom-instructions snippet if a URL, activation semantics or essential bootstrap rule changed. User must apply it where the platform cannot edit settings. Preserve their unrelated custom instructions.

**Failures:** Do not claim success when a read, write, or verification fails. Existing private workspace must remain intact. Recovery (!) and Help (?) never authorize update writes.

**Publisher checklist:** Update manifest and release notes together, verify links and compatibility, distinguish public behavior changes from private schema migrations, document tests, and avoid claims of automatic cross-chat notifications.
