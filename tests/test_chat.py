from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_select_exchange_valid():
    response = client.post("/chat", data={"action": "select_exchange", "value": "LSE"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "stock_list"
    assert payload["exchange_code"] == "LSE"
    assert "stocks" in payload


def test_select_exchange_invalid():
    response = client.post("/chat", data={"action": "select_exchange", "value": "FAKE"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "error"
    assert payload["message"] == "No exchange found for code 'FAKE'."


def test_select_stock_valid():
    response = client.post("/chat", data={"action": "select_stock", "value": "FLTR"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "stock_price"
    assert "stock_name" in payload
    assert "price" in payload


def test_select_stock_invalid():
    response = client.post("/chat", data={"action": "select_stock", "value": "INVALID"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "error"
    assert payload["message"] == "Stock with code 'INVALID' not found."


def test_invalid_action():
    response = client.post("/chat", data={"action": "unknown", "value": "anything"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "error"
    assert payload["message"] == "Invalid action: unknown"

