
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Адреса локальної бази даних SQLite
DATABASE_URL = "sqlite:///./sportspace.db"

# Створення підключення до бази
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Фабрика сесій для роботи з даними
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False
)

# Базовий клас для всіх моделей
class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as session:
        yield session