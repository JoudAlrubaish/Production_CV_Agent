#perform automated health test 
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["api"] == "healthy"
    assert data["database"] == "healthy"
    assert "model" in data


def test_model_loaded():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["model"] == "loaded"