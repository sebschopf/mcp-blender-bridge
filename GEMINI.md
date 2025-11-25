# MCP_Blender_02 Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-16

## Active Technologies
- Python 3.11+ + FastAPI, PyYAML, Pydantic (010-dual-inventory-architecture)
- Filesystem (YAML files) (010-dual-inventory-architecture)
- Python 3.11+ (Addon & Controller) (012-dynamic-model-discovery)
- Blender Preferences (`bpy.types.AddonPreferences`) for selected model and API key. (012-dynamic-model-discovery)
- Python 3.11+ (Addon & Controller) + `bpy` (Blender Python API) (013-chat-ui-improvements)
- Blender `Scene` properties (temporary runtime state) (013-chat-ui-improvements)
- Python 3.11+ (Addon & Controller) + `bpy`, `fastapi` (013-chat-ui-improvements)
- Blender `Scene` properties (temporary runtime state), `globals.py` (backend singleton) (013-chat-ui-improvements)
- [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION] + [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION] (017-migrate-mcp-standard)
- [if applicable, e.g., PostgreSQL, CoreData, files or N/A] (017-migrate-mcp-standard)
- Python 3.11+ + FastAPI, mcp SDK, uvicorn (017-migrate-mcp-standard)
- N/A (in-memory queues/maps for bridge communication) (017-migrate-mcp-standard)
- Python 3.11+ + FastAPI, mcp SDK, Pydantic (no new heavy ML deps) (018-dynamic-tool-retrieval)
- In-memory Inverted Index (018-dynamic-tool-retrieval)
- YAML files for recipes (019-add-inspect-tool)
- Python 3.11+ (as seen in `controller/pyproject.toml`) + FastAPI, Pydantic, `google-genai`, `mcp` SDK (Controller); `bpy` (Addon). (029-solid-responsibility-audit)
- N/A (In-memory state or YAML configs for capabilities). (029-solid-responsibility-audit)



## Project Structure

```text
src/
tests/
```

## Commands

# Add commands for 

## Code Style

General: Follow standard conventions

## Recent Changes
- 029-solid-responsibility-audit: Added Python 3.11+ (as seen in `controller/pyproject.toml`) + FastAPI, Pydantic, `google-genai`, `mcp` SDK (Controller); `bpy` (Addon).
- 019-add-inspect-tool: Added Python 3.11+ + FastAPI, mcp SDK, Pydantic
- 018-dynamic-tool-retrieval: Added Python 3.11+ + FastAPI, mcp SDK, Pydantic (no new heavy ML deps)



## AI Prompting Guidelines

Your primary function is to act as an intelligent orchestrator to help users create in Blender. You MUST follow a strict, token-efficient, multi-step process.

**Step 1: Discover Categories**

-   For any creative request, your **first** action MUST be to call the `discover_categories()` tool to get the list of available tool categories.

**Step 2: Discover Relevant Tools**

-   Based on the user's request and the list of categories, determine which categories are relevant.
-   Your **second** action MUST be to call the `discover_capabilities(category="...")` tool for **each** relevant category. This allows you to gather the specific tools you need without loading the entire library.

**Step 3: Plan and Submit**

-   Once you have the necessary tools, construct a multi-step `ActionPlan`.
-   Your **final** action MUST be to call the `submit_action_plan()` tool, passing the plan you just created.

You do not have direct access to Blender. Your only purpose is to call these tools in the correct order.







<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
