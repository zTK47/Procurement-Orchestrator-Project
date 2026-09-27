# UC-001 — Parse Request

**Actor:** Employee submitting a purchase need in free text.
**Use case:** `ParseRequestUseCase`

## Intent
Turn a free-text procurement need ("I need 5 new Lenovo Laptops for the IT
department") into structured data (`ParsedRequest`: quantity, product name,
category, confidence) that the rest of the pipeline can act on.

## Flow
1. Requester submits raw text + their id + a cost center id.
2. A new `ProcurementRequest` is created in status `CREATED`.
3. The `LLMAdapter` port parses the raw text into a `ParsedRequest`.
4. The request transitions to `PARSED` and is persisted.

## Acceptance Criteria (Given/When/Then)

- **Given** raw text is provided
  **When** `ParseRequestUseCase.execute` runs
  **Then** the request's status becomes `PARSED` and `parsed_data` is set.

- **Given** `raw_text` is empty or missing
  **When** the use case runs
  **Then** a `ValueError` is raised and no state changes.

## Notes
The `LLMAdapter` is mocked in the current prototype (`MockLLMAdapter`,
deterministic, no network calls) — see ADR-004. Swapping to a real LLM
provider via LiteLLM changes only the infrastructure implementation, never
this use case.
