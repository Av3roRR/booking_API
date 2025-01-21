import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app as fastapi_app

@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ("Алтай", "2023-04-01", "2023-04-15", 200),
    ("Алтай", "2023-04-01", "2023-05-02", 400),
    ("Алтай", "2023-04-15", "2023-04-01", 400),
    ("Коми", "2023-04-01", "2024-04-15", 400),
    ("Коми", "2023-04-01", "2023-04-15", 200),
])
async def test_get_hotels(location, date_from, date_to, status_code):
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        response = await ac.get(f"/hotels/{location}", params={
            "location": location,
            "date_from": date_from,
            "date_to": date_to
        })
        
        assert response.status_code == status_code
        