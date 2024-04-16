from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# Sanity check for database
def test_sanity():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# Create, read and delete a test user from database
def test_create_user():

    # Create the user
    response = client.post(
        "/users/",
        json={"username": "Example123", "email": "test@example.com", "password": "example123"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "Example123"
    assert data["email"] == "test@example.com"
    assert "id" in data
    user_id = data["id"]

    # Read user information
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "Example123"
    assert data["email"] == "test@example.com"
    assert data["id"] == user_id

    # Delete user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200, response.text

    # Read user to receive 404
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404, response.text

def test_create_catch():

    # Create test user
    response = client.post(
        "/users/",
        json={"username": "Example123", "email": "test@example.com", "password": "example123"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]

    # Create catch for test user
    response = client.post(
        f"/users/{user_id}/catches/",
        json={"species": "Northern Pike", "location": "Toronto, Canada"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["angler_id"] == user_id
    assert data["species"] == "Northern Pike"
    assert data["location"] == "Toronto, Canada"

    # Delete catch from test user

    # Delete test user