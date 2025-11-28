"""Utility to inject mock bpy module for testing."""
from ..bridge_runner.sandbox_runner import run_in_sandbox
from ..logging.bpy_audit import audit_record
from ..validators.bpy_validator import detect_forbidden_imports, find_bpy_operators, validate_syntax
from ..validators.script_extractor import extract_script_from_response
from .mcp_server import inspect_tool as mcp_inspect_tool
from .mcp_server import mcp


@mcp.tool()
async def inject_bpy_script(mode: str, script_or_text: str) -> str:
    """Handler to accept LLM responses and perform extraction, validation and sandbox run.

    Args:
        mode: 'format-to-bpy' or 'contextual'
        script_or_text: raw LLM output containing code or description
    """
    request = {
        "mode": mode,
        "script_or_text": script_or_text,
    }

    # 1) extract
    script = extract_script_from_response(script_or_text) if mode == 'format-to-bpy' else None
    if not script:
        return "Error: Could not extract Python script from input."

    # 2) syntax
    ok, err = validate_syntax(script)
    if not ok:
        audit_record({"stage": "syntax", "error": err, "request": request})
        return f"Validation failed: {err}"

    # 3) forbidden imports
    forbidden = detect_forbidden_imports(script)
    if forbidden:
        audit_record({"stage": "forbidden_imports", "forbidden": forbidden, "request": request})
        return f"Validation failed: forbidden imports detected: {forbidden}"

    # 4) find operators and verify via `inspect_tool`
    ops = find_bpy_operators(script)

    inspect_results = []
    for op in ops:
        try:
            # mcp_inspect_tool is async; call and await it
            info_str = await mcp_inspect_tool(op)
            # `inspect_tool` returns strings like 'Error: ...' on failure
            if isinstance(info_str, str) and info_str.startswith("Error:"):
                inspect_results.append({"op": op, "ok": False, "message": info_str})
            else:
                inspect_results.append({"op": op, "ok": True, "message": "OK"})
        except Exception as e:
            inspect_results.append({"op": op, "ok": False, "message": str(e)})

    # If any operator verification failed, reject
    failed_ops = [r for r in inspect_results if not r.get("ok")]
    if failed_ops:
        audit_record({"stage": "inspect_failed", "failed": failed_ops, "request": request})
        msgs = ", ".join([f"{f['op']}: {f['message']}" for f in failed_ops])
        return f"Validation failed: operator inspection failed: {msgs}"

    audit_record({"stage": "pre_sandbox", "operators": ops, "inspect_results": inspect_results, "request": request})

    # 5) sandbox run (simulation)
    sandbox_res = run_in_sandbox("req-local", script)
    audit_record({"stage": "sandbox", "sandbox_res": sandbox_res, "request": request})

    if not sandbox_res.get("success"):
        return f"Sandbox execution failed: {sandbox_res.get('stderr') or sandbox_res.get('error')}"

    return "Sandbox execution succeeded. Preview available; user confirmation required for live execution."
