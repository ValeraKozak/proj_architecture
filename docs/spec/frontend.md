# Frontend User Guide

## Запуск

### Локально
```powershell
uvicorn src.main:app --reload
cd frontend
npm install
npm run dev
```

## Адреси
- frontend: `http://127.0.0.1:5173`
- backend API: `http://127.0.0.1:8000`
- swagger: `http://127.0.0.1:8000/docs`
- MongoDB: `mongodb://localhost:27017`

## Основні сторінки
- `/` — home/showcase
- `/catalog` — публічний каталог
- `/workspace` — логін, профіль, створення оголошень, модерація
- `/errors/400`, `/errors/404`, `/errors/500` — кастомні error scenes

## Демо-сценарій
1. Відкрити `/catalog`
2. Показати пошук, фільтри й сортування
3. Перейти у `/workspace`
4. Увійти під тестовим акаунтом
5. Створити оголошення
6. Перевірити модерацію й оновлення каталогу
