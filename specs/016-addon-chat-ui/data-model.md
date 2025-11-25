# Data Model: Enhanced Chat

## MCP_ChatHistoryItem

Update the PropertyGroup to support structured data.

```python
class MCP_ChatHistoryItem(bpy.types.PropertyGroup):
    message: bpy.props.StringProperty(name="Message", description="Chat message content")
    role: bpy.props.EnumProperty(
        name="Role",
        description="The sender of the message",
        items=[
            ('USER', "User", "Message from the user"),
            ('AI', "AI", "Message from the AI"),
            ('SYSTEM', "System", "System message"),
        ],
        default='SYSTEM'
    )
```
