# Розгортання Та CI/CD

## Docker Compose
1. Скопіювати `.env.example` у `.env`
2. Заповнити безпечні значення для `APP_SECRET_KEY` і паролів БД
3. Виконати `docker compose up --build`
4. Перевірити `http://localhost:8000/health`
5. Відкрити `http://localhost:8000/docs`

`.env.example` уже налаштований для Docker Compose через
`postgresql+psycopg://postgres:postgres@db:5432/bulletin_board`.
Для локального запуску без Docker слід використовувати SQLite-URL.
Frontend у контейнерному режимі збирається у production bundle і віддається через `nginx`.
`nginx` також проксіює `/api/` запити до backend-сервісу.

## CI
GitHub Actions workflow:
- інсталює залежності;
- запускає `ruff check .`;
- запускає `pytest`;
- генерує `coverage.xml` і `pytest-report.xml`;
- зберігає звіти як артефакти;
- окремо піднімає PostgreSQL service і перевіряє застосування SQL-міграцій.

## CD
У репозиторії реалізовано окремий CD workflow:
- push у `main` запускає публікацію Docker-образу;
- образ публікується в `ghcr.io/<owner>/<repo>/bulletin-board-platform`;
- workflow також можна запустити вручну через `workflow_dispatch`.

## Політика гілок
- `main`: стабільний код
- `feature/*`: розробка нових функцій
- `fix/*`: виправлення помилок
- merge у `main` лише після зеленого CI

## Секрети
- не зберігати справжні токени або production-паролі в git;
- використовувати `.env` локально та GitHub Secrets у CI/CD;
- регулярно змінювати `APP_SECRET_KEY` у production.
