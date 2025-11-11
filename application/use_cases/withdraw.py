from decimal import Decimal
from application.dto.requests import WithdrawCommand
from application.dto.responses import WithdrawResult
from application.errors import (
    InvalidRequestError,
    AccountNotFoundError,
    AccountInactiveError,
    InsufficientFundsError,
)
from domain.entities.entities import Transaction
from domain.types.transaction import TransactionType
from domain.types.account_status import AccountStatus


class WithdrawUseCase:
    def __init__(self, account_repo, transaction_repo, clock, id_provider):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.clock = clock
        self.id_provider = id_provider

    def execute(self, cmd: WithdrawCommand) -> WithdrawResult:
        if cmd.amount <= Decimal("0"):
            raise InvalidRequestError("Withdraw amount must be positive")

        account = self.account_repo.get_by_id(cmd.account_id)
        if account is None:
            raise AccountNotFoundError("Account not found")

        if account.status != AccountStatus.ACTIVE:
            raise AccountInactiveError("Cannot withdraw from inactive account")

        current_balance = self.transaction_repo.get_balance(cmd.account_id)
        if current_balance < cmd.amount:
            raise InsufficientFundsError("Insufficient funds")

        now = self.clock.now()
        tx_id = self.id_provider.generate_id()

        txn = Transaction(
            tx_id=tx_id,
            type=TransactionType.WITHDRAW,
            account_id=cmd.account_id,
            amount=cmd.amount,
            currency=account.currency,
            occurred_at=now,
            related_account_id=None,
            note=cmd.note,
        )
        self.transaction_repo.append(txn)
        new_balance = account.balance - cmd.amount
        self.account_repo.update_balance(account.account_id, new_balance)

        #new_balance = self.transaction_repo.get_balance(cmd.account_id)

        return WithdrawResult(
            account_id=cmd.account_id,
            transaction_id=tx_id,
            new_balance=new_balance,
            occurred_at=now,
        )
