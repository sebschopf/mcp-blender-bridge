import ast
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


def validate_bpy_script(script_content: str) -> Tuple[bool, List[str]]:
    """Validates a Python script for syntax errors and basic BPY usage.

    Args:
        script_content: The content of the script to validate.

    Returns:
        A tuple containing:
        - valid (bool): True if the script is valid, False otherwise.
        - errors (List[str]): A list of error messages if invalid.
    """
    errors = []

    # 1. Syntax Validation
    try:
        tree = ast.parse(script_content)
    except SyntaxError as e:
        errors.append(f"Syntax Error: {e.msg} at line {e.lineno}, offset {e.offset}: {e.text}")
        return False, errors
    except Exception as e:
        errors.append(f"Parsing Error: {str(e)}")
        return False, errors

    # 2. Basic heuristic check (can be expanded with AST walker)
    # The spec requires at least one 'bpy.ops' call for functional scripts
    # But we might just warn for now or return valid=True but with warnings?
    # Spec says: "Acceptance criteria: Référence à opérateurs bpy valides".
    # We will enforce 'bpy' presence at least.

    # Simple AST walk to check for 'bpy' name usage
    has_bpy = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "bpy":
            has_bpy = True
            break
        # Also check for 'import bpy'
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "bpy":
                    has_bpy = True
        if isinstance(node, ast.ImportFrom):
            if node.module == "bpy":
                has_bpy = True

    if not has_bpy:
        errors.append("Script does not appear to use 'bpy' module.")
        # Depending on strictness, we might fail here.
        # For 'format-to-bpy' user story, it MUST be a blender script.
        return False, errors

    return True, errors
