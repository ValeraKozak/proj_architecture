# База Даних

## Вибір технології
Обрано SQL-підхід із PostgreSQL як основною цільовою БД. Причини:
- природні зв'язки між користувачами, категоріями, оголошеннями та повідомленнями;
- потрібна транзакційність для модерації та обміну повідомленнями;
- схема добре нормалізується і зручна для ORM.

Для локального швидкого запуску та тестів дозволено SQLite.

## Основні сутності
- `users`
- `categories`
- `listings`
- `messages`

## Нормалізація
- Категорії винесено в окрему таблицю.
- Повідомлення не дублюють дані користувачів або оголошень, а посилаються на них через FK.
- Статус модерації зберігається на рівні оголошення.

## ER-структура
- `users (1) -> (N) listings`
- `categories (1) -> (N) listings`
- `listings (1) -> (N) messages`
- `users (1) -> (N) messages` як `sender`
- `users (1) -> (N) messages` як `recipient`

## DTO
- `UserCreateDTO`, `UserLoginDTO`
- `UserUpdateDTO`, `UserAdminUpdateDTO`
- `CategoryCreateDTO`
- `CategoryUpdateDTO`
- `ListingCreateDTO`, `ListingUpdateDTO`
- `ModerationDecisionDTO`
- `MessageCreateDTO`

## Міграції
Початкова SQL-міграція знаходиться в `db/migrations/001_initial_schema.sql`.

## Локальна та контейнерна БД
- Для unit/integration тестів використовується SQLite in-memory.
- Для контейнерного та наближеного до production запуску використовується PostgreSQL.
