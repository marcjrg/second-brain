# General Help Protocol — `?` v1.0

## Trigger
Only a user message whose trimmed content is exactly `?` invokes General Help. Help does not change modes, approve pending work, persist data or perform consequential actions.

## Procedure
1. Inspect the latest answer, user intent, current task and any verified progress.
2. If the user clearly needs an explanation, answer directly: **what**, **why**, **where we are**, **what (if anything) you need to do**.
3. Otherwise provide a short context-sensitive choice menu. Recommended options:
   - **Explain something** — clarify a response, term, decision or technical step.
   - **What next?** — recommend the best next action and explain why.
   - **Show options** — compare practical paths and tradeoffs.
   - **Capabilities** — explain available Second Brain features, distinguishing verified from planned.
   - **Status** — summarize completed work, blockers and pending approvals.
4. Recommend a path where appropriate. Offer interactive radio/select controls when supported; use concise numbered text choices otherwise.
5. Keep the original task and active modes intact. Return to work when the user chooses.

## Source lookup policy
Help should be fast: use already-loaded instructions and conversation context when sufficient. Retrieve [../../SECOND_BRAIN.md](../../SECOND_BRAIN.md) or relevant modules if the requested feature is unclear, the instruction is missing, or a more detailed authoritative explanation is necessary. Never pretend inaccessible documentation was read.

## Natural language
Questions such as "Why are we doing this?", "What are my options?" and "Where are we?" should invoke the same helpful behavior without requiring the literal shortcut.
