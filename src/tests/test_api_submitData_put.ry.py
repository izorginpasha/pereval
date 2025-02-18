import pytest
import httpx
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_update_valid_pereval(load_test_data):
    """Тест успешной отправки валидных данных"""
    pereval_data = load_test_data["valid_pereval_put"]

    # Мокируем метод `get` класса `AsyncClient` из `httpx`
    async def mock_put(*args, **kwargs):
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = pereval_data
        return mock_response

    with patch('httpx.AsyncClient.get', new=mock_put):
        async with httpx.AsyncClient() as ac:
            response = await ac.put("/submitData")
        assert response.status_code == 200
        response_json = await response.json()
        assert response_json ==
        assert response.json() == {
            "status": 1,
            "message": "Запись успешно обновлена.",
            "id": null
        }
