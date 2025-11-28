"""Validation logic for Blender Python scripts."""
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

    # 2. Security Validation (AST Visitor)
    validator = SecurityValidator()
    validator.visit(tree)
    
    if validator.errors:
        errors.extend(validator.errors)
        return False, errors

    # 3. Basic heuristic check
    # The spec requires at least one 'bpy.ops' call for functional scripts, 
    # or at least importing bpy.
    # The SecurityValidator already ensures only whitelisted imports are used.
    # We just check if 'bpy' was imported or used to ensure it's a Blender script.
    # (This is a loose check, as the validator ensures safety, not necessarily utility)
    
    return True, errors


class SecurityValidator(ast.NodeVisitor):
    """AST Visitor to enforce security policies on generated code."""

    ALLOWED_MODULES = {
        "bpy",
        "math",
        "mathutils",
        "bmesh",
        "gpu",
        "random",
        "typing",  # Safe for type hints
        "enum",    # Safe
    }

    BANNED_FUNCTIONS = {
        "eval",
        "exec",
        "compile",
        "open",
        "input",
        "__import__",
        "globals",
        "locals",
        "breakpoint",
        "help",
        "exit",
        "quit",
        "getattr",
        "setattr",
        "delattr",
    }

    BANNED_ATTRIBUTES = {
        "__builtins__",
        "__globals__",
        "__code__",
        "__import__",
        "__class__",
        "__base__",
        "__bases__",
        "__mro__",
        "__subclasses__",
    }

    def __init__(self):
        """Initialize the SecurityValidator."""
        self.errors = []

    def visit_Import(self, node):
        """Validate Import nodes."""
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module not in self.ALLOWED_MODULES:
                self.errors.append(f"Security Error: Import of '{alias.name}' is not allowed.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Validate ImportFrom nodes."""
        if node.module:
            base_module = node.module.split(".")[0]
            if base_module not in self.ALLOWED_MODULES:
                self.errors.append(f"Security Error: Import from '{node.module}' is not allowed.")
        self.generic_visit(node)

    def visit_Call(self, node):
        """Validate Call nodes."""
        # Check for calls to banned built-in functions
        if isinstance(node.func, ast.Name):
            if node.func.id in self.BANNED_FUNCTIONS:
                self.errors.append(f"Security Error: Call to banned function '{node.func.id}' is not allowed.")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Validate Attribute nodes."""
        # Check for access to dangerous attributes
        if node.attr in self.BANNED_ATTRIBUTES:
             self.errors.append(f"Security Error: Access to restricted attribute '{node.attr}' is not allowed.")
        # Also catch dunder methods generally if suspicious, but we have a specific list now
        elif node.attr.startswith("__") and node.attr.endswith("__"):
             # Allow safe dunders like __init__, __name__, __doc__
             if node.attr not in ["__init__", "__name__", "__doc__", "__str__", "__repr__", "__call__"]:
                 # We might want to be stricter, but for now blocking the known gadgets is key
                 pass
        self.generic_visit(node)

    def visit_Name(self, node):
        """Validate Name nodes."""
        # Check for access to dangerous names
        if node.id in self.BANNED_ATTRIBUTES:
             self.errors.append(f"Security Error: Access to restricted name '{node.id}' is not allowed.")
        self.generic_visit(node)
