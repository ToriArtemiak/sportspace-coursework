
from pydantic import BaseModel, ConfigDict, EmailStr, Field


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


# Дані, які вводить користувач
class UserCreate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=120
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


# Дані, які сервер повертає користувачу
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
