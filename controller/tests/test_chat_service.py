import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add controller to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from controller.app.models import CommandResponse
from controller.app.services import ChatService


@pytest.fixture
def mock_gemini_client():
    client = MagicMock()
    # Default behavior for intent classification
    client.simple_generate = AsyncMock(return_value='{"intent": "contextual", "confidence": 1.0}')
    client.run_dynamic_conversation = AsyncMock()
    return client

@pytest.fixture
def chat_service(mock_gemini_client):
    return ChatService(mock_gemini_client)

def test_session_management(chat_service):
    """Test session connection and disconnection logic."""
    session_id = "test_session"
    chat_service.handle_connect(session_id)
    assert session_id in chat_service.active_sessions
    assert chat_service.active_sessions[session_id]["history"] == []
    
    chat_service.handle_disconnect(session_id)
    assert session_id not in chat_service.active_sessions

@pytest.mark.asyncio
async def test_process_message_flow(chat_service, mock_gemini_client):
    """Test the standard message processing flow."""
    session_id = "test_session"
    user_msg = "Hello"
    
    # Setup mocks
    mock_response = CommandResponse(AiMessage="Hi there", Commands=[], status="COMPLETED")
    mock_gemini_client.run_dynamic_conversation.return_value = mock_response
    
    # Patch mcp_server_instance to avoid real MCP calls
    with patch("controller.app.services.mcp_server_instance") as mock_mcp:
        mock_mcp.list_tools = AsyncMock(return_value=[])
        
        response = await chat_service.process_message(session_id, user_msg)
        
        assert response.AiMessage == "Hi there"
        assert response.status == "COMPLETED"
        
        # Verify history
        history = chat_service.active_sessions[session_id]["history"]
        assert len(history) == 2
        assert history[0].source == "USER"
        assert history[0].content == user_msg
        assert history[1].source == "AI"
        assert history[1].content == "Hi there"
        
        # Verify calls
        mock_gemini_client.simple_generate.assert_called_once() # Intent classification
        mock_gemini_client.run_dynamic_conversation.assert_called_once()

@pytest.mark.asyncio
async def test_intent_classification_reset(chat_service, mock_gemini_client):
    """Test that 'reset' intent clears the active scenario."""
    session_id = "test_session"
    chat_service.handle_connect(session_id)
    chat_service.active_sessions[session_id]["active_scenario"] = "character"
    
    # Mock intent classification to return 'reset'
    mock_gemini_client.simple_generate.return_value = '{"intent": "reset"}'
    
    # Mock conversation response
    mock_response = CommandResponse(AiMessage="Reset done", Commands=[], status="COMPLETED")
    mock_gemini_client.run_dynamic_conversation.return_value = mock_response

    with patch("controller.app.services.mcp_server_instance") as mock_mcp:
        mock_mcp.list_tools = AsyncMock(return_value=[])
        
        await chat_service.process_message(session_id, "reset please")
        
        assert chat_service.active_sessions[session_id]["active_scenario"] is None
