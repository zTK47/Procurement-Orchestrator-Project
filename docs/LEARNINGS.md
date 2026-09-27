# Learnings — Presentation Notes

Raw material for the presentation's "Architecture decisions / Coding agent
usage / Tool selection rationale / Testing & deployment strategy /
Challenges and lessons learned" sections. Keep adding to this as you work
through Phases 3-5 yourselves — the entries below cover the bootstrap
(Phases 0-2 and the initial Phase 3 pass); your own hands-on coding-agent
sessions from here on are the most valuable material to add.

## Architecture decisions

- **Clean Architecture with a verified Dependency Rule**: `domain/` has
  zero third-party imports. This was checked concretely, not just claimed —
  all 44 unit tests for domain + application run without FastAPI, Pydantic,
  or SQLAlchemy installed at all (see ADR-001).
- **UC-003/UC-004 split**: `ValidateRequestUseCase` was deliberately kept
  budget-only, with a separate `CreateOrderUseCase` handling approval
  routing — matching the original project brief's use-case naming while
  keeping each use case single-responsibility and independently testable.
- **ADR-002 (price-tie handling)**: this is a concrete example worth
  walking through live in the presentation. The original whiteboard
  brainstorm suggested `min(price)` on a tie; the implementation instead
  raises `RequiresClarificationError`. This was explicitly flagged as a
  `Proposed` ADR rather than silently implemented, discussed with the team,
  and only then marked `Accepted` — a live demonstration of the "Architecture
  Gates" mechanism from AGENTS.md actually being used, not just documented.
- **RecordApprovalDecisionUseCase** was added beyond the original prompt's
  4 use cases because the whiteboard's own workflow diagram
  (PENDING_APPROVAL -> APPROVED -> ORDER_SENT -> ...) required it to be a
  complete, working pipeline rather than stopping at PENDING_APPROVAL.

## Coding agent usage

- **Autonomy level**: work was driven in a semi-autonomous loop — proposals
  (architecture, file structure, code) were generated, then reviewed and
  explicitly confirmed or corrected by the team before being treated as
  final (e.g. the prompt/whiteboard reconciliation, and ADR-002). This
  matches Lecture 1's "semi-autonomous: agent proposes, human decides"
  level, deliberately chosen over a more autonomous mode for a graded
  academic deliverable where every business-rule decision needs to be
  attributable.
- **Reflection pattern in practice**: several early architecture proposals
  were revised after review surfaced concrete gaps — e.g. the first
  AGENTS.md-driven plan omitted SKILL.md/progressive disclosure entirely
  (Lecture 2 material); the first use-case implementation didn't match the
  original prompt's naming/JSON contract (stockCheck/budgetCheck fields
  were missing). Each gap was fed back explicitly and the next iteration
  corrected it — the same "error message -> revised attempt" loop as the
  Reflection design pattern (Lecture 1, slides 39-42), just applied to
  requirement gaps instead of failing test output.
- **Concrete example of a correction accepted**: initial `ValidateRequestUseCase`
  bundled budget-checking AND approval-level routing into one method; this
  was split into `ValidateRequestUseCase` + `CreateOrderUseCase` after
  comparing against the project brief's exact use-case list.
- **Concrete example of a bug caught by manual review, not testing** (fill
  in your own examples here as you go): a code review pass (without being
  able to execute the code in the dev sandbox) still caught a foreign-key
  constraint violation waiting to happen in the Approval repository's
  integration tests (parent User/ProcurementRequest rows were never
  seeded) — a reminder that code review remains necessary even with a
  green-looking implementation; TDD only catches what you actually run.
- [TODO: once you run your own coding-agent sessions for Phases 3-5, add
  1-2 concrete "good suggestion kept" / "suggestion rejected and why" pairs
  here, plus which tool (Copilot vs. Claude Code/Codex CLI) produced each.]

## Tool selection rationale

- FastAPI/SQLAlchemy/Neon/Render/Copilot — see `docs/PROJECT.md` tech stack
  table for the one-line rationale per choice.
- Chose comma-separated string columns for `required_approval_levels` and
  `history` on `ProcurementRequestModel` (rather than a separate join
  table) — a deliberate simplification appropriate for a 5-week prototype;
  flagged here rather than presented as if it were the "correct" enterprise
  design (a real system would likely use a separate audit-log table).
- [TODO: any tool you evaluated and did NOT use, and why]

## Testing & deployment strategy

- Testing pyramid: unit (domain + application, mocked/in-memory repos, zero
  DB dependency, **44/44 passing, verified**) → integration (real Postgres,
  SAVEPOINT-isolated) → e2e (full FastAPI stack via `TestClient` +
  `dependency_overrides`).
- Integration/e2e tests were written to the same specs as the unit tests
  but could not be executed in the development sandbox used to build them
  (no network access to install FastAPI/SQLAlchemy/pytest there) — they
  must be the very first thing run once you have a normal dev environment.
  This is itself worth mentioning as a real constraint encountered during
  the project, not hidden.
- [TODO: once run, note pass/fail counts and any fixes needed]
- [TODO: deployment verification — did the live Render URL actually work
  end-to-end, not just "CI is green"?]

## Challenges and lessons learned

- Reconciling three different sources of truth (a course-provided lecture
  framework, a teammate's own LLM-generated implementation prompt, and a
  whiteboard brainstorm) required an explicit mapping step before writing
  any code — e.g. the whiteboard's `ProcurementRequest`/`CatalogItem`
  naming had to be reconciled with generic `Department`/`PurchaseRequest`
  naming from an earlier planning pass. Skipping this and just picking one
  source would have produced an internally inconsistent project.
- [TODO: be honest here — this is explicitly graded. What took longer than
  expected once you started running real tests? What assumption in the
  SQLAlchemy mapping turned out to be wrong? What would you do differently
  with another 5 weeks?]
