# Research: Migration to google-genai

## 1. Migration Overview

The `google-generativeai` library is deprecated. The new `google-genai` SDK introduces a client-based architecture.

## 2. Key Mappings

### Initialization
**Old:**
```python
import google.generativeai as genai
genai.configure(api_key=KEY)
model = genai.GenerativeModel('model-name')
```

**New:**
```python
from google import genai
client = genai.Client(api_key=KEY)
# Model access is now via client methods
```

### Chat Session
**Old:**
```python
chat = model.start_chat(history=...)
response = chat.send_message(prompt)
```

**New:**
```python
chat = client.chats.create(model='model-name', history=..., config=...)
response = chat.send_message(prompt)
```

### Function Calling
**Old:**
```python
fc = response.candidates[0].content.parts[0].function_call
name = fc.name
args = fc.args
```

**New:**
The response structure is similar but typed.
```python
for part in response.candidates[0].content.parts:
    if part.function_call:
        name = part.function_call.name
        args = part.function_call.args
```

### Types
The new SDK uses types in `google.genai.types`.
- `types.Content`
- `types.Part`
- `types.GenerateContentConfig` (for tools)

## 3. Decisions

- **Decision**: Use `client.chats.create` as it is the standard way to handle conversations in the new SDK.
- **Decision**: Inject `api_key` and `model_name` into `GeminiClient` to allow for better testing (mocking the client) and flexibility.
- **Decision**: Maintain the manual function execution loop to minimize logic changes in `plan_executor.py` and ensure strict control over execution order.

## 4. Alternatives Considered

- **Alternative**: Use `client.models.generate_content` for everything.
    - **Rationale for Rejection**: We need to maintain conversational state (history), which `chats.create` handles natively.
- **Alternative**: Use automatic tool execution provided by the SDK.
    - **Rationale for Rejection**: This would require significantly refactoring `internal_tools` and `plan_executor`. It's safer to keep the execution logic explicit for now.
