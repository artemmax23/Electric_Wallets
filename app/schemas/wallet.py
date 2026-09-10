"""
Модуль содержит Pydantic-схемы для валидации запросов и ответов по тегам.

Схемы валидации для тегов:
        - WalletBase: Базовая схема с общими полями.
        - WalletCreate: Схема для создания кошелька.
        - WalletUpdate: Схема для полного обновления кошелька.
        - WalletResponse: Схема ответа (с id).
        - WalletBalanceUpdate: Схема для операций пополнения/списания.
"""

from pydantic import BaseModel, ConfigDict
from app.enums import TransactionType

class WalletBase(BaseModel):
    """
    Базовая схема с общими полями для кошелька.
    
    Args:
            - balance: баланс кошелька.
    """
    balance: float
    
class WalletCreate(WalletBase):
    """Схема для создания кошелька."""
    pass

class WalletUpdate(WalletBase):
    """Схема для обновления кошелька."""
    pass    
            
class WalletResponse(WalletBase):
    """
    Схема ответа для кошелька (с id)
    
    Args:
            - id: ID тега.
    """
    id: int
     
    model_config = ConfigDict(from_attributes=True) # Превращает SQLAlchemy-объект в JSON

class WalletBalanceUpdate(BaseModel):
    """Схема обновления баланса кошелька."""
    operation: TransactionType
    amount: float
    