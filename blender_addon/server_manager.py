import logging
import os
import subprocess
import sys
import time  # Added import time

import bpy

logger = logging.getLogger(__name__)

_server_process = None


def start_server(api_key: str, python_path: str, port: int, model: str = "gemini-2.0-flash-lite"):
    global _server_process
    if _server_process is not None and _server_process.poll() is None:
        logger.info("Server is already running.")
        return True

    # Validation is now handled in operators.py before calling start_server
    # if not python_path or not os.path.exists(python_path):
    #     logger.error(f"Invalid Python path: {python_path}")
    #     bpy.ops.wm.mcp_show_message('INVOKE_DEFAULT', message="Error: Controller Python path is not set or invalid.")
    #     return False

    # if not api_key:
    #     logger.error("API Key is not set.")
    #     bpy.ops.wm.mcp_show_message('INVOKE_DEFAULT', message="Error: Gemini API Key is not set.")
    #     return False

    # Construct the command to run the FastAPI server
    # Assuming main.py is in controller/app/
    # The python_path is expected to be the executable within the .venv/Scripts/ folder
    # So, go up two levels to reach the controller directory.
    controller_dir = os.path.abspath(os.path.join(os.path.dirname(python_path), "..", ".."))
    # The package is 'controller', so we need to run from the parent of 'controller_dir'
    project_root = os.path.dirname(controller_dir)

    command = [
        python_path,
        "-m",
        "uvicorn",
        "controller.app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
    ]

    # Set environment variables for the subprocess
    env = os.environ.copy()
    env["GEMINI_API_KEY"] = api_key
    env["GEMINI_MODEL"] = model  # Pass the selected model

    logger.info(f"Starting server with GEMINI_MODEL: {model}")  # Debug log

    # Add project root to PYTHONPATH just in case
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

    # Use creationflags for Windows to prevent a console window
    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP

    # Log file path
    log_file_path = os.path.join(bpy.app.tempdir, "mcp_server_log.txt")

    try:
        logger.info(f"Starting server with command: {' '.join(command)}")
        logger.info(f"Working directory: {project_root}")
        logger.info(f"Server logs will be written to: {log_file_path}")

        # Open log file in append mode
        with open(log_file_path, "w") as log_file:
            _server_process = subprocess.Popen(
                command,
                cwd=project_root,  # Set Working Directory
                env=env,
                creationflags=creationflags,
                stdout=log_file,
                stderr=subprocess.STDOUT,  # Redirect stderr to stdout (log file)
            )

        logger.info(f"Server process started with PID: {_server_process.pid}")

        # Wait a bit to check if it crashes immediately
        time.sleep(0.5)
        if _server_process.poll() is not None:
            # Process died immediately
            with open(log_file_path, "r") as f:
                error_log = f.read()
            logger.error(f"Server process died immediately. Log content:\n{error_log}")
            bpy.ops.wm.mcp_show_message(
                "INVOKE_DEFAULT", message=f"Server failed to start. Check system console or log file: {log_file_path}"
            )
            _server_process = None
            return False

        return True
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        bpy.ops.wm.mcp_show_message("INVOKE_DEFAULT", message=f"Error starting server: {e}")
        _server_process = None
        return False


def stop_server():
    global _server_process
    if _server_process is not None:
        logger.info(f"Stopping server process with PID: {_server_process.pid}")
        _server_process.terminate()
        _server_process.wait(timeout=5)  # Wait for the process to terminate
        if _server_process.poll() is None:
            logger.warning(f"Server process {_server_process.pid} did not terminate gracefully. Killing it.")
            _server_process.kill()
        _server_process = None
        logger.info("Server process stopped.")
        return True
    logger.info("No server process to stop.")
    return False
