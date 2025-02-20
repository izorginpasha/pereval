import pytest
import httpx
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_get_pereval_user_email(load_test_data):
    """Тест успешной отправки валидных данных"""
    pereval_data = load_test_data["valid_pereval_get_email"]

    # Мокируем метод `get` класса `AsyncClient` из `httpx`
    async def mock_get(*args, **kwargs):
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = pereval_data
        return mock_response

    with patch('httpx.AsyncClient.get', new=mock_get):
        async with httpx.AsyncClient() as ac:
            response = await ac.get("/submitData/?user__email=user@example.com")
        assert response.status_code == 200
        response_json = await response.json()
        assert response_json == pereval_data