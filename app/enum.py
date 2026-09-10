from enum import Enum

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"