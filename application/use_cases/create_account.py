from application.dto.requests import CreateAccountCommand
from application.dto.responses import CreateAccountResult
from application.errors import InvalidRequestError
from domain.types.account_status import AccountStatus
from domain.types.transaction import TransactionType
from domain.entities.entities import Transaction, Account

class CreateAccountUseCase:
    def __init__(self, account_repo, transaction_repo, clock, id_provider):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.clock = clock
        self.id_provider = id_provider

    def execute(self, cmd: CreateAccountCommand) -> CreateAccountResult:
        
        owner_name = cmd.owner_name.strip()
        if not owner_name:
            raise InvalidRequestError('Provide Valid name')
        
        currency = cmd.currency
        initial = cmd.initial_deposit_minor or 0
        if initial < 0:
            raise InvalidRequestError('initial_deposit_minor must be >= 0')
        
        now=self.clock.now() 
        account_id = self.id_provider.generate_id()

        account = Account(
            account_id = account_id,
            owner_name = owner_name,
            currency = currency,
            status= AccountStatus.ACTIVE,
            created_at = now,
            updated_at = now,
        )

        self.account_repo.create(account)

        if initial > 0:
            txn = Transaction(
                tx_id = self.id_provider.generate_id(),
                type = TransactionType.DEPOSIT, 
                account_id = account_id,
                amount = initial,
                created_at=now, 
                )
            self.transaction_repo.append(txn)

        return CreateAccountResult(
                account_id = account_id,
                owner_name = owner_name,
                currency = currency,
                status = AccountStatus.ACTIVE,
                created_at = now,
                initial_balance_minor = initial)