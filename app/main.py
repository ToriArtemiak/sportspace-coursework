
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy import text

from app.database import Base, engine
from app import models
from app.catalog import router as catalog_router

from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

APP_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=APP_DIR / "static"),
    name="static"
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


@app.get("/", response_class=FileResponse)
def home():
    return FileResponse(
        APP_DIR / "templates" / "index.html"
    )

@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected"
    }
