# Implementation Plan - 027-non-blocking-gemini

**Feature**: Non-Blocking Gemini API Calls
**Status**: DRAFT

## Technical Context

### Architecture Overview

The `GeminiClient` currently executes synchronous network calls to Google's API inside asynchronous methods. This blocks the Python `asyncio` Event Loop (used by Uvicorn), preventing other concurrent requests (like Blender's polling for commands) from being processed. This leads to deadlocks where the server waits for Blender to execute a command, but Blender cannot receive the command because the server is blocked waiting for Gemini.

**Existing Components:**
- `controller/app/gemini_client.py`: Contains `run_dynamic_conversation`, `simple_generate`, and `list_available_models`, all using synchronous `google.genai` calls.

### Libraries & Dependencies

- **Python Standard Library**: `asyncio` (specifically `asyncio.to_thread`).

### Project Structure

```text
controller/
  app/
    gemini_client.py       # Update: Wrap blocking calls with asyncio.to_thread
```

## Constitution Check

### Privacy & Security
- **Data Handling**: No change.
- **Safety**: Improves server stability and responsiveness.

### Technical Constraints
- **Python Version**: `asyncio.to_thread` is available in Python 3.9+. We are on 3.11+, so it's safe.

## Phase 0: Research & Decisions

### Design Decisions

1.  **Wrapper Method**: We will modify `run_dynamic_conversation`, `simple_generate`, and `list_available_models` to await `asyncio.to_thread(function, *args)`.
2.  **Chat Object**: The `chat` object created by `client.chats.create` is stateful but synchronous. We must ensure `chat.send_message` is the call being threaded.
3.  **Logging**: `PerformanceLogger` context managers should remain *outside* the `to_thread` call if possible, or inside if we want to measure thread time. Since we are measuring the "LLM Call", wrapping the `await asyncio.to_thread(...)` with the logger is correct.

## Phase 1: Design & Contracts

### API Changes

- No external API changes. Internal implementation detail.

## Phase 2: Implementation

### Dependencies

- None.

### Strategy

1.  **Update `gemini_client.py`**:
    - Import `asyncio`.
    - In `run_dynamic_conversation`:
        - Wrap `self.client.chats.create` in `to_thread`.
        - Wrap `chat.send_message` in `to_thread`.
    - In `simple_generate`:
        - Make method `async`. (Note: This requires updating call sites in `services.py`).
        - Wrap `self.client.models.generate_content` in `to_thread`.
    - In `list_available_models`:
        - Make method `async`. (Update call site in `main.py`).
        - Wrap `self.client.models.list` iteration in `to_thread` (or just the list call).

### Refactoring Note
Since `simple_generate` and `list_available_models` are currently synchronous but called from async contexts (in `services.py` and `main.py` respectively), making them `async` is the correct pattern to propagate non-blocking behavior.

## Phase 3: Polish

- Verify that `tests/` still pass (update mocks to be async where needed).