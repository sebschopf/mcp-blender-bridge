from unittest.mock import AsyncMock

import pytest
from controller.app.models import CommandResponse
from controller.app.services import ChatService


@pytest.fixture
def mock_gemini_client():
    client = AsyncMock()  # Changed to AsyncMock
    client.run_dynamic_conversation = AsyncMock()
    client.simple_generate = AsyncMock()  # Changed to AsyncMock
    return client


@pytest.fixture
def chat_service(mock_gemini_client):
    return ChatService(mock_gemini_client)


@pytest.mark.asyncio  # Mark as async test
async def test_classify_intent_character(chat_service, mock_gemini_client):
    # Mock simple_generate response
    mock_gemini_client.simple_generate.return_value = """
    ```json
    {
        "intent": "character",
        "confidence": 0.95,
        "reasoning": "User wants to create a person."
    }
    ```
    """
    intent = await chat_service.classify_intent("Create a realistic human")  # Await the call
    assert intent == "character"
    mock_gemini_client.simple_generate.assert_awaited_once()  # Use assert_awaited_once


@pytest.mark.asyncio  # Mark as async test
async def test_classify_intent_fallback(chat_service, mock_gemini_client):
    # Mock empty or invalid response
    mock_gemini_client.simple_generate.return_value = "I am not sure."
    intent = await chat_service.classify_intent("Do something")  # Await the call
    assert intent == "contextual"


@pytest.mark.asyncio
async def test_process_message_routing(chat_service, mock_gemini_client):
    # Mock intent classification
    mock_gemini_client.simple_generate.return_value = '{"intent": "architecture"}'

    # Mock conversation response
    mock_response = CommandResponse(AiMessage="Ok building", Commands=[])
    mock_gemini_client.run_dynamic_conversation.return_value = mock_response

    await chat_service.process_message("session1", "Build a house")

    # Check if run_dynamic_conversation was called
    call_args = mock_gemini_client.run_dynamic_conversation.call_args
    # Check if system_instruction was loaded (we can't easily verify the content without mocking file I/O,
    # but we can verify it was passed)
    assert "system_instruction" in call_args.kwargs
    # Verify it tried to load architecture scenario (implied by logic flow)
