import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from app.main import app
from app.routes import get_users_collection

@pytest.fixture
async def client():
    # 1. Setup Mock
    mock_result = MagicMock()
    mock_result.inserted_id = "mocked_id_123"
    
    mock_collection = AsyncMock()
    mock_collection.insert_one.return_value = mock_result
    
    # 2. Apply Dependency Override
    # This tells FastAPI: "When someone asks for get_users_collection, give them my mock"
    app.dependency_overrides[get_users_collection] = lambda: mock_collection

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    # 3. Cleanup: Remove the override so it doesn't leak into other tests
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_user_unit(client):
    payload = {
        "username": "Alice",
        "email": "alice@example.com",
        "password": "secret123"
    }

    response = await client.post("/users", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "mocked_id_123"
    assert data["username"] == "Alice"