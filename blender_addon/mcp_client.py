import logging
import threading
import time
from typing import Any, Dict, List, Optional

import bpy
import requests

logger = logging.getLogger(__name__)

SYSTEM_MESSAGE_PREFIX = "System: "


class MCPClient:
    def __init__(self, port: int = 8000, max_retries: int = 3, retry_delay: int = 1):
        self.base_url = f"http://127.0.0.1:{port}/api"
        self.session_id = "blender-session-123"  # This should be dynamic in a real app
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _show_message_in_blender(self, message: str, is_error: bool = False) -> None:
        if is_error:
            logger.error(message)
        else:
            logger.info(message)

        def show_once() -> None:
            bpy.ops.wm.mcp_show_message("INVOKE_DEFAULT", message=message)  # type: ignore
            return None  # Unregister timer after it runs once

        # Schedule the operator to run in Blender's main thread
        if not bpy.app.timers.is_registered(show_once):
            bpy.app.timers.register(show_once)

    def _send_request(
        self, method: str, endpoint: str, json_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        # Retrieve timeout from preferences if available
        timeout_duration = 30  # Default
        try:
            addon_prefs = bpy.context.preferences.addons[__package__].preferences
            if endpoint == "chat":
                timeout_duration = addon_prefs.request_timeout
            else:
                timeout_duration = 5  # Keep short timeout for non-chat endpoints
        except Exception:
            # Fallback if preferences not accessible (e.g. during registration or test)
            pass

        for attempt in range(self.max_retries):
            try:
                if method == "post":
                    response = requests.post(f"{self.base_url}/{endpoint}", json=json_data, timeout=timeout_duration)
                elif method == "get":
                    response = requests.get(f"{self.base_url}/{endpoint}", timeout=timeout_duration)
                else:
                    raise ValueError("Unsupported HTTP method")
                response.raise_for_status()
                logger.info(f"Successfully sent {method} request to {endpoint}.")
                return response.json()
            except requests.exceptions.Timeout:
                logger.warning(
                    f"Request to {endpoint} timed out (>{timeout_duration}s). Attempt {attempt + 1}/{self.max_retries}."
                )
                # Don't show a UI message for a timeout, as it's part of the retry loop
            except requests.exceptions.ConnectionError:
                # Only show the connection error on the last attempt
                if attempt == self.max_retries - 1:
                    self._show_message_in_blender("Connection error to MCP Controller.", is_error=True)
                time.sleep(self.retry_delay)
            except requests.exceptions.RequestException as e:
                self._show_message_in_blender(f"Error during request to {endpoint}: {e}", is_error=True)
                return None
        return None

    def get_available_models(self) -> List[str]:
        """Fetches the list of available models from the controller.
        """
        response_data = self._send_request("get", "models")
        if response_data and "models" in response_data:
            return response_data["models"]
        return []

    def execute_commands(self, commands: List[Dict[str, Any]]) -> None:
        """Executes a list of bpy commands sequentially.
        """
        from . import command_executor  # Local import to avoid circular dependency issues

        if not commands:
            return

        logger.info(f"Executing {len(commands)} commands from the controller.")
        for command_data in commands:
            try:
                # Assuming command_data is a dict with 'Script' and 'CommandType'
                command_type: Optional[str] = command_data.get("CommandType")
                script: Optional[str] = command_data.get("Script")

                if command_type == "EXECUTE_BPY":
                    if script:
                        command_executor.execute_bpy_script(script)
                        logger.info(f"Successfully executed script: {script}")
                    else:
                        logger.warning("Received EXECUTE_BPY command with no script.")
                else:
                    logger.warning(f"Unknown command type: {command_type}")
            except Exception as e:
                error_message = f"Error executing command: {command_data}. Error: {e}"
                self._show_message_in_blender(error_message, is_error=True)
                # Stop execution on the first error
                return

    def _send_chat_request_logic(self, message: str, mode: Optional[str] = "contextual") -> Optional[Dict[str, Any]]:
        """Performs the blocking network request for chat.
        Does NOT touch Blender UI or Context.
        """
        payload = {"SessionID": self.session_id, "Message": message, "mode": mode}
        return self._send_request("post", "chat", payload)

    def _handle_chat_response(self, response_data: Optional[Dict[str, Any]]) -> None:
        """Updates Blender UI with the response data.
        MUST be called from the Main Thread.
        """
        if response_data:
            # Display AI message in Blender UI
            ai_message: str = response_data.get("AiMessage", "No message from AI.")
            self._show_message_in_blender(ai_message)

            # Add to chat history
            try:
                item = bpy.context.scene.mcp_chat_history.add()  # type: ignore
                item.message = ai_message
                item.role = "AI"
            except Exception as e:
                logger.error(f"Failed to add AI message to history: {e}")

            # Execute any commands returned by the controller
            commands: List[Dict[str, Any]] = response_data.get("Commands", [])
            if commands:
                self.execute_commands(commands)

    def send_chat_message(self, message: str, mode: Optional[str] = "contextual") -> Optional[Dict[str, Any]]:
        """Synchronous (Blocking) chat request.
        """
        response_data = self._send_chat_request_logic(message, mode)
        self._handle_chat_response(response_data)
        return response_data

    def async_send_chat_message(self, message: str, mode: Optional[str] = "contextual", on_complete=None) -> None:
        """Asynchronous (Threaded) chat request.
        Unblocks Blender Main Thread.
        """

        def worker():
            try:
                response_data = self._send_chat_request_logic(message, mode)

                # Schedule UI update on main thread
                def update_ui():
                    self._handle_chat_response(response_data)
                    if on_complete:
                        on_complete(response_data)
                    return None

                bpy.app.timers.register(update_ui)
            except Exception as e:
                logger.error(f"Async chat error: {e}")
                # Optional: schedule error message

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def send_event(self, event_type: str) -> Optional[Dict[str, Any]]:
        return self._send_request("post", f"event/{event_type}", {"SessionID": self.session_id})


# New BridgeClient implementation
class BridgeClient:
    def __init__(self, port: int = 8000):
        self.base_url = f"http://127.0.0.1:{port}/internal"
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()
        logger.info("BridgeClient polling thread started.")

    def stop(self):
        self.running = False
        if self.thread:
            # We don't join here to avoid blocking UI if thread is sleeping
            self.thread = None
        logger.info("BridgeClient polling thread stopped.")

    def _poll_loop(self):
        while self.running:
            try:
                # Poll with timeout
                response = requests.post(f"{self.base_url}/get_command", timeout=12)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "command":
                        cmd = data["command"]
                        self._handle_command(cmd)
                elif response.status_code == 504:
                    # Timeout on server side, just retry
                    pass
                else:
                    time.sleep(1)
            except requests.exceptions.Timeout:
                # Client timeout, retry
                continue
            except Exception as e:
                logger.error(f"Polling error: {e}")
                time.sleep(5)

    def _handle_command(self, command):
        # We must execute in main thread and get result
        result_container = {}
        done_event = threading.Event()

        def execution_wrapper():
            try:
                # Logic to execute command['type'] with command['payload']
                res_data = self._execute_logic(command)
                result_container["status"] = "success"
                result_container["data"] = res_data
            except Exception as e:
                logger.error(f"Execution error: {e}")
                result_container["status"] = "error"
                result_container["error_message"] = str(e)
            finally:
                done_event.set()

        # Schedule on main thread
        bpy.app.timers.register(lambda: (execution_wrapper(), None)[1])

        # Wait for completion
        done_event.wait()

        # Post result
        result_payload = {
            "command_id": command["id"],
            "status": result_container["status"],
            "data": result_container.get("data"),
            "error_message": result_container.get("error_message"),
        }
        try:
            requests.post(f"{self.base_url}/post_result", json=result_payload, timeout=5)
        except Exception as e:
            logger.error(f"Failed to post result: {e}")

    def _execute_logic(self, command):
        cmd_type = command["type"]
        payload = command["payload"]

        if cmd_type == "execute_script":
            script = payload.get("script")
            # Execute
            from . import command_executor

            msg = command_executor.execute_bpy_script(script)
            return {"output": msg}

        elif cmd_type == "get_state":
            # Return list of objects
            objects = []
            # We need to ensure we access bpy context safely
            for obj in bpy.context.scene.objects:
                objects.append(
                    {
                        "name": obj.name,
                        "type": obj.type,
                        "location": list(obj.location),
                        "rotation": list(obj.rotation_euler),
                        "scale": list(obj.scale),
                    }
                )
            return {"scene_state": objects}

        elif cmd_type == "get_rna_info":
            tool_name = payload.get("tool_name")
            from . import introspection

            data = introspection.extract_properties(tool_name)
            if not data:
                raise ValueError(f"Could not find RNA info for {tool_name}")
            return {"rna_info": data}

        else:
            raise ValueError(f"Unknown command type: {cmd_type}")


# Singleton instance
bridge_client = BridgeClient()
