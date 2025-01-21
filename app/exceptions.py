from typing import Optional
from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail=""
    
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"


class IncorrectEMailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Пользователь ввёл неправильную почту или пароль"


class ExpiredTokenException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Пора обновить токен для продолжения работы"


class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных номеров"

class NonCorrectDates(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Некорректные даты"
    
class NonCorrectData(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Некорректные данные в csv файле"
    
class NonCorrectFileType(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Некорректный файл для заполнения"
    