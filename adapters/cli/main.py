import typer
from decimal import Decimal, InvalidOperation
from contextlib import contextmanager

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from db import SessionLocal
from adapters.repositories.sqlite_account_repository import SqliteAccountRepository
from adapters.repositories.transaction_repository import TransactionsRepository
from adapters.clock.system_clock import SystemClock
from adapters.id_provider.id_provider import UUIDIdProvider

from application.use_cases.create_account import CreateAccountUseCase
from application.use_cases.deposit import DepositUseCase
from application.use_cases.withdraw import WithdrawUseCase
from application.use_cases.transfer import TransferUseCase
from application.use_cases.get_balance import GetBalanceUseCase
from application.use_cases.list_transactions import ListTransactionsUseCase

from application.dto.requests import (
    CreateAccountCommand,
    DepositCommand,
    WithdrawCommand,
    TransferCommand,
    GetBalanceCommand,
    ListTransactionsCommand,
)

from application.errors import (
    ApplicationError,
)

from domain.types.currency import CurrencyType
from domain.types.transaction import TransactionType

app = typer.Typer(no_args_is_help=True)
console = Console()


# --------- infra: UoW + DI --------- #

class Services:
    def __init__(self, session):
        account_repo = SqliteAccountRepository(session)
        tx_repo = TransactionsRepository(session)
        clock = SystemClock()
        idp = UUIDIdProvider()

        self.create_account = CreateAccountUseCase(account_repo, tx_repo, clock, idp)
        self.deposit = DepositUseCase(account_repo, tx_repo, clock, idp)
        self.withdraw = WithdrawUseCase(account_repo, tx_repo, clock, idp)
        self.transfer = TransferUseCase(account_repo, tx_repo, clock, idp)
        self.get_balance = GetBalanceUseCase(account_repo, tx_repo, clock)
        self.list_transactions = ListTransactionsUseCase(account_repo, tx_repo)


@contextmanager
def get_services():
    session = SessionLocal()
    services = Services(session)
    try:
        yield services
        session.commit()
    except ApplicationError as e:
        session.rollback()
        _print_error(str(e))
    except Exception as e:
        session.rollback()
        _print_error(f"Unexpected error: {e}")
        raise
    finally:
        session.close()


# --------- helpers: Rich output --------- #

def _print_success(message: str):
    console.print(Panel.fit(message, style="bold green"))


def _print_error(message: str):
    console.print(Panel.fit(message, style="bold red"))


def _print_account_created(result):
    table = Table(title="Account created")
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")
    table.add_row("Account ID", result.account_id)
    table.add_row("Owner", result.owner_name)
    table.add_row("Currency", result.currency.value)
    table.add_row("Status", result.status.value)
    table.add_row("Created at", str(result.created_at))
    table.add_row("Initial balance", str(result.initial_balance))
    console.print(table)


def _print_balance(result):
    table = Table(title="Account balance")
    table.add_column("Account ID", style="bold cyan")
    table.add_column("Balance")
    table.add_column("As of")
    table.add_row(result.account_id, str(result.balance), str(result.as_of))
    console.print(table)


def _print_transactions(result):
    table = Table(title=f"Transactions for {result.account_id}")
    table.add_column("Tx ID", style="bold cyan")
    table.add_column("Type")
    table.add_column("Amount")
    table.add_column("Occurred at")
    table.add_column("Related account")
    table.add_column("Note")

    for item in result.items:
        table.add_row(
            item.transaction_id,
            item.type.value,
            str(item.amount),
            str(item.occurred_at),
            item.related_account_id or "",
            item.note or "",
        )

    console.print(table)


# --------- commands --------- #

@app.command("create-account")
def create_account(
    owner: str = typer.Option(..., "--owner", "-o", help="Owner name"),
    currency: CurrencyType = typer.Option(..., "--currency", "-c", help="Currency code"),
    initial: str = typer.Option("0", "--initial", "-i", help="Initial deposit"),
):
    """
    Create a new bank account.
    """
    with get_services() as s:
        try:
            initial_dec = Decimal(initial)
        except InvalidOperation:
            _print_error("Invalid initial amount format")
            return

        cmd = CreateAccountCommand(
            owner_name=owner,
            currency=currency,
            initial_deposit=initial_dec,
        )
        result = s.create_account.execute(cmd)
        _print_account_created(result)


@app.command("deposit")
def deposit(
    account_id: str = typer.Option(..., "--account-id", "-a"),
    amount: str = typer.Option(..., "--amount", "-m"),
    note: str = typer.Option("", "--note", "-n"),
):
    """
    Deposit money into an account.
    """
    with get_services() as s:
        try:
            amount_dec = Decimal(amount)
        except InvalidOperation:
            _print_error("Invalid amount format")
            return

        cmd = DepositCommand(
            account_id=account_id,
            amount=amount_dec,
            note=note or None,
        )
        result = s.deposit.execute(cmd)

        _print_success("Deposit completed.")
        console.print(
            f"[bold]Account:[/bold] {result.account_id}  "
            f"[bold]Tx ID:[/bold] {result.transaction_id}  "
            f"[bold]New balance:[/bold] {result.new_balance}  "
            f"[bold]At:[/bold] {result.occurred_at}"
        )


@app.command("withdraw")
def withdraw(
    account_id: str = typer.Option(..., "--account-id", "-a"),
    amount: str = typer.Option(..., "--amount", "-m"),
    note: str = typer.Option("", "--note", "-n"),
):
    """
    Withdraw money from an account.
    """
    with get_services() as s:
        try:
            amount_dec = Decimal(amount)
        except InvalidOperation:
            _print_error("Invalid amount format")
            return

        cmd = WithdrawCommand(
            account_id=account_id,
            amount=amount_dec,
            note=note or None,
        )
        result = s.withdraw.execute(cmd)

        _print_success("Withdrawal completed.")
        console.print(
            f"[bold]Account:[/bold] {result.account_id}  "
            f"[bold]Tx ID:[/bold] {result.transaction_id}  "
            f"[bold]New balance:[/bold] {result.new_balance}  "
            f"[bold]At:[/bold] {result.occurred_at}"
        )


@app.command("transfer")
def transfer(
    from_account_id: str = typer.Option(..., "--from", "-f"),
    to_account_id: str = typer.Option(..., "--to", "-t"),
    amount: str = typer.Option(..., "--amount", "-m"),
    note: str = typer.Option("", "--note", "-n"),
):
    """
    Transfer money from one account to another.
    """
    with get_services() as s:
        try:
            amount_dec = Decimal(amount)
        except InvalidOperation:
            _print_error("Invalid amount format")
            return

        cmd = TransferCommand(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount_dec,
            note=note or None,
        )
        result = s.transfer.execute(cmd)

        _print_success("Transfer completed.")
        table = Table(title="Transfer result")
        table.add_column("Field", style="bold cyan")
        table.add_column("Value")
        table.add_row("Transfer ID", result.transfer_id)
        table.add_row("From account", result.from_account_id)
        table.add_row("To account", result.to_account_id)
        table.add_row("Debit Tx ID", result.debit_tx_id)
        table.add_row("Credit Tx ID", result.credit_tx_id)
        table.add_row("From new balance", str(result.from_new_balance))
        table.add_row("To new balance", str(result.to_new_balance))
        table.add_row("At", str(result.occurred_at))
        console.print(table)


@app.command("balance")
def balance(
    account_id: str = typer.Option(..., "--account-id", "-a"),
):
    """
    Show account balance.
    """
    with get_services() as s:
        cmd = GetBalanceCommand(account_id=account_id)
        result = s.get_balance.execute(cmd)
        _print_balance(result)


@app.command("transactions")
def transactions(
    account_id: str = typer.Option(..., "--account-id", "-a"),
    limit: int = typer.Option(50, "--limit", "-l"),
    tx_type: TransactionType | None = typer.Option(
        None,
        "--type",
        help="Filter by transaction type (DEPOSIT/WITHDRAW/...)",
    ),
):
    """
    List transactions for an account.
    """
    type_filter = {tx_type} if tx_type is not None else None

    with get_services() as s:
        cmd = ListTransactionsCommand(
            account_id=account_id,
            limit=limit,
            type_filter=type_filter,
        )
        result = s.list_transactions.execute(cmd)
        _print_transactions(result)


if __name__ == "__main__":
    app()
