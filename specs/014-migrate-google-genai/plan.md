# Implementation Plan - Migrate to google-genai Library

## 1. Technical Context

**Language/Framework**: Python 3.11+, FastAPI (Controller), `google-genai` (SDK).
**Dependencies**:
- `google-genai` (New dependency)
- `uv` (Package management)
- `pytest` (Testing)

**Existing Components**:
- `GeminiClient` in `controller/app/gemini_client.py`: Needs significant refactoring.
- `main.py`: Initializes `GeminiClient`, needs to handle dependency injection if not automated.
- `requirements.txt`: Update dependencies.

**Constraints**:
- Must support `generateContent` and tool calling.
- Must maintain environment variable configuration for API Key and Model.
- Must pass all existing tests (after updates).

## 2. Constitution Check

- [x] **I. Strict MCP Architecture**: Migration of the client does not change the MCP architecture. The Controller still manages the AI communication.
- [x] **II. Conversational Interface**: The conversational flow logic is preserved, just the underlying library changes.
- [x] **III. Granular & Secure Tools**: Tool definitions remain unchanged; only their registration with the SDK changes.
- [x] **IV. User-Centric Control**: No change to user control mechanisms.
- [x] **V. Blender-Native Integration**: Controller-side change only, transparent to Blender.
- [x] **VI. Continuous Validation**: The plan includes running tests to verify the migration.

## 3. Gates

- [x] **Gate 1: Authorization**: Feature `014-migrate-google-genai` approved.
- [x] **Gate 2: Research**: Migration path and new SDK usage are documented in official guides. (See Phase 0).
- [x] **Gate 3: Constitution**: Checked above.

## Phase 0: Outline & Research

### 0.1 Research Tasks
- [x] **Task**: Research the specific method mappings between `google-generativeai` and `google-genai`.
    - `genai.configure` -> `genai.Client(api_key=...)`
    - `model.start_chat` -> `client.chats.create`
    - `response.candidates[0].content.parts[0].function_call` -> `part.function_call`
- [x] **Task**: Verify the exact import name (`google.genai`).

### 0.2 Output
- **Artifact**: `specs/014-migrate-google-genai/research.md`

## Phase 1: Design & Contracts

### 1.1 Data Model Changes
- No persistent data model changes.
- In-memory `ActionPlan` and `ChatMessage` remain standard Pydantic models.
- **Note**: The internal representation of chat history for the SDK call will change.

### 1.2 API Contract Updates
- No changes to the external REST API contracts (`/api/chat`, `/api/models`).
- The internal `GeminiClient` "contract" (public methods) remains stable, but implementation changes.

### 1.3 Agent Context Update
- Update `gemini_client` related context to reflect the new SDK usage.

### 1.4 Output
- **Artifact**: `specs/014-migrate-google-genai/data-model.md` (likely empty or noting no changes).
- **Artifact**: `specs/014-migrate-google-genai/quickstart.md` (Updated setup instructions if needed).

## Phase 2: Implementation

### 2.1 Dependency Update
- **Step 1**: Modify `requirements.txt` (remove `google-generativeai`, add `google-genai`).
- **Step 2**: Run `uv pip install -r requirements.txt`.

### 2.2 Refactoring `GeminiClient`
- **Step 3**: Update `gemini_client.py` imports.
- **Step 4**: Rewrite `__init__` for Dependency Injection and Client initialization.
- **Step 5**: Rewrite `list_available_models`.
- **Step 6**: Rewrite `run_dynamic_conversation` using `client.chats.create` and new response parsing logic.

### 2.3 Testing & Validation
- **Step 7**: Update `controller/tests/test_main.py` to mock `google.genai.Client`.
- **Step 8**: Update `controller/tests/test_new_tools.py`.
- **Step 9**: Run full test suite `pytest controller/`.

### 2.4 Cleanup
- **Step 10**: Verify no legacy code remains.