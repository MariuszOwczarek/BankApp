from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.config import SQLITE_PATH

engine = create_engine(f"sqlite:///{SQLITE_PATH}", echo=False, future=True)

create_accounts_table_sql = text("""
CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY NOT NULL,
    owner_name TEXT NOT NULL,
    currency TEXT NOT NULL CHECK (currency IN ('PLN','EUR')),
    balance NUMERIC (18,2) NOT NULL CHECK (balance >= 0),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ACTIVE','BLOCKED','CLOSED')),
    version INTEGER NOT NULL DEFAULT 0
)
""")

create_transactions_table_sql = text("""
CREATE TABLE IF NOT EXISTS transactions (
    tx_id TEXT PRIMARY KEY NOT NULL,
    account_id TEXT NOT NULL REFERENCES accounts(account_id),
    type TEXT NOT NULL CHECK (type IN ('DEPOSIT','WITHDRAW','TRANSFER_IN','TRANSFER_OUT')),
    amount NUMERIC(18,2) NOT NULL CHECK (amount > 0),
    currency TEXT NOT NULL CHECK (currency IN ('PLN','EUR')),
    created_at TEXT NOT NULL,
    related_account_id TEXT NULL REFERENCES accounts(account_id),
    note TEXT NULL
)
""")

create_transactions_index_sql = text("""
CREATE INDEX IF NOT EXISTS idx_transactions_account_created_at
ON transactions (account_id, created_at DESC)
""")

with engine.begin() as con:
    con.execute(text("PRAGMA foreign_keys=ON"))
    con.execute(text("PRAGMA journal_mode=WAL"))
    con.execute(text("PRAGMA busy_timeout=5000"))
    con.execute(create_accounts_table_sql)
    con.execute(create_transactions_table_sql)
    con.execute(create_transactions_index_sql)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)