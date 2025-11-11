# Mini Bank 🏦 (Hexagonal Architecture + CLI)

Mały, edukacyjny system bankowy napisany w Pythonie, zaprojektowany w stylu **Hexagonal Architecture (Ports & Adapters)**.

Projekt pokazuje:
- jak oddzielić **domenę** od **infrastruktury**,
- jak pisać **use-case’y** jako czystą logikę aplikacyjną,
- jak korzystać z **portów/repozytoriów** zamiast twardych zależności,
- jak zbudować **CLI (Typer + Rich)** na szczycie heksagonu,
- jak utrzymywać **stan (accounts)** + **historię (transactions)** i wersjonowanie rekordów.

---

## Spis treści

1. [Technologie](#technologie)
2. [Struktura projektu](#struktura-projektu)
3. [Model domeny](#model-domeny)
4. [Ports & Adapters](#ports--adapters)
5. [Use-case’y](#use-casey)
6. [CLI](#cli)
7. [Baza danych](#baza-danych)
8. [Testy / sandbox](#testy--sandbox)
9. [Jak rozwijać dalej](#jak-rozwijać-dalej)

---

## Technologie

- Python 3.12+
- SQLite
- SQLAlchemy (core, bez ORM)
- Typer – CLI
- Rich – kolorowy output
- `dataclasses`, `Decimal`, `Enum`

---

## Struktura projektu

```bash
project_root/
├── domain/                # Core biznesu (zero zależności od infrastruktury)
│   ├── entities/          # Account, Transaction
│   ├── ports/             # Porty (AccountRepository, TransactionRepository, Clock, IdProvider)
│   ├── types/             # Enums (CurrencyType, TransactionType, AccountStatus, ...)
│   └── errors.py          # Błędy domenowe
│
├── application/           # Use-case’y (logika aplikacyjna)
│   ├── dto/               # Request/Response DTO (komendy + wyniki)
│   ├── use_cases/         # CreateAccount, Deposit, Withdraw, Transfer, GetBalance, ListTransactions
│   └── errors.py          # Błędy warstwy aplikacyjnej (aliasy/wrappery domeny)
│
├── adapters/              # Infrastruktura
│   ├── repositories/
│   │   ├── sqlite_account_repository.py   # implementacja AccountRepository
│   │   └── transaction_repository.py      # implementacja TransactionRepository
│   ├── clock/
│   │   └── system_clock.py                # Clock → datetime.now(tz=UTC)
│   ├── id_provider/
│   │   └── id_provider.py                 # UUIDIdProvider (generate_id)
│   └── cli/
│       └── main.py                        # Typer + Rich CLI
│
├── config/
│   └── config.py          # Ścieżki, ustawienia (np. db path)
│
├── db.py                  # Inicjalizacja SQLite, tabele, SessionLocal
├── test/
│   └── tests.py           # Sandbox / scenariusz integracyjny
├── requirements.txt
└── README.md

CLI
Plik: adapters/cli/main.py
Uruchamianie (z katalogu głównego projektu):
python -m adapters.cli.main --help


Komendy
1. Utworzenie konta
python -m adapters.cli.main create-account \
  --owner "Alice" \
  --currency PLN \
  --initial 100.00

2. Wpłata
python -m adapters.cli.main deposit \
  --account-id <ACCOUNT_ID> \
  --amount 50.00 \
  --note "salary"

3. Wypłata
python -m adapters.cli.main withdraw \
  --account-id <ACCOUNT_ID> \
  --amount 20.00 \
  --note "atm"


4. Przelew
python -m adapters.cli.main transfer \
  --from <FROM_ACCOUNT_ID> \
  --to <TO_ACCOUNT_ID> \
  --amount 30.00 \
  --note "rent"

5. Saldo
python -m adapters.cli.main balance \
  --account-id <ACCOUNT_ID>

6. Historia transakcji
python -m adapters.cli.main transactions \
  --account-id <ACCOUNT_ID> \
  --limit 50




