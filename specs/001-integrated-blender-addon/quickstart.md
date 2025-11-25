# Quickstart: Integrated Blender Addon

This guide provides the steps to install, configure, and use the integrated Gemini MCP addon in Blender.

## 1. Installation

1.  **Download the Addon**: Obtain the `blender_addon.zip` file from the project's releases.
2.  **Install in Blender**:
    -   Open Blender.
    -   Go to `Edit > Preferences > Add-ons`.
    -   Click `Install...` and select the `blender_addon.zip` file.
    -   Find "MCP Gemini Assistant" in the list and enable the checkbox.

## 2. Configuration

Before you can use the assistant, you need to configure two settings in the addon preferences.

1.  **Expand the Addon**: In the Add-ons list, expand the "MCP Gemini Assistant" panel.
2.  **Set Controller Python Path**:
    -   This field requires the full path to the Python executable inside the `controller`'s virtual environment.
    -   **Example (Windows)**: `C:\path\to\your\project\controller\.venv\Scripts\python.exe`
    -   **Example (macOS/Linux)**: `/path/to/your/project/controller/.venv/bin/python`
3.  **Set Gemini API Key**:
    -   Paste your Gemini API key into this field. The key will be stored securely in your Blender preferences.
4.  **Save Preferences**: Click `Save Preferences` at the bottom of the window.

## 3. Usage

1.  **Open the MCP Panel**: In the 3D Viewport, press the `N` key to open the sidebar. You will see a new tab labeled "MCP Gemini".
2.  **Start the Server**:
    -   If the addon is configured correctly, you will see an "Activate MCP" button.
    -   Click it to start the server. The status will change to "Starting..." and then "Active".
3.  **Chat with Gemini**:
    -   Once the server is active, a chat box will appear.
    -   Type your request (e.g., "Create a cube and move it up by 2 units") and press Enter.
    -   The conversation will appear in the history panel, and the commands will be executed in Blender.
4.  **Stop the Server**:
    -   When you are finished, click the "Deactivate MCP" button.
    -   The server will shut down, and the addon will become inactive. The server will also shut down automatically when you close Blender.
