import logging

import bpy

logger = logging.getLogger(__name__)


def execute_bpy_script(script: str):
    """Executes a string of Python code using Blender's `exec` context.

    Args:
        script (str): The Python script to execute.

    Raises:
        Exception: If the script execution fails.
    """
    try:
        # The `exec` function is used here to run the bpy commands sent by the
        # controller. This is the core of the MCP's peripheral side. The controller
        # is responsible for ensuring that the script is safe and valid.
        exec(script, {"bpy": bpy})
        logger.info(f"Successfully executed script: {script}")
    except Exception as e:
        logger.error(f"Error executing script '{script}': {e}", exc_info=True)
        # Re-raise the exception so the client can handle it
        raise
