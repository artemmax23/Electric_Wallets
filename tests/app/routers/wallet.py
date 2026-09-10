"""
Маршруты (роутеры) для работы с кошельками

Предоставляет набор эндпоинтов для управления кошельками
- Создание (POST /api/v1/wallets/)
- Получение баланса кошелька по ID (GET /api/v1/wallets/{wallet_id})
- Обновление баланса кошелька(POST /api/v1/wallets/{wallet_id}/operations)
- Удаление (DELETE /api/v1/wallets/{wallet_id})

Все эндпоинты используют асинхронные сессии SQLAlchemy и валидацию через Pydantic
Автоматическая документация доступна в Swagger (/docs) и ReDoc (/redoc)

Зависимости:
        - get_db: внедряет асинхронную сессию базы данных.
        - crud: функции для работы с базой данных.
        - schemas: Pydantic-схемы для валидации запросов и ответов.
        
Пример:
        >>> # Создать кошелёк
        >>> POST /api/v1/wallets
        >>> {
        ...           "balance": 0,
        ...    }
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.database import get_db
from app.enums import TransactionType

router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])

@router.post(
        "/",
        response_model=schemas.WalletResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Создание кошелька"
)
async def create_wallet(
        wallet: schemas.WalletCreate,
        db: AsyncSession=Depends(get_db),
):
    """
    Создание кошелька.
    
    Args:
            - tag: Pydantic-схема с данными для создания кошелька (balance).
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.WalletResponse: Созданный кошелёк с полем id.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.                   
                                                                          
    Example:
            ```http
            POST /api/v1/wallets
            Content-Type: application/json
            
            {
                "balance": 0
            }
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "balance": 0
            }
            ```
    """
    return await crud.create_wallet(db, wallet)
            
@router.get(
        "/{wallet_id}",
        response_model=schemas.WalletResponse,
        summary="Получение баланса кошелька по id"
)  
async def get_balance(
        wallet_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Получение баланса кошелька по ID.
    
    Args:
            - wallet_id: ID кошелька.
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.WalletResponse: Кошелька с соответствующим ID.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если тега с указанным ID не существует в базе данных.                   
                                                                          
    Example:
            ```http
            GET /api/v1/wallets/1
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "balance": 0
            }
            ```
    """
    
    wallet = await crud.get_wallet(db, wallet_id)
   
    # Проверка существования кошелька
    if not wallet:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet with id {wallet_id} not found"
        )
    
    return wallet
    
@router.post(
        "/{wallet_id}/operation",
        response_model=schemas.WalletResponse,
        summary="Обновление баланса кошелька"
)
async def update_wallet_balance(
        wallet_id: int,
        wallet_data: schemas.WalletBalanceUpdate,
        db: AsyncSession = Depends(get_db)
):
    """
    Обновление баланса кошелька.
    
    Args:
            - wallet_id: ID кошелька для изменения.
            - wallet_data: Pydantic-схема с данными для обновления баланса кошелька (balance).
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.WalletResponse: Кошелёк с обновлённым балансом и с полем id.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если задача с указанным ID не существует в базе данных.                  
                                                                          
    Example:
            ```http
            POST /api/v1/wallets/1/operations
            Content-Type: application/json
            
             {
                "operation": "DEPOSIT",
                "amount": 1000
             }
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "balance": 1000
            }
            ```
    """
    if wallet_data.amount < 1:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Amount must be positive"
    
    wallet = await crud.get_wallet(db, wallet_id)
    
    # Проверка кошелька на существование
    if not wallet:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet with id {wallet_id} not found"
        )
    
    # Прооводим операцию с кошельком
    if wallet_data.operation == TransactionType.DEPOSIT:
        wallet.balance += wallet_data.amount
    else:
        if wallet.balance >= wallet_data.amount:
            wallet.balance -= wallet_data.amount
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient balance"
        )   
    
    wallet_update = schemas.WalletUpdate(
        balance=wallet.balance
    )         
                                        
    wallet = await crud.update_wallet(db, wallet_id, wallet_update)
        
    return wallet
    
@router.delete(
        "/{wallet_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Удалить кошелёк"
)
async def delete_wallet(
        wallet_id: int,
        db: AsyncSession=Depends(get_db)
):
    """
    Удаление кошелька.
    
    Args:
            - wallet_id: ID кошелька для изменения.
            - db: Асинхронная сессия SQLAlchemy.     
     
     Returns:
             None: При успешном выполнении возвращается статус 204 No Content.
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если кошелёк с указанным ID не существует в базе данных.     
                                                                          
    Example:
            ```http
            DELETE /api/v1/wallets/1
            ```
    Response:
            ```http
            HTTP/1.1 204 No Content
            ```
    """
    deleted = await crud.delete_wallet(db, wallet_id) 
    
    if not deleted:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet with id {wallet_id} not found"
        )
        
    return None