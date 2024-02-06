from fastapi.testclient import TestClient

from apis_in_ml.main import app

client = TestClient(app)


def test_root():
    """Test the root of the API."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello MLE Fellowship!"}

# TODO: fix the filepath issue
def test_get_participant():
    participant_id = 1
    response = client.get(f"/participant/{participant_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": participant_id,
        "first_name": "alex",
        "last_name": "rogers",
        "role": "mle",
    }
