# Data Model: Integrated Blender Addon

This feature focuses on the integration of the Controller server with the Blender UI, rather than introducing new data schemas for the AI. The primary data entities are related to the addon's configuration and state management within Blender.

## 1. Addon Preferences

This data is managed by Blender's `bpy.types.AddonPreferences` system and stored in user preferences.

-   **Entity**: `MCPAddonPreferences`
-   **Description**: Stores the user-specific settings for the addon.
-   **Fields**:
    -   `api_key`: (`StringProperty`, `subtype='PASSWORD'`)
        -   **Description**: The user's Gemini API key.
        -   **Validation**: Must not be empty for the server to start.
    -   `controller_python_path`: (`StringProperty`, `subtype='FILE_PATH'`)
        -   **Description**: The absolute path to the Python executable within the controller's virtual environment (e.g., `.../controller/.venv/Scripts/python.exe`).
        -   **Validation**: Must be a valid file path. The addon will check if the file exists before attempting to start the server.

## 2. Addon State

This is transient state managed within the addon's Python modules during a Blender session. It is not persisted.

-   **Entity**: `AddonState`
-   **Description**: Represents the current operational status of the addon and the server.
-   **Fields**:
    -   `server_process`: (`subprocess.Popen` object or `None`)
        -   **Description**: The handle to the running FastAPI server subprocess. `None` if the server is not running.
    -   `status_message`: (`String`)
        -   **Description**: A user-facing message displayed in the UI panel (e.g., 'Inactive', 'Starting...', 'Active', 'Error: Port in use').
    -   `chat_history`: (`List[Tuple[String, String]]`)
        -   **Description**: A list of tuples representing the conversation, where each tuple is (speaker, message). E.g., `("User", "Hello")`, `("Gemini", "Hi there!")`.
