import pytest

from app.bookings.dao import BookingDAO

from datetime import date, datetime

async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d")
    )
    
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2
    
    new_booking = await BookingDAO.find_by_id(new_booking.id)
    
    assert new_booking is not None


async def test_crud_operations():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-04-03", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-04-17", "%Y-%m-%d")
    )
    
    assert new_booking is not None
    
    my_booking = await BookingDAO.find_by_id(new_booking.id)
    
    assert my_booking is not None

    await BookingDAO.delete(my_booking.id)

    check_booking = await BookingDAO.find_one_or_none(id=new_booking.id, user_id=2)
    
    assert check_booking is None