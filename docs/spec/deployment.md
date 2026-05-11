# Розгортання

## Локально
1. Створити `.env` на основі `.env.example`
2. Запустити MongoDB локально
3. Підняти API:
   `uvicorn src.main:app --reload`
4. Підняти frontend:
   `cd frontend && npm run dev`

## CI/CD
- `CI` запускає lint і тести
- окремий `mongodb-smoke` job перевіряє bootstrap Mongo-підходу

## Змінні середовища
Основна змінна:
```env
APP_DATABASE_URL=mongodb://localhost:27017/bulletin_board
```
