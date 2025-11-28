import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add controller to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Set dummy API key to avoid ValueError during import of controller.app.main
os.environ["GEMINI_API_KEY"] = "dummy_key"

from controller.app import main
from controller.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    """Verify the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MCP Controller is running"}

@pytest.mark.asyncio
async def test_send_chat_message_success():
    """Verify the chat endpoint delegates to ChatService correctly."""
    # Mock the chat_service instance on the main module
    with patch.object(main, 'chat_service') as mock_service:
        # Setup mock return value
        mock_response = MagicMock()
        mock_response.AiMessage = "Hello from Mock"
        mock_response.Commands = []
        mock_response.status = "COMPLETED"
        # Pydantic models might be returned as dicts by FastAPI, but the service returns an object
        # We need to ensure the mock behaves like the real object or its return value is compatible
        
        # process_message is async
        mock_service.process_message = AsyncMock(return_value=mock_response)
        
        payload = {
            "SessionID": "test_session",
            "Message": "Hello",
            "mode": "chat"
        }
        
        response = client.post("/api/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["AiMessage"] == "Hello from Mock"
        
        mock_service.process_message.assert_called_once()
