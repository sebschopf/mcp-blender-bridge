# Quickstart: Dynamic Model Discovery

This guide covers the new model selection features in the Gemini MCP Addon.

## 1. Setting up API Key (Environment Variable)

If you prefer not to store your API key in Blender preferences:

1.  **Set Environment Variable**:
    -   **Windows**: Set `GEMINI_API_KEY` in your user environment variables.
    -   **macOS/Linux**: Add `export GEMINI_API_KEY='your_key'` to your `.bashrc` or `.zshrc`.
2.  **Blender Configuration**:
    -   Leave the "Gemini API Key" field **empty** in the addon preferences.
    -   The addon will automatically use the system variable.

## 2. Selecting a Model

1.  **Open Preferences**: Go to `Edit > Preferences > Add-ons > MCP Gemini Assistant`.
2.  **Refresh Models**:
    -   Click the **"Refresh Models"** button.
    -   The addon will query your controller (which talks to Google's API) to find compatible models.
3.  **Choose a Model**:
    -   Select your preferred model from the dropdown list (e.g., `gemini-1.5-pro`).
    -   Select **"Custom"** to manually enter a model name if it's not listed.

## 3. Using Custom Models

1.  Select **"Custom"** in the model dropdown.
2.  A new text field "Custom Model Name" will appear.
3.  Enter the full model ID (e.g., `models/gemini-1.5-flash-001`).
