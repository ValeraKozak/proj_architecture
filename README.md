# Платформа Для Дошки Оголошень

Навчальний проєкт на `FastAPI` для розміщення оголошень, модерації, категорій і повідомлень між користувачами. Поточна версія використовує `MongoDB` як основну базу даних і зберігає зовнішній API з числовими `id`, щоб не ламати frontend.

## Основні можливості
- JWT-реєстрація та логін
- ролі `user`, `moderator`, `admin`
- створення, редагування і видалення оголошень
- модерація оголошень
- повідомлення між користувачами
- пошук, фільтри й сортування каталогу
- OpenAPI / Swagger
- unit та integration тести
- CI/CD

## Технологічний стек
- Python 3.11
- FastAPI
- MongoDB
- PyMongo
- PyTest + mongomock
- GitHub Actions

## Структура
```text
src/
  controllers/
  services/
  repositories/
  models/
  dto/
tests/
  unit/
  integration/
db/
  seed/
docs/
  diagrams/
  spec/
frontend/
```

## Локальний запуск
```powershell
py -m venv .venv
. .venv\Scripts\Activate.ps1
py -m pip install -e .[dev]
Copy-Item .env.example .env
uvicorn src.main:app --reload
```

Для локального запуску MongoDB має бути доступна за URL з `.env`, наприклад:
```env
APP_DATABASE_URL=mongodb://localhost:27017/bulletin_board
```

Swagger:
- `http://127.0.0.1:8000/docs`

Frontend окремо:
```powershell
cd frontend
npm install
npm run dev
```

## Одинарний запуск
```powershell
.\run.ps1
```

## Тести
```powershell
py -m pytest --cov=src --cov-report=term-missing
```

## Документація
- [Вимоги](docs/spec/requirements.md)
- [Архітектура](docs/spec/architecture.md)
- [База даних](docs/spec/database.md)
- [API](docs/spec/api.md)
- [Frontend User Guide](docs/spec/frontend.md)
- [Deployment](docs/spec/deployment.md)
- [Testing](docs/spec/testing.md)

## Безпека
- JWT для автентифікації
- RBAC для доступу до модерації та керування користувачами
- валідація через Pydantic
- ізоляція persistence-логіки в репозиторіях
- конфігурація через `.env`
