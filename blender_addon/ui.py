import textwrap

import bpy


def draw_multiline_label(layout, text, icon="NONE", width=40):
    """Draws a label with text wrapped to a specific width (in characters).

    This simulates a multi-line label which layout.label() does not support.
    """
    lines = textwrap.wrap(text, width=width)

    # Create a column to stack the lines
    col = layout.column(align=True)

    for i, line in enumerate(lines):
        # Only show icon on the first line if provided
        icon_to_use = icon if i == 0 else "NONE"
        col.label(text=line, icon=icon_to_use)


class MCP_PT_Panel(bpy.types.Panel):
    bl_label = "Gemini MCP"
    bl_idname = "MCP_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Gemini MCP"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        addon_prefs = context.preferences.addons[__package__].preferences

        import os

        api_key_set = bool(addon_prefs.api_key) or bool(os.environ.get("GEMINI_API_KEY"))
        python_path_set = bool(addon_prefs.controller_python_path)

        if not api_key_set or not python_path_set:
            box = layout.box()
            box.label(text="Gemini API Key or Controller Python Path not configured.", icon="INFO")
            box.label(text="Please go to Edit > Preferences > Add-ons > MCP Gemini Assistant to set them.")
            # Disable connect button if preferences are not set
            layout.operator("wm.mcp_connect", text="Connect", icon="PLAY").enabled = False
            return

        status = scene.mcp_connection_status  # type: ignore

        # Connection Status
        row = layout.row()
        row.label(text="Status:")

        if status == "CONNECTED":
            row.label(text="Connected", icon="LINKED")
        elif status == "CONNECTING":
            row.label(text="Connecting...", icon="TIME")
        elif status == "CONNECTION_FAILED":
            row.label(text="Connection Failed", icon="ERROR")
        else:  # DISCONNECTED
            row.label(text="Disconnected", icon="UNLINKED")

        # Connect/Disconnect Buttons
        row = layout.row()
        if status == "CONNECTED":
            row.operator("wm.mcp_disconnect", text="Disconnect", icon="PAUSE")
        elif status == "CONNECTING":
            row.operator("wm.mcp_disconnect", text="Cancel", icon="CANCEL")
        elif status == "CONNECTION_FAILED":
            row.operator("wm.mcp_connect", text="Retry Connection", icon="FILE_REFRESH")
        else:  # DISCONNECTED
            row.operator("wm.mcp_connect", text="Connect", icon="PLAY")

        # Console Toggle Button (Helpful for debugging)
        row = layout.row()
        row.operator("wm.console_toggle", text="Toggle System Console", icon="CONSOLE")
        row.operator("wm.mcp_open_log", text="Open Server Log", icon="TEXT")

        # Chat History (only if connected or connecting)
        if status == "CONNECTED" or status == "CONNECTING":
            layout.separator()
            box = layout.box()
            box.label(text="Chat History:")

            if len(scene.mcp_chat_history) == 0:
                box.label(text="Waiting for instructions...", icon="INFO")
            else:
                # Display only the last 10 messages to avoid clutter
                # Iterate through the collection
                history = scene.mcp_chat_history
                start_index = max(0, len(history) - 10)

                # Try to estimate character width based on region width
                # Standard default is roughly 30-40 chars.
                # context.region.width is in pixels.
                # Approx 7-8 pixels per char on average?
                try:
                    # Provide a safe fallback if region is not accessible
                    char_width = int(context.region.width / 9)
                    if char_width < 20:
                        char_width = 20  # Minimum width
                except Exception:
                    char_width = 35

                for i in range(start_index, len(history)):
                    item = history[i]

                    # Use a sub-box or column for each message to group them visually
                    msg_col = box.column(align=True)

                    if item.role == "USER":
                        # For user, we can just label "You:" then the message
                        msg_col.label(text="You:", icon="USER")
                        # Indent the message slightly
                        sub = msg_col.row()
                        sub.separator()
                        draw_multiline_label(sub, item.message, icon="NONE", width=char_width)

                    elif item.role == "AI":
                        msg_col.label(text="AI:", icon="OUTLINER_OB_LIGHT")
                        sub = msg_col.row()
                        sub.separator()
                        draw_multiline_label(sub, item.message, icon="NONE", width=char_width)

                    else:  # SYSTEM
                        draw_multiline_label(msg_col, item.message, icon="INFO", width=char_width)

                    # Add a small spacer between messages
                    box.separator()

            layout.separator()

            # LLM Mode Selector
            row = layout.row(align=True)
            row.prop(scene, "mcp_llm_mode", text="")

            row = layout.row(align=True)
            row.prop(scene, "mcp_chat_input", text="")
            # Enable send button only if connected (not just connecting)
            sub = row.row()
            sub.enabled = status == "CONNECTED"
            sub.operator("wm.mcp_send_chat", text="Send")


class MCP_ChatHistoryItem(bpy.types.PropertyGroup):
    message: bpy.props.StringProperty(name="Message", description="Chat message content")
    role: bpy.props.EnumProperty(
        name="Role",
        description="The sender of the message",
        items=[
            ("USER", "User", "Message from the user"),
            ("AI", "AI", "Message from the AI"),
            ("SYSTEM", "System", "System message"),
        ],
        default="SYSTEM",
    )
