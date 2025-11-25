# Specification: Migrate to google-genai Library

## 1. Overview

### 1.1 Goal
Migrate the project's dependency from the deprecated `google-generativeai` library to the new `google-genai` SDK. This migration aims to align with Google's latest recommended practices, ensure long-term support, and improve code quality by adhering to SOLID principles, specifically Dependency Injection.

### 1.2 Core Value
- **Sustainability**: Ensures the application continues to function after the deprecation of the old library (Nov 30, 2025).
- **Maintainability**: Adopts a cleaner, more modular architecture supported by the new SDK.
- **Robustness**: Leverages the improved client architecture for better session and tool management.

### 1.3 Success Criteria
- [ ] The `google-generativeai` package is removed from `requirements.txt`.
- [ ] The `google-genai` package is added to `requirements.txt`.
- [ ] `GeminiClient` class handles initialization via Dependency Injection (API Key, Model Name).
- [ ] `GeminiClient` uses the new `client.chats.create` pattern for conversations.
- [ ] All existing unit tests in `controller/tests/` pass without modification to the test logic itself (only setup if needed).
- [ ] The application successfully starts and connects to the Gemini API using the new SDK.

## 2. User Stories

### 2.1 As a Developer
I want to use the supported `google-genai` library
So that the project remains maintainable and compatible with future Google API updates.

**Acceptance Criteria:**
- The project builds and installs dependencies using `uv` without errors.
- The `google-generativeai` library is no longer a direct dependency.
- The code uses `google.genai.Client` instead of `google.generativeai.GenerativeModel` (legacy usage).

### 2.2 As a Maintainer
I want the `GeminiClient` to follow SOLID principles
So that testing and future refactoring are easier.

**Acceptance Criteria:**
- `GeminiClient` constructor accepts `api_key` and `model_name` as optional arguments.
- Configuration is not hardcoded or implicitly global; it relies on the injected or environment-derived values within the instance.

## 3. Functional Requirements

### 3.1 Dependency Management
- **FR 3.1.1**: Replace `google-generativeai` with `google-genai` in `controller/requirements.txt`.
- **FR 3.1.2**: Update `uv.lock` to reflect dependency changes.

### 3.2 GeminiClient Refactoring
- **FR 3.2.1**: Update `GeminiClient.__init__` to initialize `google.genai.Client`.
- **FR 3.2.2**: Implement `GeminiClient.list_available_models` using `client.models.list()`.
- **FR 3.2.3**: Update `GeminiClient.run_dynamic_conversation` to use `client.chats.create`.
- **FR 3.2.4**: Adapt the tool calling logic to compatible with the new SDK's response structure (`types.Content`, `types.Part`, etc.).

### 3.3 Test Updates
- **FR 3.3.1**: Update test mocks in `controller/tests/test_main.py` and `controller/tests/test_new_tools.py` to match the new `GeminiClient` structure and `google-genai` objects.

## 4. Technical Considerations

### 4.1 Migration Specifics
- The new SDK uses a `Client` object as the entry point.
- Chat history formatting changes from `{"role": "user", "parts": [...]}` to `types.Content` objects or compatible dicts required by the new SDK.
- Function calling handling (parsing `function_call` from response) might differ in the new `GenerateContentResponse` object.

### 4.2 Security
- API Keys must continue to be managed via environment variables (`GEMINI_API_KEY`) or passed securely via constructor.
- No secrets should be logged during the migration process.

## 5. Assumptions
- The `google-genai` library supports all features currently used (chat, function calling, model listing).
- The Gemini API backend behavior remains consistent for the models used (`gemini-1.5-flash-001`, etc.).
- The environment configuration (`.env`) structure remains unchanged.

## 6. Out of Scope
- Adding new features or tools to the AI.
- changing the Blender Addon code (this is a controller-side change only).