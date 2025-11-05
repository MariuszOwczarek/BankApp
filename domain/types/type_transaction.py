from enum import Enum

class TransactionType(Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    TRANSFER_IN = 'TRANSFER_IN'
    TRANSFER_OUT = 'TRANSFER_OUT'

    def __str__(self):
        return self.value