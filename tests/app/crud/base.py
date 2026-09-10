"""
Общие CRUD операции (дженерики) для работы с базой данных.

Содержит общие функции для создания, чтения, обновления и удаления
объектов. Все функции асинхронны и принимают сессию SQLAlchemy в качестве 
первого аргумента.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
     
async def get_by_id(
        db: AsyncSession, 
        model, 
        obj_id: int
):
    """
    Возвращает объект модели по его ID.
    
    Args:
        db: Асинхронная сессия SQLAlchemy.
        model: Класс модели SQLAlchemy.
        obj_id: ID объекта.
        
    Returns:
         Объект модели или None, если объект не найден.
    """
    query = select(model).where(model.id == obj_id)
    result = await db.execute(query)
    
    return result.scalar_one_or_none()
    
async def create(
        db: AsyncSession, 
        model, 
        obj_data
):
    """
    Создаёт новый объект модели в базе данных.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_data: Словарь с данными для создания объекта.
            
    Returns:
            Созданный объект модели с заполненными полями (id и т.д.)
    """    
    if isinstance(obj_data, dict):
        data = obj_data.copy()
    else:
        data = obj_data.model_dump()
    
    db_obj = model(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj
    
async def update(
        db: AsyncSession, 
        model, 
        obj_id: int, 
        obj_data
):
    """
    Обновляет объект модели по ID.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_id: ID объекта для обновления.
            obj_data: Словарь с полями для обновления.
            
    Returns:
            Обновлённый объект или None, если объект не найден.
    """
    db_obj = await get_by_id(db, model, obj_id)
    
    if not db_obj:
        return None
    
    update_data = obj_data if isinstance(obj_data, dict) else obj_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_obj, key, value)
        
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj
    
async def delete(
        db: AsyncSession, 
        model, 
        obj_id: int
) -> bool:
    """
    Удаляет объект модели по ID.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_id: ID объекта для удаления.
            
    Returns:
            bool: True, если объект был удалён, иначе False
    """
    db_obj = await get_by_id(db, model, obj_id)
    
    if not db_obj:
        return False
        
    await db.delete(db_obj)
    await db.commit()
    
    return True
