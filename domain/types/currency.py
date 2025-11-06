from enum import Enum

class CurrencyType(Enum):
    PLN = 'PLN'
    EUR = 'EUR'

    def __str__(self):
        return self.value
