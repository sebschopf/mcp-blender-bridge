# Inject BPY Workflow (Controller) — Overview

This document describes the controlled workflow for generating, validating, sandboxing and optionally executing Blender Python scripts produced by an LLM.

Actors
- LLM: Generates script or formatted output.
- Controller (this repo): Receives LLM output, validates, audits, and runs sandbox.
- Bridge/API: Executes scripts in Blender (via addon) when execution is confirmed.

High-level flow
1. LLM returns content in `format-to-bpy` mode (fenced Python block preferred).
2. Controller extracts the script with `script_extractor.extract_script_from_response`.
3. Validator (`bpy_validator`) runs checks:
   - `ast.parse` syntax check
   - Forbidden imports detection
   - Operator detection (`bpy.ops.*`) and `inspect_tool` verification
4. Sandbox runner executes script in isolation (Docker+Blender or local simulation). Results captured.
5. Controller returns preview (extraction, validation, sandbox logs). User must explicitly confirm to perform live execution.
6. On confirmation, the controller routes the script to the bridge for live execution in Blender.

Testing & Debugging
- Use `controller/tests/test_end_to_end_flow.py` for a preview flow smoke test.
- To simulate `inspect_tool` responses, use `controller/tests/test_inspect_integration.py`.
- Logs and audit artifacts are stored under `controller/logging` and `controller/logs/`.

Security Notes
- Live execution is blocked unless sandbox succeeded and the user explicitly confirmed.
- The validator blocks system-level imports and detects file/network access attempts.
