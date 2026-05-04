# Розгортання

## Локально
1. Створити `.env` на основі `.env.example`
2. Запустити MongoDB локально або через Docker
3. Підняти API:
   `uvicorn src.main:app --reload`
4. Підняти frontend:
   `cd frontend && npm run dev`

## Docker Compose
```powershell
docker compose up --build
```

Stack:
- `db` — MongoDB
- `api` — FastAPI
- `frontend` — production build через `nginx`

## CI/CD
- `CI` запускає lint і тести
- окремий `mongodb-smoke` job перевіряє bootstrap Mongo-підходу

## Змінні середовища
Основна змінна:
```env
APP_DATABASE_URL=mongodb://db:27017/bulletin_board
```
