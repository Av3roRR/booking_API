from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, ForeignKey

from app.database import Base

class Rooms(Base):
    __tablename__ = 'rooms'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] 
    description: Mapped[str | None]
    price: Mapped[int]
    services: Mapped[dict | None] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]
    
    booking = relationship("Bookings", back_populates="room")
    hotel = relationship("Hotels", back_populates="room")
    
    def __str__(self) -> str:
        return f"Описание комнаты: {self.description}"