"""Tests for Sticky Scenario Logic in ChatService."""
from unittest.mock import AsyncMock

import pytest
from controller.app.models import CommandResponse
from controller.app.services import ChatService


@pytest.fixture
def mock_gemini_client():
    """Mock Gemini client."""
    client = AsyncMock()  # Changed to AsyncMock
    client.run_dynamic_conversation = AsyncMock()
    client.simple_generate = AsyncMock()  # Changed to AsyncMock
    return client


@pytest.fixture
def chat_service(mock_gemini_client):
    """ChatService fixture."""
    return ChatService(mock_gemini_client)


@pytest.mark.asyncio
async def test_sticky_scenario_persistence(chat_service, mock_gemini_client):
    """Tests that a scenario (prop) sticks across subsequent contextual requests."""
    session_id = "sticky_test"
    chat_service.handle_connect(session_id)

    # 1. Initial request -> Prop
    mock_gemini_client.simple_generate.return_value = '{"intent": "prop"}'
    mock_gemini_client.run_dynamic_conversation.return_value = CommandResponse(AiMessage="Prop started", Commands=[])

    await chat_service.process_message(session_id, "Make a chair")

    assert chat_service.active_sessions[session_id]["active_scenario"] == "prop"

    # 2. Follow-up -> Contextual (Ambiguous)
    mock_gemini_client.simple_generate.return_value = '{"intent": "contextual"}'
    await chat_service.process_message(session_id, "Make it red")

    # Should STAY prop
    assert chat_service.active_sessions[session_id]["active_scenario"] == "prop"

    # Verify the prop scenario prompt was loaded (check args passed to gemini)
    # We assume "prop.md" content is passed. Since we can't easily verify file content without IO mocking,
    # we trust the logic flow for now, or we could mock _load_system_prompt.


@pytest.mark.asyncio
async def test_sticky_scenario_reset(chat_service, mock_gemini_client):
    """Tests that 'reset' intent clears the active scenario."""
    session_id = "reset_test"
    chat_service.handle_connect(session_id)

    # 1. Start prop
    mock_gemini_client.simple_generate.return_value = '{"intent": "prop"}'
    mock_gemini_client.run_dynamic_conversation.return_value = CommandResponse(AiMessage="ok", Commands=[])
    await chat_service.process_message(session_id, "Make a chair")
    assert chat_service.active_sessions[session_id]["active_scenario"] == "prop"

    # 2. Reset
    mock_gemini_client.simple_generate.return_value = '{"intent": "reset"}'
    await chat_service.process_message(session_id, "Stop")

    assert chat_service.active_sessions[session_id]["active_scenario"] is None


@pytest.mark.asyncio
async def test_sticky_scenario_switch(chat_service, mock_gemini_client):
    """Tests switching from one scenario (prop) to another (character) explicitly."""
    session_id = "switch_test"
    chat_service.handle_connect(session_id)

    # 1. Start prop
    mock_gemini_client.simple_generate.return_value = '{"intent": "prop"}'
    mock_gemini_client.run_dynamic_conversation.return_value = CommandResponse(AiMessage="ok", Commands=[])
    await chat_service.process_message(session_id, "Make a chair")

    # 2. Switch to Character
    mock_gemini_client.simple_generate.return_value = '{"intent": "character"}'
    await chat_service.process_message(session_id, "Actually make a human")

    assert chat_service.active_sessions[session_id]["active_scenario"] == "character"
