from datetime import date
from sqlalchemy import Select, func

from app.dao.base import BaseDAO 
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.hotels.schemas import HotelInfo
from app.hotels.rooms.schemas import SRooms
from app.hotels.rooms.dependencies import remaining_rooms, remaining_rooms_hotels
from app.database import async_session_maker

class HotelDAO(BaseDAO):
    model=Hotels

    @classmethod
    async def find_on_territory(
        cls,
        location: str,
        date_from: date,
        date_to: date
    ):
        async with async_session_maker() as session:
            hotels_in_location = Select(Hotels).where(Hotels.location.match(f"{location}"))
            
            if hotels_in_location is not None:
                local_hotels = await session.execute(hotels_in_location)
                local_hotels =  local_hotels.scalars().all() 

                non_empty_hotels = []
                for hotel in local_hotels:
                    hotel_id = hotel.id
                    quantity = await remaining_rooms_hotels(
                        hotel_id=hotel_id,
                        date_from=date_from,
                        date_to=date_to
                    )
                    if quantity > 0:
                        non_empty_hotels.append(
                            HotelInfo(
                                id=hotel.id,
                                name = hotel.name,
                                location = hotel.location,
                                services = hotel.services,
                                rooms_quantity = hotel.rooms_quantity,
                                image_id = hotel.image_id,
                                rooms_left = quantity,
                            )
                        )

                return non_empty_hotels
    
    @classmethod
    async def get_hotel_rooms(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date
    ):
        async with async_session_maker() as session:
            query = Select(Rooms).where(hotel_id==hotel_id)
            
            hotel_rooms = await session.execute(query)
            hotel_rooms = hotel_rooms.scalars().all()
            
            rooms_schemas = []
            
            for room in hotel_rooms:
                delta_days = date_to - date_from
                rem_rooms = await remaining_rooms(
                    room_id = room.id,
                    date_from = date_from,
                    date_to = date_to
                )
                if rem_rooms > 0:
                    rooms_schemas.append(SRooms(
                        id=room.id,
                        hotel_id=room.hotel_id,
                        name=room.name,
                        description=room.description,
                        price=room.price,
                        services=room.services,
                        quantity=room.quantity,
                        image_id=room.image_id,
                        total_cost= delta_days.days * room.price,
                        rooms_left=rem_rooms,
                    ))
                
            return rooms_schemas