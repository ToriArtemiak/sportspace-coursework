
from pydantic import BaseModel, ConfigDict


class SportsCenterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    address: str


class SportsHallRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    capacity: int
    sport_center_id: int
    center: SportsCenterRead


class TrainerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    specialization: str
    experience_years: int


class SportsSectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sport_type: str
    level: str
    min_age: int
    max_age: int
    capacity: int
    price_uah: int

    hall: SportsHallRead
    trainer: TrainerRead
