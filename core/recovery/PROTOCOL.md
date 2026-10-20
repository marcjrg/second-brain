# Recovery Protocol — `!` v1.0

## Trigger
Only a user message whose trimmed content is exactly `!` invokes recovery. Do not interpret `!` as permission to execute, retry, publish, overwrite, deploy, or repeat consequential actions.

## Procedure
1. Capture the currently visible task, last verified result, pending decisions, active communication style and workflow mode. Mark uncertain state as uncertain.
2. Attempt a **fresh read** of [../../SECOND_BRAIN.md](../../SECOND_BRAIN.md), this protocol, and relevant interaction/module instructions from the authoritative public repository. Use a verified private workspace only when authorized and accessible.
3. Compare current conduct with the retrieved standard: modes, task continuity, approval boundaries, privacy, controls, and claimed tool capabilities.
4. Restore only instructions and state actually recoverable from verified sources. Do not silently modify files or user preferences.
5. Report in compact form: **Detected**, **Recovered**, **Unavailable/Unverified**, **Safe next step**. If nothing was wrong, say no discrepancy was found within the checks performed, not that the system is perfect.
6. Return to the original task without automatically performing a pending action.

## Offline fallback
If the repository cannot be reached, inspect the visible conversation and bootstrap custom instructions. Clearly label recovery as partial and provide a link to the authoritative file. Never fabricate missing instructions or claim fresh verification.

## Improvement pathway
If recovery reveals a missing or contradictory rule, explain a proposed framework change. Obtain the required approval before editing GitHub. A repository change can improve future sessions; this command does not retrain the underlying model.
