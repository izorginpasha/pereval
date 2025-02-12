import httpx
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_create_pereval():
    # Данные, которые отправляются на сервер
    pereval_data = {
        "beauty_title": "string",
        "title": "string",
        "other_titles": "string",
        "connect": "string",
        "add_time": "2025-02-12T05:41:40.748Z",
        "user": {
            "email": "user@example.com",
            "fam": "string",
            "name": "string",
            "otc": "string",
            "phone": "string"
        },
        "coords": {
            "latitude": 0,
            "longitude": 0,
            "height": 0
        },
        "level": {
            "level_winter": "string",
            "level_summer": "string",
            "level_autumn": "string",
            "level_spring": "string"
        },
        "images": [
            {
                "data": "https://lookw.net/9/949/1566941551-1920h1080.-winter-patterns-1-16.jpg",
                "title": "string"
            }
        ]
    }

    # Ожидаемый ответ от сервера
    expected_response = {
        "status": 200,
        "message": "Отправлено успешно",
        "id": 15
    }

    # Мокируем метод `post` класса `AsyncClient` из `httpx`
    async def mock_post(*args, **kwargs):
        assert kwargs["json"] == pereval_data  # Проверяем, что на сервер ушли правильные данные
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response  # Возвращаем ожидаемый ответ
        return mock_response

    with patch('httpx.AsyncClient.post', new=mock_post):
        async with httpx.AsyncClient() as ac:
            response = await ac.post("/submitData", json=pereval_data)

        assert response.status_code == 200
        response_json = await response.json()  # <--- добавлено await
        print(response_json)
        assert response_json == expected_response
