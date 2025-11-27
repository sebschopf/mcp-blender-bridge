import logging
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from . import globals
from .bridge_api import BridgeCommand, bridge_manager
from .models import SaveRecipeRequest

logger = logging.getLogger(__name__)

mcp = FastMCP("BlenderController", dependencies=["bpy"])

TYPE_MAPPING = {
    "string": str,
    "str": str,
    "float": float,
    "int": int,
    "integer": int,
    "boolean": bool,
    "bool": bool,
    "array": list,
    "list": list,
    "dict": dict,
    "tuple": list,
    "vector": list,
}


async def execute_tool_logic(tool_name: str, **kwargs) -> str:
    # Construct script
    args_str_parts = []
    for k, v in kwargs.items():
        if isinstance(v, str):
            args_str_parts.append(f"{k}='{v}'")
        else:
            args_str_parts.append(f"{k}={v}")

    args_str = ", ".join(args_str_parts)
    script = f"{tool_name}({args_str})"

    cmd = BridgeCommand(type="execute_script", payload={"script": script})
    result = await bridge_manager.execute_command(cmd)

    if result.status == "success":
        return str(result.data.get("output", "Success"))
    else:
        return f"Error: {result.error_message}"


# --- Meta Tools for RAG ---


@mcp.tool()
async def search_tools(query: str) -> str:
    """Searches for available Blender tools based on a natural language query.

    Returns a list of relevant tools with their descriptions and usage signatures.

    Args:
        query: The search query (e.g., "create a cube", "rotate object").
    """
    ke = globals.get_knowledge_engine()
    if not ke:
        return "Error: KnowledgeEngine not initialized."

    results = ke.search_tools(query)
    if not results:
        logger.info(f"Search for '{query}' returned NO results.")
        return "No tools found matching your query."

    output = []
    for res in results:
        output.append(f"- Name: {res.name}")
        output.append(f"  Description: {res.description}")
        output.append(f"  Usage: {res.usage}")
        output.append("")

    result_str = "\n".join(output)
    logger.info(f"Search for '{query}' returned {len(results)} results. First: {results[0].name}")
    return result_str


@mcp.tool()
async def execute_command(tool_name: str, params: Dict[str, Any]) -> str:
    """Executes a specific Blender tool found via search_tools.

    Args:
        tool_name: The exact name of the tool (e.g., "bpy.ops.mesh.primitive_cube_add").
        params: A dictionary of parameters for the tool (e.g., {"size": 2.0}).
    """
    ke = globals.get_knowledge_engine()
    if not ke:
        return "Error: KnowledgeEngine not initialized."

    # Validate tool existence
    tool_def = ke.get_tool(tool_name)
    if not tool_def:
        return f"Error: Tool '{tool_name}' not found in allowed capabilities."

    # --- VALIDATION START ---
    allowed_params = tool_def.params.keys() if tool_def.params else []
    provided_params = params.keys()
    
    # Check for unknown parameters
    unknown_params = [p for p in provided_params if p not in allowed_params]
    
    if unknown_params:
        # Construct a helpful error message
        msg = f"Error: The following parameters are not valid for '{tool_name}': {', '.join(unknown_params)}.\n"
        if allowed_params:
            msg += f"Allowed parameters are: {', '.join(sorted(allowed_params))}.\n"
        else:
            msg += "This tool takes no parameters (or none are documented).\n"
        msg += "Please use 'inspect_tool' to verify parameter names and types."
        return msg

    # Check for required parameters
    # (assuming tool_def.params values are ToolParameter objects with a 'required' attribute)
    missing_required = []
    if tool_def.params:
        for p_name, p_def in tool_def.params.items():
            if getattr(p_def, 'required', False) and p_name not in params:
                 missing_required.append(p_name)
    
    if missing_required:
        return f"Error: Missing required parameters for '{tool_name}': {', '.join(missing_required)}."
    # --- VALIDATION END ---

    return await execute_tool_logic(tool_name, **params)


@mcp.tool()
async def inspect_tool(tool_name: str) -> str:
    """Queries Blender to get detailed information about a specific tool's parameters at runtime.

    Use this when you know the tool name but need to know its exact parameters (names, types, defaults).

    Args:
        tool_name: The exact name of the tool (e.g., "bpy.ops.mesh.primitive_cube_add").
    """
    cmd = BridgeCommand(type="get_rna_info", payload={"tool_name": tool_name})
    result = await bridge_manager.execute_command(cmd)

    if result.status == "success":
        data = result.data.get("rna_info")
        if not data:
            return f"Error: No info returned for {tool_name}"

        # Format readable output
        output = [f"Tool: {data.get('name')} ({tool_name})", f"Description: {data.get('description')}", "Parameters:"]

        for prop in data.get("properties", []):
            p_str = f"  - {prop['identifier']} ({prop['type']}): {prop.get('description', '')}"
            output.append(p_str)

        return "\n".join(output)
    else:
        return f"Error: {result.error_message}"


@mcp.tool()
async def save_recipe(name: str, description: str, steps: List[Dict[str, Any]]) -> str:
    """Saves a sequence of steps as a reusable recipe in the knowledge base.

    Args:
        name: A unique name for the recipe (e.g. "Wooden Table").
        description: What the recipe does.
        steps: A list of steps, where each step has 'operation' (tool name) and 'params' (dict).
    """
    ke = globals.get_knowledge_engine()
    if not ke:
        return "Error: KnowledgeEngine not initialized."

    # Validate input
    try:
        req = SaveRecipeRequest(name=name, description=description, steps=steps)
    except Exception as e:
        return f"Error validating recipe: {e}"

    # Format for YAML
    recipe_data = {
        "name": req.name,
        "category": "internal",
        "version": "1.0",
        "tags": ["user-created"],
        "description": req.description,
        "steps": req.steps,
        "parameters": [],  # User defined params support could be added later
    }

    if ke.save_recipe(recipe_data):
        # Force re-indexing or simple addition
        # For now, save_recipe adds it to memory too, so it should be searchable immediately if re-indexed
        # Ideally KnowledgeEngine.save_recipe handles the memory update.
        return f"Recipe '{name}' saved successfully."
    else:
        return f"Error saving recipe '{name}'."


@mcp.tool()
async def get_scene_state() -> str:
    """Returns the current list of objects in the Blender scene."""
    cmd = BridgeCommand(type="get_state", payload={})
    result = await bridge_manager.execute_command(cmd)
    if result.status == "success":
        import json

        return json.dumps(result.data.get("scene_state", []), indent=2)
    else:
        return f"Error: {result.error_message}"


@mcp.tool()
async def submit_script(script: str) -> str:
    """Submits a complete Python script for execution in Blender.

    This is the PREFERRED method for performing multiple actions or complex tasks.
    The script allows you to maintain context (variables) between steps.

    Args:
        script: A valid, safe Python script using 'bpy'.
    """
    from .validation import validate_bpy_script

    # 1. Security Validation
    is_valid, error_msg = validate_bpy_script(script)
    if not is_valid:
        return f"Security Error: Script rejected.\nDetails: {error_msg}"

    # 2. Execution
    cmd = BridgeCommand(type="execute_script", payload={"script": script})
    result = await bridge_manager.execute_command(cmd)

    if result.status == "success":
        return str(result.data.get("output", "Success: Script executed."))
    else:
        return f"Runtime Error: {result.error_message}"


# --- Registration ---


def register_tools():
    """Registers only the meta-tools by default.

    Specific tools are no longer registered individually to save tokens.
    """
    # Meta tools (search_tools, execute_command, get_scene_state, inspect_tool, save_recipe)
    # are registered via decorators.
    logger.info("Registered meta-tools (search_tools, execute_command, get_scene_state, inspect_tool, save_recipe).")


@mcp.resource("blender://scene/objects")
async def get_scene_objects_resource() -> str:
    """Returns the current list of objects in the Blender scene."""
    return await get_scene_state()
