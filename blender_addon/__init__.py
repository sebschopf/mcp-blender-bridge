bl_info = {
    "name": "Gemini MCP Integration",
    "author": "Gemini",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Gemini MCP",
    "description": "Integrates Blender with a Gemini-powered MCP Controller",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}

import logging

import bpy
import bpy.app.timers

# Configure logging for Blender Addon
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from . import (  # noqa: E402
    command_executor,
    mcp_client,  # Import mcp_client to access bridge_client
    operators,
    preferences,
    server_manager,
    ui,
)


def attempt_connection():
    """Timer function that attempts to connect to the server."""
    # Initialize retry counter if it doesn't exist
    if not hasattr(attempt_connection, "retries"):
        attempt_connection.retries = 0

    if bpy.context.scene.mcp_connection_status != "CONNECTING":  # type: ignore
        attempt_connection.retries = 0  # Reset counter if stopped externally
        return None  # Stop the timer if we are no longer trying to connect

    logger.info(f"Attempting to connect (Attempt {attempt_connection.retries + 1}/5)...")
    response = operators._mcp_client_instance.send_event("connect")

    if response and response.get("status") == "ok":
        bpy.context.scene.mcp_connection_status = "CONNECTED"  # type: ignore
        bpy.app.timers.register(poll_mcp_controller)

        # Start the BridgeClient for polling commands
        mcp_client.bridge_client.start()

        logger.info("Connected to MCP Controller.")

        # Inject connection success message
        item = bpy.context.scene.mcp_chat_history.add()  # type: ignore
        item.message = "System: Connected. Waiting for AI..."

        attempt_connection.retries = 0  # Reset counter
        return None  # Stop this timer, connection successful

    attempt_connection.retries += 1
    if attempt_connection.retries >= 5:
        logger.error("Failed to connect to MCP Controller after 5 attempts.")
        bpy.context.scene.mcp_connection_status = "CONNECTION_FAILED"  # type: ignore

        # Inject failure message
        item = bpy.context.scene.mcp_chat_history.add()  # type: ignore
        item.message = "System: Connection Failed."

        bpy.ops.wm.mcp_show_message("INVOKE_DEFAULT", message="Connection failed. Check System Console for details.")
        attempt_connection.retries = 0  # Reset for next time
        return None  # Stop the timer

    return 3.0  # Retry every 3 seconds


# Timer for periodic polling
def poll_mcp_controller():
    # Polling is currently disabled to prevent spamming the LLM with 'poll_for_commands'
    # until a dedicated polling endpoint is implemented on the controller.
    return None

    # if bpy.context.scene.mcp_connection_status == 'CONNECTED':  # type: ignore
    #     logger.info("Polling MCP Controller...")
    #     response = operators._mcp_client_instance.send_chat_message("poll_for_commands") # Placeholder for actual polling endpoint

    #     if response:
    #         # Check for error status
    #         if response.get("status") == "ERROR":
    #             logger.error(f"MCP Controller returned error: {response.get('AiMessage')}")
    #             bpy.context.scene.mcp_connection_status = 'CONNECTION_FAILED'  # type: ignore
    #
    #             # Inject failure message into chat
    #             item = bpy.context.scene.mcp_chat_history.add() # type: ignore
    #             item.message = f"System Error: {response.get('AiMessage')}"
    #
    #             # Stop the timer
    #             return None

    #         if response.get("Commands"):
    #             for cmd_data in response["Commands"]:
    #                 command_executor.execute_bpy_script(cmd_data['script'])

    #         # Update chat history
    #         if response and response.get("AiMessage"):
    #             bpy.context.scene.mcp_chat_history.add().message = f"AI: {response['AiMessage']}"  # type: ignore
    #     else:
    #         # Network error handling (optional, could stop polling after N failures)
    #         pass

    # return 1.0 # Poll every 1 second


def undo_post_handler(scene):
    logger.info("Undo event detected.")
    operators._mcp_client_instance.send_event("undo")


# List of all classes that need to be registered
# The order matters for dependencies
CLASSES = (
    preferences.MCPAddonPreferences,
    ui.MCP_ChatHistoryItem,
    ui.MCP_PT_Panel,
    operators.WM_OT_MCP_Connect,
    operators.WM_OT_MCP_Disconnect,
    operators.WM_OT_MCP_Send_Chat,
    operators.WM_OT_MCP_ShowMessage,
    operators.WM_OT_MCP_OpenLog,
    operators.MCP_OT_RefreshModels,
)


def register():
    """Registers all addon classes and properties."""
    # Register classes
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    # Initialize operators with necessary instances/functions
    operators.initialize_operators(attempt_connection, poll_mcp_controller)

    # Register scene properties
    bpy.types.Scene.mcp_chat_input = bpy.props.StringProperty(  # type: ignore
        name="MCP Chat Input",
        description="Enter your prompt for the MCP AI",
        default="",
    )
    bpy.types.Scene.mcp_connection_status = bpy.props.EnumProperty(  # type: ignore
        name="MCP Connection Status",
        description="The current status of the connection to the MCP Controller.",
        items=[
            ("DISCONNECTED", "Disconnected", "Not connected to the server."),
            ("CONNECTING", "Connecting", "Attempting to connect to the server."),
            ("CONNECTED", "Connected", "Connected to the server."),
            ("CONNECTION_FAILED", "Connection Failed", "Failed to connect to the server."),
        ],
        default="DISCONNECTED",
    )
    bpy.types.Scene.mcp_llm_mode = bpy.props.EnumProperty(  # type: ignore
        name="LLM Mode",
        description="Select the mode for LLM interaction",
        items=[
            ("contextual", "Contextual (Chat)", "Chat with the AI to get advice and execute tools"),
            ("format-to-bpy", "Script Generation", "Generate and validate a Python script for the requested task"),
        ],
        default="contextual",
    )
    bpy.types.Scene.mcp_chat_history = bpy.props.CollectionProperty(type=ui.MCP_ChatHistoryItem)  # type: ignore

    # Register handlers
    bpy.app.handlers.undo_post.append(undo_post_handler)

    # Register atexit handler for server cleanup
    import atexit

    atexit.register(server_manager.stop_server)

    logger.info("Gemini MCP Addon registered successfully.")


def unregister():
    """Unregisters all addon classes, properties, and handlers."""
    logger.info("Unregistering Gemini MCP Addon.")

    # Stop BridgeClient
    mcp_client.bridge_client.stop()

    # Unregister handlers
    if undo_post_handler in bpy.app.handlers.undo_post:
        bpy.app.handlers.undo_post.remove(undo_post_handler)
    if bpy.app.timers.is_registered(poll_mcp_controller):
        bpy.app.timers.unregister(poll_mcp_controller)

    # Delete scene properties
    del bpy.types.Scene.mcp_chat_input  # type: ignore
    del bpy.types.Scene.mcp_connection_status  # type: ignore
    del bpy.types.Scene.mcp_llm_mode  # type: ignore
    del bpy.types.Scene.mcp_chat_history  # type: ignore

    # Unregister classes in reverse order
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
