# Quickstart

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repo_url>
    cd MCP_Blender_02
    ```

2.  **Setup Controller Environment:**
    ```bash
    cd controller
    uv venv .venv
    uv pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    - Create `controller/app/.env` (or set via system env vars):
      ```
      GEMINI_API_KEY=your_api_key_here
      GEMINI_MODEL=gemini-1.5-flash-001
      ```

4.  **Run Tests:**
    ```bash
    uv run pytest
    ```

## Usage

The usage of the Blender Addon and the Controller API remains unchanged. The migration is internal.
