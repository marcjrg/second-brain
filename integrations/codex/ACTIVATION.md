# Automatic activation and environment routing — v1.2.1

## Design intent

**Second Brain is ambient; Project Mode is opt-in; Codex orchestration is contextual.** Invoking Project Mode should not require an extra command to enable the existing Project Mode anti-loop instructions, or the Codex-specific policy when a Codex development execution context is verified. **Do not create workers, start an external controller, modify project configuration, or deploy anything merely because an instruction file was loaded.**

This is capability-aware routing, **not guaranteed ChatGPT UI mode detection**. A selected UI experience (Chat, Work, or Codex) may not be exposed as trusted machine-readable metadata in an ordinary conversation. Never invent a mode flag, inspect hidden system internals, claim to have read UI chrome, or treat the model's assumptions as verification.

## Routing on Project Mode activation (and meaningful environment change)

1. Activate Project Mode for the requested project and read its own [canonical rules](https://github.com/marcjrg/project-mode-framework/blob/main/PROJECT_MODE.md) as available.
2. **Load the existing Project Mode instruction watchdog** for multi-step work, regardless of whether the project runs in Chat, Work, or Codex. Instruction checkpoints only occur when an assistant has control; do not imply they can interrupt a hung process.
3. Determine the **actual execution context**, in this precedence order:
   - **Confirmed Codex:** a trusted host/runtime identification of a Codex execution context, or a directly verified live Codex session/API connection in the execution environment. It must correspond to the session where the work will execute.
   - **Confirmed Work:** a trusted host/runtime identification of Work when supplied. Work being selected in the user's UI is **not always visible to the assistant**.
   - **Other/unknown:** no trusted mode identifier or live Codex confirmation. Route using *verified available tools*, not an inferred product label.
4. Only when **Codex is confirmed AND the approved project task involves Codex software development**, load [ORCHESTRATION.md](ORCHESTRATION.md), [WATCHDOG.md](WATCHDOG.md), and relevant project `AGENTS.md` instructions. Prefer **one** agent; up to **three** concurrently active specialist workers only when justified and supported. The per-session native limit does not guarantee a cross-session project limit.
5. Otherwise use ordinary Project Mode with the tools and scope actually available. **Do not launch Codex subagents, claim the Codex configuration loaded, or claim runtime watchdog coverage** in Work/Chat/unknown contexts. The assistant can still assist with coding and use approved tools, but must not claim Codex-specific orchestration.
6. To activate *external* runtime supervision, require an independently deployed controller, a confirmed healthy connection to the **target execution**, valid worker/process mapping, and tested interrupt and recovery paths. If any check fails, label the external watchdog **NOT ACTIVE**. Do not promote instruction checkpoints into a claim of true independent supervision.

## Evidence rules

- **Strong positive evidence:** host-provided mode identity (when actually available), or successfully connected Codex-native app-server/CLI session or equivalent verified Codex runtime interface. This confirms only what was tested for the current execution context.
- **Context but not proof:** user says "I'm using Codex"; a repository has `AGENTS.md` or `.codex/config.toml`; a GitHub connector is installed; shell access exists; the task involves code; Codex was used in another chat; a model name matches a model also supported by Codex.
- **Absence of a Codex API does not prove Work mode.** The assistant may say it cannot independently see which UI option was selected and proceed safely.
- Do not interrogate the user solely to label a mode when a safe, useful plan or approved task can proceed. Ask a targeted question only if a genuinely Codex-only operation is essential and cannot be validated.

## Behavior matrix

| Confirmed execution context | Task | Activate automatically | Execution limitation |
| --- | --- | --- | --- |
| Ordinary Chat | Any Project Mode project | Project Mode + instruction watchdog for multi-step tasks | No assumed background process or Codex agents |
| Work | Research, documents, general projects | Project Mode + available Work tools + instruction watchdog | No assumed Codex session |
| Work | Coding project | Project Mode + verified Work coding tools + instruction watchdog | Codex configuration/subagents are **not** presumed active |
| Codex | Software development | Project Mode + Codex policy + instruction watchdog | Up to 3 specialist workers **only when delegated**, within authorization |
| Unknown | Any | Project Mode + verified tools + instruction watchdog | Use conservative single-agent workflow and disclose relevant unknowns |

If Work uses a verified, separately connected Codex runtime, the controller can route **that specific coding subtask** to Codex under the same Codex approval/supervision rules. Do not conflate a Codex subtask with the entire Work session changing mode.

## One-time status reporting

At Project Mode activation or the first applicable coding step, optionally show a concise status only when relevant:
- `Environment: Codex (verified)` **or** `Environment: Work (verified)` **or** `Environment: not independently confirmed`
- `Orchestration: Codex active / standard Project Mode`
- `Instruction watchdog: in effect for multi-step execution`
- `External watchdog: ACTIVE (verified) / NOT ACTIVE`

Never claim an automatic launcher, automatic tool installation, background service, or cross-session process monitoring exists solely because these rules were read. Reroute on genuine environment changes or resume, not on every chat message.

## Security and approval

Loading policy is not approval to execute. Consequential operations require explicit user authorization. All agents inherit the same scope and approval boundaries. A runtime watchdog **must not** self-approve actions or work around a denied permission.

## Acceptance criteria

- Starting Project Mode in Work does **not** claim native Codex agent activation.
- Starting Project Mode in confirmed Codex on a coding task loads the Codex policy without a second \"enable watchdog\" command.
- Unknown contexts use the safe fallback, with honest labeling.
- Host metadata absent: no false \"detected Work\" or \"detected Codex\" assertions.
- External watchdog never reports ACTIVE without live, tested, task-matched controller coverage.
- Simple tasks prefer one agent; no more than three specialist workers admitted when supervision is deployed.
- Approval boundaries and private configuration remain untouched.
