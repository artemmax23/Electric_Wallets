# Electronic Wallet API

REST API для управления кошельками пользователей с поддержкой пополнения, снятия средств и проверки баланса. Проект реализован на FastAPI с асинхронной работой с PostgreSQL.

---

## 📋 Содержание

- [Технологии](#технологии)
- [Возможности API](#возможности-api)
- [Запуск проекта](#запуск-проекта)
- [Запуск через Docker](#запуск-через-docker)
- [Тестирование](#тестирование)
- [Примеры запросов](#примеры-запросов)
- [Структура проекта](#структура-проекта)

---

## 🛠 Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** — асинхронный ORM
- **PostgreSQL** — реляционная база данных
- **Alembic** — миграции
- **Pydantic** — валидация данных
- **Pytest + httpx** — тестирование
- **Docker + Docker Compose** — контейнеризация
- **Uvicorn** — ASGI сервер

---

## ✨ Возможности API

| Метод | Эндпоинт | Описание |
| :--- | :--- | :--- |
| `POST` | `/api/v1/wallets/` | Создание кошелька |
| `GET` | `/api/v1/wallets/{wallet_id}` | Получение баланса кошелька |
| `POST` | `/api/v1/wallets/{wallet_id}/operation` | Пополнение или снятие средств |
| `DELETE` | `/api/v1/wallets/{wallet_id}` | Удаление кошелька |

**Валидация:**
- Нельзя снять больше, чем есть на балансе.
- Сумма операции должна быть положительной.
- Нельзя создать кошелёк с отрицательным балансом.

---

## 🚀 Запуск проекта

### Локально (без Docker)

1. **Клонируй репозиторий:**
```bash
git clone https://github.com/artemmax23/Electric_Wallets.git
cd Electric_Wallets
```

2. Создай и активируй виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. Установи зависимости:

```bash
pip install -r requirements.txt
```

4. Создай файл .env в корне проекта:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=wallet_db
DB_USER=postgres
DB_PASSWORD=postgres
```

5. Создай базу данных и примени миграции:

```bash
createdb wallet_db -U postgres
alembic upgrade head
```

6. Запусти сервер:

```bash
uvicorn app.main:app --reload
```

7. Открой документацию:
      Swagger: http://localhost:8000/docs
      ReDoc: http://localhost:8000/redoc

---

🐳 Запуск через Docker

1. Убедись, что установлены Docker и Docker Compose.
2. Собери и запусти контейнеры:

```bash
docker-compose up --build
```

3. Примени миграции (внутри контейнера):

```bash
docker-compose exec app alembic upgrade head
```

4. API доступно: http://localhost:8000
      Swagger: http://localhost:8000/docs

---

🧪 Тестирование

Запуск всех тестов:

```bash
pytest -v
```

Запуск конкретного файла:

```bash
pytest tests/test_wallets.py -v
```

Что покрыто тестами:

· Создание кошелька
· Получение баланса по ID
· Пополнение (успех, ошибки)
· Снятие (успех, ошибки, недостаток средств)
· Удаление кошелька
· Операции с несуществующими кошельками

---

📝 Примеры запросов

Создать кошелёк

```http
POST /api/v1/wallets/
Content-Type: application/json

{
    "balance": 0
}
```

Получить баланс

```http
GET /api/v1/wallets/1
```

Пополнить кошелёк

```http
POST /api/v1/wallets/1/operation
Content-Type: application/json

{
    "operation": "DEPOSIT",
    "amount": 1000
}
```

Снять средства

```http
POST /api/v1/wallets/1/operation
Content-Type: application/json

{
    "operation": "WITHDRAW",
    "amount": 500
}
```

Удалить кошелёк

```http
DELETE /api/v1/wallets/1
```

---

📁 Структура проекта

```
Electric_Wallets/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── config.py            # Настройки (pydantic-settings)
│   ├── database.py          # Подключение к БД
│   ├── models.py            # SQLAlchemy модели (Wallet)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── wallet.py        # Pydantic схемы
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py          # Дженерики CRUD
│   │   └── wallet.py        # CRUD для кошельков
│   ├── routers/
│   │   ├── __init__.py
│   │   └── wallets.py       # Эндпоинты
│   └── enums.py             # TransactionType
├── migrations/              # Alembic миграции
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Фикстуры
│   └── test_wallets.py      # Тесты
├── .env                     # Переменные окружения
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

---

👨‍💻 Автор

Артём Золотарев
GitHub: @artemmax23
