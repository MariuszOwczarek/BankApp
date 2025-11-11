# domain/errors.py

class DomainError(Exception):
    """Base class for all domain-level errors."""
    pass


# --- Account-related ---
class AccountAlreadyExists(DomainError):
    """Raised when trying to create an account that already exists."""
    pass

class ApplicationError(DomainError):
    """Base class for all application-level errors."""
    pass

class AccountNotFoundError(DomainError):
    """Raised when an account with given ID does not exist."""
    pass

class AccountNotFound(DomainError):
    """Raised when an account with given ID does not exist."""
    pass

class AccountInactiveError(DomainError):
    """Raised when an operation is attempted on an inactive account."""
    pass


# --- Transaction-related ---
class TransactionAlreadyExists(DomainError):
    """Raised when inserting a transaction that already exists."""
    pass


class InvalidTransactionType(DomainError):
    """Raised when transaction type is not valid."""
    pass


class CurrencyMismatchError(DomainError):
    """Raised when transaction currencies do not match."""
    pass


class InsufficientFundsError(DomainError):
    """Raised when an account does not have enough balance."""
    pass


class SameAccountTransferNotAllowedError(DomainError):
    """Raised when a transfer is attempted within the same account."""
    pass


# --- Validation / input ---
class InvalidRequestError(DomainError):
    """Raised when a use-case or domain rule receives invalid input."""
    pass


class OwnerNameNotProvided(DomainError):
    """Raised when owner name is missing during account creation."""
    pass
