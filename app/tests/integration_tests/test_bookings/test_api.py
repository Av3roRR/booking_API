from httpx import AsyncClient
import pytest

from app.bookings.dao import BookingDAO

@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", *[
    [(4, "2030-05-01", "2030-05-15", i, 200) for i in range(3, 11)] +
    [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
])
async def test_add_and_get_booking(room_id, date_from, date_to,
                                   status_code, booked_rooms,
                                   authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": 4,
        "date_from": "2030-05-01",
        "date_to": "2030-05-15"
    })
    
    assert response.status_code == status_code
    
    response = await authenticated_ac.get("/bookings")
    
    assert len(response.json()) == booked_rooms
    
    
@pytest.mark.parametrize("user_id,booking_id,status_code", [
    (1, 1, 200)
])
async def test_get_and_delete_booking(user_id, booking_id, status_code,
                                      authenticated_ac: AsyncClient):
    user_bookings = await authenticated_ac.get("/bookings")
    
    assert user_bookings.status_code == status_code
    
    for booking in user_bookings.json():
        await authenticated_ac.delete(f"/bookings/{booking['id']}")
    
    user_bookings = await authenticated_ac.get("/bookings")
    
    assert len(user_bookings.json()) == 0