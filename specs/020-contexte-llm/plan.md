# Implementation Plan - 020-contexte-llm

**Feature**: Contexte LLM pour Blender
**Status**: DRAFT

## Technical Context

### Architecture Overview

This feature enhances the Controller layer by introducing dynamic context management for the LLM. It intercepts the chat flow to inject specialized system prompts based on the user's intent (Contextual chat vs. BPY script generation). It also adds a validation layer for generated Python code before it is presented to the user.

**Existing Components:**
- `GeminiClient` (`controller/app/gemini_client.py`): Currently initializes with a static system prompt. Needs modification to accept per-request overrides.
- `ChatService` (`controller/app/services.py`): Manages the conversation flow. Needs logic to determine the mode and select the appropriate prompt template.
- `mcp_server.py`: Exposes tools. Likely needs to expose the new validation capabilities or be used by the validator (via `inspect_tool`).

**New Components:**
- `PromptManager`: A simple utility to load and format templates from `controller/resources/llm_prompts/`.
- `BPYValidator`: A service to validate syntax and basic `bpy` usage of generated scripts.

### Libraries & Dependencies

- **Python Standard Library**: `ast` (for syntax validation).
- **Existing**: `google-generativeai` (for Gemini interaction), `pydantic` (for data models).
- **New**: No new external dependencies required.

### Project Structure

```text
controller/
  app/
    gemini_client.py       # Modify: add system_instruction override
    services.py            # Modify: logic for mode selection
    validation.py          # New: BPYValidator logic
  resources/
    llm_prompts/           # New Directory
      contextual.md        # New: Template for contextual chat
      format-to-bpy.md     # New: Template for script generation
```

## Constitution Check

### Privacy & Security
- **Data Handling**: User prompts are sent to LLM. No change in data sensitivity.
- **Safety**:
  - **Critical**: Generated BPY scripts can be dangerous.
  - **Mitigation**: FR-009 mandates "Validate in sandbox + require user confirmation". We will implement the validation (syntax check) and ensure the UI/Controller flow requires explicit user confirmation before execution.

### Technical Constraints
- **Performance**: Validation must be fast (NFR-001 < 2s). `ast.parse` is extremely fast.
- **Scalability**: Templates are static files, negligible overhead.

## Phase 0: Research & Decisions

### Resolution of Unknowns

- **How to inject system prompt dynamically?**
  - *Decision*: `GenerativeModel.generate_content` and chat sessions support `system_instruction` at initialization. For `google-generativeai`, we might need to re-initialize the `ChatSession` or `GenerativeModel` if the system prompt changes, or use the `system_instruction` argument if supported per-call (API dependent).
  - *Research Task*: Verify if `google-generativeai` Python SDK allows overriding system instructions on an existing chat session or requires a new session/model instance.
  - *Fallback*: If per-call override isn't supported on existing chat, we instantiate a new lightweight client/model wrapper for the specific request.

### Design Decisions

1.  **Prompt Storage**: Markdown files in `controller/resources/llm_prompts/`.
2.  **Validation**: `ast.parse` for syntax, regex/heuristic for `bpy.ops` existence (checking against a known list or `inspect_tool` cache).

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

- `BPYScript`: Wrapper for generated code `{ code: str, valid: bool, errors: list[str] }`.
- `PromptMode`: Enum `['contextual', 'format-to-bpy']`.

### API Changes (`contracts/`)

- `POST /chat`: Add optional `mode` parameter (default `contextual`).
- `POST /validate-script`: (Internal/Dev) Endpoint to test validation logic.

## Phase 2: Implementation

### Dependencies

1.  **Validation Logic**: Must be robust before we trust LLM output.
2.  **Prompt Templates**: Must be refined to ensure LLM adheres to them.

### Strategy

1.  **Foundation**: Create the prompt directory and files. Implement the `GeminiClient` update (solving the "dynamic system prompt" research task first).
2.  **Logic**: Implement `BPYValidator` (pure function).
3.  **Integration**: Wire `ChatService` to use Validator and PromptManager.
4.  **Test**: Unit tests for validator; E2E test for "Generate a cube" -> Script.

## Phase 3: Polish

- Tuning the prompts based on failure rates.
- Improving error messages for invalid scripts.