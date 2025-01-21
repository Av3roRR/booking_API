from httpx import AsyncClient, ASGITransport
import pytest

from app.main import app as fastapi_app

@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "kotopes", 200),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "pesokot", 200),
    ("abcde", "pesokot", 422)
])
async def test_register_user(email, password, status_code):
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": email,
            "password": password,
        })
        
        assert response.status_code == status_code
        

@pytest.mark.parametrize("email,password,status_code", [
    ("user@example.com", "string", 200)
])
async def test_login_user(email, password, status_code):
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "email": email,
            "password": password,
        })
        
        assert response.status_code == status_code