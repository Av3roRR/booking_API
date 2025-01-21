from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date | None]
    date_to: Mapped[date | None]
    price: Mapped[int | None]
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price")) 
    total_days: Mapped[int] = mapped_column(Computed("(date_to - date_from)"))

    user = relationship("Users", back_populates="booking")
    room = relationship("Rooms", back_populates="booking")

    def __str__(self) -> str:
        return f"Бронь #{self.id}"
