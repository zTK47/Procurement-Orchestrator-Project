# ADR-004: LLM parsing stays behind a mockable port, never called from domain/application

**Status:** Accepted (24.09.2026)

## Context
Free-text intake (UC-001) needs to extract structured data from natural
language. A real LLM call is slow, non-deterministic, costs money/quota,
and requires network + an API key.

## Decision
`ParseRequestUseCase` depends only on the abstract `LLMAdapter` port. For
this prototype, `MockLLMAdapter` (infrastructure layer) implements it with a
deterministic, regex-based heuristic — no network calls. A real
LiteLLM-backed adapter can be substituted later without touching
domain/application code or existing tests.

## Consequences
- All 44 unit tests run in milliseconds, deterministically, without an API
  key, in any environment (including one with no network access — this
  was verified directly while building this prototype).
- The "AI" in "AI-Assisted Procurement" is deliberately kept at the edge of
  the system (an adapter), not the core — the tested, auditable business
  rules (Sourcing Funnel, approval routing, budget checks) are pure Python
  and do not depend on any LLM's output being correct.
