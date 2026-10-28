# Two-layer Codex watchdog policy

## Status: policy published, external runtime NOT deployed by this repository

Layer 1 is the **instruction-level checkpoint policy** owned by [Project Mode watchdog v1.0](https://github.com/marcjrg/project-mode-framework/blob/main/skills/watchdog/SKILL.md). It executes when an agent regains control and cannot interrupt hidden reasoning or a hung tool.

Layer 2 is a separately deployed **independent runtime controller**. Publishing this contract does **not** start it or provide guaranteed cancellation. A controller implementation must pass the [acceptance plan](tests/ACCEPTANCE.md) before anyone claims the two-layer configuration is operational.

## Thresholds (consistent with the existing Project Mode skill)

| Trigger | Action |
| --- | --- |
| Same failure twice, unchanged inputs/prerequisites | Do not issue a third equivalent retry; enter diagnosis |
| Three consecutive actions without measurable task-state progress | Enter diagnosis |
| Two reversals between competing approaches without new evidence | Flag oscillation and diagnose |
| Every five implementation/tool actions | Check objective and evidence |
| Two unsuccessful **materially different** recovery attempts | BLOCK affected task; preserve verified artifacts |
| Configured wall-clock or resource budget exceeded | Request interruption through the running controller; do not silently reset budget |

These are heuristics for Level 1. They only become enforceable external limits if the Level 2 controller observes relevant events, implements deterministic counters, and owns interruption and execution leases. Do not treat an LLM's progress narration, token usage, heartbeat, or raw number of tool calls as proof of progress.

## Progress evidence

Record minimally: task ID, worker ID, action type, normalized intent/target/input fingerprint, error signature, observed result, artifact/revision/check ID, timestamp, attempt number, and next action. Hash or redact inputs when necessary; exclude credentials, personal records, full prompts, and hidden reasoning. Detect genuinely equivalent retries using intent + prerequisite state + failure signature; a repeated command on changed inputs may be legitimate.

Valid progress: passing targeted test, verified artifact readback, accepted code revision, resolved prerequisite, newly satisfied acceptance criterion. Distinct pagination, build stages, legitimate slow jobs, or successful batch processing are not loops.

## Task-local recovery

1. Suspend the affected task and acquire a consistent snapshot of last verified progress.
2. Determine whether failure is transient, environmental, permission-related, dependency-related, deterministic, or genuinely unknown.
3. Select **one materially different** recovery and define the evidence needed to prove it worked.
4. Allow no more than **two distinct unsuccessful** recovery strategies.
5. If both fail: mark `BLOCKED`, preserve work, report blocker and safe next action; never mark complete.
6. Block dependent tasks that need its output. Continue independent tasks only if approved scope and shared resources remain safe.

If the suspected issue involves shared repository corruption, credentials, sandbox escape, or global budget exhaustion, escalate to **project-wide PAUSED** even if one worker detected it.

## Runtime adapter contract

For an app-server-based implementation:
- Establish and maintain Codex app-server connections via documented `initialize` / `initialized`, `thread/start` / `thread/resume`, `turn/start`, and event notifications.
- Track worker-to-thread/turn/process mapping and global specialist leases. Admit at most three specialists **across all supervised sessions**, including nested delegation.
- Distinguish activity heartbeat from verified progress. Use monotonic time for local deadlines. A disconnected event stream means status **UNKNOWN/PAUSED**, not completion.
- Request `turn/interrupt` on the correct active turn, wait for a terminal turn status and reconcile worker/process state. Do not assume a successful request means the operating-system process was killed. Process termination, if supported, is a separate bounded escalation.
- Persist sanitized task state, dependency graph, leases and approval decisions atomically. On restart **reconcile active workers before accepting more work**; fail closed when reconciliation is impossible.
- Provide `WAITING_APPROVAL` with timeout policy **separate from stall detection**. The watchdog must not self-approve and must never turn a denial into a retry.
- Treat duplicate/out-of-order events idempotently where identifiers are available; cap queues, attempts, output size and logging; stop on unrecoverable controller failures.
- Separate monitoring credentials and data access; protect private repositories and secrets. Never create paid infrastructure or external communications without approval.

## Operational verification and release gates

Evidence must demonstrate: global concurrency never over three; equivalent retry stopped; false positives avoided; independent work continues; dependents pause; denial preserved; controller restart reconciles; interruption really terminates the affected turn; no false COMPLETE; and no leaking sensitive content. Test with injected faults and a disposable Codex repository before live deployment.

**Fallback:** When no independent controller is running, use Level 1 only. Report `external_watchdog = NOT_ACTIVE`; never imply that this GitHub file itself monitors or cancels execution.
