"""
Модуль содержит модели таблиц базы данных

Зависимости:
        - Base: базовая модель для таблицы базы данных
        
Модели:
        - Wallet: Модель таблицы для кошелька.
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Integer, Float, ForeignKey
from app.database import Base

class Wallet(Base):
    """
    Модель таблицы для кошелька
    
    Args:
            - id: ID кошелька.
            - balance: Баланс кошелька.
    """
    
    __tablename__ = "wallets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    balance: Mapped[float] = mapped_column(nullable=False, default=0.0)
