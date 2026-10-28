# Codex orchestration contract

## Goal, roles, and routing

Second Brain supplies preferences and user authorization. Project Mode owns goals, scope, acceptance criteria, task ledger, and source-control policy. Codex performs development tasks. The external controller, **if separately installed**, owns worker admission, lifecycle events, timeouts, and interruptions. The independent watchdog is deterministic software, not a fourth LLM worker.

Prefer a single agent for sequential or tightly coupled work. Delegate only when independent tasks can be verified separately and expected benefits justify integration cost. Typical specialist roles: explorer, implementer, tester/reviewer. Roles are **assignments**; do not spawn one of each automatically.

## Concurrency and isolation

- **Project-wide limit: 3 simultaneous specialist workers.** The coordinator is separate.
- A native Codex session should use `[agents] max_concurrent_threads_per_session = 3`. This is a **per-session** limit, not a global cross-session enforcement mechanism.
- An independent controller managing multiple Codex sessions **must** obtain one of three global worker leases **before** starting any worker, release it only after the worker is confirmed inactive, and prevent nested untracked workers. On restart, reconcile existing processes and leases **before** admitting new work.
- Workers receive task-scoped working directories or Git worktrees, narrow file ownership, limited command permissions, and no unnecessary secrets.
- Do not let two writers mutate the same files simultaneously. Prefer isolated branches/worktrees; a dedicated integration step reviews and combines verified work.

## Task contract (required)

Every delegated task receives:
- Stable task ID and owning project/repository (verify repo and branch)
- Concrete objective and acceptance criteria
- Allowed files, commands, integrations, and explicit non-goals
- Dependencies and expected progress signals
- Runtime/attempt/cost budgets if actually configured
- Approval requirements and destination of the final evidence report

Suggested states: `QUEUED`, `RUNNING`, `DIAGNOSING`, `RECOVERING`, `WAITING_APPROVAL`, `PAUSED`, `BLOCKED`, `COMPLETE`, `CANCELLED`. Treat `COMPLETE` as valid only after objective evidence and all required dependencies are satisfied.

## Dependency-aware continuation

The scheduler uses a directed acyclic dependency graph. If a task is blocked, pause tasks requiring its missing output; continue only tasks proven independent and within existing authorization. Reallocate a worker slot only after it is safe to do so. Detect and reject dependency cycles at preflight.

The coordinator integrates outputs only after reviewing diffs, tests, security/privacy boundaries, compatibility, and acceptance criteria. No worker's self-reported \"done\" is sufficient.

## Approval contract

No agent, coordinator, watchdog, or recovery step may infer user consent to:
- Deployment/publication, external messages or data sharing
- Deleting or destructively rewriting user data
- Purchasing or provisioning billable resources
- Credentials, permission changes, security posture changes
- Expanding scope, repository exposure, or otherwise consequential changes

Existing approved scope allows ordinary reversible edits/tests only. Require a distinct, recorded human approval for each consequential operation. `approval_policy = "on-request"` helps with Codex escalation, **but is not sufficient** to enforce all these business approvals. Enforce policy in the host/controller and, for critical boundaries, in external systems too.

## Workflow

1. Read project instructions and verify identity, branch, permissions and constraints.
2. Create bounded tasks and dependency graph, define progress evidence and owner.
3. Admit up to three workers; start external monitoring if available and verified.
4. Log structured events (not secret-bearing tool output), run instruction watchdog checkpoints.
5. On stall, suspend only affected work, diagnose, try bounded materially distinct recoveries, then BLOCK if exhausted.
6. Continue independent workers and pause dependents when required.
7. Merge only verified changes; report blockers, pending approvals and exact remaining work.
8. Release worker leases only on confirmed shutdown; reconcile state after any crash.

Do not describe asynchronous/background monitoring as active without a running service and confirmed observability. See [WATCHDOG.md](WATCHDOG.md).
