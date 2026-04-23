# API Та OpenAPI

## Базові ресурси
- `POST /auth/register`
- `POST /auth/login`
- `GET /users/me`
- `PATCH /users/me`
- `GET /users`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`
- `POST /categories`
- `GET /categories`
- `GET /categories/{category_id}`
- `PUT /categories/{category_id}`
- `DELETE /categories/{category_id}`
- `POST /listings`
- `PUT /listings/{listing_id}`
- `GET /listings`
- `GET /listings/me/owned`
- `GET /listings/{listing_id}`
- `DELETE /listings/{listing_id}`
- `GET /listings/moderation/pending`
- `POST /moderation/listings/{listing_id}`
- `POST /messages`
- `GET /messages/me`
- `GET /messages/{message_id}`
- `DELETE /messages/{message_id}`
- `GET /health`

## OpenAPI
- Swagger UI доступний за адресою `/docs`
- ReDoc доступний за адресою `/redoc`
- FastAPI автоматично генерує схему OpenAPI на `/openapi.json`

## HTTP статуси
- `200 OK`: успішне читання, оновлення або видалення
- `201 Created`: успішне створення ресурсу
- `400 Bad Request`: невалідний бізнес-сценарій
- `401 Unauthorized`: відсутній або невалідний токен
- `403 Forbidden`: недостатньо прав
- `404 Not Found`: ресурс не знайдено
- `409 Conflict`: дубльований або конфліктний стан ресурсу

## Аутентифікація
- Bearer JWT токен передається в заголовку `Authorization`
- ролі доступу: `user`, `moderator`, `admin`
