from typing import Any, Dict
from .mcp_server import mcp

from ..validators.script_extractor import extract_script_from_response
from ..validators.bpy_validator import validate_syntax, detect_forbidden_imports, find_bpy_operators
from ..bridge_runner.sandbox_runner import run_in_sandbox


@mcp.tool()
async def preview_bpy(mode: str, script_or_text: str) -> Dict[str, Any]:
    """Return a structured preview: extraction, validation, operator inspection, sandbox run.

    This is a read-only preview to show results before user confirmation.
    """
    result: Dict[str, Any] = {"mode": mode}

    # Extract
    script = extract_script_from_response(script_or_text) if mode == "format-to-bpy" else None
    result["extracted_script"] = script
    if not script:
        result["status"] = "error"
        result["error"] = "Could not extract Python script from input"
        return result

    # Syntax
    ok, err = validate_syntax(script)
    result["syntax_ok"] = ok
    result["syntax_error"] = err
    if not ok:
        result["status"] = "invalid"
        return result

    # Forbidden imports
    forbidden = detect_forbidden_imports(script)
    result["forbidden_imports"] = forbidden
    if forbidden:
        result["status"] = "invalid"
        return result

    # Operators
    ops = find_bpy_operators(script)
    result["operators_detected"] = ops

    # Inspect each operator using mcp.inspect_tool
    inspect_results = []
    from .mcp_server import inspect_tool as mcp_inspect_tool

    inspect_available = True
    for op in ops:
        try:
            info = await mcp_inspect_tool(op)
            if isinstance(info, str) and info.startswith("Error:"):
                # explicit operator-not-found -> fail preview
                inspect_results.append({"op": op, "ok": False, "message": info})
            else:
                inspect_results.append({"op": op, "ok": True, "message": "OK"})
        except Exception as e:
            # Bridge/inspect not available in this environment; record and continue
            inspect_available = False
            inspect_results.append({"op": op, "ok": None, "message": str(e)})

    result["inspect_results"] = inspect_results
    # If any operator explicitly returned an error from inspect_tool, reject.
    if any(r.get("ok") is False for r in inspect_results):
        result["status"] = "invalid"
        return result

    # If inspect is unavailable, include a warning but continue preview (sandbox may still catch runtime issues)
    result["inspect_available"] = inspect_available

    # Sandbox run (local simulation)
    sandbox = run_in_sandbox("preview-local", script)
    result["sandbox"] = sandbox

    result["status"] = "ok" if sandbox.get("success") else "sandbox_failed"
    return result
