from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from controller.app.gemini_client import GeminiClient
from controller.app.models import ChatMessage
from google.genai import types  # Import types


# Mock the google.genai.Client and related classes/functions
@pytest.fixture
def mock_genai_client():
    with patch("controller.app.gemini_client.genai.Client") as MockClient:
        mock_client_instance = MockClient.return_value
        # Mock models.list (Synchronous)
        mock_model = MagicMock()
        mock_model.name = "models/gemini-2.5-flash"
        mock_model.supported_generation_methods = ["generateContent", "tool_calling"]
        mock_client_instance.models.list.return_value = [mock_model]

        # Mock models.generate_content (Synchronous)
        mock_response = MagicMock()
        mock_response.text = "Generated content"
        mock_client_instance.models.generate_content.return_value = mock_response

        # Mock chats.create (Synchronous)
        mock_chat_instance = MagicMock()
        mock_chat_instance.send_message.return_value = mock_response
        mock_client_instance.chats.create.return_value = mock_chat_instance

        yield mock_client_instance


@pytest.mark.asyncio
async def test_list_available_models_async(mock_genai_client):
    client = GeminiClient(api_key="TEST_KEY", model_name="gemini-2.5-flash")
    models = await client.list_available_models()
    # models.list is called in a thread, so we check if called
    mock_genai_client.models.list.assert_called_once()
    assert "models/gemini-2.5-flash" in models


@pytest.mark.asyncio
async def test_simple_generate_async(mock_genai_client):
    client = GeminiClient(api_key="TEST_KEY", model_name="gemini-2.5-flash")
    response_text = await client.simple_generate(prompt="test prompt")
    mock_genai_client.models.generate_content.assert_called_once()
    assert response_text == "Generated content"


@pytest.mark.asyncio
async def test_run_dynamic_conversation_async_no_tools(mock_genai_client):
    client = GeminiClient(api_key="TEST_KEY", model_name="gemini-2.5-flash")
    chat_history = [ChatMessage(source="USER", content="Hello"), ChatMessage(source="AI", content="Hi there!")]
    
    # Pass empty tools list
    response = await client.run_dynamic_conversation("test_session", "new message", chat_history, tools_list=[])

    mock_genai_client.chats.create.assert_called_once()
    mock_genai_client.chats.create.return_value.send_message.assert_called_once()
    assert response.AiMessage == "Generated content"
    assert response.status == "COMPLETED"


@pytest.mark.asyncio
async def test_run_dynamic_conversation_async_with_tool_call(mock_genai_client):
    # Mock tool definition
    mock_tool = AsyncMock()
    mock_tool.name = "test_tool"
    mock_tool.description = "a test tool"
    mock_tool.inputSchema = {}
    tools_list = [mock_tool]

    # Mock tool executor
    async def mock_tool_executor(name, args):
        mock_tool_result = AsyncMock()
        mock_tool_result.content = [AsyncMock(type="text", text="Tool output")]
        mock_tool_result.isError = False
        return mock_tool_result

    # Use REAL types for response structure to avoid Pydantic validation errors with Mocks

    # 1. Tool Call Response
    tool_call_part = types.Part(function_call=types.FunctionCall(name="test_tool", args={"param1": "value1"}))
    response_tool_call = types.GenerateContentResponse(
        candidates=[types.Candidate(content=types.Content(parts=[tool_call_part], role="model"))]
    )

    # 2. Final Text Response
    text_part = types.Part(text="Final AI Message")
    response_final_text = types.GenerateContentResponse(
        candidates=[types.Candidate(content=types.Content(parts=[text_part], role="model"))]
    )

    mock_genai_client.chats.create.return_value.send_message.side_effect = [response_tool_call, response_final_text]

    client = GeminiClient(api_key="TEST_KEY", model_name="gemini-2.5-flash")
    chat_history = [
        ChatMessage(source="USER", content="Use the tool"),
    ]
    response = await client.run_dynamic_conversation(
        "test_session", 
        "new message", 
        chat_history, 
        tools_list=tools_list, 
        tool_executor=mock_tool_executor
    )

    mock_genai_client.chats.create.assert_called_once()
    assert mock_genai_client.chats.create.return_value.send_message.call_count == 2
    assert response.AiMessage == "Final AI Message"
    assert response.status == "COMPLETED"
