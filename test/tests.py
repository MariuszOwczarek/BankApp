from decimal import Decimal

from domain.types.currency import CurrencyType
from adapters.id_provider.id_provider import UUIDIdProvider
from adapters.repositories.sqlite_account_repository import SqliteAccountRepository
from adapters.repositories.transaction_repository import TransactionsRepository
from adapters.clock.system_clock import SystemClock
from application.use_cases.create_account import CreateAccountUseCase
from application.use_cases.deposit import DepositUseCase
from application.use_cases.withdraw import WithdrawUseCase
from application.use_cases.transfer import TransferUseCase
from application.use_cases.get_balance import GetBalanceUseCase
from application.dto.requests import (
    CreateAccountCommand,
    DepositCommand,
    WithdrawCommand,
    TransferCommand,
    GetBalanceCommand,
)
from db import SessionLocal


def main():
    session = SessionLocal()
    account_repo = SqliteAccountRepository(session)
    tx_repo = TransactionsRepository(session)
    clock = SystemClock()
    idp = UUIDIdProvider()

    create_uc = CreateAccountUseCase(account_repo, tx_repo, clock, idp)
    deposit_uc = DepositUseCase(account_repo, tx_repo, clock, idp)
    withdraw_uc = WithdrawUseCase(account_repo, tx_repo, clock, idp)
    transfer_uc = TransferUseCase(account_repo, tx_repo, clock, idp)
    balance_uc = GetBalanceUseCase(account_repo, tx_repo, clock)

    # 1) Create two accounts
    acc1 = create_uc.execute(CreateAccountCommand(owner_name="Alice", currency=CurrencyType.PLN))
    acc2 = create_uc.execute(CreateAccountCommand(owner_name="Bob", currency=CurrencyType.PLN))
    print("Created:", acc1)
    print("Created:", acc2)

    # 2) Deposit on Alice: 200
    dep = deposit_uc.execute(DepositCommand(account_id=acc1.account_id, amount=Decimal("200")))
    print("Deposit:", dep)

    # 3) Withdraw from Alice: 50
    wd = withdraw_uc.execute(WithdrawCommand(account_id=acc1.account_id, amount=Decimal("50")))
    print("Withdraw:", wd)

    # 4) Transfer 100 from Alice to Bob
    tr = transfer_uc.execute(
        TransferCommand(
            from_account_id=acc1.account_id,
            to_account_id=acc2.account_id,
            amount=Decimal("100"),
        )
    )
    print("Transfer:", tr)

    # 5) Check balances
    bal1 = balance_uc.execute(GetBalanceCommand(account_id=acc1.account_id))
    bal2 = balance_uc.execute(GetBalanceCommand(account_id=acc2.account_id))

    print("Balance Alice:", bal1)
    print("Balance Bob:", bal2)

    session.commit()


if __name__ == "__main__":
    main()
