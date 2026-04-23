from fastapi import FastAPI

from src.controllers import auth, categories, listings, messages, moderation
from src.db.database import Base, engine


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    application = FastAPI(
        title="Bulletin Board Platform",
        version="0.1.0",
        description=(
            "REST API for managing listings, categories, moderation workflows "
            "and messages."
        ),
    )
    application.include_router(auth.router)
    application.include_router(categories.router)
    application.include_router(listings.router)
    application.include_router(messages.router)
    application.include_router(moderation.router)
    return application


app = create_app()


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
