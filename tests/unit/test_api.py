from fastapi.testclient import TestClient

from codebase_assistant.interfaces.api.app import app

client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "Codebase Assistant",
    }
