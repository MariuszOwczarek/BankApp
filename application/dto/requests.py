from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from domain.types.currency import CurrencyType
from domain.types.transaction import TransactionType

@dataclass(frozen=True)
class CreateAccountCommand:
    """Żądanie utworzenia konta."""
    owner_name: str
    currency: CurrencyType
    initial_deposit: Decimal = field(default=Decimal("0"))

@dataclass(frozen=True)
class DepositCommand:
    account_id: str
    amount: Decimal = field(default=Decimal("0"))
    note: str | None = None

@dataclass(frozen=True)
class WithdrawCommand:
    account_id: str
    amount: Decimal = field(default=Decimal("0"))
    note: str | None = None

@dataclass(frozen=True)
class TransferCommand:
    from_account_id: str
    to_account_id: str
    amount: Decimal = field(default=Decimal("0"))
    note: str | None = None

@dataclass(frozen=True)
class GetBalanceCommand:
    account_id: str

@dataclass(frozen=True)
class ListTransactionsCommand:
    account_id: str
    date_from: datetime | None = None
    date_to: datetime | None = None
    limit: int = field(default=100)
    cursor: str | None = None
    type_filter: set[TransactionType] | None = None
