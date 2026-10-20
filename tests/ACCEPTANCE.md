# Second Brain installation acceptance plan

Report PASS / FAIL / NOT TESTED with evidence for each:
1. Verify private owner, private visibility, branch and authorized permissions.
2. Verify private template files and `schema_version`.
3. Validate all preference values against `schema/PREFERENCES.md`.
4. Verify direct private preferences file read after write.
5. Verify generated bootstrap has public contract URL, verified private repository URL, direct private config URL, activation and !/? URLs.
6. Check Always On startup in a separate configured fresh chat.
7. Check On Demand starts inactive and responds to explicit on/off commands.
8. Check ordinary factual questions do not trigger unnecessary repository retrieval.
9. Check ! and ? protocols without unauthorized writes.
10. Check preview/approval and persistence for a harmless Knowledge Vault record; delete test data only with permission.
11. Check settings edit preserves unrelated keys and validates write/readback.
12. Check rerun installation is idempotent and preserves existing data.
13. Check inaccessible GitHub gives truthful fallback.
14. Check response-level UI where supported; never claim a native persistent toolbar.
15. In a separate configured Always On fresh chat, ask an ordinary short factual question as the first message. Verify that the assistant answers directly, includes exactly one compact collapsed Second Brain control if supported, and that Modes, Save and Actions open appropriately. A GitHub request must not be required to show the control. If a platform limitation prevents it, record the omission and fallback instead of reporting PASS.

Repository checks do not prove custom instructions were applied or fresh-chat behavior. Do not mark release fully verified until relevant live checks are completed.

16. Test all three launcher buttons on a factual exchange: the initial dropdown must contain exactly `Modes`, `Save`, `Actions`, not a proposed switch, specific save, or suggested action. Each click must lead to a distinct submenu in the next reply with multiple available options and conversation context; opening the submenu must not change modes, persist data or execute a tool action. Verify that the Save path requests preview and approval before a later write, and that the current mode/task is preserved.
17. Hybrid UI-first bootstrap: confirm a short custom instruction supplies the exact fixed-label compact control on the very first reply; when GitHub is authorized and available, verify an attempted one-time public interaction-standard read at chat startup, and no redundant fetch for subsequent ordinary questions. Simulate unavailable repository access: the assistant must still answer and show the control if the UI is supported, without claiming an unverified read. Check the public read never overrides higher-priority requirements or directly invokes Save/Actions.
