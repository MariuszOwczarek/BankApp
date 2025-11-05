from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from domain.types.type_transaction import TransactionType
from domain.types.type_currency import CurrencyType
from domain.types.account_status import AccountStatus

@dataclass(frozen=True)
class Account:
    account_id: str
    owner_name: str
    currency: CurrencyType
    balance: Decimal
    created_at: datetime
    updated_at: datetime
    status: AccountStatus

@dataclass(frozen=True)
class Transaction:
    tx_id: str
    type: TransactionType
    account_id: str
    amount: Decimal
    currency: CurrencyType
    created_at: datetime
    related_account_id: str | None = None # up to decission
    note: str | None = None # up to decission