
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy import text

from app.database import Base, engine
from app import models
from app.catalog import router as catalog_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SportSpace API",
    description="Online sports facilities booking system",
    version="0.3.0",
    lifespan=lifespan,
)

@app.middleware("http")
async def add_utf8_charset(request: Request, call_next):
    response = await call_next(request)

    content_type = response.headers.get("content-type", "")

    if content_type.startswith("application/json"):
        response.headers["content-type"] = "application/json; charset=utf-8"

    return response

# Підключаємо маршрути каталогу
app.include_router(catalog_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to SportSpace!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected"
    }
