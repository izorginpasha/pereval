import pytest
import httpx
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_create_valid_pereval(load_test_data):
    """Тест успешной отправки валидных данных"""
    pereval_data = load_test_data["valid_pereval"]

    expected_response = {
        "status": 200,
        "message": "Отправлено успешно",
        "id": None
    }

    async def mock_post(*args, **kwargs):
        assert kwargs["json"] == pereval_data  # Проверяем, что на сервер ушли правильные данные
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        return mock_response

    with patch('httpx.AsyncClient.post', new=mock_post):
        async with httpx.AsyncClient() as ac:
            response = await ac.post("/submitData", json=pereval_data)

        assert response.status_code == 200
        assert await response.json() == expected_response


@pytest.mark.asyncio
async def test_create_invalid_pereval(load_test_data):
    """Тест отправки невалидных данных"""
    pereval_data = load_test_data["invalid_pereval"]

    expected_response = {
        "status": 400,
        "message": "Ошибка валидации данных"
    }

    async def mock_post(*args, **kwargs):
        assert kwargs["json"] == pereval_data  # Проверяем, что на сервер ушли неправильные данные
        mock_response = AsyncMock()
        mock_response.status_code = 400
        mock_response.json.return_value = expected_response
        return mock_response

    with patch('httpx.AsyncClient.post', new=mock_post):
        async with httpx.AsyncClient() as ac:
            response = await ac.post("/submitData", json=pereval_data)

        assert response.status_code == 400
        assert await response.json() == expected_response
@pytest.mark.asyncio
async def test_create_invalid_pereval(load_test_data):
    """Тест отправки невалидных данных"""
    pereval_data = load_test_data["valid_pereval"]
    pereval_data["images"][0]["data"] = "null"

    expected_response = {
        "status": 400,
        "message": "Ошибка валидации данных"
    }

    async def mock_post(*args, **kwargs):
        assert kwargs["json"] == pereval_data  # Проверяем, что на сервер ушли неправильные данные
        mock_response = AsyncMock()
        mock_response.status_code = 400
        mock_response.json.return_value = expected_response
        return mock_response

    with patch('httpx.AsyncClient.post', new=mock_post):
        async with httpx.AsyncClient() as ac:
            response = await ac.post("/submitData", json=pereval_data)

        assert response.status_code == 400
        assert await response.json() == expected_response