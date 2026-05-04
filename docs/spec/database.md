# База Даних

## Обрано MongoDB
Поточна версія проєкту використовує `MongoDB` як основну базу даних.

## Колекції
- `users`
- `categories`
- `listings`
- `listing_images`
- `messages`
- `counters`

## Ідентифікатори
Зовнішній API зберігає числові `id`. Для цього в MongoDB використовується службова колекція `counters`, яка видає наступний integer id для кожної колекції.

## Індекси
- `users.email` — unique
- `categories.name` — unique
- `listings(status, created_at)` — для каталогу та модерації
- `listing_images(listing_id, position)` — для галерей
- `messages(listing_id, created_at)` — для читання переписок

## Нормалізація
Документна модель комбінує два підходи:
- основні сутності зберігаються окремими колекціями;
- галерея оголошення збирається з `listing_images`, щоб не ламати наявний API і тестові сценарії.

## Тестування
У тестах використовується `mongomock`, тому unit та integration тести не залежать від реального локального MongoDB-сервера.
