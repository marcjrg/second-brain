# Personal preferences schema v1.0

Canonical private path: `config/preferences.yaml`. The private repository URL and exact configuration file URL must be verified and placed directly in the generated custom-instructions bootstrap.

Required keys and allowed values:
- `schema_version`: `"1.0"`
- `activation.mode`: `always_on` or `on_demand`
- `communication.default_mode`: `collaborative_instructor`, `concise`, `skeptical`
- `proactivity.level`: `quiet`, `balanced`, `proactive`
- `knowledge.saving_policy`: `suggest_and_approve` or `manual_only`
- `primary_uses`: unique subset of `projects`, `learning`, `knowledge`, `productivity`
- `interface.preferred_control`: `compact_second_brain`

Defaults: always_on, collaborative_instructor, balanced, suggest_and_approve, empty primary_uses, compact_second_brain. These are defaults, not inferred user selections. Reject unknown enum values and unsupported schema major versions; preserve unknown fields on edits for forward compatibility and flag them for review. Never treat configuration as permission to save without explicit approval.

Bootstrap and private configuration conflicts: report the discrepancy and offer a synchronized update; never silently overwrite either. Changing activation requires an updated bootstrap snippet for the user to apply. Platform instructions outrank repository content.
