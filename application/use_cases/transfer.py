from decimal import Decimal
from application.dto.requests import TransferCommand
from application.dto.responses import TransferResult
from application.errors import (
    InvalidRequestError,
    AccountNotFoundError,
    AccountInactiveError,
    InsufficientFundsError,
    CurrencyMismatchError,
    SameAccountTransferNotAllowedError,
)
from domain.entities.entities import Transaction
from domain.types.transaction import TransactionType
from domain.types.account_status import AccountStatus


class TransferUseCase:
    def __init__(self, account_repo, transaction_repo, clock, id_provider):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.clock = clock
        self.id_provider = id_provider

    def execute(self, cmd: TransferCommand) -> TransferResult:
        if cmd.from_account_id == cmd.to_account_id:
            raise SameAccountTransferNotAllowedError("Cannot transfer to the same account")

        if cmd.amount <= Decimal("0"):
            raise InvalidRequestError("Transfer amount must be positive")

        from_account = self.account_repo.get_by_id(cmd.from_account_id)
        to_account = self.account_repo.get_by_id(cmd.to_account_id)

        if from_account is None:
            raise AccountNotFoundError("Source account not found")
        if to_account is None:
            raise AccountNotFoundError("Target account not found")

        if from_account.status != AccountStatus.ACTIVE:
            raise AccountInactiveError("Source account inactive")
        if to_account.status != AccountStatus.ACTIVE:
            raise AccountInactiveError("Target account inactive")

        if from_account.currency != to_account.currency:
            raise CurrencyMismatchError("Cannot transfer between accounts with different currencies")

        from_balance = self.transaction_repo.get_balance(cmd.from_account_id)
        if from_balance < cmd.amount:
            raise InsufficientFundsError("Insufficient funds on source account")

        now = self.clock.now()
        transfer_id = self.id_provider.generate_id()
        debit_tx_id = self.id_provider.generate_id()
        credit_tx_id = self.id_provider.generate_id()

        debit_tx = Transaction(
            tx_id=debit_tx_id,
            type=TransactionType.WITHDRAW,
            account_id=cmd.from_account_id,
            amount=cmd.amount,
            currency=from_account.currency,
            occurred_at=now,
            related_account_id=cmd.to_account_id,
            note=cmd.note,
        )

        credit_tx = Transaction(
            tx_id=credit_tx_id,
            type=TransactionType.DEPOSIT,
            account_id=cmd.to_account_id,
            amount=cmd.amount,
            currency=to_account.currency,
            occurred_at=now,
            related_account_id=cmd.from_account_id,
            note=cmd.note,
        )

        # Zakładamy, że sesja/commit jest wyżej i oba append są atomowe.
        self.transaction_repo.append(debit_tx)
        self.transaction_repo.append(credit_tx)


        new_from_balance = from_account.balance - cmd.amount
        new_to_balance = to_account.balance + cmd.amount

        self.account_repo.update_balance(from_account.account_id, new_from_balance)
        self.account_repo.update_balance(to_account.account_id, new_to_balance)

        #from_new_balance = self.transaction_repo.get_balance(cmd.from_account_id)
        #to_new_balance = self.transaction_repo.get_balance(cmd.to_account_id)

        return TransferResult(
            transfer_id=transfer_id,
            from_account_id=cmd.from_account_id,
            to_account_id=cmd.to_account_id,
            debit_tx_id=debit_tx_id,
            credit_tx_id=credit_tx_id,
            occurred_at=now,
            from_new_balance=new_from_balance,
            to_new_balance=new_to_balance,
        )
