# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_book():
    response = client.post("/books", json={"title": "Test Book", "author": "Test Author", "genre": "Fiction", "year_published": 2024, "summary": "This is a test book."})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"
