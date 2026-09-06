from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MLOps Model API is Live!"}

def test_predict_endpoint_valid():
    payload = [5.1, 3.5, 1.4, 0.2]
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], int)