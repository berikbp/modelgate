from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_health():
    response = client.get("/healthz")
    assert response.status_code == 201
    assert response.json() == {"status": "healthy"}

def test_models():
    response = client.get("/v1/models")
    assert response.status_code == 200
    assert len(response.json()['models']) > 2

def test_chat():
    response = client.post(
        '/v1/chat',
        json={"model": "GPT-4", "prompt": "Hello, how are you?"}
    )

    assert response.status_code == 200
    assert response.json()['model'] == "GPT-4"
    assert response.json()['prompt'] == "Hello, how are you?"


def test_chat_invalid_model():
    response = client.post(
        '/v1/chat',
        json={'model': 'DEPEPE', 'prompt': 'Hello, how are you?'}
    )

    assert response.status_code == 404
