import bpy


class MCPAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    api_key: bpy.props.StringProperty(
        name="Gemini API Key",
        description="Your API key for accessing the Gemini AI. If you don't have one, create it here: https://aistudio.google.com/app/apikey. Keep this confidential.",
        subtype="PASSWORD",
    )

    controller_python_path: bpy.props.StringProperty(
        name="Controller Python Path",
        description="Absolute path to the Python executable in the controller's virtual environment. \nExamples: \n- Windows: C:\\path\\to\\project\\controller\\.venv\\Scripts\\python.exe \n- macOS/Linux: /path/to/project/controller/.venv/bin/python",
        subtype="FILE_PATH",
    )

    port: bpy.props.IntProperty(
        name="Controller Port",
        description="The port on which the MCP Controller FastAPI server will run.",
        default=8000,
        min=1024,
        max=65535,
    )

    # Cache for available models to avoid fetching on every draw
    _available_models_cache = [("gemini-2.0-flash-lite", "gemini-2.0-flash-lite (Default)", "")]

    def get_model_items(self, context):
        items = MCPAddonPreferences._available_models_cache.copy()
        items.append(("Custom", "Custom...", "Enter a model name manually"))
        return items

    selected_model: bpy.props.EnumProperty(
        name="Model",
        description="Select the Gemini model to use.",
        items=get_model_items,
        default=0,
    )

    custom_model_name: bpy.props.StringProperty(
        name="Custom Model Name",
        description="Enter the full model name (e.g. models/gemini-1.5-pro-001)",
        default="",
    )

    request_timeout: bpy.props.IntProperty(
        name="Request Timeout (s)",
        description="Timeout in seconds for AI requests. Increase if you experience timeouts with complex tasks.",
        default=60,
        min=5,
        max=300,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key")
        layout.prop(self, "controller_python_path")
        layout.prop(self, "port")
        layout.prop(self, "request_timeout")

        layout.separator()
        layout.label(text="Model Configuration")
        row = layout.row()
        row.prop(self, "selected_model")
        row.operator("mcp.refresh_models", text="", icon="FILE_REFRESH")

        if self.selected_model == "Custom":
            layout.prop(self, "custom_model_name")
