"""Business-rule violations of the Order PDF Orchestration context."""


class DomainError(Exception):
    """Base class for all domain rule violations."""


class InvalidLineItemError(DomainError):
    """A line item has a blank description or a quantity that is not positive."""
