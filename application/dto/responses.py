from dataclasses import dataclass
from datetime import datetime
from domain.types.account_status import AccountStatus
from domain.types.currency import CurrencyType
from decimal import Decimal

MoneyMinor = Decimal

@dataclass(frozen=True)
class CreateAccountResult:
    """Wynik utworzenia konta. Czas w UTC (tz-aware)."""
    account_id: str
    owner_name: str            # po normalizacji (strip)
    currency: CurrencyType
    status: AccountStatus
    created_at: datetime       # z Clock.now(), UTC tz-aware
    initial_balance_minor: MoneyMinor  # 0 lub kwota pierwszej wpłaty

