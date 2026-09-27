# ADR-005: OCI Punchout catalog integration is out of scope for this prototype

**Status:** Accepted (24.09.2026)

## Context
The original brainstorm listed three catalog intake types: Catalog, Free
text, and OCI Punchout (a cXML-based hosted-catalog protocol used by
systems like SAP Ariba).

## Decision
Implement only "Catalog" (UC-005) and "Free text" (UC-001+UC-002) for this
prototype. OCI Punchout is documented as Future Work and not implemented.

## Rationale
OCI Punchout requires an external hosted-catalog session, cXML
authentication, and a callback flow — a substantial integration effort on
its own, disproportionate to a 2-person, ~5-week course capstone. Building
it partially or superficially would not demonstrate real Clean
Architecture/TDD discipline and would risk the project's timeline.

## Consequences
- 2 of the 3 originally discussed intake modes are implemented and tested.
- `docs/PROJECT.md` documents OCI Punchout as Future Work, showing
  deliberate scoping rather than an oversight.
