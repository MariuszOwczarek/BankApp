from domain.ports.ports import AccountRepository
from domain.entities.entities import Account
from decimal import Decimal
from domain.errors import DomainError, AccountAlreadyExists, AccountNotFound
from sqlalchemy.orm import Session 
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError as SAIntegrityError
from datetime import datetime, timezone
from domain.types.account_status import AccountStatus
from domain.types.currency import CurrencyType


class SqliteAccountRepository(AccountRepository):
    def __init__(self, session: Session):
        self._session = session


    def create(self, account: Account) -> None:
        """Zapisuje nowe konto."""

        create_account_entity_sql = """
            INSERT INTO 
            accounts (account_id, owner_name, currency, balance, created_at, updated_at, status, version) 
            VALUES(:account_id, :owner_name, :currency, :balance, :created_at, :updated_at, :status, :version)
        """
        params = {
            'account_id' : account.account_id,
            'owner_name' : account.owner_name,
            'currency' : account.currency.value,
            'balance' : account.balance,
            'created_at' : account.created_at.isoformat(),
            'updated_at': account.updated_at.isoformat(),
            'status' : account.status.value,
            'version' : 0, 
        }

        try:
            with self._session.begin():
                self._session.execute(text(create_account_entity_sql), params)
        except SAIntegrityError as e:
            message = str(e.orig)
            if "UNIQUE constraint failed" in message and "accounts.account_id" in message:
                raise AccountAlreadyExists(f"Account with id={account.account_id} already exists")
            elif "CHECK constraint failed" in message and "balance" in message:
                raise DomainError("Balance must be >= 0")
            elif "CHECK constraint failed" in message and "currency" in message:
                raise DomainError("Invalid currency")
            elif "CHECK constraint failed" in message and "status" in message:
                raise DomainError("Invalid status")
            elif "NOT NULL constraint failed" in message:
                raise DomainError(f"Missing required field ({message.split(':')[-1].strip()})")
            else:
                raise DomainError(f"Database constraint error: {message}")


    def get(self, account_id: str) -> Account:
        """Zwraca konto po ID lub rzuca AccountNotFound."""

        get_account_entity_sql = """
            SELECT
                account_id,
                owner_name,
                currency,
                balance,
                created_at,
                updated_at,
                status
            FROM accounts
            WHERE account_id = :account_id
        """
        result = self._session.execute(text(get_account_entity_sql),{"account_id": account_id})
        row = result.mappings().fetchone()
        if not row:
            raise AccountNotFound(f"Account with id={account_id} does not exist")
        
        return Account(
        account_id=row["account_id"],
        owner_name=row["owner_name"],
        currency=CurrencyType(row["currency"]),
        balance=Decimal(row["balance"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
        status=AccountStatus(row["status"]),
        )


    def update_balance(self, account_id: str, new_balance: Decimal) -> None:
        """Aktualizuje saldo i znacznik czasu konta."""

        update_account_sql = """
            UPDATE accounts
            SET
                balance = :balance,
                updated_at = :updated_at,
                version = version + 1
            WHERE account_id = :account_id
        """

        params = {
            "balance": new_balance,
            "updated_at": datetime.now(timezone.utc).isoformat(),  # lub Clock.now() przekazany wyżej
            "account_id": account_id,
        }

        with self._session.begin():
            result = self._session.execute(text(update_account_sql), params)
            if result.rowcount == 0:
                raise AccountNotFound(f"Account with id={account_id} not found")


    def list_all(self, limit: int | None = None) -> list[Account]:
        """Zwraca listę kont, najnowsze najpierw. Opcjonalny LIMIT."""
        base_sql = """
            SELECT
                account_id,
                owner_name,
                currency,
                balance,
                created_at,
                updated_at,
                status
            FROM accounts
            ORDER BY created_at DESC
        """

        if limit is not None and limit > 0:
            sql = base_sql + " LIMIT :limit"
            params = {"limit": limit}
        else:
            sql = base_sql
            params = {}

        result = self._session.execute(text(sql), params)
        rows = result.mappings().fetchall()

        # Mapowanie rekordów → encje domenowe
        accounts: list[Account] = [
            Account(
                account_id=row["account_id"],
                owner_name=row["owner_name"],
                currency=CurrencyType(row["currency"]),
                balance=Decimal(row["balance"]),
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                status=AccountStatus(row["status"]),
            )
            for row in rows
        ]
        return accounts