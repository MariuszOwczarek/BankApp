from enum import Enum

class AccountStatus(Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'
    CLOSED = 'CLOSED'

    def __str__(self):
        return self.value