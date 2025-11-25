import logging
import os
import re
from typing import Any, Dict, Optional

from . import globals
from .gemini_client import GeminiClient
from .logging_utils import PerformanceLogger
from .mcp_server import mcp as mcp_server_instance
from .models import ActionPlan, BpyCommand, ChatMessage, CommandResponse
from .validation import validate_bpy_script

logger = logging.getLogger(__name__)

# Constants
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "../resources/llm_prompts")
MODE_FORMAT_TO_BPY = "format-to-bpy"


class ChatService:
    """Service for handling chat interactions and session management."""

    def __init__(self, gemini_client: GeminiClient):
        """Initializes the ChatService.

        Args:
            gemini_client: The GeminiClient instance to use for AI interactions.
        """
        self.gemini_client = gemini_client
        # Dictionary to store session state: {session_id: {"history": [], "active_scenario": None}}
        self.active_sessions: Dict[str, Dict] = {}

    def _load_system_prompt(self, mode: str) -> Optional[str]:
        """Loads the system prompt for the specified mode."""
        filename = f"{mode}.md"
        filepath = os.path.join(PROMPT_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt template {filename} not found at {filepath}. Using default.")
            return None

    def _extract_python_code(self, text: str) -> str:
        """Extracts Python code from markdown backticks."""
        pattern = r"```python(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()

        # Fallback: check for generic backticks
        pattern_generic = r"```(.*?)```"
        matches_generic = re.findall(pattern_generic, text, re.DOTALL)
        if matches_generic:
            return matches_generic[0].strip()

        return text.strip()

    async def classify_intent(self, user_message: str) -> str:
        """Classifies the user's intent using the router prompt."""
        with PerformanceLogger("ROUTER", f"Classifying intent for: {user_message[:50]}...") as pl:
            router_prompt = self._load_system_prompt("router")
            if not router_prompt:
                return "contextual"

            try:
                response_text = await self.gemini_client.simple_generate(
                    prompt=f"User Request: {user_message}", system_instruction=router_prompt
                )

                # Extract JSON from markdown if present
                match = re.search(r"```json(.*?)```", response_text, re.DOTALL)
                if match:
                    json_str = match.group(1).strip()
                else:
                    json_str = response_text.strip()

                import json

                data = json.loads(json_str)
                intent = data.get("intent", "contextual")
                confidence = data.get("confidence", 0.0)
                pl.logger.info(f"Intent classified: {intent} (Confidence: {confidence})")
                return intent

            except Exception as e:
                pl.logger.error(f"Error classifying intent: {e}")
                return "contextual"

    async def process_message(
        self, session_id: str, user_message: str, action_plan: Optional[ActionPlan] = None, mode: str = "contextual"
    ) -> CommandResponse:
        """Processes a chat message or action plan from the user."""
        with PerformanceLogger("REQ", f"Processing message for {session_id} (Mode: {mode})"):
            logger.info(f"Processing message for session {session_id}: '{user_message}' (Mode: {mode})")

            # 1. Handle direct ActionPlan execution (Deprecated)
            if action_plan:
                logger.warning(f"ActionPlan received for session {session_id} but Action Plans are deprecated.")
                return CommandResponse(
                    AiMessage="Action Plans are no longer supported in this version.", Commands=[], status="ERROR"
                )

            # 2. Ensure session exists
            if session_id not in self.active_sessions:
                self.handle_connect(session_id)

            # Access session state
            session_state = self.active_sessions[session_id]
            chat_history = session_state["history"]
            active_scenario = session_state["active_scenario"]

            # 3. Append user message to history
            chat_history.append(ChatMessage(source="USER", content=user_message))

            # 4. Load System Instruction (Sticky Scenario Logic)
            target_scenario = "contextual"  # Default fallback

            if mode == "contextual":
                # Classify intent
                new_intent = await self.classify_intent(user_message)

                if new_intent == "reset":
                    # Explicit reset command
                    logger.info("Resetting scenario state.")
                    active_scenario = None
                    target_scenario = "contextual"
                elif new_intent == "contextual":
                    # Ambiguous or general intent
                    if active_scenario:
                        # STICKY: Keep previous scenario
                        logger.info(f"Sticky Scenario: Maintaining '{active_scenario}' despite ambiguous input.")
                        target_scenario = active_scenario
                    else:
                        target_scenario = "contextual"
                elif new_intent in ["character", "architecture", "prop", "scripting"]:
                    # Specific intent detected - switch context
                    logger.info(f"Switching scenario to '{new_intent}'")
                    active_scenario = new_intent
                    target_scenario = new_intent
                else:
                    # Unknown intent fallback
                    target_scenario = "contextual"

                # Update session state with potentially new active scenario
                session_state["active_scenario"] = active_scenario

                # Resolve prompt path
                if target_scenario in ["character", "architecture", "prop", "scripting"]:
                    system_instruction = self._load_system_prompt(f"scenarios/{target_scenario}")
                    if not system_instruction:
                        logger.warning(f"Scenario prompt for '{target_scenario}' not found. Falling back to default.")
                        system_instruction = self._load_system_prompt("contextual")
                else:
                    system_instruction = self._load_system_prompt("contextual")

            else:
                # Use explicit mode (e.g., format-to-bpy) - overrides sticky state logic
                system_instruction = self._load_system_prompt(mode)

            # 5. Run dynamic conversation
            try:
                logger.info(f"Starting dynamic AI conversation for session {session_id}...")

                # Fetch tools and executor from MCP
                tools_list = await mcp_server_instance.list_tools()

                async def tool_executor(name: str, args: Dict) -> Any:
                    return await mcp_server_instance.call_tool(name, arguments=args)

                final_response = await self.gemini_client.run_dynamic_conversation(
                    session_id=session_id,
                    user_prompt=user_message,
                    chat_history=chat_history,
                    tools_list=tools_list,
                    tool_executor=tool_executor,
                    system_instruction=system_instruction,
                )

                # 6. Post-processing for format-to-bpy
                if mode == MODE_FORMAT_TO_BPY:
                    raw_text = final_response.AiMessage
                    script_content = self._extract_python_code(raw_text)

                    is_valid, errors = validate_bpy_script(script_content)

                    if is_valid:
                        # Create a command to suggest execution
                        cmd = BpyCommand(CommandType="EXECUTE_SCRIPT", Script=script_content, RequiresConfirmation=True)
                        # We might need to ensure Commands list exists
                        if final_response.Commands is None:
                            final_response.Commands = []

                        final_response.Commands.append(cmd)
                        final_response.AiMessage = (
                            f"Script generated and validated.\n\n```python\n{script_content}\n```"
                        )
                    else:
                        error_msg = "\n- ".join(errors)
                        final_response.AiMessage = (
                            f"**Script Validation Failed**:\n- {error_msg}\n\n**Raw Output**:\n{raw_text}"
                        )
                        final_response.status = "ERROR"
                        # Do not append the command if invalid

                # 7. Append AI response to history
                chat_history.append(ChatMessage(source="AI", content=final_response.AiMessage))
                return final_response

            except Exception as e:
                error_message = f"Error during dynamic conversation: {e}"
                logger.error(error_message, exc_info=True)
                return CommandResponse(AiMessage=error_message, Commands=[], status="ERROR")

    def handle_connect(self, session_id: str) -> None:
        """Handles a new session connection."""
        # Initialize new session structure
        self.active_sessions[session_id] = {"history": [], "active_scenario": None}
        logger.info(f"Session {session_id} connected. Active sessions: {len(self.active_sessions)}")

    def handle_disconnect(self, session_id: str) -> None:
        """Handles a session disconnection."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logger.info(f"Session {session_id} disconnected. Active sessions: {len(self.active_sessions)}")
