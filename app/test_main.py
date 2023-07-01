from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_get_all_ids():
    response = client.get('/receipts/ids')
    assert response.status_code == 200
    assert response.json() == []