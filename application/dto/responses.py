from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from domain.types.account_status import AccountStatus
from domain.types.currency import CurrencyType
from domain.types.transaction import TransactionType

@dataclass(frozen=True)
class CreateAccountResult:
    account_id: str
    owner_name: str
    currency: CurrencyType
    status: AccountStatus
    created_at: datetime
    initial_balance: Decimal = field(default=Decimal("0"))

@dataclass(frozen=True)
class DepositResult:
    account_id: str
    transaction_id: str
    new_balance: Decimal
    occurred_at: datetime

@dataclass(frozen=True)
class WithdrawResult:
    account_id: str
    transaction_id: str
    new_balance: Decimal
    occurred_at: datetime

@dataclass(frozen=True)
class TransferResult:
    transfer_id: str
    from_account_id: str
    to_account_id: str
    debit_tx_id: str
    credit_tx_id: str
    occurred_at: datetime
    from_new_balance: Decimal
    to_new_balance: Decimal

@dataclass(frozen=True)
class GetBalanceResult:
    account_id: str
    balance: Decimal
    as_of: datetime

@dataclass(frozen=True)
class TransactionItem:
    transaction_id: str
    type: TransactionType
    amount: Decimal
    occurred_at: datetime
    related_account_id: str | None = None
    note: str | None = None

@dataclass(frozen=True)
class ListTransactionsResult:
    account_id: str
    items: list[TransactionItem]
    next_cursor: str | None = None
    total_count: int | None = None
