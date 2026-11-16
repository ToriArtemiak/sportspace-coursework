
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Створюємо таблиці, якщо їх ще немає
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SportSpace API",
    description="Online sports facilities booking system",
    version="0.2.0",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SportSpace!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    # Перевіряємо підключення до бази даних
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected"
    }
