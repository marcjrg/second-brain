# Codex integration acceptance plan

Status labels: PASS, FAIL, NOT TESTED, NOT AVAILABLE. Record environment, Codex version, repo revision, evidence link, and date; documentation review is **not** runtime proof.

## Static/public checks
1. `SECOND_BRAIN.md` links to the Codex integration without activating it for ordinary chats.
2. Native config example parses as TOML; `agents.enabled=true`, `max_concurrent_threads_per_session=3`, `interrupt_message=true`, and `approval_policy="on-request"`.
3. All links resolve; Project Mode remains source of truth for instruction-level watchdog thresholds.
4. Private templates, preferences, Knowledge Vault and activation/UI behavior are not overwritten.
5. Manifest, release notes and public contract agree on version, compatibility and capability status.

## Native Codex smoke tests (disposable repo)
6. Verify project config actually loads for a trusted project; roles are offered where supported.
7. Spawn one, then up to three subagents; check that per-session cap applies; no unrequested agents are automatically spawned.
8. Concurrent writers use separate branches or worktrees; reviewer reports findings; integration tests validate merged results.
9. Confirm ordinary single-agent use and approval prompts remain usable.

## External runtime controller acceptance — must be demonstrated BEFORE claiming active
10. Global project semaphore never admits more than three concurrent specialists across **multiple Codex sessions**, including nested spawn pathways. Coordinator is not counted.
11. Repeated equivalent failure triggers diagnosis by second instance and does not execute a third identical retry; changed prerequisites do not cause a false positive.
12. Three no-progress actions, two oscillatory reversals, and five-action checkpoints produce expected events, without flagging legitimate distinct batch outputs.
13. Two distinct unsuccessful recovery attempts BLOCK affected task, preserve verified output and block dependent tasks, while independent authorized tasks continue.
14. Global incident (shared corruption, unauthorized credential request, or project-wide budget) PAUSES entire project instead of continuing unsafely.
15. Real `turn/interrupt` targets the correct active thread/turn; confirm terminal status, resource release and durable state; simulate failed interruption/connection loss.
16. Restart controller while two workers run: reconcile processes/leases before permitting any new worker; on unresolved state fail closed.
17. Human approval denial and `WAITING_APPROVAL` cannot be converted into automatic approval or unauthorized retry.
18. Secrets, personal data and hidden reasoning are absent from logs; failed writes or missing evidence never yield COMPLETE.
19. Run against at least one actual local Codex app-server instance. Synthetic events alone are insufficient to pass runtime tests.

## Environment-aware activation routing (documented behavior; live tests still required)
20. In an ordinary Chat Project Mode session, verify no Codex agent or independent watchdog is claimed and the baseline instruction watchdog applies to multi-step work.
21. In a verified Work session, confirm Project Mode works with available tools but does not infer Codex from GitHub, terminal access, coding subject or `AGENTS.md`.
22. In a verified Codex coding session, confirm it automatically loads the Codex orchestration policy, without a separate activation command and without automatically spawning three workers.
23. With no trustworthy mode signal, confirm safe fallback reports the environment as unconfirmed and avoids fabricated Work/Codex mode detection.
24. Simulate a live Codex runtime within Work only when an actual Codex connector/session is verified; route only the Codex subtask, not the whole Work session.
25. Without a healthy external controller linked to the target execution, verify `external_watchdog = NOT_ACTIVE`, even if instruction-level monitoring and Codex native config exist.
26. Confirm consequential actions still request explicit approval; switching execution environments does not silently upgrade scope.

## Reference runner v0.1.0 verification
27. Verify [runtime/watchdog/runtime.py](../runtime/watchdog/runtime.py) is executable and the package has no non-stdlib runtime dependencies.
28. Run `python -m unittest discover -s tests -v` from [runtime/](../runtime/README.md) and record test results (15 mocked tests passed in the initial authoring environment).
29. Verify the runner enforces the three-slot cap, a project-wide same-host lock, no overlapping worker cwd roots, and safe default `codex -c agents.enabled=false app-server`.
30. Verify denied server-initiated approval does not lead to an unauthorized request, and hung turns are interrupted or the owned process is terminated.
31. **Mandatory for real activation:** run with a pinned local Codex CLI on a disposable Git repository and prove initialize/initialized, thread/start, turn/start, item/completed and turn/completed, interrupt, and process cleanup.
32. Document that the reference runner **fails closed on restart** and does not yet support durable process adoption, automatic repair prompts, distributed multi-host leases or unattended launch from ChatGPT Work.

## Release policy
- Public instructions/templates may be shipped with runtime tests marked NOT TESTED.
- Mark **external watchdog operational** only after all runtime gates pass for the stated environment and version.
- Do not claim a Codex install, active workers, independent supervision, or deployment merely because these files were published.
