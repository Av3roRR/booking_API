from datetime import date
from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.tasks.tasks import email_booking_confirm
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked, NonCorrectDates

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    if booking is None:
        raise RoomCannotBeBooked
    
    if date_from <= date_to:    
        booking_dict = TypeAdapter(SBooking).validate_python(booking).model_dump()
        email_booking_confirm.delay(booking_dict, user.email)
        return booking_dict
    else:
        raise NonCorrectDates


@router.delete("/{id}")
async def delete(
    id: int,
    user_bookings: list[SBooking] = Depends(get_bookings)
):
    message = await BookingDAO.delete_booking(booking_id=id, user_bookings=user_bookings)
    return message
