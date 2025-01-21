from datetime import datetime
from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
import csv
from io import StringIO

from typing import Literal

from app.bookings.dao import BookingDAO
from app.hotels.hotels_dao import HotelDAO
from app.hotels.rooms.rooms_dao import RoomDAO
from app.hotels.schemas import HotelInfoToAdd
from app.users.models import Users

from app.exceptions import NonCorrectData, NonCorrectFileType
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/importer",
    tags=["Вставка"]
)

@router.get("/info")
def info():
    return "привет"

@router.post("/import/hotel")
async def import_hotel(table_name: Literal["Hotels", "Rooms", "Bookings"], 
                       file: UploadFile, 
                       current_user: Users =  Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован")
    if not file.filename.endswith(".csv"):
        raise NonCorrectFileType
    file = file.file.read().decode("utf-8")
    csv_file = StringIO(file)
    reader = csv.reader(csv_file)
    for data in reader:
        try:
            if table_name == "Hotels":
                name, location, services, rooms_quantity, image_id = data
                services = services.split(", ")
                result = await HotelDAO.add(
                    name=name,
                    location=location,
                    services=services,
                    rooms_quantity=int(rooms_quantity),
                    image_id=int(image_id),
                )
            elif table_name == "Rooms":
                hotel_id, name, description, price, services, quantity, image_id = data
                services = services.split(", ")
                print(
                    hotel_id,
                    name,
                    description,
                    price,
                    services,
                    quantity,
                    image_id
                )
                result = await RoomDAO.add(
                    hotel_id=int(hotel_id),
                    name=name,
                    description=description,
                    price=int(price),
                    services=services,
                    quantity=int(quantity),
                    image_id=int(image_id),
                )
            else:
                room_id, user_id, date_from, date_to = data
                result = await BookingDAO.add(  
                    room_id=int(room_id),
                    user_id=int(user_id),
                    date_from=datetime.strptime(date_from, "%Y-%m-%d").date(),
                    date_to=datetime.strptime(date_to, "%Y-%m-%d").date()
                )
        except ValueError:
            raise NonCorrectData  
    else:
        return result