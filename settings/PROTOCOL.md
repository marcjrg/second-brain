# Settings and updates protocol

Trigger: "Second Brain Settings" or relevant Actions selection. Read authorized private `config/preferences.yaml` directly. If inaccessible, explain and do not claim current values.

Display current and allowed values; preview a minimal edit; request approval; update with the latest blob SHA to avoid stale writes; read back and compare. Preserve unrelated fields and records. For activation/default startup style changes, generate a revised bootstrap and ask the user to apply it; a repository write alone cannot modify ChatGPT custom instructions.

Track `schema_version` separately from `framework_version`. Compatible framework changes must preserve personal data. For schema migration, show a diff, preserve recoverable previous content and request approval. For breaking changes, require explicit approval. Never automatically import, delete, publish or expose personal information. Report any unavailable permissions or UI support.

Recovery (!), Help (?) and reading settings do not authorize writes.
