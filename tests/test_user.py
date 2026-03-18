import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def app():
    # Force a fresh import of the app inside the fixture
    from app.main import app as fastapi_app
    return fastapi_app

@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_user_unit(client, monkeypatch):
    # 1. Setup the Mock Result
    mock_result = MagicMock()
    mock_result.inserted_id = "mocked_id_123"
    
    # 2. Create the AsyncMock
    # We use return_value because insert_one is awaited
    mock_insert = AsyncMock(return_value=mock_result)

    # 3. THE CRITICAL PATCH
    # You must point this to the file where 'db' is USED.
    # If your file is app/routes.py, use "app.routes.db.users.insert_one"
    # If your file is app/main.py, use "app.main.db.users.insert_one"
    monkeypatch.setattr("app.routes.db.users.insert_one", mock_insert)

    payload = {
        "username": "TestUser", 
        "email": "test@example.com", 
        "password": "password123"
    }

    # 4. Execute
    response = await client.post("/users", json=payload)

    # 5. Assertions
    assert response.status_code == 200
    assert response.json()["username"] == "TestUser"
    
    # 6. Verify the mock was actually called (Proof it didn't hit the real DB)
    # mock_insert.assert_called_once()