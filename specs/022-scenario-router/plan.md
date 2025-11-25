# Implementation Plan - 022-scenario-router

**Feature**: Intelligent LLM Scenario Routing System
**Status**: DRAFT

## Technical Context

### Architecture Overview

The goal is to introduce a "Scenario Router" (or Intent Classifier) step *before* the main conversation loop. This allows the system to switch from a generic "Contextual" mode to a specialized, high-guidance "Scenario" mode based on the user's request.

**Existing Components:**
- `GeminiClient` (`controller/app/gemini_client.py`): Needs a lightweight method for single-shot classification.
- `ChatService` (`controller/app/services.py`): Needs logic to call the classifier and then load the appropriate scenario prompt.
- `Prompt Templates` (`controller/resources/llm_prompts/`): Will host the router prompt and the scenario definitions.

**New Components:**
- `IntentRouter`: Logic within `ChatService` (or a helper) to map the user's message to a scenario ID.
- `Scenario Definitions`: New markdown files in `controller/resources/llm_prompts/scenarios/`.

### Libraries & Dependencies

- **No new libraries required**. Reusing `google-generativeai` via `GeminiClient`.

### Project Structure

```text
controller/
  app/
    services.py            # Update: Add routing logic in process_message
    gemini_client.py       # Update: Add simple_generate() method
  resources/
    llm_prompts/
      router.md            # New: System prompt for classification
      scenarios/           # New: Directory for scenario prompts
        character.md       # New: Scenario for characters
        architecture.md    # New: Scenario for architecture
        prop.md            # New: Scenario for props
        scripting.md       # New: Scenario for coding tasks
```

## Constitution Check

### Privacy & Security
- **Data Handling**: User prompt is sent to LLM for classification. Standard API usage.
- **Safety**: Scenarios provide *stricter* control over LLM output, improving safety by reducing hallucinations.

### Technical Constraints
- **Latency**: Adding a classification step adds latency. The classification call must be fast (using `gemini-1.5-flash` or similar lightweight model/config) and minimal token usage.
- **Fallback**: If classification fails, fallback to "Contextual" (default).

## Phase 0: Research & Decisions

### Design Decisions

1.  **Classification Mechanism**: Use a single-shot LLM call with a strict JSON output schema (or structured text) to determine the intent.
    - *Input*: User message.
    - *Output*: `{"intent": "character", "confidence": 0.9}`.
2.  **Prompt Storage**:
    - Router prompt: `router.md`.
    - Scenarios: Subdirectory `scenarios/` to keep things organized.
3.  **Integration Point**: In `ChatService.process_message`, if `mode` is "contextual" (default), we attempt to refine it via routing. If the user explicitly selected "format-to-bpy" (via the UI selector from feature 021), we might skip routing or use a specific "scripting" scenario. *Decision: UI selection overrides router for now, or router refines "Contextual". Let's make the Router run if `mode == 'contextual'`.*

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

- **ScenarioConfig**: Internal struct `{ id: str, prompt_path: str, description: str }`.

### API Changes (`contracts/`)

- No external API changes. The routing happens server-side. The client still sends `mode="contextual"`.

## Phase 2: Implementation

### Dependencies

- Feature 021 (UI Mode Selector) is a prerequisite for the `mode` parameter handling, which is already done.

### Strategy

1.  **Gemini Update**: Add `simple_generate(prompt, system_instruction)` to `GeminiClient` for non-chat, single-turn tasks.
2.  **Prompts**: Create `router.md` and the initial set of scenario prompts (`character.md`, etc.).
3.  **Service Logic**: In `ChatService`, implement `classify_intent(user_message)`.
4.  **Integration**: Update `process_message` to call `classify_intent` and load the corresponding scenario prompt instead of the generic `contextual.md`.

## Phase 3: Polish

- Tuning the `router.md` to avoid false positives.
- Ensuring the "Scenario" prompts are robust (using the lessons from `format-to-bpy`).