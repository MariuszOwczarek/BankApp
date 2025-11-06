from typing import Protocol
from domain.entities.entities import Account
from domain.entities.entities import Transaction
from decimal import Decimal
from datetime import datetime


class IdProvider (Protocol):
    def generate_id(self) -> str:
        """Zwraca nowy unikalny identyfikator (np. UUID, ULID)."""
        ...


class Clock (Protocol):
    def now(self) -> datetime:
        """Zwraca aktualny czas (datetime, nie string)."""
        ...


class AccountRepository(Protocol):
    def create(self, account: Account) -> None:
        """Zapisuje nowe konto."""
        ...
    
    def get(self, account_id: str) -> Account:
        """Zwraca konto po ID lub rzuca AccountNotFound."""
        ...

    def update_balance(self, account_id: str, new_balance: Decimal) -> None:
        """Aktualizuje saldo konta."""
        ...

    def list_all(self, limit: int | None = None) -> list[Account]:
        """Zwraca liste kont."""
        ...


class TransactionRepository(Protocol):
    def append(self, transaction: Transaction) -> None: 
        """Dodaje nowa transakcje do historii."""
        ...
    
    def list_for_account(self, account_id: str, limit: int | None = None) -> list[Transaction]:
        """Zwraca historie transakcji danego konta."""
        ...

