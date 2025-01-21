from sqlalchemy import JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship


from app.database import Base


class Hotels(Base):
    __tablename__ = 'hotels'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[dict | None] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int | None]
    
    room = relationship("Rooms", back_populates="hotel")
    
    def __str__(self) -> str:
        return f"Отель {self.name[:30]}"

