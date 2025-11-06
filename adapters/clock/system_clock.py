from domain.ports.ports import Clock
from datetime import datetime, timezone

class SystemClock(Clock):
    def now(self):
        """Zwraca bieżący czas UTC."""
        return datetime.now(timezone.utc)