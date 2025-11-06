from domain.ports.ports import TransactionRepository
from sqlalchemy.orm import Session
from domain.entities.entities import Transaction
from sqlalchemy.exc import IntegrityError as SAIntegrityError
from domain.errors import DomainError, TransactionAlreadyExists, AccountNotFound
from sqlalchemy import text
from decimal import Decimal
from domain.types.currency import CurrencyType
from domain.types.transaction import TransactionType
from datetime import datetime

class TransactionsRepository(TransactionRepository):
    def __init__(self, session: Session):
        self._session = session
    
    def append(self, transaction: Transaction) -> None: 
        """Dodaje nowa transakcje do historii."""

        append_transaction_sql = """
            INSERT INTO 
            transactions (tx_id, account_id, type, amount, currency, created_at, related_account_id, note) 
            VALUES(:tx_id, :account_id, :type, :amount, :currency, :created_at, :related_account_id, :note)
        """

        params = {
            'tx_id': transaction.tx_id,
            'account_id': transaction.account_id,
            'type': transaction.type.value,
            'amount': transaction.amount,
            'currency': transaction.currency.value,
            'created_at': transaction.created_at.isoformat(),
            'related_account_id': transaction.related_account_id,
            'note': transaction.note
        }

        try:
            with self._session.begin():
                self._session.execute(text(append_transaction_sql), params)
        except SAIntegrityError as e:
            message = str(e.orig)
            if "UNIQUE constraint failed" in message and "transactions.tx_id" in message:
                raise TransactionAlreadyExists(f"transaction with id={transaction.tx_id} already exists")
            elif "FOREIGN KEY constraint failed" in message:
                raise AccountNotFound(f"No account id={transaction.account_id}")
            elif "CHECK constraint failed" in message :
                raise DomainError("Constraint failed (amount>0, valid type/currency?)")
            elif "NOT NULL constraint failed" in message:
                raise DomainError(f"Missing required field ({message.split(':')[-1].strip()})")
            else:
                raise DomainError(f"Database constraint error: {message}")

    
    def list_for_account(self, account_id: str, limit: int | None = None) -> list[Transaction]:
        base_sql = """
            SELECT
                tx_id, 
                account_id, 
                type, 
                amount, 
                currency, 
                created_at, 
                related_account_id, 
                note
            FROM transactions
            WHERE account_id = :account_id
            ORDER BY created_at DESC
        """

        if limit is not None and limit > 0:
            sql = base_sql + " LIMIT :limit"
            params = {"account_id": account_id, "limit": limit}
        else:
            sql = base_sql
            params = {"account_id": account_id}

        result = self._session.execute(text(sql), params)
        rows = result.mappings().fetchall()

        return [
            Transaction(
                tx_id=row["tx_id"],
                type=TransactionType(row["type"]),
                account_id=row["account_id"],
                amount=Decimal(row["amount"]),
                currency=CurrencyType(row["currency"]),
                created_at=datetime.fromisoformat(row["created_at"]),
                related_account_id=row["related_account_id"],
                note=row["note"],
            )
            for row in rows
        ]