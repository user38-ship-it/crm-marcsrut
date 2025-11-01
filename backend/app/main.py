from fastapi import FastAPI

from app import models  # noqa: F401
from app.api.routes import auth as auth_routes
from app.api.routes import survey as survey_routes
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

settings = get_settings()

app = FastAPI(title=settings.project_name)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(auth_routes.router)
app.include_router(survey_routes.router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
