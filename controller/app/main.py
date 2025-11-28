"""Main entry point for the MCP Controller FastAPI application."""
import logging
from typing import Any, Dict, List

from fastapi import Body, FastAPI

from . import globals
from .bridge_api import router as bridge_router
from .gemini_client import GeminiClient
from .logging_utils import LOG_FORMAT
from .mcp_server import mcp as mcp_server_instance
from .mcp_server import register_tools
from .models import CommandRequest, CommandResponse
from .services import ChatService

# Configure logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Blender-Gemini MCP Controller",
    description="API for communication between the Blender Addon (Peripheral) and the FastAPI server (Controller).",
    version="1.1.0",
)

app.include_router(bridge_router)

# Initialize the Knowledge Engine as a singleton
globals.initialize_knowledge_engine()

# Register MCP tools from capabilities
register_tools()

# Mount MCP Server (SSE)
app.mount("/mcp", mcp_server_instance.sse_app)

gemini_client = GeminiClient()
chat_service = ChatService(gemini_client)


@app.get("/")
def read_root() -> Dict[str, str]:
    """Health check endpoint."""
    logger.info("Root endpoint accessed.")
    return {"message": "MCP Controller is running"}


@app.get("/api/models")
async def get_models() -> Dict[str, List[str]]:
    """Retrieves the list of available Gemini models."""
    logger.info("Models endpoint accessed.")
    return {"models": await gemini_client.list_available_models()}


@app.post("/api/chat", response_model=CommandResponse)
async def send_chat_message(request: CommandRequest) -> CommandResponse:
    """Handles incoming chat messages and executes action plans.

    If the request contains an explicit action plan, it is executed directly.
    Otherwise, the message is forwarded to the Gemini AI for dynamic conversation
    and potential tool execution.
    """
    return await chat_service.process_message(
        session_id=request.SessionID, user_message=request.Message, action_plan=request.action_plan, mode=request.mode
    )


@app.post("/api/event/{event_type}")
async def handle_event(event_type: str, payload: Dict[str, Any] = Body(...)) -> Dict[str, str]:
    """Handles system events from the Blender Addon (connect, disconnect, undo)."""
    session_id = payload.get("SessionID")
    if not session_id:
        return {"status": "error", "message": "SessionID is required"}

    logger.info(f"Received event '{event_type}' for session {session_id}")
    # Handle events
    if event_type == "connect":
        chat_service.handle_connect(session_id)
    elif event_type == "disconnect":
        chat_service.handle_disconnect(session_id)
    elif event_type == "undo":
        # Logic to handle an undo event
        logger.info(
            f"Undo event received for session {session_id}. State synchronization logic should be implemented here."
        )

    return {"status": "ok"}
