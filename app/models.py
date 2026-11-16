
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SportsCenter(Base):
    __tablename__ = "sports_centers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(120), nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(80), nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(180), nullable=False
    )
