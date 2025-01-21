from fastapi import APIRouter

from app.hotels.rooms.rooms_dao import RoomDAO

router = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router.get("")
async def get_all_rooms():
    booked_rooms = await RoomDAO.find_all()
    return booked_rooms


@router.post("/add")
async def set_new_room(
    hotel_id: int,
    name: str,
    description: str,
    price: int,
    services: str,
    quantity: int,
    image_id: int
):
    services = [el for el in services.split(", ")]
    await RoomDAO.add(
        hotel_id = hotel_id,
        name = name,
        description = description,
        price = price,
        services = services,
        quantity = quantity,
        image_id = image_id
    )
    
    
@router.post("/update")
async def update_room(room_id: int, field: str, data):
    updated_room = await RoomDAO.update(id=room_id, field=field, data=data)
    
    print(updated_room)

@router.delete("/delete")
async def delete_room(room_id: int):
    await RoomDAO.delete(room_id)