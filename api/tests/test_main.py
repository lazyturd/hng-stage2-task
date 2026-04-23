import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app  # noqa: E402

client = TestClient(app)


@patch("main.r")
def test_create_job(mock_redis):
    """
    Test that the POST /jobs endpoint correctly generates a UUID
    and pushes the expected commands to the mocked Redis client.
    """
    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data

    # Verify the Redis methods were called with the correct argument types
    assert mock_redis.lpush.called
    assert mock_redis.hset.called


@patch("main.r")
def test_get_job_status_existing(mock_redis):
    """
    Test that the GET /jobs/{job_id} endpoint correctly decodes
    and returns the status of an existing job.
    """
    # Redis returns byte strings natively. Mock the byte string return.
    mock_redis.hget.return_value = b"completed"

    test_id = "12345-abcde"
    response = client.get(f"/jobs/{test_id}")

    assert response.status_code == 200
    assert response.json() == {"job_id": test_id, "status": "completed"}

    # Verify it queried the correct Redis key
    mock_redis.hget.assert_called_with(f"job:{test_id}", "status")


@patch("main.r")
def test_get_job_status_not_found(mock_redis):
    """
    Test that the GET /jobs/{job_id} endpoint handles missing jobs
    by returning the expected error schema.
    """
    # If a key doesn't exist, Redis hget returns None
    mock_redis.hget.return_value = None

    response = client.get("/jobs/missing-id-999")

    assert response.status_code == 200
    assert response.json() == {"error": "not found"}
