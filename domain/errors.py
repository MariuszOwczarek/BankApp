
class DomainError(Exception):
    """Base class for domain-level errors."""
    pass


class AccountAlreadyExists(DomainError):
    """Raised when trying to create an account with an existing id."""
    pass


class AccountNotFound(DomainError):
    """Raised when account cannot be found."""
    pass

class TransactionAlreadyExists(DomainError):
    """Raised when trying to create a transaction with an existing id."""
    pass


class ApplicationError(Exception):
    """Bazowy wyjątek warstwy application."""


class InvalidRequestError(ApplicationError):
    """Nieprawidłowe dane wejściowe do use-case'a."""


class AccountNotFoundError(ApplicationError):
    """Konto nie istnieje."""


class AccountInactiveError(ApplicationError):
    """Operacja na nieaktywnym koncie."""


class InsufficientFundsError(ApplicationError):
    """Brak środków na wykonanie operacji."""


class CurrencyMismatchError(ApplicationError):
    """Niezgodność walut między kontami/operacjami."""


class SameAccountTransferNotAllowedError(ApplicationError):
    """Próba przelewu na to samo konto."""
