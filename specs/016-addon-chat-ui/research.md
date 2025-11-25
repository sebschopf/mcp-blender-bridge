# Research: Addon Chat UI

## 1. Current Implementation
- `MCP_ChatHistoryItem` has only a `message` field (StringProperty).
- The UI iterates through messages and draws them using `box.label(text=item.message)`.
- Currently, "You: " and "AI: " prefixes are hardcoded into the message string when added (in `operators.py` for user, and `mcp_client.py` for AI).

## 2. Decisions
- **Decision**: Add a `role` field to `MCP_ChatHistoryItem`. This allows cleaner UI logic (e.g., using different icons or alignments) rather than parsing string prefixes.
- **Decision**: Keep the N-panel simple. Use `layout.box()` for the container, and `column` for messages. Use icons to distinguish roles.

## 3. Alternatives
- **UIList**: Good for scrolling long lists, but adds complexity (requires operators for index management). For a chat log, a simple slice in `draw` is simpler and "good enough" for the N-panel.
