import pytest
import json

@pytest.fixture
def load_test_data():
    """Загружает тестовые данные из JSON-файла."""
    with open("src/tests/test_data.json", encoding="utf-8") as f:
        return json.load(f)
