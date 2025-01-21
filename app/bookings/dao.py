from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from datetime import date

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.bookings.schemas import SBooking
from app.hotels.rooms.dependencies import remaining_rooms
from app.logger import logger


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from <= '2023-06-20' AND date_to >= '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:

                rooms_left = await remaining_rooms(
                    room_id=room_id, date_from=date_from, date_to=date_to
                )

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                msg = "Database exc"
            elif isinstance(err, Exception):
                msg = "Unknown exc"
            
            msg += ": can't add booking"
            
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            
            logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def delete_booking(cls, booking_id: int, user_bookings: list[SBooking]):
        async with async_session_maker() as session:
            if booking_id in [book.id for book in user_bookings]:
                query = delete(Bookings).where(Bookings.id == booking_id)
                if query is not None:

                    await session.execute(query)
                    await session.commit()

                    return "Удаление прошло успешно"
