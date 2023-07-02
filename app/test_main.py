from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

dummy_receipt = {"retailer": "Target","purchaseDate": "2022-01-01","purchaseTime": "13:01","items": [{"shortDescription": "Mountain Dew 12PK","price": "6.49"},{"shortDescription": "Emils Cheese Pizza","price": "12.25"},{"shortDescription": "Knorr Creamy Chicken","price": "1.26"},{"shortDescription": "Doritos Nacho Cheese","price": "3.35"},{"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ","price": "12.00"}],"total": "35.35"}

def test_get_all_ids():
    response = client.get('/receipts/ids')
    assert response.status_code == 200
    assert response.json() == []

def test_process_receipt():
    response = client.post('/receipts/process', json=dummy_receipt)
    assert response.status_code == 200
    assert response.json() == {"id" : "7565dd88-4ce3-3d0c-a489-fd8331c3877b"}
    
def test_get_points():
    response = client.get('/receipts/7565dd88-4ce3-3d0c-a489-fd8331c3877b/points')
    assert response.status_code == 200
    assert response.json() == {"points": 28}

def test_get_all_receipts():
    response = client.get('/receipts/ids')
    assert response.status_code == 200
    assert response.json() == [{"id": "7565dd88-4ce3-3d0c-a489-fd8331c3877b","receipt": dummy_receipt,"points": 28}]