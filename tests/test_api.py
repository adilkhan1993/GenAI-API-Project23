import pytest
from fastapi.testclient import TestClient
from app.main import app

# Эта фикстура заставит тестовый клиент имитировать полный старт сервера
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    """Тест эндпоинта /health."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint(client):
    """Тест корневого эндпоинта /."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["service"] == "GenAI API"

def test_generate_valid_request(client):
    """Тест эндпоинта /generate с валидным запросом"""
    payload = {
        "prompt": "Напиши SQL-запрос для выборки всех пользователей",
        "max_tokens": 50
    }
    response = client.post("/generate", json=payload)
    
    # Ожидаем успешный ответ
    assert response.status_code == 200
    
    # Проверяем структуру ответа
    data = response.json()
    assert "prompt" in data
    assert "response" in data
    assert "model" in data
    assert "tokens_used" in data

def test_generate_invalid_request_empty_prompt(client):
    """Тест эндпоинта /generate с пустым промптом (ожидаем ошибку 422)"""
    payload = {
        "prompt": "",
        "max_tokens": 50
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "prompt"]