# UC-005 — Submit Catalog Selection

**Use case:** `SubmitCatalogSelectionUseCase`

## Intent
Covers the "Catalog" intake mode (as opposed to "Free text", UC-001+UC-002):
the requester already knows exactly which `CatalogItem` (by SKU) and
quantity they want, so there is no NLP parsing or sourcing/ranking — only an
availability check.

("OCI Punchout", the third originally-discussed intake mode, is out of
scope for this prototype — see docs/PROJECT.md, Future Work.)

## Acceptance Criteria

- **Given** a valid SKU from an approved supplier with enough stock
  **When** submitting the selection
  **Then** the request moves directly to `RESOLVED` (via a synthetic,
  confidence=1.0 `ParsedRequest`), with the correct `amount` and
  `stock_check = "PASSED"`.

- **Given** an unknown SKU
  **When** submitting the selection
  **Then** `SelectedItemUnavailableError` is raised.

- **Given** a SKU whose supplier is not approved
  **When** submitting the selection
  **Then** `SelectedItemUnavailableError` is raised.

- **Given** a SKU with insufficient stock for the requested quantity
  **When** submitting the selection
  **Then** `SelectedItemUnavailableError` is raised.
