# Розгортання Та CI/CD

## Docker Compose
1. Скопіювати `.env.example` у `.env`
2. Заповнити безпечні значення для `APP_SECRET_KEY` і паролів БД
3. Виконати `docker compose up --build`
4. Перевірити `http://localhost:8000/health`
5. Відкрити `http://localhost:8000/docs`

## CI
GitHub Actions workflow:
- інсталює залежності;
- запускає `ruff check .`;
- запускає `pytest`;
- генерує `coverage.xml` і `pytest-report.xml`;
- зберігає звіти як артефакти.

## CD
У навчальному репозиторії реалізовано основу для CD:
- стабільна гілка `main`;
- автоматична перевірка якості на `push` і `pull_request`;
- контейнеризований спосіб запуску, готовий до розгортання на VPS або PaaS.

## Політика гілок
- `main`: стабільний код
- `feature/*`: розробка нових функцій
- `fix/*`: виправлення помилок
- merge у `main` лише після зеленого CI

## Секрети
- не зберігати справжні токени або production-паролі в git;
- використовувати `.env` локально та GitHub Secrets у CI/CD;
- регулярно змінювати `APP_SECRET_KEY` у production.
