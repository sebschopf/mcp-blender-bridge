import ast
import re
from typing import List, Tuple

FORBIDDEN_MODULES = {"os", "subprocess", "socket", "ctypes", "multiprocessing"}

operator_regex = re.compile(r"bpy\.ops\.([a-zA-Z0-9_\.]+)")

def validate_syntax(script: str) -> Tuple[bool, str]:
    """Return (is_valid, error_message) using ast.parse"""
    try:
        ast.parse(script)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"

def detect_forbidden_imports(script: str) -> List[str]:
    """Return list of forbidden module names imported in the script."""
    try:
        tree = ast.parse(script)
    except Exception:
        return []

    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split(".")[0]
                if name in FORBIDDEN_MODULES:
                    found.add(name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split(".")[0]
                if name in FORBIDDEN_MODULES:
                    found.add(name)

    return sorted(found)


FORBIDDEN_CALLS = {
    "exec",
    "eval",
    "compile",
    "open",
    "__import__",
    "execfile",
    "os.system",
    "os.popen",
    "subprocess.run",
    "subprocess.Popen",
    "socket",
}


def detect_forbidden_calls(script: str) -> List[str]:
    """Return list of forbidden call patterns detected in the AST of the script.

    This detects direct uses of builtin `open`, `eval`, `exec`, as well as attribute
    calls like `subprocess.run` or `os.system` where possible.
    """
    try:
        tree = ast.parse(script)
    except Exception:
        return []

    found = set()

    for node in ast.walk(tree):
        # Detect calls to names like open(), eval(), exec()
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                name = func.id
                if name in FORBIDDEN_CALLS:
                    found.add(name)
            elif isinstance(func, ast.Attribute):
                # e.g., subprocess.run or os.system
                parts = []
                cur = func
                while isinstance(cur, ast.Attribute):
                    parts.insert(0, cur.attr)
                    cur = cur.value
                if isinstance(cur, ast.Name):
                    parts.insert(0, cur.id)

                full = ".".join(parts)
                # Check against forbidden patterns
                for pat in FORBIDDEN_CALLS:
                    if pat.endswith("*"):
                        if full.startswith(pat[:-1]):
                            found.add(full)
                    else:
                        if full == pat:
                            found.add(full)

    return sorted(found)


def validate_script(script: str) -> Tuple[bool, List[str], List[str]]:
    """High-level validation combining syntax, forbidden imports, and forbidden calls.

    Returns (is_valid, errors, warnings).
    """
    errors: List[str] = []
    warnings: List[str] = []

    ok, err = validate_syntax(script)
    if not ok:
        errors.append(err)
        return False, errors, warnings

    forbidden_imports = detect_forbidden_imports(script)
    if forbidden_imports:
        errors.append(f"Forbidden imports: {', '.join(forbidden_imports)}")

    forbidden_calls = detect_forbidden_calls(script)
    if forbidden_calls:
        errors.append(f"Forbidden calls/usages: {', '.join(forbidden_calls)}")

    return (len(errors) == 0), errors, warnings

def find_bpy_operators(script: str) -> List[str]:
    """Return a list of operator full names detected (e.g. 'mesh.primitive_cube_add')."""
    return operator_regex.findall(script)

def verify_operators_with_inspect(operator_list: List[str], inspect_caller) -> List[Tuple[str, bool, str]]:
    """Verify operators by calling `inspect_caller(tool_name)`.

    `inspect_caller` should be a callable that accepts a full operator name and returns
    a dict-like result or raises on unknown operator. This function returns a list of
    tuples: (operator_name, exists_bool, message)
    """
    results = []
    for op in operator_list:
        try:
            info = inspect_caller(op)
            # If the caller returns a dict with 'error' key it's invalid
            if not info:
                results.append((op, False, "No info returned"))
            else:
                results.append((op, True, "OK"))
        except Exception as e:
            results.append((op, False, str(e)))
    return results
