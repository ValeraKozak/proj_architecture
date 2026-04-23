# Платформа Для Дошки Оголошень

Навчальний backend-проєкт для розміщення оголошень, категоризації, модерації контенту та обміну повідомленнями між користувачами.

## Основні можливості
- реєстрація та логін через JWT;
- ролі `user`, `moderator`, `admin`;
- створення й редагування оголошень;
- модерація публікацій;
- повідомлення між користувачами;
- OpenAPI документація через FastAPI;
- unit та integration тести;
- Docker, `docker-compose` і GitHub Actions CI.

## Технологічний стек
- Python 3.11
- FastAPI
- SQLAlchemy 2
- PostgreSQL / SQLite
- PyTest
- Docker

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
  migrations/
  seed/
docs/
  diagrams/
  spec/
```

## Локальний запуск
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e .[dev]
uvicorn src.main:app --reload
```

## Тести
```bash
pytest --cov=src --cov-report=term-missing
```

## Docker
```bash
docker compose up --build
```

## Документація
- [Вимоги](docs/spec/requirements.md)
- [Архітектура](docs/spec/architecture.md)
- [База даних](docs/spec/database.md)
- [Тестування](docs/spec/testing.md)
- [Доменна модель](docs/diagrams/domain-model.md)

## Безпека
- JWT для автентифікації;
- RBAC для модерації та керування категоріями;
- Pydantic валідація;
- ORM для захисту від SQL injection;
- явні перевірки прав доступу в сервісному шарі.
