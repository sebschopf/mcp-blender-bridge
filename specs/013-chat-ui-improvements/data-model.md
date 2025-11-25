# Data Model: Chat UI Improvements

**Feature**: `013-chat-ui-improvements`

## Entities

### MCP_ChatHistoryItem (Update)
- **Context**: Blender Addon (Runtime)
- **Fields**:
    - `message`: StringProperty (Existing)
    - `source`: EnumProperty (New - Optional)
        - Items: `['SYSTEM', 'USER', 'AI']`
        - Default: `SYSTEM`

### UI State (Implicit)
- **Context**: Blender Addon UI
- **Logic**:
    - IF `mcp_connection_status` IN `['CONNECTING', 'CONNECTED']` THEN:
        - Show Chat Box
        - IF `len(mcp_chat_history) == 0`:
            - Show "Waiting for instructions..."
        - ELSE:
            - Render `mcp_chat_history` items

### Globals (Backend)
- **Context**: Controller (Python Memory)
- **Instance**: `knowledge_engine: KnowledgeEngine`
- **Access**: Shared by `main.py` and `internal_tools.py`