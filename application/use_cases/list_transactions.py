from application.dto.requests import ListTransactionsCommand
from application.dto.responses import ListTransactionsResult, TransactionItem
from application.errors import AccountNotFoundError, InvalidRequestError


class ListTransactionsUseCase:
    def __init__(self, account_repo, transaction_repo):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def execute(self, cmd: ListTransactionsCommand) -> ListTransactionsResult:
        account = self.account_repo.get_by_id(cmd.account_id)
        if account is None:
            raise AccountNotFoundError("Account not found")

        if cmd.limit <= 0:
            raise InvalidRequestError("Limit must be positive")

        # Na tym etapie wspieramy tylko account_id + limit.
        # date_from, date_to, type_filter, cursor ignorujemy (są pod przyszłą rozbudowę).
        transactions = self.transaction_repo.list_for_account(
            account_id=cmd.account_id,
            limit=cmd.limit,
        )

        items = [
            TransactionItem(
                transaction_id=tx.tx_id,
                type=tx.type,
                amount=tx.amount,
                occurred_at=tx.occurred_at,
                related_account_id=tx.related_account_id,
                note=tx.note,
            )
            for tx in transactions
        ]

        return ListTransactionsResult(
            account_id=cmd.account_id,
            items=items,
            next_cursor=None,
            total_count=None,
        )
