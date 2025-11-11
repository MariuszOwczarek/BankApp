from decimal import Decimal
from application.dto.requests import CreateAccountCommand
from application.dto.responses import CreateAccountResult
from application.errors import InvalidRequestError
from domain.types.account_status import AccountStatus
from domain.entities.entities import Account, Transaction
from domain.types.transaction import TransactionType


class CreateAccountUseCase:
    def __init__(self, account_repo, transaction_repo, clock, id_provider):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.clock = clock
        self.id_provider = id_provider

    def execute(self, cmd: CreateAccountCommand) -> CreateAccountResult:
        owner_name = (cmd.owner_name or "").strip()
        if not owner_name:
            raise InvalidRequestError("Owner name is required")

        if cmd.initial_deposit < Decimal("0"):
            raise InvalidRequestError("Initial deposit must be >= 0")

        now = self.clock.now()
        account_id = self.id_provider.generate_id()

        # saldo początkowe na koncie
        initial_balance = cmd.initial_deposit if cmd.initial_deposit > 0 else Decimal("0")

        account = Account(
            account_id=account_id,
            owner_name=owner_name,
            currency=cmd.currency,
            balance=initial_balance,          # 🔴 TU BYŁ BRAK
            status=AccountStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        self.account_repo.create(account)

        if cmd.initial_deposit > 0:
            tx_id = self.id_provider.generate_id()
            txn = Transaction(
                tx_id=tx_id,
                type=TransactionType.DEPOSIT,
                account_id=account_id,
                amount=cmd.initial_deposit,
                currency=cmd.currency,
                occurred_at=now,
                related_account_id=None,
                note="initial deposit",
            )
            self.transaction_repo.append(txn)

        return CreateAccountResult(
            account_id=account_id,
            owner_name=owner_name,
            currency=cmd.currency,
            status=AccountStatus.ACTIVE,
            created_at=now,
            initial_balance=initial_balance,
        )
