"""
Модуль содержит тесты для проверки API кошельков
"""

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_wallet(client: AsyncClient, created_wallet):
    """Создание кошелька."""                        
    wallet = created_wallet
    assert wallet["balance"] == 1000
    assert "id" in wallet
    
@pytest.mark.asyncio
async def test_get_wallet_by_id(client: AsyncClient, created_wallet):
    """Получение кошелька по ID."""
    wallet_id = created_wallet["id"]
    
    response = await client.get(
            f"/api/v1/wallets/{wallet_id}"
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 1000

@pytest.mark.asyncio
async def test_operation_on_nonexistent_wallet(client: AsyncClient):
    """Операция с несуществующим кошельком."""
    response = await client.post(
        "/api/v1/wallets/9999/operation",
        json={"operation": "DEPOSIT", "amount": 100}
    )
    assert response.status_code == 404
            
@pytest.mark.asyncio
async def test_deposit_balance_correct(client: AsyncClient, created_wallet):
    """Положить деньги на кошелёк по ID."""
    wallet_id = created_wallet["id"]
    
    response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", 
            json={
                "operation": "DEPOSIT",
                "amount": 1000
            }
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 2000
    
@pytest.mark.asyncio
async def test_deposit_balance_with_negative_amount(client: AsyncClient, created_wallet):
    """Попытка пополнить кошелёк отрицательной суммой."""
    wallet_id = created_wallet["id"]
    
    response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", 
            json={
                "operation": "DEPOSIT",
                "amount": -1000
            }
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_deposit_balance_with_zero(client: AsyncClient, created_wallet):
    """Попытка пополнить кошелёк на нулевую сумму."""
    wallet_id = created_wallet["id"]
    
    response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", 
            json={
                "operation": "DEPOSIT",
                "amount": 0
            }
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_withdraw_balance_correct(client: AsyncClient, created_wallet):
    """Снять деньги c кошелька по ID."""
    wallet_id = created_wallet["id"]
    
    response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", 
            json={
                "operation": "WITHDRAW",
                "amount": 500
            }
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 500
    
@pytest.mark.asyncio
async def test_withdraw_balance_all_correct(client: AsyncClient, created_wallet):
    """Снять все деньги с кошелька по ID."""
    wallet_id = created_wallet["id"]
    
    response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", 
            json={
                "operation": "WITHDRAW",
                "amount": 1000
            }
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 0
    
@pytest.mark.asyncio
async def test_withdraw_balance_incorrect(client: AsyncClient, created_wallet):
    """Снять больше денег, чем есть в кошельке по ID."""
    wallet_id = created_wallet["id"]
    
    response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", 
            json={
                "operation": "WITHDRAW",
                "amount": 1500
            }
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_withdraw_from_empty_wallet(client: AsyncClient, empty_wallet):
    """Попытка снять деньги с пустого кошелька."""
    wallet_id = empty_wallet

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation": "WITHDRAW",
            "amount": 100
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"
                        
@pytest.mark.asyncio
async def test_delete_wallet(client: AsyncClient, created_wallet):
    """Удаление кошелька по ID."""
    wallet_id = created_wallet["id"]
    
    response = await client.delete(
            f"/api/v1/wallets/{wallet_id}",
    )
    assert response.status_code == 204
    
    response = await client.get(
            f"/api/v1/wallets/{wallet_id}"
    )
    assert response.status_code == 404
    
    
@pytest.mark.asyncio
async def test_delete_nonexistent_wallet(client: AsyncClient):
    """Попытка удалить несуществующий кошелёк."""
    response = await client.delete("/api/v1/wallets/9999")
    assert response.status_code == 404