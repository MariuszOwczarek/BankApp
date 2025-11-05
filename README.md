```markdown
# 🏦 Bank System — Hexagonal Architecture (Python)

A small educational **banking system** built in **Python**, following the principles of **Hexagonal Architecture (Ports & Adapters)**.  
The goal of this project is to clearly separate the **domain**, **application**, and **infrastructure** layers while keeping the core logic independent of frameworks and databases.

---

## 📚 Features

- Create and manage accounts (`create_account`)
- Deposit and withdraw money (`deposit`, `withdraw`)
- Transfer funds between accounts (`transfer`)
- Get balance and view transaction history
- Persistent storage in **SQLite**
- Rich CLI interface (Typer + Rich planned)
- Config-driven setup (`config.toml`)

---

## 🧩 Architecture Overview

```

project_root/
├── domain/                # Core business logic
│   ├── entities/          # Account, Transaction (pure dataclasses)
│   ├── ports/             # Interfaces (Repository, Clock, IdProvider, etc.)
│   ├── errors.py          # Domain exceptions
│   └── types/             # Enums (CurrencyType, TransactionType, etc.)
│
├── application/           # Use-cases (CreateAccount, Deposit, etc.)
│
├── adapters/              # Infrastructure
│   ├── repositories/      # SQLite repositories
│   ├── id_provider/       # UUID/ULID generator
│   ├── clock/             # SystemClock adapter
│   └── cli/               # Typer CLI (planned)
│
├── config/                # Configuration (TOML, env variables)
│
├── db.py                  # SQLite schema & session setup
├── requirements.txt       # Dependencies
└── README.md

````

---

## ⚙️ Setup

### 1️⃣ Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate     # macOS/Linux
# or
.venv\Scripts\activate        # Windows
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, create one later with:

```bash
pip freeze > requirements.txt
```

---

## 🧠 Database Initialization

SQLite database file is configured in `config/config.py` (variable `SQLITE_PATH`).

When you run `db.py`, it automatically:

* creates the `accounts` and `transactions` tables,
* enables `PRAGMA foreign_keys`,
* sets journal mode to `WAL`.

To initialize manually:

```bash
python db.py
```

---

## 🧪 Testing (soon)

Planned structure:

```
tests/
├── unit/            # pure domain tests
└── integration/     # SQLite repository + use-case tests
```

Example (pytest style):

```bash
pytest -v
```

---

## 🧭 Next Steps

* Implement use-cases in `application/`:

  * `CreateAccountUseCase`
  * `DepositUseCase`
  * `WithdrawUseCase`
  * `TransferUseCase`
* Add CLI (Typer + Rich)
* Write integration tests for repositories

---

## 🧰 Tech Stack

| Area         | Technology                      |
| ------------ | ------------------------------- |
| Language     | Python 3.11+                    |
| DB           | SQLite (SQLAlchemy Core)        |
| CLI          | Typer + Rich (planned)          |
| Architecture | Hexagonal / Ports & Adapters    |
| ORM          | SQLAlchemy Core (no ORM models) |

---

## 👤 Author

Created by **[Mariusz Owczarek]**
Learning and implementing clean architecture with Python step by step.

---

## 📄 License

MIT License — free to use, modify, and learn from.

```
