from datetime import date
from fastapi import APIRouter

from app.hotels.hotels_dao import HotelDAO
from app.hotels.schemas import HotelInfo
from app.exceptions import NonCorrectDates

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
async def get_all_hotels_by_location_and_time(
    location: str,
    date_from: date,
    date_to: date
) -> list[HotelInfo]:
    if date_from < date_to and (date_to - date_from).days < 31:    
        all_hotels = await HotelDAO.find_on_territory(
            location=location,
            date_from=date_from,
            date_to=date_to
        )
        
        return all_hotels
    else:
        raise NonCorrectDates


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date
):
    hotel_rooms = await HotelDAO.get_hotel_rooms(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )
    
    return hotel_rooms

@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    return await HotelDAO.find_by_id(model_id=hotel_id)