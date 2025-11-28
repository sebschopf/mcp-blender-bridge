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
        # Capture active object before execution
        # Use view_layer.objects.active which is more reliable than context.active_object
        prev_active = bpy.context.view_layer.objects.active
        
        # The `exec` function is used here to run the bpy commands sent by the
        # controller. This is the core of the MCP's peripheral side. The controller
        # is responsible for ensuring that the script is safe and valid.
        exec(script, {"bpy": bpy})
        
        # Check active object after execution
        curr_active = bpy.context.view_layer.objects.active
        
        result_msg = f"Successfully executed script: {script}"
        
        # Debug logging to understand why it was failing
        logger.info(f"[DEBUG] prev_active: {prev_active}, curr_active: {curr_active}")
        
        if curr_active and curr_active != prev_active:
            result_msg += f". Created/Selected Object: '{curr_active.name}'"
        elif curr_active:
             # Even if it didn't change, mention the active object to reassure the AI
             result_msg += f". Active Object: '{curr_active.name}'"
            
        logger.info(result_msg)
        return result_msg
        
    except Exception as e:
        logger.error(f"Error executing script '{script}': {e}", exc_info=True)
        # Re-raise the exception so the client can handle it
        raise
