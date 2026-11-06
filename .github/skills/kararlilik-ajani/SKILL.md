---
name: kararlilik-ajani
description: "Use when a task is stuck, ambiguous, or requires steady debugging and implementation. This skill helps maintain momentum, isolate root causes, and finish with evidence-based verification."
argument-hint: "Describe the problem, goal, or blocker"
user-invocable: true
disable-model-invocation: false
---

# Kararlılık Ajani

## When to Use
- A task is blocked, unclear, or taking too many retries.
- You need a calm, systematic way to debug or complete implementation.
- You want to avoid guesswork and finish with verified results.

## Core Approach
1. Restate the goal clearly.
   - Identify the expected outcome, the current state, and the evidence of the problem.
2. Reduce the problem to the smallest reproducible case.
   - Strip away unrelated variables until the failure or gap is easy to observe.
3. Find the root cause before changing behavior.
   - Trace the relevant path, inspect data flow, and look for the first point where expectations diverge.
4. Apply one focused fix at a time.
   - Prefer the smallest change that addresses the actual cause rather than a broad workaround.
5. Verify with concrete evidence.
   - Run a targeted test, check output, or compare behavior against the original requirement.
6. Summarize the result clearly.
   - State what changed, what was verified, and what remains if anything.

## Completion Checklist
- The problem is understood in plain language.
- The root cause was identified rather than guessed.
- The change is minimal and intentional.
- Verification was performed with fresh evidence.
- The final state is summarized with next steps if needed.

## Guardrails
- Do not make multiple speculative changes at once.
- Do not declare success without a verification step.
- If the issue is still unclear, pause and gather more evidence before continuing.

## Example Prompts
- "Investigate this failing import and verify the fix."
- "Help me finish this implementation without guessing."
- "Break this blocker into smaller steps and verify each one."
