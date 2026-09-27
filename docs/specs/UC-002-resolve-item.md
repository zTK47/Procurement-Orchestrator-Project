# UC-002 — Resolve Item (Sourcing Funnel)

**Use case:** `ResolveItemUseCase`
**Domain service:** `SourcingRule`

## Intent
Given a `ParsedRequest`, find the single best `CatalogItem` to fulfil it.

## The Sourcing Funnel
1. Filter to items in the same category, from an **approved** supplier.
2. Filter out items with insufficient stock or a lead time above the
   allowed maximum (default: 14 days).
3. Rank the remainder by unit price, ascending.
4. If exactly one item is cheapest → resolve to it.
5. If two or more items tie on price → raise `RequiresClarificationError`
   (human decision required — see ADR-002).
6. If nothing survives the filters → raise `NoMatchingCatalogItemError`.

## Acceptance Criteria

- **Given** two approved-supplier items in the requested category, one
  cheaper than the other, both with enough stock
  **When** resolving
  **Then** the cheaper item is selected, `stock_check = "PASSED"`, and the
  request moves to `RESOLVED` with `amount = unit_price * quantity`.

- **Given** the cheapest matching item is from an unapproved supplier
  **When** resolving
  **Then** it is excluded and the next cheapest approved item is selected.

- **Given** two approved items tie exactly on price
  **When** resolving
  **Then** `RequiresClarificationError` is raised and the request status
  does not change.

- **Given** no item in the category has an approved supplier with enough
  stock and an acceptable lead time
  **When** resolving
  **Then** `NoMatchingCatalogItemError` is raised.
