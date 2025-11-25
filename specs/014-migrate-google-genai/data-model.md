# Data Model

No changes to the persistent data model are required for this migration.

## In-Memory Structures

The `GeminiClient` will internally use `google.genai.types` for chat history management, converting from the application's `ChatMessage` Pydantic model.

### Chat History Conversion

**From:**
```python
ChatMessage(source="USER", content="Hello")
```

**To:**
```python
types.Content(
    role="user",
    parts=[types.Part.from_text(text="Hello")]
)
```
