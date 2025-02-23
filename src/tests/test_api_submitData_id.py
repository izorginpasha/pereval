import pytest
import httpx
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_create_valid_pereval(load_test_data):
    """Тест успешной отправки валидных данных"""
    pereval_data = load_test_data["valid_pereval_id"]

    # Мокируем метод `get` класса `AsyncClient` из `httpx`
    async def mock_get(*args, **kwargs):
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = pereval_data
        return mock_response

    with patch('httpx.AsyncClient.get', new=mock_get):
        async with httpx.AsyncClient() as ac:
            response = await ac.get("/submitData/23")
        assert response.status_code == 200
        response_json = await response.json()
        assert response_json == pereval_data


@pytest.mark.asyncio
async def test_invalid_pereval_id():
    """Тест на некорректный ввод"""
    async with httpx.AsyncClient(base_url="http://localhost:8010") as ac:
        response = await ac.get("/submitData/-")  # Неверное значение
    assert response.status_code == 400
    assert response.json() == {"state": 0, "message": "Ошибка валидации JSON", "detail": "Некорректные данные. Проверьте ввод и повторите попытку."}
