from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker

async def remaining_rooms(
    room_id: int,
    date_from: date,
    date_to: date
):
    booked_rooms = select(Bookings).where(
            and_(
                Bookings.room_id == room_id,
                and_(
                    Bookings.date_from <= date_to,
                    Bookings.date_to >= date_from
                )
            )
        ).cte("booked_rooms")
        
    get_rooms_left = select(
        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
        ).select_from(Rooms).outerjoin(
            booked_rooms, booked_rooms.c.room_id == Rooms.id
        ).where(Rooms.id == room_id).group_by(
            Rooms.quantity, booked_rooms.c.room_id
        )
        
    async with async_session_maker() as session:
        rooms_left = await session.execute(get_rooms_left)
        rooms_left: int = rooms_left.scalar()
        
        return rooms_left


async def remaining_rooms_hotels(
    hotel_id: int,
    date_from: date,
    date_to: date
):
    async with async_session_maker() as session:
        query = select(Rooms).where(Rooms.hotel_id == hotel_id)
        hotel_rooms = await session.execute(query)
        hotel_rooms = hotel_rooms.scalars().all()
        
        quantity = 0        
        for room in hotel_rooms:
            quantity += await remaining_rooms(
                room_id=room.id,
                date_from=date_from,
                date_to=date_to
            )
        
        return quantity