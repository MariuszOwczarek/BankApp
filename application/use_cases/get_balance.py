from application.dto.requests import GetBalanceCommand
from application.dto.responses import GetBalanceResult
from application.errors import AccountNotFoundError
from decimal import Decimal


class GetBalanceUseCase:
    def __init__(self, account_repo, transaction_repo, clock):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.clock = clock

    def execute(self, cmd: GetBalanceCommand) -> GetBalanceResult:
        account = self.account_repo.get_by_id(cmd.account_id)
        if account is None:
            raise AccountNotFoundError("Account not found")

        as_of = self.clock.now()
        balance = self.transaction_repo.get_balance(cmd.account_id)

        return GetBalanceResult(
            account_id=cmd.account_id,
            balance=balance,
            as_of=as_of,
        )
