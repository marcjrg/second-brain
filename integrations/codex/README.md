# Codex multi-agent orchestration — Second Brain v1.2.0

Optional integration for **Codex development projects**. This module is **not** a new Second Brain mode, and it does not run when answering ordinary ChatGPT questions.

## Status and honest capability boundary

- **Available now:** project instructions, a native Codex configuration example, task delegation contracts, two-layer watchdog specification, approval policy, and acceptance-test plan.
- **Already available separately:** the instruction-level anti-loop skill at [Project Mode](https://github.com/marcjrg/project-mode-framework/blob/main/skills/watchdog/SKILL.md).
- **Not installed or running merely by reading this repository:** the independent external watchdog/controller. No process, scheduler, timer, or Codex task is started by a GitHub document.
- **Runtime integration gate:** a separate executable controller must subscribe to Codex events, own worker lifecycle/interruption, persist evidence, and pass the tests in [tests/ACCEPTANCE.md](tests/ACCEPTANCE.md) before being described as operational.

## Defaults

| Setting | Default |
| --- | --- |
| Specialist worker concurrency | Maximum **3** per project, not a target |
| Coordinator | Separate; does not occupy one of the three specialist slots |
| Supervision | Instruction checkpoints **plus** independently running runtime watchdog when installed and verified |
| Failed recovery | Block the affected task and dependent tasks; allow independent authorized work |
| High-impact actions | Explicit human authorization, never inferred from task delegation |
| Default execution mode | One agent unless parallelism has a justified benefit |

## How to adopt in a development repo

1. Read [ORCHESTRATION.md](ORCHESTRATION.md) and [WATCHDOG.md](WATCHDOG.md), and the canonical [Project Mode entry point](https://github.com/marcjrg/project-mode-framework/blob/main/PROJECT_MODE.md).
2. Merge relevant [AGENTS.template.md](AGENTS.template.md) clauses into that project's existing `AGENTS.md`; preserve its existing constraints.
3. Adapt [config.example.toml](config.example.toml) to `.codex/config.toml` **in a trusted development repository**. This config limits *spawned subagents within a native session*, not separately started Codex processes.
4. Specify each job's output, owned files, dependency list, authorization boundary, and proof of completion before delegation.
5. For true independent supervision, deploy and verify a **separate controller** according to the interface and acceptance criteria below. If unavailable, use the instruction watchdog only and label external supervision **NOT ACTIVE**.
6. Test in a disposable repo before granting wider file/network permissions or applying to a live project.

This is a portable public template. Personal data, secrets, project logs, approval records, and private configuration remain in the user's private project/workspace, never this repository.

## Source documentation

- Codex configuration: https://learn.chatgpt.com/docs/config-file/config-reference
- Codex subagents: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Codex app-server: https://learn.chatgpt.com/docs/app-server
- Project Mode watchdog: https://github.com/marcjrg/project-mode-framework/blob/main/skills/watchdog/SKILL.md
