import pytest
from ..fastapi_app import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_stream():
    response = client.get("/stream")
    assert response.status_code == 200

def test_websocket_endpoint():
    response = client.get("/ws")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()
