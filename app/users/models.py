from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    
    booking = relationship("Bookings", back_populates="user")
    
    def __str__(self) -> str:
        return f"Пользователь {self.email}"