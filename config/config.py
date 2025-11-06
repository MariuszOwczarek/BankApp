from pathlib import Path
import os

# zawsze wróć do katalogu projektu (w aplikacji bank)
BASE_DIR = Path(__file__).resolve().parents[1]

# folder z danymi obok paczki, nie w niej
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SQLITE_PATH = Path(os.getenv("BANK_SQLITE_PATH", DATA_DIR / "bank.db"))