# Learnings — Presentation Notes

Keep this updated as you work. It is the raw material for the
"Architecture decisions / Coding agent usage / Tool selection rationale /
Testing & deployment strategy / Challenges and lessons learned" sections of
the presentation. Fill in the `[TODO: ...]` placeholders as a team.

## Architecture decisions

- Clean Architecture with a strict Dependency Rule (see ADR-001):
  `domain/` has zero third-party imports, verified concretely — all 44 unit
  tests for domain + application run without FastAPI, Pydantic, or
  SQLAlchemy installed.
- Split `ValidateRequestUseCase` (budget only) from `CreateOrderUseCase`
  (approval routing + transition) — single-responsibility per use case,
  matching the original prompt's structure while staying testable in
  isolation.
- [TODO: discuss ADR-002 as a team — did you keep RequiresClarificationError
  on price ties, or fall back to the whiteboard's original min(price)?
  Explain why in 2-3 sentences for the presentation.]

## Coding agent usage

- Autonomy level: [TODO — state explicitly whether you ran the agent in
  semi-autonomous mode (agent proposes a diff/plan, human reviews before
  commit) vs. more autonomous. For a graded project, semi-autonomous is the
  defensible choice — see Lecture 1, "Levels of Autonomy".]
- Test creation variant used: [TODO — Spec-Agent-Review loop (agent
  generates full test functions from the spec, you review in chat) vs.
  Comment-Completion-Code (you write a comment, inline completion suggests
  the test)? See Lecture 2, slide 20. Different use cases might use
  different variants — record which.]
- Reflection pattern example: [TODO — if the agent's first attempt at a
  test/implementation failed and you had it self-correct from the error
  message, that is literally the "Reflection" design pattern (Lecture 1,
  slides 39-42). Give one concrete example: what failed, what error message
  was fed back, what changed.]
- One good agent suggestion you kept: [TODO]
- One agent suggestion you rejected/corrected, and why: [TODO]

## Tool selection rationale

- FastAPI/SQLAlchemy/Neon/Render/Copilot — see `docs/PROJECT.md` tech stack
  table for the one-line rationale per choice.
- [TODO: any tool you evaluated and did NOT use, and why]

## Testing & deployment strategy

- Testing pyramid: unit (domain + application, mocked/in-memory repos, zero
  DB dependency) → integration (real Postgres) → e2e (full FastAPI stack).
- [TODO: once integration/e2e tests exist, note how many and what they
  cover]
- [TODO: deployment verification — did the live Render URL actually work
  end-to-end, not just "CI is green"?]

## Challenges and lessons learned

- [TODO: be honest here — this is explicitly graded. Example prompts:
  What took longer than expected? What did you get wrong on the first
  attempt (state machine transitions, approval routing edge cases, budget
  double-check timing)? What would you do differently with another 5 weeks?]
