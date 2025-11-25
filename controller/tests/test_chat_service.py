from unittest.mock import AsyncMock, MagicMock

import pytest
from controller.app.models import CommandResponse
from controller.app.services import ChatService


@pytest.fixture
def mock_gemini_client():
    client = MagicMock()
    client.run_dynamic_conversation = AsyncMock()
    return client


@pytest.fixture
def chat_service(mock_gemini_client):
    return ChatService(mock_gemini_client)


@pytest.mark.asyncio
async def test_process_message_contextual(chat_service, mock_gemini_client):
    mock_response = CommandResponse(AiMessage="Hello", Commands=[])
    mock_gemini_client.run_dynamic_conversation.return_value = mock_response

    response = await chat_service.process_message("session1", "Hi")

    assert response.AiMessage == "Hello"
    mock_gemini_client.run_dynamic_conversation.assert_called_once()

    # Verify call args
    call_args = mock_gemini_client.run_dynamic_conversation.call_args
    assert call_args.kwargs["session_id"] == "session1"
    # system_instruction might be loaded from file or None


@pytest.mark.asyncio
async def test_process_message_format_to_bpy_valid(chat_service, mock_gemini_client):
    # Mocking a valid BPY response
    valid_script = """python
import bpy
bpy.ops.mesh.primitive_cube_add()
"""
    mock_response = CommandResponse(AiMessage=valid_script, Commands=[])
    mock_gemini_client.run_dynamic_conversation.return_value = mock_response

    response = await chat_service.process_message("session1", "Make cube", mode="format-to-bpy")

    assert "Script generated and validated" in response.AiMessage
    assert len(response.Commands) == 1
    assert response.Commands[0].CommandType == "EXECUTE_SCRIPT"
    assert "bpy.ops.mesh.primitive_cube_add()" in response.Commands[0].Script
    assert response.Commands[0].RequiresConfirmation is True


@pytest.mark.asyncio
async def test_process_message_format_to_bpy_invalid(chat_service, mock_gemini_client):
    # Mocking an invalid response (missing bpy)
    invalid_script = """python
print('no bpy')
"""
    mock_response = CommandResponse(AiMessage=invalid_script, Commands=[])
    mock_gemini_client.run_dynamic_conversation.return_value = mock_response

    response = await chat_service.process_message("session1", "Make cube", mode="format-to-bpy")

    assert "Script Validation Failed" in response.AiMessage
    assert response.status == "ERROR"
    assert len(response.Commands) == 0
