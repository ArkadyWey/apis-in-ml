from fastapi.testclient import TestClient


def test_root(client: TestClient):
    """Test the root of the API."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello MLE Fellowship!"}


def test_no_participants(client: TestClient):
    """Test no participants in DB."""
    response = client.get(
        "/participant/1",
    )
    assert response.status_code == 404


def test_create_participant(client: TestClient):
    """Test creating a participant."""

    # TODO: 1. Create a participant
    # 2. Validate the creation

    assert 1 == 1
