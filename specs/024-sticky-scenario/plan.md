# Implementation Plan - 024-sticky-scenario

**Feature**: Sticky Scenario Routing
**Status**: DRAFT

## Technical Context

### Architecture Overview

The goal is to make the scenario selection (from Feature 022) persistent within a session. Currently, `ChatService` re-evaluates the intent for every message. We want to "lock in" the scenario until the user explicitly changes it.

**Existing Components:**
- `ChatService` (`controller/app/services.py`): Manages session history and routing. Currently stores `active_sessions` as `{session_id: [messages]}`. This needs to change to store state.
- `router.md`: The prompt for classification. Needs to know about "exiting" or "resetting" context.

**New Components:**
- **Session State Structure**: `{ "history": List[ChatMessage], "active_scenario": Optional[str] }`.

### Libraries & Dependencies

- No new libraries.

### Project Structure

```text
controller/
  app/
    services.py            # Modify: Update active_sessions structure and process_message logic
  resources/
    llm_prompts/
      router.md            # Modify: Add 'reset' intent
```

## Constitution Check

### Privacy & Security
- **Data Handling**: Storing `active_scenario` is minimal metadata. Safe.
- **Safety**: Improves consistency of LLM behavior, reducing unexpected "I cannot do that" errors.

### Technical Constraints
- **Backward Compatibility**: `active_sessions` change is internal to `ChatService` (in-memory), so no DB migration needed. But we must ensure existing code reading `self.active_sessions[id]` (if any outside methods do) is updated or the structure is backward compatible. *Check*: `active_sessions` is private-ish, used only in `services.py`.

## Phase 0: Research & Decisions

### Design Decisions

1.  **State Storage**: Change `active_sessions` value from `List[ChatMessage]` to `Dict` or a `SessionData` object. For simplicity, `Dict` is fine: `{"history": [], "scenario": None}`.
2.  **Router Logic**:
    - If `scenario` is set: Skip routing *unless* we implement a "check for exit" logic.
    - *Refined Decision*: It's safer to ALWAYS route but give the router context, OR simple heuristic.
    - *Chosen Path*: **Always Route** but with a new intent `reset`/`cancel`. If router returns `contextual` (default) or same intent, keep sticking. If router returns `reset` or a *different specific* scenario with high confidence, switch.
    - *Actually, simpler*: If we are in a scenario (e.g., `prop`), short messages like "make it red" will likely be classified as `contextual` or `prop`. If `contextual`, we should **keep** the active scenario `prop`. Only switch if a **new** specific intent is detected or `reset`.

## Phase 1: Design & Contracts

### API Changes

- None external.

## Phase 2: Implementation

### Dependencies

- Feature 022 (Router).

### Strategy

1.  **Router Update**: Update `router.md` to include `reset` intent (e.g., "stop", "new task").
2.  **Service Refactor**: Update `ChatService` to store `active_scenario`.
    - Update `handle_connect`, `handle_disconnect`.
    - Update `process_message` to handle the state machine:
        - `new_intent = classify()`
        - `if new_intent == 'reset': active_scenario = None`
        - `elif new_intent != 'contextual': active_scenario = new_intent`
        - `final_scenario = active_scenario or 'contextual'`

## Phase 3: Polish

- Verify "Make it red" (likely `contextual`) keeps `prop` active.