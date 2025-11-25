# Data Model: Dynamic Model Discovery

**Feature**: `012-dynamic-model-discovery`

## Entities

### AvailableModels
- **Context**: Controller (In-memory), Addon (Runtime cache)
- **Type**: List[str]
- **Description**: A list of valid Gemini model names (e.g., `['models/gemini-1.5-flash', 'models/gemini-1.5-pro']`).
- **Source**: Google Generative AI API via Controller.

### AddonPreferences (Update)
- **Context**: Blender Addon
- **Fields**:
    - `selected_model`: EnumProperty (Dynamic items)
        - **Description**: The model chosen by the user.
        - **Items**: Dynamically populated from `AvailableModels` + "Custom".
    - `custom_model_name`: StringProperty
        - **Description**: Manually entered model name if `selected_model` is "Custom".
    - `gemini_api_key`: StringProperty (Existing)
        - **Validation**: If empty, checks system env var `GEMINI_API_KEY`.

### API Contract (New)

#### GET /api/models
- **Description**: Retrieves the list of available models.
- **Request**: None
- **Response**:
    ```json
    {
      "models": [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-1.0-pro"
      ]
    }
    ```
