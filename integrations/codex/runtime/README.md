# Independent Codex Level 2 Watchdog — experimental runner v0.1.0

An **actual external Python process** that owns and supervises up to three independent Codex app-server workers. This is executable code, not just a prompt. It is for **user-launched local Codex development projects**; it cannot attach itself to unrelated ChatGPT Work conversations, Codex Cloud tasks, or an existing desktop Codex session. **The CLI must be running** to supervise anything.

## Status

- **Implementation:** working Python stdlib runtime and mock app-server integration tests.
- **Mock tests:** run with `python -m unittest discover -s tests -v`.
- **Real Codex live validation:** NOT TESTED in the authoring environment because `codex` is not installed there. Test against a disposable local Codex repo before trusting it on an important project.
- **Release classification:** experimental. Not a system service, automatic startup agent, or verified cross-host supervisor.

## Requirements

- Python 3.11+.
- A locally installed, authenticated [Codex CLI](https://learn.chatgpt.com/docs/cli/reference) for live use.
- Dedicated **existing** non-overlapping project worktrees for concurrent write tasks; do not give different workers overlapping directories.
- Each user's explicit permission to execute the plan and to allow any local writes/verification scripts.

## Quick start

1. On a development machine, download or clone the public Second Brain repository and navigate to `integrations/codex/runtime`.
2. Prepare a *disposable* project and independent directories/worktrees. Edit `examples/plan.example.json` to use your real **absolute paths** and bounded task prompts. Each task defines `evidence_files` and/or `verify_argv`, which constitute your acceptance checks.
3. From that folder, run:

```bash
python -m watchdog run --plan examples/plan.example.json --state-dir /tmp/my-codex-watchdog-run
```

The default is **read-only Codex sandbox**, no execution of verification scripts, no extra Codex subagents, and **deny all server-initiated approvals**. For an intentionally approved development task with file edits, explicitly opt in:

```bash
python -m watchdog run --plan /absolute/path/to/plan.json \
  --state-dir /absolute/path/to/fresh-private-state-directory \
  --allow-writes
```

If your plan contains `verify_argv`, also use `--allow-verify-exec`. This executes the plan's test command *on your machine outside the Codex sandbox*; only use plans you reviewed and trust. The plan and its prompt are not permission to deploy, publish, email, install paid resources, or change security privileges.

Inspect the persisted record without starting anything:

```bash
python -m watchdog status --state-dir /absolute/path/to/state-directory
```

The state directory must be **new** for each run. On an interrupted run, inspect workers and outputs manually; this version deliberately **fails closed** instead of guessing that an orphaned worker is gone. Do not resume automatically.

## What the watchdog actually enforces

- At most **three actively launched specialist workers per project per host/user** through a project-specific lock and in-process semaphore. Nested Codex agents are **disabled by default** using `codex -c agents.enabled=false app-server`. This is **not** a cross-host/distributed lock, and does not govern unrelated Codex sessions outside this runner.
- Dedicated Codex app-server child process per worker; JSON-RPC initialize / initialized, thread/start, turn/start, and streamed event intake.
- **Timeouts:** wall-clock budget plus a no-evidence-progress budget. A stalled worker gets `turn/interrupt`; its owned process group is terminated if still running after a grace period.
- **Repeat failure:** two equivalent command failures trigger interruption; three non-progress actions and every fifth action create diagnostic checkpoints.
- **Deny all approvals:** command, file, permission, and tool input approval requests are not silently accepted; the affected task blocks. Users must separately authorize consequential changes via a capable interactive execution path.
- **Dependency-aware continuation:** blocked tasks skip dependent tasks; unrelated tasks continue.
- **No self-reported completion:** a terminal `completed` turn also needs new/modified evidence files and/or an explicitly authorized successful verification command.
- **Atomic, restrictive local state:** task status, thread/turn IDs and sanitized reasons stored in `state.json`; no prompts, secret-bearing tool output or reasoning copied into the state file.

## Scope limitations / known engineering work

1. **Live app-server compatibility and version checks require a Codex installation.** Protocol shapes are based on OpenAI's current documented JSON-RPC app-server interface; app-server can change.
2. The watchdog implements **bounded termination**, not automated AI-generated repairs. Its recovery policy is intentionally **zero self-authorized retries**. Project Mode may plan at most two materially distinct, separately approved recovery strategies, but this runtime does not invent or run recovery prompts automatically.
3. Crash recovery is **fail closed**, not automatic process adoption. On restart, inspect and terminate any orphaned workers and choose a new state directory. Never treat existing `RUNNING` ledger entries as safely finished.
4. Global concurrency is enforced only among invocations sharing a filesystem/user/project identity on the same host. External desktop Codex or cloud tasks are not counted.
5. The controller does not implement user-facing approval UI. It *denies* requests rather than granting them unattended. Requests may cause the affected task to be blocked.
6. Local file-edit restrictions rely on Codex's sandbox and individual worktree boundaries, not a hardened container security boundary. Review commands and use a disposable repository first.
7. Integration/merging of separate worktrees is still an explicitly reviewed project step, not an automated merge.

## Security note

**This is experimental agent execution software.** The Codex subprocess can make changes permitted by its effective sandbox and underlying OS account. `--allow-writes` must be treated as authorization to edit the specified worktrees, not authorization for wider or irreversible operations. Do not use on sensitive production directories or pass secrets in prompts or state files. The project lock lives in the current user's `~/.cache/second-brain-watchdog/locks/` directory (same-host guard). A custom `--server-cmd` can defeat the safe nested-agent default; use only a reviewed server command.

## Architecture and specifications

- [Codex app-server reference](https://learn.chatgpt.com/docs/app-server)
- [Second Brain orchestration policy](../ORCHESTRATION.md)
- [Second Brain watchdog policy](../WATCHDOG.md)
- [Runtime acceptance plan](../tests/ACCEPTANCE.md)
