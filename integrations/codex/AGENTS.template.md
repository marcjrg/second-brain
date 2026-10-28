# Optional clauses for a project's AGENTS.md

Merge into the existing project instructions; do not blindly replace an existing `AGENTS.md`. A repository that already uses Project Mode should keep its current entry point and watchdog rules.

## Automatic activation gate
On Project Mode use, read https://github.com/marcjrg/second-brain/blob/main/integrations/codex/ACTIVATION.md. The Project Mode instruction watchdog applies during multi-step execution in Chat, Work and Codex. Enable Codex-specific orchestration automatically **only when the current coding execution is confirmed to be Codex**. An `AGENTS.md` file or `.codex/config.toml` alone is not proof of a live Codex session. If unverified, avoid spawning or claiming Codex-native subagents and use the standard Project Mode fallback.

## Second Brain / Project Mode Codex workflow

For multi-step coding work, follow:
- https://github.com/marcjrg/project-mode-framework/blob/main/PROJECT_MODE.md
- https://github.com/marcjrg/project-mode-framework/blob/main/skills/watchdog/SKILL.md
- https://github.com/marcjrg/second-brain/blob/main/integrations/codex/ORCHESTRATION.md
- https://github.com/marcjrg/second-brain/blob/main/integrations/codex/WATCHDOG.md

Prefer a single agent by default. Delegate independent, bounded tasks only when beneficial; use no more than **three concurrently active specialist workers** across the project. Native Codex per-session configuration does not enforce a project-wide cap across separate sessions.

Require task ID, file ownership, dependencies, acceptance evidence and scope boundaries for each delegate. Preserve separate worktrees/branches for concurrent writers. Integrate only verified results. Use the existing Project Mode anti-loop thresholds: two equivalent failures, three non-progress actions, two oscillatory reversals, checkpoint every five actions, and at most two distinct recovery attempts. After recovery exhaustion, BLOCK the affected task and dependent work; continue independent authorized tasks.

Do not claim an independent watchdog is running unless a separately deployed controller is actually connected and tested. Never bypass explicit approval for destructive, costly, security-sensitive, public or other consequential operations. If execution cannot be supervised as required, disclose the limitation and run a safer single-agent or instruction-only workflow rather than pretending to enforce runtime guarantees.
