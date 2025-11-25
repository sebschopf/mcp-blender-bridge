import logging
import os  # Added import os
import subprocess
import sys

import bpy

from . import (
    mcp_client,
    preferences,  # Import preferences module
    server_manager,
)

logger = logging.getLogger(__name__)

_mcp_client_instance = None
_attempt_connection = None
_poll_mcp_controller = None


def initialize_operators(attempt_conn_func, poll_func):
    global _attempt_connection, _poll_mcp_controller
    _attempt_connection = attempt_conn_func
    _poll_mcp_controller = poll_func


class WM_OT_MCP_OpenLog(bpy.types.Operator):
    bl_label = "Open Server Log"
    bl_idname = "wm.mcp_open_log"
    bl_description = "Opens the log file of the MCP Server for debugging."

    def execute(self, context):
        log_file_path = os.path.join(bpy.app.tempdir, "mcp_server_log.txt")
        if os.path.exists(log_file_path):
            try:
                if sys.platform == "win32":
                    os.startfile(log_file_path)
                else:
                    # Basic cross-platform fallback
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.Popen([opener, log_file_path])
                self.report({"INFO"}, f"Opened log file: {log_file_path}")
            except Exception as e:
                self.report({"ERROR"}, f"Failed to open log file: {e}")
        else:
            self.report({"WARNING"}, "Log file not found. Server might not have been started yet.")
        return {"FINISHED"}


class MCP_OT_RefreshModels(bpy.types.Operator):
    bl_label = "Refresh Models"
    bl_idname = "mcp.refresh_models"
    bl_description = "Fetch available Gemini models from the server"

    def execute(self, context):
        global _mcp_client_instance
        if _mcp_client_instance is None:
            self.report({"ERROR"}, "MCP Client not initialized. Connect first.")
            return {"CANCELLED"}

        try:
            # We need to access the private method or add a public one.
            # For now, we'll add a public method to MCPClient in a moment.
            # Assuming mcp_client.get_available_models() exists or using internal request
            models = _mcp_client_instance.get_available_models()

            if models:
                # Update the cache in preferences
                new_items = []
                for m in models:
                    # Tuple format: (identifier, name, description)
                    new_items.append((m, m, f"Gemini Model: {m}"))

                # Update the cache on the class
                preferences.MCPAddonPreferences._available_models_cache = new_items
                self.report({"INFO"}, f"Found {len(models)} models.")
            else:
                self.report({"WARNING"}, "No models found or server error.")
        except Exception as e:
            self.report({"ERROR"}, f"Failed to refresh models: {e}")
            return {"CANCELLED"}

        return {"FINISHED"}


class WM_OT_MCP_Connect(bpy.types.Operator):
    bl_label = "Connect to MCP"
    bl_idname = "wm.mcp_connect"
    bl_description = "Starts the local MCP Server and establishes a connection."

    def execute(self, context):
        global _mcp_client_instance

        # Retrieve preferences via context, handling potential key differences
        addon_prefs = None
        keys_to_try = [__package__, "blender_addon", "addon"]

        for key in keys_to_try:
            if key in context.preferences.addons:
                addon_prefs = context.preferences.addons[key].preferences
                break

        if addon_prefs is None:
            # Fallback for headless testing where preferences might be injected on the class
            try:
                api_key = preferences.MCPAddonPreferences.api_key
                controller_python_path = preferences.MCPAddonPreferences.controller_python_path
                port = getattr(preferences.MCPAddonPreferences, "port", 8000)
                # If these are PropertyGroups/PropertyDefinitions (not strings/ints), then we are in real Blender
                # and failed to find prefs.
                if isinstance(api_key, bpy.types.Property) or isinstance(api_key, tuple):
                    logger.error("Could not find addon preferences in context.")
                    bpy.ops.wm.mcp_show_message("INVOKE_DEFAULT", message="Error: Could not find addon preferences.")
                    return {"CANCELLED"}
            except AttributeError:
                logger.error("Could not find addon preferences in context or on class.")
                bpy.ops.wm.mcp_show_message("INVOKE_DEFAULT", message="Error: Could not find addon preferences.")
                return {"CANCELLED"}
        else:
            api_key = addon_prefs.api_key
            controller_python_path = addon_prefs.controller_python_path
            port = addon_prefs.port

        logger.info(f"[DEBUG] addon_prefs retrieved: {addon_prefs}")
        # Retrieve model selection
        selected_model = getattr(addon_prefs, "selected_model", "gemini-1.5-flash")
        logger.info(f"[DEBUG] selected_model (raw): {selected_model}")

        if selected_model == "Custom":
            custom_model = getattr(addon_prefs, "custom_model_name", "")
            logger.info(f"[DEBUG] custom_model: {custom_model}")
            if not custom_model:
                bpy.ops.wm.mcp_show_message("INVOKE_DEFAULT", message="Error: Custom model name is empty.")
                return {"CANCELLED"}
            model_to_use = custom_model
        else:
            model_to_use = selected_model
        logger.info(f"[DEBUG] model_to_use: {model_to_use}")

        logger.info(f"Initializing MCP Client on port {port}...")
        _mcp_client_instance = mcp_client.MCPClient(port=port)

        logger.info(f"Attempting to connect to MCP Controller with model {model_to_use}...")
        if server_manager.start_server(api_key, controller_python_path, port, model=model_to_use):
            context.scene.mcp_connection_status = "CONNECTING"  # type: ignore
            # Clear history and add initial system message
            context.scene.mcp_chat_history.clear()
            item = context.scene.mcp_chat_history.add()
            item.message = "System: Connecting..."
            item.role = "SYSTEM"

            bpy.app.timers.register(_attempt_connection)
        return {"FINISHED"}  # type: ignore


class WM_OT_MCP_Disconnect(bpy.types.Operator):
    bl_label = "Disconnect from MCP"
    bl_idname = "wm.mcp_disconnect"
    bl_description = "Stops the MCP Server and closes the connection."

    def execute(self, context):
        logger.info("Attempting to disconnect from MCP Controller...")
        server_manager.stop_server()
        context.scene.mcp_connection_status = "DISCONNECTED"  # type: ignore
        if bpy.app.timers.is_registered(_poll_mcp_controller):
            bpy.app.timers.unregister(_poll_mcp_controller)
        if bpy.app.timers.is_registered(_attempt_connection):
            bpy.app.timers.unregister(_attempt_connection)
        logger.info("Disconnected from MCP Controller.")
        return {"FINISHED"}  # type: ignore


class WM_OT_MCP_Send_Chat(bpy.types.Operator):
    bl_label = "Send Chat to MCP"
    bl_idname = "wm.mcp_send_chat"
    bl_description = "Sends the typed message to the AI Assistant."

    def execute(self, context):
        message = context.scene.mcp_chat_input  # type: ignore
        mode = context.scene.mcp_llm_mode  # type: ignore
        logger.info(f"Sending message to MCP: {message} (Mode: {mode})")

        item = bpy.context.scene.mcp_chat_history.add()  # type: ignore
        item.message = message
        item.role = "USER"

        # Clear input immediately
        context.scene.mcp_chat_input = ""  # type: ignore

        # Feedback message (optional, maybe just clearing input is enough)
        # item = bpy.context.scene.mcp_chat_history.add()
        # item.message = "Thinking..."
        # item.role = 'SYSTEM'

        def handle_complete(response_data):
            # Response handling logic is mostly in _handle_chat_response,
            # but here we could do operator-specific cleanup if needed.
            logger.info("Async chat completed.")

        _mcp_client_instance.async_send_chat_message(message, mode=mode, on_complete=handle_complete)

        return {"FINISHED"}  # type: ignore


class WM_OT_MCP_ShowMessage(bpy.types.Operator):
    bl_label = "MCP Message"
    bl_idname = "wm.mcp_show_message"
    message: bpy.props.StringProperty(name="Message")  # Added name for clarity and consistency

    def execute(self, context):
        self.report({"INFO"}, self.message)
        return {"FINISHED"}  # type: ignore
