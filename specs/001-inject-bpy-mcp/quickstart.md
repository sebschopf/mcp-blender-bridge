# Quickstart: Inject BPY Script (001-inject-bpy-mcp)

This quickstart explains how to manually test the Inject BPY feature locally and the expected sandbox behaviour.

Prerequisites
- A working Python environment with project deps installed (see `controller/requirements.txt`).
- Optional: Docker + Blender headless image for real sandbox runs. If Docker is not available, a local simulation will run and detect syntax/runtime errors but will not execute Blender operators.

Manual test steps
1. Start the controller (FastAPI) per repo instructions (e.g., `python -m controller.app.main`).
2. Use the `preview_bpy` tool via MCP or call the FastAPI endpoint that triggers the `preview_bpy` tool. Example parameters:
   - `mode`: `format-to-bpy`
   - `script_or_text`: the LLM response containing a fenced Python code block (```python ... ```)
3. Expected flow:
   - The controller extracts the script from the response.
   - Syntax validation (`ast.parse`) runs.
   - Heuristic checks detect forbidden imports and `bpy` operator usage.
   - For each detected operator, the controller attempts to call `inspect_tool` to verify parameters. If `inspect_tool` is unavailable, preview will still proceed but include a warning.
   - The script is executed in the sandbox runner (Docker/Blender if available; otherwise local python simulation) and stdout/stderr are returned.
4. If sandbox run succeeds, the preview response indicates `status: ok`. The UI or caller must request explicit user confirmation to perform live execution.

Failure modes
- If extraction fails (no code detected), the preview returns `status: error` with a message.
- If syntax or forbidden imports are detected, the preview returns `status: invalid` with reasons.
- If `inspect_tool` explicitly returns an operator-not-found error, the preview rejects the script.
- If sandbox times out or fails, preview returns `sandbox_failed` with logs.

Notes for developers
- The prompt templates are in `controller/resources/llm_prompts/` (`contextual.md`, `format-to-bpy.md`).
- The validator skeleton is in `controller/validators/bpy_validator.py`.
- Sandbox runners are under `controller/bridge_runner/`.
