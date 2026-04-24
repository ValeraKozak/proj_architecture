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
copy .env.example .env
uvicorn src.main:app --reload
```

Для локального запуску без Docker заміни `APP_DATABASE_URL` у `.env` на:
```env
APP_DATABASE_URL=sqlite:///./bulletin_board.db
```

Для Docker Compose залишай PostgreSQL-URL з драйвером `postgresql+psycopg://...`.

## Frontend запуск
```bash
cd frontend
npm install
npm run dev
```

Frontend dev server очікує backend на `http://127.0.0.1:8000` і за замовчуванням запускається на `http://127.0.0.1:5173`.

## Тести
```bash
pytest --cov=src --cov-report=term-missing
```

## Docker
```bash
copy .env.example .env
docker compose up --build
```

Під час контейнерного запуску застосунок автоматично виконує SQL-міграції з `db/migrations/`.

## Документація
- [Вимоги](docs/spec/requirements.md)
- [Архітектура](docs/spec/architecture.md)
- [База даних](docs/spec/database.md)
- [API та OpenAPI](docs/spec/api.md)
- [Розгортання та CI/CD](docs/spec/deployment.md)
- [Тестування](docs/spec/testing.md)
- [Доменна модель](docs/diagrams/domain-model.md)
- [Use Case Diagram](docs/diagrams/use-case-diagram.mmd)
- [ER Diagram](docs/diagrams/er-diagram.mmd)
- [Class Diagram](docs/diagrams/class-diagram.mmd)
- [Фінальна презентація](docs/presentation/final-presentation-notes.md)

## API
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- healthcheck: `/health`

## Розгалуження
- `main`: стабільна гілка, готова до демонстрації або релізу.
- feature branches: окремі гілки під задачі, наприклад `feature/full-crud`.
- pull request: злиття в `main` після проходження CI.

## Розгортання
1. Створити `.env` на основі `.env.example`.
2. Переконатися, що Docker і Docker Compose доступні.
3. Запустити `docker compose up --build`.
4. Відкрити `http://localhost:8000/docs`.
5. Для продакшн-середовища замінити `APP_SECRET_KEY` і паролі БД.
6. Після push у `main` CD workflow публікує контейнер у GitHub Container Registry.

## Безпека
- JWT для автентифікації;
- RBAC для модерації та керування категоріями;
- Pydantic валідація;
- ORM для захисту від SQL injection;
- явні перевірки прав доступу в сервісному шарі;
- `.env` для секретів і середовищних налаштувань;
- структуроване логування HTTP-запитів.
