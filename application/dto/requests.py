from dataclasses import dataclass, field
from domain.types.currency import CurrencyType
from decimal import Decimal

MoneyMinor = Decimal  # grosze/centy

@dataclass(frozen=True)
class CreateAccountCommand:
    """Żądanie utworzenia konta. Kwoty w minor units (int, np. 100 = 1.00 PLN)."""
    owner_name: str
    currency: CurrencyType
    initial_deposit_minor: MoneyMinor = field(default=0, metadata={"units": "minor"})
