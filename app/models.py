
from sqlalchemy import String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# Спортивний центр
class SportsCenter(Base):
    __tablename__ = "sports_centers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    address: Mapped[str] = mapped_column(String(180), nullable=False)

    halls: Mapped[list["SportsHall"]] = relationship(
        back_populates="center"
    )


# Спортивний зал
class SportsHall(Base):
    __tablename__ = "sports_halls"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)

    sport_center_id: Mapped[int] = mapped_column(
        ForeignKey("sports_centers.id"),
        nullable=False
    )

    center: Mapped["SportsCenter"] = relationship(
        back_populates="halls"
    )

    sections: Mapped[list["SportsSection"]] = relationship(
        back_populates="hall"
    )

    __table_args__ = (
        CheckConstraint("capacity > 0", name="hall_capacity_positive"),
    )


# Тренер
class Trainer(Base):
    __tablename__ = "trainers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    specialization: Mapped[str] = mapped_column(
        String(80), nullable=False
    )
    experience_years: Mapped[int] = mapped_column(default=0)

    sections: Mapped[list["SportsSection"]] = relationship(
        back_populates="trainer"
    )

    __table_args__ = (
        CheckConstraint(
            "experience_years >= 0",
            name="trainer_experience_nonnegative"
        ),
    )


# Спортивна секція
class SportsSection(Base):
    __tablename__ = "sports_sections"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    sport_type: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[str] = mapped_column(String(30), nullable=False)
    min_age: Mapped[int] = mapped_column(default=6)
    max_age: Mapped[int] = mapped_column(default=80)
    capacity: Mapped[int] = mapped_column(nullable=False)
    price_uah: Mapped[int] = mapped_column(nullable=False)

    hall_id: Mapped[int] = mapped_column(
        ForeignKey("sports_halls.id"),
        nullable=False
    )

    trainer_id: Mapped[int] = mapped_column(
        ForeignKey("trainers.id"),
        nullable=False
    )

    hall: Mapped["SportsHall"] = relationship(
        back_populates="sections"
    )

    trainer: Mapped["Trainer"] = relationship(
        back_populates="sections"
    )

    __table_args__ = (
        CheckConstraint("capacity > 0", name="section_capacity_positive"),
        CheckConstraint("min_age >= 0", name="section_min_age_valid"),
        CheckConstraint("max_age >= min_age", name="section_age_range_valid"),
        CheckConstraint("price_uah >= 0", name="section_price_nonnegative"),
    )


# Користувач системи
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="client",
        nullable=False
    )
