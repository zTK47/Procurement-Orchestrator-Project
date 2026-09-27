# ADR-002: Price ties in the Sourcing Funnel require human clarification

**Status:** Proposed (awaiting team confirmation before submission)

## Context
The original whiteboard brainstorm suggested resolving a price tie
automatically: `return min(matching_items, key=lambda x: x.unit_price)`.
During implementation we chose the opposite: raise
`RequiresClarificationError` and stop, requiring a human to pick.

## Decision (proposed)
When two or more `CatalogItem`s tie for the lowest price after filtering,
the `SourcingRule` domain service raises `RequiresClarificationError`
instead of picking one arbitrarily (e.g. by insertion order, which is what
`min()` would silently do on a tie).

## Rationale
- An arbitrary automatic pick on a tie is a real business risk in
  procurement (e.g. picking a lower-quality supplier by accident because it
  happened to appear first in a list) — silent and unauditable.
- Raising a clear domain error keeps the decision auditable and gives a
  human (or a future "tie-breaker" business rule) an explicit point to
  intervene, rather than hiding it inside `min()`'s ordering behavior.

## Consequences
- The pipeline stops and surfaces a 422 error via the API when a tie
  occurs, instead of silently completing.
- This is a deliberate deviation from the original brainstorm and is
  presented explicitly in the capstone presentation as an architecture
  decision worth discussing.
- **Action required:** the team must explicitly accept or reject this ADR
  before submission (see AGENTS.md "Architecture Gates"). If rejected,
  `SourcingRule.resolve` should fall back to `min(candidates, key=...)`
  instead of raising on ties.
