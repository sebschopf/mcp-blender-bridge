from unittest.mock import AsyncMock, MagicMock, patch  # Add AsyncMock

import pytest  # Add import
from controller.app.main import app
from controller.app.models import CommandResponse
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_root():
    """Health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MCP Controller is running"}


@pytest.mark.asyncio  # Mark as async test
async def test_get_models():  # Make function async
    """Tests the /api/models endpoint."""
    # Patch the instance method on the global gemini_client in app.main
    with patch(
        "controller.app.main.gemini_client.list_available_models", new_callable=AsyncMock
    ) as mock_list_models:  # Use AsyncMock
        mock_list_models.return_value = ["models/gemini-1.5-flash", "models/gemini-pro"]

        response = client.get("/api/models")
        if response.status_code != 200:
            print(f"Response Error: {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert isinstance(data["models"], list)
        assert "models/gemini-1.5-flash" in data["models"]
        mock_list_models.assert_awaited_once()  # Use assert_awaited_once


@patch("controller.app.main.chat_service")
def test_chat_initiates_dynamic_conversation(mock_chat_service):
    """Tests that a simple chat message correctly initiates the dynamic conversation flow."""
    # Configure the mock to return a successful async result
    mock_response = CommandResponse(AiMessage="Conversation complete", Commands=[], status="COMPLETED")

    # Since the method is async, the mock needs to be an async function
    async def mock_process_message(*args, **kwargs):
        return mock_response

    mock_chat_service.process_message = MagicMock(side_effect=mock_process_message)

    request_data = {
        "SessionID": "test-session-dynamic",
        "Message": "start dynamic flow",
    }

    response = client.post("/api/chat", json=request_data)

    assert response.status_code == 200
    mock_chat_service.process_message.assert_called_once()
    data = response.json()
    assert data["AiMessage"] == "Conversation complete"
