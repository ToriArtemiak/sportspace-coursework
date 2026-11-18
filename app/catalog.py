
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import SessionLocal
from app.models import (
    SportsCenter,
    SportsHall,
    Trainer,
    SportsSection,
)
from app.schemas import (
    SportsCenterRead,
    SportsHallRead,
    TrainerRead,
    SportsSectionRead,
)


router = APIRouter(
    prefix="/api",
    tags=["Sports Catalog"]
)


# Підключення до бази даних для кожного запиту
def get_db():
    with SessionLocal() as session:
        yield session


# Список спортивних центрів
@router.get("/centers", response_model=list[SportsCenterRead])
def get_centers(db: Session = Depends(get_db)):
    statement = select(SportsCenter).order_by(SportsCenter.id)
    return db.scalars(statement).all()


# Список спортивних залів
@router.get("/halls", response_model=list[SportsHallRead])
def get_halls(db: Session = Depends(get_db)):
    statement = (
        select(SportsHall)
        .options(joinedload(SportsHall.center))
        .order_by(SportsHall.id)
    )
    return db.scalars(statement).all()


# Список тренерів
@router.get("/trainers", response_model=list[TrainerRead])
def get_trainers(db: Session = Depends(get_db)):
    statement = select(Trainer).order_by(Trainer.id)
    return db.scalars(statement).all()


# Секції з можливістю фільтрації
@router.get("/sections", response_model=list[SportsSectionRead])
def get_sections(
    sport_type: str | None = None,
    level: str | None = None,
    max_price: int | None = Query(default=None, ge=0),
    age: int | None = Query(default=None, ge=0, le=120),
    db: Session = Depends(get_db),
):
    statement = select(SportsSection).options(
        joinedload(SportsSection.hall).joinedload(SportsHall.center),
        joinedload(SportsSection.trainer),
    )

    if sport_type:
        statement = statement.where(
            SportsSection.sport_type == sport_type
        )

    if level:
        statement = statement.where(
            SportsSection.level == level
        )

    if max_price is not None:
        statement = statement.where(
            SportsSection.price_uah <= max_price
        )

    if age is not None:
        statement = statement.where(
            SportsSection.min_age <= age,
            SportsSection.max_age >= age,
        )

    statement = statement.order_by(SportsSection.id)

    return db.scalars(statement).all()


# Отримання однієї секції за ID
@router.get(
    "/sections/{section_id}",
    response_model=SportsSectionRead
)
def get_section(
    section_id: int,
    db: Session = Depends(get_db),
):
    statement = (
        select(SportsSection)
        .options(
            joinedload(SportsSection.hall).joinedload(SportsHall.center),
            joinedload(SportsSection.trainer),
        )
        .where(SportsSection.id == section_id)
    )

    section = db.scalar(statement)

    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Sports section not found"
        )

    return section
