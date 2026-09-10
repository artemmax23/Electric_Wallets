"""
Специализированные CRUD операции для кошельков (Wallet).

Содержит функции для создания, чтения, обновления и удаления
кошельков (Wallet). Все функции асинхронны и принимают сессию SQLAlchemy 
в качестве первого аргумента.

Зависимости:
        - models: Модели таблиц.
        - schemas: Pydantic-схемы для валидации.
        - crud: CRUD операции. Нужен для дженериков.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.crud import base
    
async def get_wallet(
        db: AsyncSession, 
        wallet_id: int, 
) -> models.Wallet | None:
    """Возвращает объект кошелька по ID или None."""
    return await base.get_by_id(db, models.Wallet, wallet_id)
    
async def create_wallet(
        db: AsyncSession, 
        wallet: schemas.WalletCreate
) -> models.Wallet:
    """Создаем кошелёк"""
    return await base.create(db, models.Wallet, wallet)
    
async def update_wallet(
        db: AsyncSession, 
        wallet_id: int, 
        wallet_update: schemas.WalletUpdate | dict,
) -> models.Wallet | None:
    """Обновляет кошелёк по ID. Принимает схему или словарь"""
    return await base.update(db, models.Wallet, wallet_id, wallet_update)
    
async def delete_wallet(
        db: AsyncSession,
        wallet_id: int
 ) -> bool:
    """Удаляет кошелёк по ID."""
    return await base.delete(db, models.Wallet, wallet_id)
