"""Gemini Client for interacting with Google's Generative AI."""
import asyncio  # T001: Import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

import google.genai as genai
from dotenv import load_dotenv
from google.genai import types

from .logging_utils import PerformanceLogger
from .models import ChatMessage, CommandResponse

logger = logging.getLogger(__name__)
# Load .env from the controller root directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)


def _clean_schema_for_gemini(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively removes 'additionalProperties' and 'title' from a JSON schema dictionary.

    These fields can cause INVALID_ARGUMENT errors with the Gemini API.
    """
    if not isinstance(schema, dict):
        return schema

    cleaned_schema = {}
    for key, value in schema.items():
        if key in ["additionalProperties", "title"]:
            continue
        elif isinstance(value, dict):
            cleaned_schema[key] = _clean_schema_for_gemini(value)
        elif isinstance(value, list):
            cleaned_schema[key] = [_clean_schema_for_gemini(item) for item in value]
        else:
            cleaned_schema[key] = value
    return cleaned_schema


class GeminiClient:
    """Client for interacting with the Google Gemini API."""

    def __init__(self, api_key: str | None = None, model_name: str | None = None):
        """Initializes the Gemini Client."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        self.client = genai.Client(api_key=self.api_key)
        # Switch to standard flash for better instruction following
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        # Load system prompt from file
        prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.md")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_instruction = f.read()
        except FileNotFoundError:
            logger.warning(f"System prompt file not found at {prompt_path}, using default.")
            self.system_instruction = "You are an expert Blender assistant. Use the provided tools."

    async def list_available_models(self) -> List[str]:  # T004: Make async
        """Lists Gemini models that support generateContent and tool_calling."""
        available_models = []
        try:
            # T004: Wrap blocking call in asyncio.to_thread
            models_list = await asyncio.to_thread(self.client.models.list)
            for m in models_list:  # type: ignore
                supported_methods = getattr(m, "supported_generation_methods", [])
                if "generateContent" in (supported_methods or []):
                    if m.name and m.name.startswith("models/gemini"):
                        available_models.append(m.name)
        except Exception as e:
            logger.error(f"Error listing models from Gemini API: {e}")
            return []

        return available_models

    async def simple_generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:  # T003: Make async
        """Generates a simple text response for a single prompt, without chat history or tools.

        Useful for classification or summarization tasks.
        """
        if not self.model_name:
            raise ValueError("Model name is not set.")

        try:
            config = types.GenerateContentConfig(system_instruction=system_instruction)
            # T003: Wrap blocking call in asyncio.to_thread
            response = await asyncio.to_thread(
                self.client.models.generate_content, model=self.model_name, contents=prompt, config=config
            )
            return response.text if response.text else ""
        except Exception as e:
            logger.error(f"Error in simple_generate: {e}")
            return ""

    async def run_dynamic_conversation(
        self,
        session_id: str,
        user_prompt: str,
        chat_history: List[ChatMessage],
        tools_list: Optional[List[Any]] = None,
        tool_executor: Optional[Any] = None,
        system_instruction: Optional[str] = None,
    ) -> CommandResponse:
        """Orchestrates the full, multi-turn conversation with Gemini."""
        with PerformanceLogger("LLM_CALL", f"Gemini Conversation session={session_id}"):
            formatted_history: List[types.Content | types.ContentDict] = []
            for msg in chat_history:
                role = "user" if msg.source == "USER" else "model"
                formatted_history.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.content)]))

            if not self.model_name:
                raise ValueError("Model name is not set.")

            gemini_tools = []
            if tools_list:
                for t in tools_list:
                    # Clean the inputSchema before sending to Gemini
                    cleaned_parameters = _clean_schema_for_gemini(t.inputSchema)
                    gemini_tools.append(
                        types.FunctionDeclaration(name=t.name, description=t.description, parameters=cleaned_parameters)
                    )

            tools_config = [types.Tool(function_declarations=gemini_tools)] if gemini_tools else None

            # T002: Wrap blocking call in asyncio.to_thread
            chat = await asyncio.to_thread(
                self.client.chats.create,
                model=self.model_name,
                history=formatted_history,
                config=types.GenerateContentConfig(
                    tools=tools_config, system_instruction=system_instruction or self.system_instruction
                ),
            )

            # T002: Wrap blocking call in asyncio.to_thread
            response = await asyncio.to_thread(chat.send_message, user_prompt)

            while True:
                # Check for function calls in the response
                function_calls = []
                if response.candidates:
                    content = response.candidates[0].content
                    if content and content.parts:
                        for part in content.parts:
                            if part.function_call:
                                function_calls.append(part.function_call)

                if not function_calls:
                    break

                # Execute all function calls found in this turn
                function_responses = []
                for fc in function_calls:
                    fname = fc.name
                    fargs = fc.args
                    logger.info(f"AI calling tool: {fname} with args: {fargs}")

                    try:
                        args_dict = dict(fargs) if fargs else {}
                        with PerformanceLogger("TOOL_EXEC", f"Tool: {fname}"):
                            if tool_executor:
                                result = await tool_executor(fname, args_dict)
                            else:
                                result = None
                                logger.error("No tool executor provided.")

                        output_text = ""
                        if result:
                            if hasattr(result, "content"):
                                for c in result.content:
                                    if hasattr(c, "type") and c.type == "text":
                                        output_text += c.text + "\n"
                                    elif hasattr(c, "type") and c.type == "image":
                                        output_text += "[Image Content]\n"
                                    else:
                                        output_text += str(c) + "\n"
                            else:
                                # Fallback for non-standard results (str, list, tuple)
                                # This handles cases where the tool executor returns a raw value or a tuple
                                output_text = str(result)

                        if hasattr(result, "isError") and result.isError:
                            output_text = f"Error: {output_text}"

                    except Exception as e:
                        output_text = f"System Error executing tool: {e}"
                    
                    # Create the response part for this specific function call
                    function_responses.append(
                        types.Part.from_function_response(name=fname, response={"content": output_text})
                    )

                # Send all function responses back to the model in a single message
                logger.info(f"Sending function responses to Gemini: {function_responses}")
                # T002: Wrap blocking call in asyncio.to_thread
                response = await asyncio.to_thread(
                    chat.send_message, function_responses
                )

            ai_text = response.text if response.text else "Done."

            return CommandResponse(AiMessage=ai_text, Commands=[], status="COMPLETED")
